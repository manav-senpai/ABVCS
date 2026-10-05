# 🏛️ ABVCS System Architecture & Multi-Agent Swarm

---

## 1. High-Level Architectural Model

ABVCS is engineered as a decoupled, multi-layered Python architecture consisting of:
1. **The Ingestion & Event Monitoring Layer (File Watcher & AST Tracker)**
2. **The Agent Orchestrator & State Machine**
3. **The Specialized Agent Swarm (Sub-Agents)**
4. **The Verification & Gatekeeping Engine**
5. **The Deterministic Git & Storage Engine**
6. **The User Interface Layer (CLI, TUI, Interactive Daemon)**

```
+-------------------------------------------------------------------------+
|                         CLI / Terminal UI (Rich / Click)                |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                         ABVCS Daemon Core (AsyncIO)                     |
|                                                                         |
|   +-----------------------------------------------------------------+   |
|   |                  File System & AST Change Watcher               |   |
|   |          (Debounced Event Stream, Tree-Sitter / AST Parser)     |   |
|   +-----------------------------------------------------------------+   |
|                                    |                                    |
|                                    v                                    |
|   +-----------------------------------------------------------------+   |
|   |                     Agent Orchestrator Pipeline                 |   |
|   |         - Working Memory & Context Aggregator                   |   |
|   |         - Task Dispatcher & Agent Router                        |   |
|   |         - Intent Classifier (Prompt Mode vs. Auto Mode)         |   |
|   +-----------------------------------------------------------------+   |
|            |                |                 |                |        |
|            v                v                 v                v        |
|     +-------------+  +-------------+   +-------------+  +-------------+ |
|     |   Change    |  |   Commit    |   | Review & Sec|  |  Conflict   | |
|     |  Analyzer   |  |   Planner   |   |   Auditor   |  |  Resolver   | |
|     |   Agent     |  |   Agent     |   |   Agent     |  |   Agent     | |
|     +-------------+  +-------------+   +-------------+  +-------------+ |
|            |                |                 |                |        |
|            +----------------+--------+--------+----------------+        |
|                                      |                                  |
|                                      v                                  |
|   +-----------------------------------------------------------------+   |
|   |                    Policy & Gatekeeper Engine                   |   |
|   |         - Syntax Check & AST Validity Verification              |   |
|   |         - Isolated Sandbox Test Execution (PyTest/Unittest)     |   |
|   |         - Confidence Scorer & Human-in-the-Loop Thresholds      |   |
|   +-----------------------------------------------------------------+   |
|                                      |                                  |
|                                      v                                  |
|   +-----------------------------------------------------------------+   |
|   |                   Deterministic Git Controller                  |   |
|   |      (Atomic Git Commits, Branching, Staging, Reverts, Diffs)   |   |
|   +-----------------------------------------------------------------+   |
+-------------------------------------------------------------------------+
```

---

## 2. The Specialized Agent Swarm Breakdown

Each agent in ABVCS is a focused reasoning unit with a discrete prompt contract, specific tools, and a strictly structured Pydantic schema output.

```
                  +-------------------------------+
                  |       Agent Orchestrator      |
                  +---------------+---------------+
                                  |
         +------------------------+------------------------+
         |                        |                        |
         v                        v                        v
+------------------+     +------------------+     +------------------+
|  Change Analyzer |     |  Commit Planner  |     |  Review & Security|
|      Agent       |     |      Agent       |     |      Agent       |
|                  |     |                  |     |                  |
| - AST Difference |     | - Chunking Diffs |     | - Vulnerabilities|
| - Semantic Units |     | - Atomic Commits |     | - Code Quality   |
| - Scope Detection|     | - Commit Messages|     | - Anti-Patterns  |
+------------------+     +------------------+     +------------------+
         |                        |                        |
         +------------------------+------------------------+
                                  |
                                  v
                  +-------------------------------+
                  |  Conflict & Resolution Agent  |
                  |                               |
                  | - 3-Way AST Conflict Parsing  |
                  | - Contextual Code Merging     |
                  | - Human Override Fallbacks    |
                  +-------------------------------+
```

### 2.1 Change Analyzer Agent (The "Sensor")
* **Responsibility:** Ingests raw file system diffs and groups them into logical semantic changes using language AST analysis (e.g. function additions, refactors, config changes, test updates).
* **Inputs:** Raw unified diff, modified file paths, file AST snapshots.
* **Output:** `SemanticChangeGroup` (list of related file patches categorized by functional intent).

### 2.2 Commit Planner Agent (The "Architect")
* **Responsibility:** Determines if a change group is ready for atomic committing. Formulates high-quality semantic commit messages following the Conventional Commits standard (`feat(auth): ...`, `fix(db): ...`, `refactor(api): ...`).
* **Inputs:** `SemanticChangeGroup`, recent commit history context, optional user prompt.
* **Output:** `CommitPlan` (target files to stage, commit type, scope, subject, detailed body justification).

### 2.3 Review & Security Auditor Agent (The "Guardian")
* **Responsibility:** Analyzes code diffs for security vulnerabilities (hardcoded secrets, SQL injection vectors, memory leaks, unhandled exceptions) and stylistic regressions.
* **Inputs:** Staged code diffs, project security rules.
* **Output:** `AuditReport` (status: `PASS` / `WARN` / `BLOCK`, list of detected issues with severity and remediation suggestions).

### 2.4 Conflict Resolution Agent (The "Mediator")
* **Responsibility:** When a Git merge/rebase yields conflicts (`<<<<<<<`, `=======`, `>>>>>>>`), this agent extracts the base ancestor, current branch, and incoming branch, determines the intent of both changes, and generates an integrated, syntactically valid resolution.
* **Inputs:** Conflicted file content with standard conflict markers, commit logs of both branches.
* **Output:** `ConflictResolution` (resolved code buffer, explanation of merged logic, confidence rating).

### 2.5 Natural Language Interactive Assistant Agent (The "Partner")
* **Responsibility:** Allows the developer to interact with the repository using conversational commands via CLI (e.g., `abvcs explain "why was this endpoint modified?"` or `abvcs rollback "undo the broken payment changes"`).
* **Inputs:** Natural language query, git log, blame metadata, code snippets.
* **Output:** Structured explanation or executable repository action plan.

---

## 3. Decision Boundary: Autonomous Mode vs. Human-in-the-Loop

```
                       [ Incoming Code Change ]
                                  |
                                  v
                      [ Change Analyzer Agent ]
                                  |
                                  v
                      [ Commit Planner Agent ]
                                  |
                                  v
                      [ Review & Security Agent ]
                                  |
                  +---------------+---------------+
                  | Any Security Blocker Or Error?|
                  +---------------+---------------+
                         /                 \
                     [YES]                 [NO]
                      /                     \
        +-----------------------+     +-------------------------------+
        |  HALT: Alert User in  |     |  Calculate Confidence Score   |
        |  CLI / TUI Terminal   |     +---------------+---------------+
        +-----------------------+                     |
                                    +-----------------+-----------------+
                                    |                                   |
                             Confidence >= 95%                   Confidence < 95%
                             & Auto-Mode Active                  (Or Prompt Mode)
                                    |                                   |
                                    v                                   v
                      +---------------------------+       +---------------------------+
                      |  Autonomous Execution:    |       |  Interactive Approval:    |
                      |  - Stage Files            |       |  - Display Proposed Plan  |
                      |  - Execute Atomic Commit  |       |  - Await User Confirm/Edit|
                      |  - Log Audit Entry        |       |  - Execute on Approval    |
                      +---------------------------+       +---------------------------+
```
