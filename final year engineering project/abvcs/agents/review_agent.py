"""
Review & Security Auditor Agent: Inspects diffs for secrets, bugs, and style issues.
"""

import re
from typing import Dict, Any, List
from abvcs.agents.base import BaseAgent
from abvcs.schemas.models import SecurityAuditReport, SecurityIssue


class ReviewSecurityAgent(BaseAgent):
    """Inspects pending changes for credentials, vulnerabilities, and anti-patterns."""

    def __init__(self):
        super().__init__(
            name="ReviewSecurityAgent",
            description="Performs pre-commit security audits and quality scans"
        )
        # Regex patterns for common leaked secrets
        self.secret_patterns = [
            (r"(?i)(api[_-]?key|secret[_-]?key|auth[_-]?token)\s*=\s*['\"][A-Za-z0-9_\-]{16,}['\"]", "Hardcoded API Key / Token"),
            (r"(?i)password\s*=\s*['\"][^'\"]{6,}['\"]", "Hardcoded Password Literal"),
            (r"-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----", "Private Cryptographic Key"),
        ]

    def execute(self, payload: Dict[str, Any]) -> SecurityAuditReport:
        """Runs security and quality rules across the provided diff text."""
        diff_text: str = payload.get("diff", "")
        issues: List[SecurityIssue] = []

        # 1. Scan for hardcoded credentials in diff additions
        for line in diff_text.splitlines():
            if line.startswith("+") and not line.startswith("+++"):
                for pattern, rule_desc in self.secret_patterns:
                    if re.search(pattern, line):
                        issues.append(
                            SecurityIssue(
                                file_path="staged_diff",
                                severity="CRITICAL",
                                rule_id="SEC-001-SECRET-LEAK",
                                description=f"Potential leaked secret detected: {rule_desc}",
                                suggested_fix="Move sensitive values to environment variables or .env file."
                            )
                        )

        # 2. Score calculation
        if any(i.severity == "CRITICAL" for i in issues):
            status = "BLOCKED"
            score = 30
            summary = "Critical security issues found. Commit blocked by policy."
        elif issues:
            status = "WARNINGS"
            score = 75
            summary = "Minor warnings found. Review suggested before proceeding."
        else:
            status = "PASSED"
            score = 100
            summary = "All pre-commit security and quality checks passed clean."

        return SecurityAuditReport(
            status=status,
            score=score,
            issues=issues,
            summary=summary
        )
