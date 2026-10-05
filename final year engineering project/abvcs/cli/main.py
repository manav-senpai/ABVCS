"""
ABVCS Command-Line Interface (CLI).
Interactive terminal commands for agent-based version control operations.
Built with zero external dependency requirements (stdlib fallback).
"""

import sys
import os
import argparse
from abvcs.core.git_engine import GitController
from abvcs.agents.orchestrator import AgentOrchestrator

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    console = Console()
    HAS_RICH = True
except ImportError:
    console = None
    HAS_RICH = False


if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def print_banner():
    """Prints the ABVCS CLI banner."""
    if HAS_RICH:
        console.print("[bold cyan]=============================================================[/bold cyan]")
        console.print("[bold white] [*] ABVCS: Agent-Based Version Control System[/bold white]")
        console.print("[dim] AI Understands | AI Recommends | Humans Decide | Git Executes[/dim]")
        console.print("[bold cyan]=============================================================[/bold cyan]\n")
    else:
        print("=============================================================")
        print(" [*] ABVCS: Agent-Based Version Control System")
        print(" AI Understands | AI Recommends | Humans Decide | Git Executes")
        print("=============================================================\n")


def cmd_init(args):
    """Initialize a new ABVCS repository."""
    print_banner()
    git = GitController()
    if git.is_git_repository():
        if HAS_RICH:
            console.print("[yellow]ℹ️ Repository is already initialized.[/yellow]")
        else:
            print("ℹ️ Repository is already initialized.")
    else:
        out = git.init()
        if HAS_RICH:
            console.print(f"[green]✓ Initialized ABVCS repository:[/green] {out}")
        else:
            print(f"✓ Initialized ABVCS repository: {out}")


def cmd_status(args):
    """Check repository status with agent-assisted analysis."""
    print_banner()
    git = GitController()
    if not git.is_git_repository():
        if HAS_RICH:
            console.print("[red]✗ Not a git repository. Run 'python run_cli.py init' first.[/red]")
        else:
            print("✗ Not a git repository. Run 'python run_cli.py init' first.")
        return

    branch = git.get_current_branch()
    deltas = git.get_status()

    if HAS_RICH:
        console.print(f"[bold]Active Branch:[/bold] [magenta]{branch}[/magenta]\n")
        if not deltas:
            console.print("[green]✓ Working directory clean. No modified files.[/green]")
            return

        table = Table(title="Detected Changes")
        table.add_column("Status", style="cyan", justify="center")
        table.add_column("File Path", style="white")

        for d in deltas:
            color = "green" if d.status == "added" else "yellow" if d.status == "modified" else "red"
            table.add_row(f"[{color}]{d.status.upper()}[/{color}]", d.file_path)

        console.print(table)
    else:
        print(f"Active Branch: {branch}\n")
        if not deltas:
            print("✓ Working directory clean. No modified files.")
            return
        print("Detected Changes:")
        for d in deltas:
            print(f"  [{d.status.upper()}] {d.file_path}")
        print()


def cmd_commit(args):
    """Run multi-agent review, planning, and commit pipeline."""
    print_banner()
    orchestrator = AgentOrchestrator()
    result = orchestrator.process_workspace_changes(user_prompt=args.message or "")

    if result["status"] == "NO_CHANGES":
        if HAS_RICH:
            console.print(f"[yellow]{result['message']}[/yellow]")
        else:
            print(f"ℹ️ {result['message']}")
        return

    if result["status"] == "BLOCKED":
        report = result["security_report"]
        if HAS_RICH:
            console.print(Panel(f"[bold red]⛔ COMMIT BLOCKED BY SECURITY AGENT[/bold red]\n\n{report.summary}", border_style="red"))
            for issue in report.issues:
                console.print(f" - [red]{issue.severity}[/red]: {issue.description}")
        else:
            print(f"⛔ COMMIT BLOCKED: {report.summary}")
            for issue in report.issues:
                print(f" - [{issue.severity}]: {issue.description}")
        return

    # Ready state
    proposal = result["commit_proposal"]
    report = result["security_report"]

    if HAS_RICH:
        console.print(f"[bold green]✓ Pre-commit Security Audit Passed[/bold green] (Score: {report.score}/100)")
        console.print(Panel(
            f"[bold cyan]Proposed Conventional Commit:[/bold cyan]\n\n"
            f"[bold white]{proposal.formatted_message}[/bold white]\n\n"
            f"[dim]Confidence Score: {proposal.confidence_score * 100:.1f}% | Files: {len(proposal.files_to_stage)}[/dim]",
            title="Commit Planner Agent Recommendation",
            border_style="cyan"
        ))
    else:
        print(f"✓ Pre-commit Security Audit Passed (Score: {report.score}/100)")
        print("\n--- Proposed Conventional Commit ---")
        print(proposal.formatted_message)
        print(f"Confidence Score: {proposal.confidence_score * 100:.1f}% | Staging {len(proposal.files_to_stage)} file(s)")
        print("------------------------------------\n")

    if args.auto:
        if HAS_RICH:
            console.print("[green]🚀 Autonomous Mode Enabled: Executing commit...[/green]")
        else:
            print("🚀 Autonomous Mode: Executing commit...")
        out = orchestrator.execute_commit(proposal)
        print(out)
    else:
        try:
            choice = input("Do you approve and wish to execute this commit? [Y/n]: ").strip().lower()
        except EOFError:
            choice = "y"
        if choice in ["", "y", "yes"]:
            out = orchestrator.execute_commit(proposal)
            if HAS_RICH:
                console.print(f"[bold green]✓ Commit Successfully Executed![/bold green]\n{out}")
            else:
                print(f"✓ Commit Successfully Executed!\n{out}")
        else:
            if HAS_RICH:
                console.print("[yellow]Commit aborted by user.[/yellow]")
            else:
                print("Commit aborted by user.")


def main():
    parser = argparse.ArgumentParser(
        prog="abvcs",
        description="ABVCS: Agent-Based Version Control System"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init
    subparsers.add_parser("init", help="Initialize a new repository")

    # status
    subparsers.add_parser("status", help="Show intelligent status of working tree")

    # commit
    commit_parser = subparsers.add_parser("commit", help="Run multi-agent commit pipeline")
    commit_parser.add_argument("-m", "--message", default="", help="Optional prompt guidance for Commit Agent")
    commit_parser.add_argument("--auto", action="store_true", help="Autonomous mode: auto-commit on verification")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "commit":
        cmd_commit(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
