# ⚙️ Technology Stack & Engineering Justification

---

## 1. Why a Python-Native CLI / Daemon System?

Many final year projects default to generic web applications (React + HTML/CSS forms). While visually accessible, a web-based VCS has fundamental drawbacks for real developer workflows:

1. **Workflow Disruption:** Developers do not want to switch from VS Code / Terminal to a web browser tab just to stage and commit their code.
2. **True System-Level Access:** A background Python daemon can watch the file system directly, parse syntax trees natively, and invoke local test runners without web latency or upload overhead.
3. **Terminal First UI (TUI):** Modern Terminal User Interfaces (using libraries like `Rich` and `Textual`) provide state-of-the-art aesthetics, live animations, colored diffs, and interactive prompts directly inside the developer's terminal.
4. **Offline Capability & Local Execution:** Python can run lightweight local models (via Ollama or Llama-cpp) alongside cloud APIs, allowing full functionality even when completely offline.

---

## 2. Core Technology Stack

| Layer | Technology | Role & Justification |
| :--- | :--- | :--- |
| **Language** | **Python 3.11+** | Modern async/await primitives, type annotations, rich ecosystem for AST parsing and agent orchestration. |
| **CLI & Interface** | **Click / Typer + Rich** | High-performance CLI commands with beautiful colored outputs, progress spinners, interactive selection menus, and formatted tables. |
| **Terminal TUI (Optional Live Dashboard)** | **Textual** | A full terminal-based dashboard rendering real-time agent status, commit graphs, and conflict diffs right in the console. |
| **File System Watcher** | **Watchfiles / Watchdog** | Rust-backed async file-system watcher capable of debouncing rapid file saves and detecting modified/created/deleted files instantly. |
| **Git Engine** | **GitPython + Native Git Subprocesses** | Safe, low-level bindings to the local Git binary, guaranteeing that repository operations remain 100% compliant with standard Git repositories. |
| **AST & Code Analysis** | **Python `ast` / Tree-Sitter** | Parses source code structure to detect function additions, modified classes, and structural code boundaries before staging. |
| **Agent Reasoning & Models** | **LiteLLM / Custom Provider Engine** | Universal interface supporting local models (Ollama, DeepSeek, LLaMA) and cloud providers (Gemini, Claude, GPT) with zero vendor lock-in. |
| **Data Validation & Schemas** | **Pydantic v2** | Enforces strict JSON Schema validation on all AI agent outputs, completely eliminating hallucinated formats and malformed payloads. |
| **Local Memory & Auditing** | **SQLite + SQLAlchemy Core** | Lightweight, zero-config local database storing agent execution logs, commit confidence scores, and historical user approvals. |
| **Test Execution Sandbox** | **Subprocess Sandbox / Pytest Runner** | Runs project tests in an isolated child process before commits are approved, preventing broken code from entering the commit log. |

---

## 3. Comparative Matrix: Traditional Git vs. Copilot vs. ABVCS

| Feature | Traditional Git | GitHub Copilot CLI | **ABVCS (Our Project)** |
| :--- | :---: | :---: | :---: |
| **Operation Type** | Manual | Reactive Prompt | **Autonomous & Proactive** |
| **Semantic Boundary Detection** | ❌ None | ❌ None | ✅ **AST-based Automatic Staging** |
| **Multi-Agent Review Pipeline** | ❌ None | ❌ Single Prompt | ✅ **Dedicated Review & Security Agents** |
| **Test Verification Gate** | ❌ Manual | ❌ None | ✅ **Automated Pre-Commit Test Check** |
| **Interactive Conflict Resolution** | ❌ Manual text edits | ❌ None | ✅ **AI-Assisted 3-Way Merge Agent** |
| **Terminal Integration** | ✅ Native | ⚠️ Basic CLI | ✅ **Rich Interactive TUI & Background Daemon** |
| **Safety Gate (Human-in-the-loop)** | ✅ Full Control | ⚠️ Prompt Only | ✅ **Multi-Tier Confidence Gates** |
