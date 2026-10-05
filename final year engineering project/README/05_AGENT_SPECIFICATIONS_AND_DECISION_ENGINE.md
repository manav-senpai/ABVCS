# 🧠 Agent Specifications & Decision Engine Mechanics

---

## 1. Multi-Agent Decision Pipeline

The core intelligence of ABVCS lies in the separation of concerns between specialized agents. Each agent operates with a dedicated domain prompt, a restricted toolset, and structured output validation.

```
Raw File Changes (Diff / AST)
               │
               ▼
   [ Change Analyzer Agent ]
   │ - Detects modified functions & symbols
   │ - Clusters related files into Atomic Units
   │
   ▼
   [ Review & Security Agent ] ──(Found Critical Vulnerability)──► [ ABORT / NOTIFY ]
   │ - Scans for API secrets & logic bugs
   │ - Assigns Security Confidence Score
   │
   ▼
   [ Commit Planner Agent ]
   │ - Formulates Conventional Commit
   │ - Drafts Scope, Subject & Technical Body
   │
   ▼
   [ Gatekeeper Decision Engine ]
   ├── High Confidence (>= 95%) & Auto-Mode Enabled ──► [ Execute Deterministic Commit ]
   └── Low Confidence (< 95%) OR Interactive Mode ────► [ CLI/TUI Interactive Approval ]
```

---

## 2. Agent 1: Change Analyzer Agent

* **Role:** Parse raw diffs and AST changes into logical, cohesive change units.
* **Input Schema:**
  ```json
  {
    "raw_diff": "diff --git a/auth.py b/auth.py...",
    "changed_files": ["backend/auth.py", "tests/test_auth.py"],
    "ast_symbols_modified": ["authenticate_user", "generate_jwt_token"]
  }
  ```
* **Output Pydantic Schema (`SemanticChangeUnit`):**
  ```python
  class SemanticChangeUnit(BaseModel):
      unit_id: str
      primary_module: str
      change_category: Literal["feature", "bugfix", "refactor", "test", "docs", "chore"]
      related_files: list[str]
      ast_summary: str
      confidence: float
  ```

---

## 3. Agent 2: Commit Planner Agent

* **Role:** Transform semantic change units into human-grade, standardized Conventional Commits.
* **Prompt Strategy:** Enforces concise 50-character header, explicit scope, and a bulleted technical summary explaining *why* the change was made.
* **Output Pydantic Schema (`CommitProposal`):**
  ```python
  class CommitProposal(BaseModel):
      type: Literal["feat", "fix", "docs", "style", "refactor", "perf", "test", "chore"]
      scope: Optional[str]
      subject: str
      body: list[str]
      breaking_change: bool
      suggested_branch: Optional[str]
      confidence_score: float
  ```

---

## 4. Agent 3: Review & Security Auditor Agent

* **Role:** Act as an automated pre-flight security and quality gatekeeper.
* **Checks Performed:**
  1. Secret Detection (API keys, AWS credentials, passwords).
  2. Injection Vectors (SQL formatting without parameters, unsanitized subprocess calls).
  3. Logic Flaws (Unbounded loops, uncaught exceptions, dead code).
* **Output Pydantic Schema (`SecurityReviewReport`):**
  ```python
  class SecurityIssue(BaseModel):
      file_path: str
      line_number: Optional[int]
      severity: Literal["INFO", "WARNING", "CRITICAL"]
      rule_violated: str
      description: str
      suggested_fix: str

  class SecurityReviewReport(BaseModel):
      overall_status: Literal["PASSED", "WARNINGS_FOUND", "BLOCKED"]
      security_score: int  # 0 to 100
      issues: list[SecurityIssue]
      summary_remarks: str
  ```

---

## 5. Agent 4: Conflict Resolution Agent

* **Role:** Analyze 3-way Git merge conflicts and propose contextually sound code merges.
* **Conflict Input Format:**
  - `OURS` (Current Branch Changes)
  - `BASE` (Common Ancestor Version)
  - `THEIRS` (Incoming Branch Changes)
* **Output Pydantic Schema (`ConflictResolution`):**
  ```python
  class ConflictResolution(BaseModel):
      file_path: str
      resolved_code: str
      resolution_strategy: Literal["ours", "theirs", "synthesized_merge"]
      rationale: str
      syntax_valid: bool
      confidence: float
  ```
