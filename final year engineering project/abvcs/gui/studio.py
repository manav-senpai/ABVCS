"""
ABVCS Desktop Interface: Native Python Workspace.
Classic engineering layout with pastel background and direct Git / Agent operations.
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from pathlib import Path
from typing import Optional

# Ensure abvcs package is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from abvcs.core.git_engine import GitController, GitError
from abvcs.agents.orchestrator import AgentOrchestrator
from abvcs.schemas.models import CommitProposal, SecurityAuditReport


class ClassicTheme:
    """Pastel, vintage engineering palette (#f0eeea base)."""
    BG_MAIN = "#f0eeea"
    BG_PANEL = "#e7e4dc"
    BG_CARD = "#ded9cf"
    BG_INPUT = "#fbfaf8"
    TEXT_MAIN = "#2b2927"
    TEXT_MUTED = "#5f5c56"
    ACCENT_PRIMARY = "#3e5264"
    ACCENT_SECONDARY = "#61714d"
    ACCENT_WARN = "#a65b40"
    BORDER_DARK = "#b8b2a5"
    BORDER_LIGHT = "#ffffff"
    FONT_CODE = "Consolas" if sys.platform == "win32" else "Courier"
    FONT_TEXT = "Segoe UI" if sys.platform == "win32" else "Tahoma"


class ABVCSStudioApp(tk.Tk):
    """Classic Native Desktop Workspace for ABVCS."""

    def __init__(self):
        super().__init__()
        self.title("Agent-Based Version Control System")
        self.geometry("1240x800")
        self.minsize(1000, 680)
        self.configure(bg=ClassicTheme.BG_MAIN)

        self.git = GitController()
        self.orchestrator = AgentOrchestrator()
        self.current_proposal: Optional[CommitProposal] = None

        self._configure_styles()
        self._build_layout()
        self._refresh_repository_state()

    def _configure_styles(self):
        """Configures ttk widget styling for sharp classic pastel theme."""
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(".", background=ClassicTheme.BG_MAIN, foreground=ClassicTheme.TEXT_MAIN)
        style.configure("TFrame", background=ClassicTheme.BG_MAIN)
        
        # Notebook Tab styling
        style.configure("TNotebook", background=ClassicTheme.BG_MAIN, borderwidth=1)
        style.configure("TNotebook.Tab", background=ClassicTheme.BG_CARD, foreground=ClassicTheme.TEXT_MAIN,
                        padding=[10, 4], font=(ClassicTheme.FONT_TEXT, 9))
        style.map("TNotebook.Tab",
                  background=[("selected", ClassicTheme.BG_PANEL)],
                  foreground=[("selected", ClassicTheme.ACCENT_PRIMARY)])

        # Treeview styling
        style.configure("Treeview", background=ClassicTheme.BG_INPUT, foreground=ClassicTheme.TEXT_MAIN,
                        fieldbackground=ClassicTheme.BG_INPUT, borderwidth=1, font=(ClassicTheme.FONT_CODE, 9))
        style.configure("Treeview.Heading", background=ClassicTheme.BG_CARD, foreground=ClassicTheme.TEXT_MAIN,
                        font=(ClassicTheme.FONT_TEXT, 9, "bold"), relief="raised")
        style.map("Treeview", background=[("selected", ClassicTheme.BG_CARD)], foreground=[("selected", ClassicTheme.TEXT_MAIN)])

    def _build_layout(self):
        """Constructs the 3-panel classic layout."""
        # Top Header Bar
        self.header_frame = tk.Frame(self, bg=ClassicTheme.BG_PANEL, height=44, padx=12, pady=6,
                                     relief=tk.RAISED, bd=1)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)
        self._build_header()

        # Main 3-Column Container
        self.main_container = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg=ClassicTheme.BG_MAIN,
                                            sashwidth=4, sashrelief=tk.RAISED)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        # 1. Left Panel (Workspace Files & Actions)
        self.left_frame = tk.Frame(self.main_container, bg=ClassicTheme.BG_PANEL, width=260,
                                   relief=tk.GROOVE, bd=1)
        self._build_left_panel()
        self.main_container.add(self.left_frame, minsize=220)

        # 2. Center Panel (Editor / Diff & Terminal)
        self.center_frame = tk.Frame(self.main_container, bg=ClassicTheme.BG_MAIN)
        self._build_center_panel()
        self.main_container.add(self.center_frame, minsize=480)

        # 3. Right Panel (Agent Window & HITL Window)
        self.right_frame = tk.Frame(self.main_container, bg=ClassicTheme.BG_PANEL, width=280,
                                    relief=tk.GROOVE, bd=1)
        self._build_right_panel()
        self.main_container.add(self.right_frame, minsize=250)

        # Bottom Status Bar
        self.status_bar = tk.Frame(self, bg=ClassicTheme.BG_PANEL, height=24, padx=10, pady=2,
                                   relief=tk.SUNKEN, bd=1)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self._build_status_bar()

    def _build_header(self):
        """Header bar with project title, branch label, and action buttons."""
        title_box = tk.Frame(self.header_frame, bg=ClassicTheme.BG_PANEL)
        title_box.pack(side=tk.LEFT)

        tk.Label(title_box, text="Agent-Based Version Control System", font=(ClassicTheme.FONT_TEXT, 11, "bold"),
                 bg=ClassicTheme.BG_PANEL, fg=ClassicTheme.TEXT_MAIN).pack(side=tk.LEFT)

        self.branch_badge = tk.Label(self.header_frame, text="Branch: master", font=(ClassicTheme.FONT_CODE, 9),
                                     bg=ClassicTheme.BG_CARD, fg=ClassicTheme.ACCENT_SECONDARY,
                                     padx=8, pady=2, relief=tk.SOLID, bd=1)
        self.branch_badge.pack(side=tk.LEFT, padx=14)

        # Action Toolbar (Right side)
        action_box = tk.Frame(self.header_frame, bg=ClassicTheme.BG_PANEL)
        action_box.pack(side=tk.RIGHT)

        tk.Button(action_box, text="Refresh", font=(ClassicTheme.FONT_TEXT, 8),
                  bg=ClassicTheme.BG_CARD, fg=ClassicTheme.TEXT_MAIN,
                  relief=tk.RAISED, bd=1, padx=8, pady=1, command=self._refresh_repository_state).pack(side=tk.LEFT, padx=3)

        tk.Button(action_box, text="Stage All", font=(ClassicTheme.FONT_TEXT, 8),
                  bg=ClassicTheme.BG_CARD, fg=ClassicTheme.TEXT_MAIN,
                  relief=tk.RAISED, bd=1, padx=8, pady=1, command=self._action_stage_all).pack(side=tk.LEFT, padx=3)

        tk.Button(action_box, text="Initialize Git", font=(ClassicTheme.FONT_TEXT, 8),
                  bg=ClassicTheme.BG_CARD, fg=ClassicTheme.TEXT_MAIN,
                  relief=tk.RAISED, bd=1, padx=8, pady=1, command=self._action_init_git).pack(side=tk.LEFT, padx=3)

    def _build_left_panel(self):
        """Left panel: Workspace Explorer and Add File / Folder controls."""
        header_bar = tk.Frame(self.left_frame, bg=ClassicTheme.BG_PANEL, padx=8, pady=6)
        header_bar.pack(fill=tk.X)

        tk.Label(header_bar, text="Workspace & Git Status", font=(ClassicTheme.FONT_TEXT, 9, "bold"),
                 bg=ClassicTheme.BG_PANEL, fg=ClassicTheme.TEXT_MAIN).pack(side=tk.LEFT)

        # File creation actions bar
        btn_bar = tk.Frame(self.left_frame, bg=ClassicTheme.BG_PANEL, padx=8, pady=2)
        btn_bar.pack(fill=tk.X)

        tk.Button(btn_bar, text="+ File", font=(ClassicTheme.FONT_TEXT, 8),
                  bg=ClassicTheme.BG_CARD, fg=ClassicTheme.TEXT_MAIN,
                  relief=tk.RAISED, bd=1, padx=6, pady=1, command=self._action_create_file).pack(side=tk.LEFT, padx=2)

        tk.Button(btn_bar, text="+ Folder", font=(ClassicTheme.FONT_TEXT, 8),
                  bg=ClassicTheme.BG_CARD, fg=ClassicTheme.TEXT_MAIN,
                  relief=tk.RAISED, bd=1, padx=6, pady=1, command=self._action_create_folder).pack(side=tk.LEFT, padx=2)

        # Changes Treeview
        tree_frame = tk.Frame(self.left_frame, bg=ClassicTheme.BG_PANEL, padx=6, pady=4)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.file_tree = ttk.Treeview(tree_frame, columns=("status", "path"), show="headings", selectmode="browse")
        self.file_tree.heading("status", text="Stat")
        self.file_tree.heading("path", text="File Path")
        self.file_tree.column("status", width=45, anchor="center")
        self.file_tree.column("path", width=180, anchor="w")

        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=tree_scroll.set)
        self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.file_tree.bind("<<TreeviewSelect>>", self._on_file_select)

        # Summary
        bot_box = tk.Frame(self.left_frame, bg=ClassicTheme.BG_PANEL, padx=8, pady=4)
        bot_box.pack(fill=tk.X)
        self.lbl_change_count = tk.Label(bot_box, text="0 pending changes", font=(ClassicTheme.FONT_TEXT, 8),
                                         bg=ClassicTheme.BG_PANEL, fg=ClassicTheme.TEXT_MUTED)
        self.lbl_change_count.pack(anchor="w")

    def _build_center_panel(self):
        """Center panel: Top tabs (Diff / Git Log) and Bottom Interactive Console."""
        paned = tk.PanedWindow(self.center_frame, orient=tk.VERTICAL, bg=ClassicTheme.BG_MAIN,
                               sashwidth=4, sashrelief=tk.RAISED)
        paned.pack(fill=tk.BOTH, expand=True)

        # Top Section: Tabs
        top_container = tk.Frame(paned, bg=ClassicTheme.BG_PANEL)
        self.notebook = ttk.Notebook(top_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: File / Diff Viewer
        self.tab_diff = tk.Frame(self.notebook, bg=ClassicTheme.BG_PANEL)
        self.diff_text = scrolledtext.ScrolledText(
            self.tab_diff, bg=ClassicTheme.BG_INPUT, fg=ClassicTheme.TEXT_MAIN,
            insertbackground=ClassicTheme.TEXT_MAIN, font=(ClassicTheme.FONT_CODE, 9),
            relief=tk.SUNKEN, bd=1, wrap=tk.NONE
        )
        self.diff_text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        self._setup_diff_syntax_tags()
        self.notebook.add(self.tab_diff, text=" File / Diff Inspector ")

        # Tab 2: Commit History
        self.tab_history = tk.Frame(self.notebook, bg=ClassicTheme.BG_PANEL)
        self._build_history_tab()
        self.notebook.add(self.tab_history, text=" Git Commit Log ")

        paned.add(top_container, minsize=260)

        # Bottom Section: Console
        bot_container = tk.Frame(paned, bg=ClassicTheme.BG_PANEL, padx=6, pady=4, relief=tk.GROOVE, bd=1)
        
        term_header = tk.Frame(bot_container, bg=ClassicTheme.BG_PANEL)
        term_header.pack(fill=tk.X, pady=(0, 2))
        
        tk.Label(term_header, text="Interactive Console", font=(ClassicTheme.FONT_TEXT, 8, "bold"),
                 bg=ClassicTheme.BG_PANEL, fg=ClassicTheme.ACCENT_PRIMARY).pack(side=tk.LEFT)

        for cmd_name, cmd_action in [
            ("git status", lambda: self._run_console_cmd("status")),
            ("git diff", lambda: self._run_console_cmd("diff")),
            ("git log -n 5", lambda: self._run_console_cmd("log")),
        ]:
            tk.Button(term_header, text=cmd_name, font=(ClassicTheme.FONT_CODE, 8),
                      bg=ClassicTheme.BG_CARD, fg=ClassicTheme.TEXT_MAIN,
                      relief=tk.RAISED, bd=1, padx=5, pady=1, command=cmd_action).pack(side=tk.RIGHT, padx=2)

        # Terminal Output Box
        self.term_output = scrolledtext.ScrolledText(
            bot_container, bg="#201f1d", fg="#e0ded9",
            insertbackground="#e0ded9", font=(ClassicTheme.FONT_CODE, 9),
            relief=tk.SUNKEN, bd=1, wrap=tk.CHAR, height=9
        )
        self.term_output.pack(fill=tk.BOTH, expand=True)

        # Command Input Line
        cmd_bar = tk.Frame(bot_container, bg=ClassicTheme.BG_PANEL, pady=3)
        cmd_bar.pack(fill=tk.X)

        tk.Label(cmd_bar, text="vcs >", font=(ClassicTheme.FONT_CODE, 9, "bold"),
                 bg=ClassicTheme.BG_PANEL, fg=ClassicTheme.ACCENT_PRIMARY).pack(side=tk.LEFT, padx=(0, 4))

        self.cmd_entry = tk.Entry(cmd_bar, bg=ClassicTheme.BG_INPUT, fg=ClassicTheme.TEXT_MAIN,
                                  insertbackground=ClassicTheme.TEXT_MAIN, font=(ClassicTheme.FONT_CODE, 9),
                                  relief=tk.SUNKEN, bd=1)
        self.cmd_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.cmd_entry.bind("<Return>", lambda e: self._on_console_enter())

        tk.Button(cmd_bar, text="Execute", font=(ClassicTheme.FONT_TEXT, 8),
                  bg=ClassicTheme.BG_CARD, fg=ClassicTheme.TEXT_MAIN,
                  relief=tk.RAISED, bd=1, padx=8, pady=1, command=self._on_console_enter).pack(side=tk.LEFT, padx=(4, 0))

        paned.add(bot_container, minsize=180)

    def _build_history_tab(self):
        """Builds commit log table in history tab."""
        self.history_tree = ttk.Treeview(self.tab_history, columns=("hash", "author", "message", "time"),
                                         show="headings", selectmode="browse")
        self.history_tree.heading("hash", text="Commit")
        self.history_tree.heading("author", text="Author")
        self.history_tree.heading("message", text="Message")
        self.history_tree.heading("time", text="Date")

        self.history_tree.column("hash", width=70, anchor="center")
        self.history_tree.column("author", width=110, anchor="w")
        self.history_tree.column("message", width=280, anchor="w")
        self.history_tree.column("time", width=100, anchor="e")

        h_scroll = ttk.Scrollbar(self.tab_history, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=h_scroll.set)
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4, pady=4)
        h_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def _build_right_panel(self):
        """Right panel: Agent Window & HITL Window."""
        # Section 1: Agent Window
        agent_box = tk.Frame(self.right_frame, bg=ClassicTheme.BG_PANEL, padx=8, pady=6)
        agent_box.pack(fill=tk.X)

        tk.Label(agent_box, text="Agent Window", font=(ClassicTheme.FONT_TEXT, 9, "bold"),
                 bg=ClassicTheme.BG_PANEL, fg=ClassicTheme.TEXT_MAIN).pack(anchor="w", pady=(0, 4))

        # Status text
        self.lbl_agent_state = tk.Label(agent_box, text="Status: Ready", font=(ClassicTheme.FONT_TEXT, 8),
                                        bg=ClassicTheme.BG_CARD, fg=ClassicTheme.TEXT_MAIN,
                                        relief=tk.SOLID, bd=1, padx=6, pady=2)
        self.lbl_agent_state.pack(fill=tk.X, pady=(0, 6))

        tk.Button(agent_box, text="Run Agent Plan", font=(ClassicTheme.FONT_TEXT, 8, "bold"),
                  bg=ClassicTheme.BG_CARD, fg=ClassicTheme.TEXT_MAIN,
                  relief=tk.RAISED, bd=1, pady=3, command=self._action_plan_commit).pack(fill=tk.X)

        # Section 2: HITL Window
        hitl_box = tk.Frame(self.right_frame, bg=ClassicTheme.BG_PANEL, padx=8, pady=6)
        hitl_box.pack(fill=tk.BOTH, expand=True, pady=(4, 0))

        tk.Label(hitl_box, text="HITL Window", font=(ClassicTheme.FONT_TEXT, 9, "bold"),
                 bg=ClassicTheme.BG_PANEL, fg=ClassicTheme.TEXT_MAIN).pack(anchor="w", pady=(0, 2))

        self.lbl_security_status = tk.Label(hitl_box, text="Review: Standby",
                                            font=(ClassicTheme.FONT_TEXT, 8), bg=ClassicTheme.BG_PANEL,
                                            fg=ClassicTheme.TEXT_MUTED)
        self.lbl_security_status.pack(anchor="w")

        self.proposal_text = scrolledtext.ScrolledText(
            hitl_box, bg=ClassicTheme.BG_INPUT, fg=ClassicTheme.TEXT_MAIN,
            insertbackground=ClassicTheme.TEXT_MAIN, font=(ClassicTheme.FONT_CODE, 8),
            relief=tk.SUNKEN, bd=1, wrap=tk.WORD, height=8
        )
        self.proposal_text.pack(fill=tk.BOTH, expand=True, pady=4)
        self.proposal_text.insert(tk.END, "No active recommendations.\nClick 'Run Agent Plan' to inspect changes.")
        self.proposal_text.configure(state="disabled")

        # Action Buttons in HITL
        btn_row = tk.Frame(hitl_box, bg=ClassicTheme.BG_PANEL)
        btn_row.pack(fill=tk.X, pady=(2, 4))

        self.btn_approve = tk.Button(btn_row, text="Approve & Commit", font=(ClassicTheme.FONT_TEXT, 8, "bold"),
                                     bg=ClassicTheme.BG_CARD, fg=ClassicTheme.ACCENT_SECONDARY,
                                     relief=tk.RAISED, bd=1, pady=3, state="disabled", command=self._action_approve_commit)
        self.btn_approve.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))

        self.btn_reject = tk.Button(btn_row, text="Reject", font=(ClassicTheme.FONT_TEXT, 8),
                                    bg=ClassicTheme.BG_CARD, fg=ClassicTheme.ACCENT_WARN,
                                    relief=tk.RAISED, bd=1, pady=3, state="disabled", command=self._action_reject_proposal)
        self.btn_reject.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(2, 0))

    def _build_status_bar(self):
        """Bottom status bar."""
        self.lbl_status = tk.Label(self.status_bar, text="Ready", font=(ClassicTheme.FONT_TEXT, 8),
                                   bg=ClassicTheme.BG_PANEL, fg=ClassicTheme.TEXT_MUTED)
        self.lbl_status.pack(side=tk.LEFT)

        tk.Label(self.status_bar, text="Repository System", font=(ClassicTheme.FONT_TEXT, 8),
                 bg=ClassicTheme.BG_PANEL, fg=ClassicTheme.TEXT_MUTED).pack(side=tk.RIGHT)

    def _setup_diff_syntax_tags(self):
        """Configures color tags for diff rendering."""
        self.diff_text.tag_config("added", foreground="#2e6930", background="#eaf3ea")
        self.diff_text.tag_config("deleted", foreground="#942a2a", background="#faebeb")
        self.diff_text.tag_config("header", foreground="#23425f", font=(ClassicTheme.FONT_CODE, 9, "bold"))

    def _log_terminal(self, message: str):
        """Appends output to the console."""
        self.term_output.insert(tk.END, message + "\n")
        self.term_output.see(tk.END)

    def _refresh_repository_state(self):
        """Scans the repository and updates file trees, branches, and commit logs."""
        if not self.git.is_git_repository():
            self.branch_badge.config(text="Branch: Uninitialized", fg=ClassicTheme.ACCENT_WARN)
            self._log_terminal("Repository not initialized. Click 'Initialize Git' to begin.")
            return

        branch = self.git.get_current_branch()
        self.branch_badge.config(text=f"Branch: {branch}", fg=ClassicTheme.ACCENT_SECONDARY)

        for item in self.file_tree.get_children():
            self.file_tree.delete(item)

        deltas = self.git.get_status()
        self.lbl_change_count.config(text=f"{len(deltas)} item(s) detected")

        for d in deltas:
            tag = "M" if d.status == "modified" else "A" if d.status == "added" else "?" if d.status == "untracked" else "D"
            self.file_tree.insert("", tk.END, values=(tag, d.file_path))

        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        commits = self.git.get_recent_commits(limit=15)
        for c in commits:
            self.history_tree.insert("", tk.END, values=(c["hash"], c["author"], c["subject"], c["relative_date"]))

        diff_content = self.git.get_diff()
        self._display_diff_text(diff_content if diff_content else "Select a file from the workspace list to view contents or diff.")
        self.lbl_status.config(text=f"Synced: {len(deltas)} change(s) • {len(commits)} commit(s)")

    def _display_diff_text(self, text: str):
        """Renders text into the viewer with diff tags."""
        self.diff_text.delete("1.0", tk.END)
        for line in text.splitlines():
            if line.startswith("+") and not line.startswith("+++"):
                self.diff_text.insert(tk.END, line + "\n", "added")
            elif line.startswith("-") and not line.startswith("---"):
                self.diff_text.insert(tk.END, line + "\n", "deleted")
            elif line.startswith("diff ") or line.startswith("@@"):
                self.diff_text.insert(tk.END, line + "\n", "header")
            else:
                self.diff_text.insert(tk.END, line + "\n")

    def _on_file_select(self, event):
        """Handles selecting a file in the explorer tree."""
        selected = self.file_tree.selection()
        if not selected:
            return
        item = self.file_tree.item(selected[0])
        file_path = item["values"][1]
        
        diff = self.git.get_diff(file_path=file_path)
        if diff:
            self._display_diff_text(diff)
        else:
            abs_path = self.git.repo_path / file_path
            if abs_path.is_file():
                try:
                    with open(abs_path, "r", encoding="utf-8", errors="ignore") as f:
                        self._display_diff_text(f.read())
                except Exception as e:
                    self._display_diff_text(f"Error opening file: {e}")

    def _action_create_file(self):
        """Dialog to create a new file in repository."""
        dialog = tk.Toplevel(self)
        dialog.title("Create New File")
        dialog.geometry("340x120")
        dialog.configure(bg=ClassicTheme.BG_PANEL)
        dialog.transient(self)

        tk.Label(dialog, text="File Name / Relative Path:", font=(ClassicTheme.FONT_TEXT, 9),
                 bg=ClassicTheme.BG_PANEL, fg=ClassicTheme.TEXT_MAIN).pack(anchor="w", padx=12, pady=(10, 4))
        
        entry = tk.Entry(dialog, bg=ClassicTheme.BG_INPUT, fg=ClassicTheme.TEXT_MAIN,
                         font=(ClassicTheme.FONT_CODE, 9), relief=tk.SUNKEN, bd=1)
        entry.pack(fill=tk.X, padx=12, pady=(0, 8))
        entry.focus_set()

        def confirm():
            val = entry.get().strip()
            if val:
                target = self.git.repo_path / val
                target.parent.mkdir(parents=True, exist_ok=True)
                if not target.exists():
                    target.write_text("# New file\n", encoding="utf-8")
                self._log_terminal(f"Created file: {val}")
                self._refresh_repository_state()
            dialog.destroy()

        btn_row = tk.Frame(dialog, bg=ClassicTheme.BG_PANEL)
        btn_row.pack(fill=tk.X, padx=12)
        tk.Button(btn_row, text="Create", font=(ClassicTheme.FONT_TEXT, 8, "bold"),
                  bg=ClassicTheme.BG_CARD, fg=ClassicTheme.TEXT_MAIN,
                  relief=tk.RAISED, bd=1, padx=10, command=confirm).pack(side=tk.RIGHT)

    def _action_create_folder(self):
        """Dialog to create a new directory in repository."""
        dialog = tk.Toplevel(self)
        dialog.title("Create New Folder")
        dialog.geometry("340x120")
        dialog.configure(bg=ClassicTheme.BG_PANEL)
        dialog.transient(self)

        tk.Label(dialog, text="Folder Name / Relative Path:", font=(ClassicTheme.FONT_TEXT, 9),
                 bg=ClassicTheme.BG_PANEL, fg=ClassicTheme.TEXT_MAIN).pack(anchor="w", padx=12, pady=(10, 4))
        
        entry = tk.Entry(dialog, bg=ClassicTheme.BG_INPUT, fg=ClassicTheme.TEXT_MAIN,
                         font=(ClassicTheme.FONT_CODE, 9), relief=tk.SUNKEN, bd=1)
        entry.pack(fill=tk.X, padx=12, pady=(0, 8))
        entry.focus_set()

        def confirm():
            val = entry.get().strip()
            if val:
                target = self.git.repo_path / val
                target.mkdir(parents=True, exist_ok=True)
                self._log_terminal(f"Created directory: {val}")
                self._refresh_repository_state()
            dialog.destroy()

        btn_row = tk.Frame(dialog, bg=ClassicTheme.BG_PANEL)
        btn_row.pack(fill=tk.X, padx=12)
        tk.Button(btn_row, text="Create", font=(ClassicTheme.FONT_TEXT, 8, "bold"),
                  bg=ClassicTheme.BG_CARD, fg=ClassicTheme.TEXT_MAIN,
                  relief=tk.RAISED, bd=1, padx=10, command=confirm).pack(side=tk.RIGHT)

    def _on_console_enter(self):
        """Executes command from the console entry line."""
        cmd = self.cmd_entry.get().strip()
        if not cmd:
            return
        self.cmd_entry.delete(0, tk.END)
        self._log_terminal(f"vcs > {cmd}")
        self._run_console_cmd(cmd)

    def _run_console_cmd(self, cmd: str):
        """Runs supported CLI commands inside the console."""
        if cmd in ["status", "git status"]:
            deltas = self.git.get_status()
            if not deltas:
                self._log_terminal("Working directory clean.")
            else:
                for d in deltas:
                    self._log_terminal(f"  [{d.status.upper()}] {d.file_path}")
        elif cmd in ["diff", "git diff"]:
            diff = self.git.get_diff()
            self._log_terminal(diff if diff else "No uncommitted differences.")
        elif cmd.startswith("log") or cmd.startswith("git log"):
            commits = self.git.get_recent_commits(limit=5)
            for c in commits:
                self._log_terminal(f"  {c['hash']} - {c['subject']} ({c['author']}, {c['relative_date']})")
        elif cmd in ["init", "git init"]:
            out = self.git.init()
            self._log_terminal(out)
            self._refresh_repository_state()
        else:
            try:
                args = cmd.replace("git ", "").split()
                res = self.git._run(args, check=False)
                if res.stdout:
                    self._log_terminal(res.stdout.strip())
                if res.stderr:
                    self._log_terminal(res.stderr.strip())
            except Exception as e:
                self._log_terminal(f"Error: {e}")
        self._refresh_repository_state()

    def _action_init_git(self):
        """Handles Initialize Git button."""
        out = self.git.init()
        self._log_terminal(f"Initialized repository: {out}")
        self._refresh_repository_state()

    def _action_stage_all(self):
        """Stages all working files."""
        deltas = self.git.get_status()
        if not deltas:
            messagebox.showinfo("VCS", "No modified files to stage.")
            return
        self.git.stage_files([d.file_path for d in deltas])
        self._log_terminal(f"Staged {len(deltas)} file(s).")
        self._refresh_repository_state()

    def _action_plan_commit(self):
        """Triggers the agent pipeline and updates the HITL window."""
        self._log_terminal("Analyzing workspace changes...")
        self.lbl_agent_state.config(text="Status: Processing...", fg=ClassicTheme.ACCENT_PRIMARY)

        result = self.orchestrator.process_workspace_changes()

        if result["status"] == "NO_CHANGES":
            messagebox.showinfo("VCS", "Working directory clean. No changes to commit.")
            self._log_terminal("No modified files found.")
            self.lbl_agent_state.config(text="Status: Ready", fg=ClassicTheme.TEXT_MAIN)
            return

        if result["status"] == "BLOCKED":
            report: SecurityAuditReport = result["security_report"]
            self.lbl_security_status.config(text=f"Review: BLOCKED ({report.score}/100)", fg=ClassicTheme.ACCENT_WARN)
            self.proposal_text.configure(state="normal")
            self.proposal_text.delete("1.0", tk.END)
            self.proposal_text.insert(tk.END, f"STATUS: BLOCKED\n{report.summary}\n\n")
            for issue in report.issues:
                self.proposal_text.insert(tk.END, f"- [{issue.severity}] {issue.description}\n")
            self.proposal_text.configure(state="disabled")
            self.btn_approve.config(state="disabled")
            self.btn_reject.config(state="normal")
            self.lbl_agent_state.config(text="Status: Issues Found", fg=ClassicTheme.ACCENT_WARN)
            return

        proposal: CommitProposal = result["commit_proposal"]
        report: SecurityAuditReport = result["security_report"]
        self.current_proposal = proposal

        self.lbl_security_status.config(text=f"Review: PASSED ({report.score}/100)", fg=ClassicTheme.ACCENT_SECONDARY)
        
        self.proposal_text.configure(state="normal")
        self.proposal_text.delete("1.0", tk.END)
        self.proposal_text.insert(tk.END, f"RECOMMENDED COMMIT:\n\n{proposal.formatted_message}\n\n")
        self.proposal_text.insert(tk.END, f"Confidence: {proposal.confidence_score * 100:.1f}%\nTarget Files: {len(proposal.files_to_stage)}")
        self.proposal_text.configure(state="disabled")

        self.btn_approve.config(state="normal")
        self.btn_reject.config(state="normal")
        self.lbl_agent_state.config(text="Status: Recommendation Ready", fg=ClassicTheme.ACCENT_SECONDARY)
        self._log_terminal(f"Generated commit recommendation: '{proposal.subject}'")

    def _action_approve_commit(self):
        """Executes the approved commit."""
        if not self.current_proposal:
            return
        out = self.orchestrator.execute_commit(self.current_proposal)
        self._log_terminal(f"Commit Executed:\n{out}")
        messagebox.showinfo("VCS", "Commit successfully created.")
        self._action_reject_proposal()
        self._refresh_repository_state()

    def _action_reject_proposal(self):
        """Clears active proposal."""
        self.current_proposal = None
        self.proposal_text.configure(state="normal")
        self.proposal_text.delete("1.0", tk.END)
        self.proposal_text.insert(tk.END, "Cleared.\nClick 'Run Agent Plan' to analyze new changes.")
        self.proposal_text.configure(state="disabled")
        self.btn_approve.config(state="disabled")
        self.btn_reject.config(state="disabled")
        self.lbl_security_status.config(text="Review: Standby", fg=ClassicTheme.TEXT_MUTED)
        self.lbl_agent_state.config(text="Status: Ready", fg=ClassicTheme.TEXT_MAIN)


def main():
    app = ABVCSStudioApp()
    app.mainloop()


if __name__ == "__main__":
    main()
