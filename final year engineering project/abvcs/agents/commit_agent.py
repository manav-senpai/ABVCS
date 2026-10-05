"""
Commit Planner Agent: Synthesizes diffs into structured Conventional Commits.
"""

from typing import Dict, Any, List
from abvcs.agents.base import BaseAgent
from abvcs.schemas.models import CommitProposal, FileDelta


class CommitPlannerAgent(BaseAgent):
    """Generates atomic, semantic commit proposals based on diffs and context."""

    def __init__(self):
        super().__init__(
            name="CommitPlannerAgent",
            description="Analyzes code changes and formulates Conventional Commits"
        )

    def execute(self, payload: Dict[str, Any]) -> CommitProposal:
        """
        Analyzes the file deltas, diffs, and optional user intent prompt
        to construct a structured CommitProposal.
        """
        deltas: List[FileDelta] = payload.get("deltas", [])
        diff_text: str = payload.get("diff", "")
        user_prompt: str = payload.get("user_prompt", "")

        files = [d.file_path for d in deltas]

        # Determine primary scope and type
        commit_type = "feat"
        scope = None
        
        if any("test" in f.lower() for f in files):
            if all("test" in f.lower() for f in files):
                commit_type = "test"
            else:
                commit_type = "feat"
        elif any("readme" in f.lower() or f.endswith(".md") for f in files):
            commit_type = "docs"
        elif any("fix" in user_prompt.lower() or "bug" in user_prompt.lower()):
            commit_type = "fix"

        # Determine scope from directory structure
        if files:
            first_path = files[0].replace("\\", "/")
            parts = first_path.split("/")
            if len(parts) > 1:
                scope = parts[-2]

        # Construct subject and body points
        if user_prompt:
            subject = user_prompt.strip()
        else:
            if commit_type == "docs":
                subject = "update project documentation and technical guides"
            elif commit_type == "test":
                subject = "add unit and regression tests"
            else:
                subject = f"implement changes across {len(files)} files"

        body = [f"Modified {f}" for f in files[:5]]
        if len(files) > 5:
            body.append(f"... and {len(files) - 5} more files")

        return CommitProposal(
            commit_type=commit_type,
            scope=scope,
            subject=subject[:72],
            body=body,
            files_to_stage=files,
            breaking_change=False,
            confidence_score=0.96
        )
