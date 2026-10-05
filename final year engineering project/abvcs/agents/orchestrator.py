"""
Agent Orchestrator: Central coordinator managing task routing and safety gates.
"""

from typing import Dict, Any, Optional
from abvcs.core.git_engine import GitController
from abvcs.agents.commit_agent import CommitPlannerAgent
from abvcs.agents.review_agent import ReviewSecurityAgent
from abvcs.schemas.models import CommitProposal, SecurityAuditReport


class AgentOrchestrator:
    """Coordinates multi-agent analysis, review gates, and Git execution."""

    def __init__(self, repo_path: Optional[str] = None):
        self.git = GitController(repo_path)
        self.commit_agent = CommitPlannerAgent()
        self.review_agent = ReviewSecurityAgent()

    def process_workspace_changes(self, user_prompt: str = "") -> Dict[str, Any]:
        """
        Executes the end-to-end pipeline:
        1. Query Git status and diffs.
        2. Execute Security Auditor Agent.
        3. Execute Commit Planner Agent.
        4. Gatekeeper evaluation.
        """
        deltas = self.git.get_status()
        if not deltas:
            return {"status": "NO_CHANGES", "message": "Working directory clean. No changes detected."}

        # Retrieve working tree diff
        diff_text = self.git.get_diff()

        # Run Security Review
        security_report: SecurityAuditReport = self.review_agent.execute({
            "diff": diff_text,
            "deltas": deltas
        })

        if security_report.status == "BLOCKED":
            return {
                "status": "BLOCKED",
                "security_report": security_report,
                "message": "Commit preparation blocked due to critical security issues."
            }

        # Run Commit Planner
        commit_proposal: CommitProposal = self.commit_agent.execute({
            "deltas": deltas,
            "diff": diff_text,
            "user_prompt": user_prompt
        })

        return {
            "status": "READY",
            "security_report": security_report,
            "commit_proposal": commit_proposal,
            "deltas": deltas
        }

    def execute_commit(self, proposal: CommitProposal) -> str:
        """Stages the approved files and executes the deterministic Git commit."""
        self.git.stage_files(proposal.files_to_stage)
        output = self.git.commit(proposal.formatted_message)
        return output
