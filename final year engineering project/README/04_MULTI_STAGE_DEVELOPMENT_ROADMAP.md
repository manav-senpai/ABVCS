# 🗺️ Multi-Stage Engineering Roadmap & Milestones

---

## Overview

ABVCS is architected to be delivered across **6 comprehensive, independently verifiable engineering stages**. This structured lifecycle guarantees that at the end of every stage, a working, demonstrable deliverable is produced.

```
+--------------------------------------------------------------------------------+
|  STAGE 1: Deterministic Git Engine & Repository Management Core                |
|  - Working Checkpoint: Robust Python Git interop, status, diff, staging, logs  |
+--------------------------------------------------------------------------------+
                                       |
                                       v
+--------------------------------------------------------------------------------+
|  STAGE 2: File-System Watcher & AST Semantic Boundary Engine                   |
|  - Working Checkpoint: Debounced event stream & language AST difference parser |
+--------------------------------------------------------------------------------+
                                       |
                                       v
+--------------------------------------------------------------------------------+
|  STAGE 3: Multi-Agent Orchestrator Framework & Schema Validation               |
|  - Working Checkpoint: Pydantic schemas, state machine, multi-provider LLM bus |
+--------------------------------------------------------------------------------+
                                       |
                                       v
+--------------------------------------------------------------------------------+
|  STAGE 4: Autonomous Commit Planner, Review & Security Auditor                 |
|  - Working Checkpoint: Conventional commit generator, vulnerability detector   |
+--------------------------------------------------------------------------------+
                                       |
                                       v
+--------------------------------------------------------------------------------+
|  STAGE 5: Intelligent Merge Conflict Resolver & Repository History Agent       |
|  - Working Checkpoint: 3-way AST conflict analysis, natural language git query |
+--------------------------------------------------------------------------------+
                                       |
                                       v
+--------------------------------------------------------------------------------+
|  STAGE 6: Rich Terminal UI (TUI), Daemon Mode & Evaluation Benchmark Suite     |
|  - Working Checkpoint: Complete CLI suite, live dashboard, benchmark metrics   |
+--------------------------------------------------------------------------------+
```

---

## Stage 1: Deterministic Git Engine Core
* **Objective:** Build a rock-solid, production-grade Python abstraction over the local Git binary and repository objects.
* **Key Components:**
  - `GitController`: Handles `init`, `status`, `diff`, `add`, `commit`, `branch`, `checkout`, `log`, and `stash`.
  - Robust exception handling for uncommitted changes, dirty trees, and detached HEAD states.
  - Safe subprocess execution preventing shell injection.
* **Deliverable Checkpoint:** A Python module capable of performing 100% of standard Git operations programmatically with typed return objects.

---

## Stage 2: File-System Watcher & AST Semantic Boundary Engine
* **Objective:** Implement a real-time monitoring engine that detects when code changes reach logical completion.
* **Key Components:**
  - `FileSystemWatcher`: Async file tracking with configurable debounce windows (e.g. 2.5s idle after typing).
  - `ASTChangeParser`: Extracts function/class level diffs rather than naive line numbers.
  - `ChangeGrouper`: Clusters related files (e.g., `user_service.py` + `test_user_service.py`) into atomic change units.
* **Deliverable Checkpoint:** Live event stream detecting when a developer finishes editing a function or module.

---

## Stage 3: Multi-Agent Orchestrator Framework & Schema Validation
* **Objective:** Construct the foundational multi-agent communication and routing pipeline.
* **Key Components:**
  - `AgentOrchestrator`: Coordinates task lifecycle, context memory, and agent dispatching.
  - Strict Pydantic Models: `CommitProposal`, `SecurityReviewReport`, `ConflictSolution`, `HistoryAnswer`.
  - Fallback Redundancy: Automatic fallback to local regex/heuristics if LLM API is unavailable.
* **Deliverable Checkpoint:** Orchestration engine that dispatches diffs to dummy/real agents and validates structured JSON schemas.

---

## Stage 4: Specialized Agents (Commit, Review & Security, Test)
* **Objective:** Implement the core cognitive intelligence for commit drafting and code safety audits.
* **Key Components:**
  - `CommitPlannerAgent`: Analyzes staged diffs, generates Conventional Commits with scope, rationale, and body.
  - `ReviewSecurityAgent`: Scans for OWASP top vulnerabilities (API keys, SQL injections, insecure deserialization, unhandled errors).
  - `TestRunnerAgent`: Detects test frameworks (pytest, unittest), executes tests in an isolated subprocess, and verifies code stability.
* **Deliverable Checkpoint:** Autonomous generation of atomic commits with comprehensive security scorecards.

---

## Stage 5: Intelligent Merge Conflict Resolver & History Agent
* **Objective:** Tackle complex Git branch merging and natural language repository exploration.
* **Key Components:**
  - `ConflictResolverAgent`: Parses 3-way merge conflicts (`<<<<<<<`, `=======`, `>>>>>>>`), examines intent on both branches, and proposes syntactically clean merge solutions.
  - `RepositoryHistoryAgent`: Vector/semantic or context-augmented search over commit history to answer natural language developer questions.
* **Deliverable Checkpoint:** Automated resolution of merge conflicts with clear developer explanations.

---

## Stage 6: Rich Interactive CLI/TUI, Daemon Mode & Evaluation Harness
* **Objective:** Polish the developer experience with a stunning terminal interface and rigorous evaluation metrics.
* **Key Components:**
  - `abvcs` CLI Suite: Commands like `abvcs start`, `abvcs status`, `abvcs commit`, `abvcs review`, `abvcs resolve`, `abvcs ask`.
  - `Rich` / `Textual` TUI: Interactive visual commit log, live diff inspector, and real-time agent status cards.
  - Evaluation Harness: Quantitative metrics (Commit Acceptance Rate, False Positive Review Rate, Merge Conflict Success Rate, Mean Time to Commit).
* **Deliverable Checkpoint:** Full-fledged, production-ready system with complete user documentation and evaluation benchmarks.
