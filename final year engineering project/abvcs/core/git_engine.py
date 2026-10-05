"""
Core Git engine providing safe, deterministic Git command execution.
"""

import subprocess
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from abvcs.schemas.models import FileDelta


class GitError(Exception):
    """Custom exception raised when a Git operation fails."""
    pass


class GitController:
    """Encapsulates all direct Git CLI interactions and state queries."""

    def __init__(self, repo_path: Optional[str] = None):
        self.repo_path = Path(repo_path or os.getcwd()).resolve()
        if self.is_git_repository():
            try:
                self._run(["config", "user.name"], check=True)
            except Exception:
                self._run(["config", "user.name", "ABVCS Developer"], check=False)
            try:
                self._run(["config", "user.email"], check=True)
            except Exception:
                self._run(["config", "user.email", "developer@abvcs.local"], check=False)

    def _run(self, args: List[str], check: bool = True) -> subprocess.CompletedProcess:
        """Runs a Git command securely via subprocess without shell execution."""
        full_cmd = ["git"] + args
        try:
            result = subprocess.run(
                full_cmd,
                cwd=str(self.repo_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=check
            )
            return result
        except subprocess.CalledProcessError as e:
            raise GitError(f"Git command failed: {' '.join(full_cmd)}\nError: {e.stderr.strip()}")

    def is_git_repository(self) -> bool:
        """Verifies if the target directory is a valid Git repository."""
        try:
            res = self._run(["rev-parse", "--is-inside-work-tree"], check=False)
            return res.returncode == 0 and res.stdout.strip() == "true"
        except Exception:
            return False

    def init(self) -> str:
        """Initializes a new Git repository and ensures local identity is configured."""
        res = self._run(["init"])
        # Configure fallback local identity if none exists
        try:
            self._run(["config", "user.name"], check=True)
        except Exception:
            self._run(["config", "user.name", "ABVCS Developer"])
        try:
            self._run(["config", "user.email"], check=True)
        except Exception:
            self._run(["config", "user.email", "developer@abvcs.local"])
        return res.stdout.strip()

    def get_current_branch(self) -> str:
        """Returns the active branch name."""
        res = self._run(["branch", "--show-current"])
        branch = res.stdout.strip()
        return branch if branch else "HEAD (detached)"

    def get_status(self) -> List[FileDelta]:
        """Parses porcelain status into structured FileDelta objects."""
        res = self._run(["status", "--porcelain"])
        deltas: List[FileDelta] = []
        
        for line in res.stdout.splitlines():
            if not line.strip():
                continue
            status_code = line[:2]
            file_name = line[3:].strip()
            
            # Categorize status
            if "?" in status_code:
                status = "untracked"
            elif "D" in status_code:
                status = "deleted"
            elif "A" in status_code:
                status = "added"
            else:
                status = "modified"
                
            deltas.append(FileDelta(file_path=file_name, status=status))
            
        return deltas

    def get_diff(self, staged: bool = False, file_path: Optional[str] = None) -> str:
        """Retrieves unified diff of working tree or index."""
        args = ["diff"]
        if staged:
            args.append("--staged")
        if file_path:
            args.extend(["--", file_path])
        res = self._run(args, check=False)
        return res.stdout

    def stage_files(self, files: List[str]) -> None:
        """Stages specified files to the Git index."""
        if not files:
            return
        self._run(["add"] + files)

    def commit(self, message: str) -> str:
        """Creates a Git commit with the given message."""
        res = self._run(["commit", "-m", message])
        return res.stdout.strip()

    def get_recent_commits(self, limit: int = 5) -> List[Dict[str, str]]:
        """Retrieves recent commit history log."""
        format_str = "%H%x1f%an%x1f%s%x1f%cr"
        res = self._run(["log", f"-n{limit}", f"--pretty=format:{format_str}"], check=False)
        if res.returncode != 0 or not res.stdout.strip():
            return []
            
        commits = []
        for line in res.stdout.splitlines():
            parts = line.split("\x1f")
            if len(parts) == 4:
                commits.append({
                    "hash": parts[0][:7],
                    "author": parts[1],
                    "subject": parts[2],
                    "relative_date": parts[3]
                })
        return commits
