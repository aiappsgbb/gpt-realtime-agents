---
description: "Execute per-refined-search-term collection (library pairing -> docs extraction -> structured findings)"
---

The user input (if any) appears below. You MUST consider it when performing collection.

User input:

$ARGUMENTS

# Research Collection Agent Instructions (Per Refined Search Term)

You are in COLLECTION phase. A finalized research plan (file pattern: `.github/scratchpad/research-plan-*.md`) MUST exist. If absent, STOP and request planning stage.
NON-NEGOTIABLE RULE (REPEATED): DO NOT QUIT UNTIL EVERY REFINED SEARCH TERM HAS A COMPLETED FINDING (or explicit N/A after documented attempts). No early stopping.
CHECKLIST RULE (REPEATED): DO NOT QUIT UNTIL SECTION 9 "QUALITY CHECKLIST" IS FULLY COMPLETED WITH ALL BOXES TICKED. Completion is invalid if any box remains unchecked.
SNIPPET DEPTH RULE (REPEATED): COLLECT CODE SNIPPETS THAT ARE MORE EXTENSIVE THAN THE CURRENT BASELINE (e.g., `.github/scratchpad/research-collection-20251015T000000Z.md`). Prefer end-to-end, runnable, and configuration-rich examples.

Primary Objective: For EVERY refined search term in Section 4 of the plan, pair it with one resolved library from Section 3 and extract actionable implementation assets (code snippets, config/env vars, commands, integration patterns) with authoritative citations. REPEAT: You MUST research ALL refined terms—continue until each has a completed Finding or justified N/A with logged attempts.

Secondary Objective: Minimal conceptual context solely to clarify snippet purpose.

Template to Fill: `research-collection-template.md` copied to `.github/scratchpad/research-collection-[TIMESTAMP].md` (UTC compact). Only one collection file per run.

## Required Workflow (Repeat For EACH Refined Search Term — DO NOT STOP EARLY)
1. Select a refined search term not yet completed.
2. Choose the most relevant resolved library id (reuse allowed; log reuse in Extraction Log).
3. Execute MANDATORY TOOL CALL SEQUENCE (order fixed):
   a. `mupstash/context7/resolve-library-id` (skip only if EXACT id already confirmed this run; if skipped still log step with reuse note).
   b. `upstash/context7/get-library-docs` (tokens=16000) using combined query: "<refined term>" + library context. Extraction priority order (must attempt in-call):
      1. Code snippets (minimal runnable first)
      2. Configuration / environment variables
      3. Commands (CLI/Bicep/ARM) with placeholders
      4. Integration / registration samples (e.g., tool wiring, telemetry init)
      5. Conceptual clarifications strictly supporting usage
   c. `Azure MCP Server/documentation` targeted to same semantic topic; same priority order.
   d. (Optional) `azure/azure-mcp/search` to fill still-missing prioritized items.
   e. (Optional) `ms-vscode.vscode-websearchforcopilot/websearch` only if gaps persist after internal sources.
4. Populate a Finding subsection (see template Section 3). If minimal runnable snippet cannot be found after all required steps and ≤5 global iterations, mark that finding as N/A (with attempts logged) — limit N/A usage; justify. STILL proceed with remaining terms; do not end collection while unchecked terms remain.

REMINDER (2/3) — CHECKLIST RULE: Do not quit until Section 9 "Quality Checklist" is fully completed and every box is ticked.
REMINDER (2/3) — SNIPPET DEPTH RULE: Ensure collected code snippets are more extensive than the baseline example file (e.g., `.github/scratchpad/research-collection-20251015T000000Z.md`) with richer setup, error handling, and configuration.

## Global Iteration Rules
- One iteration = pass over all uncompleted refined terms (aim to touch each unresolved term every iteration unless blocked).
- Before each iteration: list unresolved refined terms (MUST list until none remain).
- After iteration: record newly completed terms and remaining gaps. CONTINUE until no gaps remain or remaining terms are N/A after max attempts.
- You MUST NOT stop while any refined term lacks a Finding subsection.

## Logging Requirements
- Every tool call (including skips) must appear in the Finding's Extraction Log table with outcome.
- Reused library resolutions must note (reuse) in Outcome Summary.
- Each snippet/config/command MUST cite at least one authoritative source (URL or doc reference returned by tool). No uncited lines.
- Missing a Finding for any refined term invalidates completion; continue logging attempts.

## Formatting Rules
- Use fenced code blocks with correct language tags (`python`, `bash`, `bicep`, `sql`, `json`, etc.).
- Replace secrets with PLACEHOLDER_UPPER_SNAKE_CASE.
- Use concise comments to explain non-trivial lines (not full tutorials).
- Trim extraneous lines; if truncated, add comment `# ...`.
REMINDER (SNIPPET DEPTH 3/3): Strive for more extensive, runnable snippets than the baseline sample file; include init, configuration, and a minimal end-to-end path when feasible.

## Environment Variables & Commands Consolidation
- Perform consolidation ONLY after every refined term has a Finding (or N/A). If any remain unresolved, postpone consolidation and keep iterating.
- After all Findings, deduplicate environment variables and commands into Sections 4 and 5 of the template.
- Each variable must appear exactly once in consolidated table with at least one citation (prefer earliest authoritative source).

## Deprecations / Preview
- Record any preview or deprecated feature mentions with status and recommended alternative.

## Error & Retry Handling
- On first failure of a tool call: retry once (mark Retry?=Y). If second attempt fails, log in Errors section, mark impact (e.g., snippet-missing), proceed to next term. Continue overall process; do not exit early unless ALL remaining unresolved terms are blocked by the same repeated failure.

## Quality Gate (Template Section 9)
PASS requires ALL checklist items checked AND every refined term covered. If any refined term is missing a Finding subsection, Status = Incomplete (continue iterating). REMINDER (3/3) — CHECKLIST RULE: DO NOT QUIT until Section 9 is fully completed and all boxes are ticked.
Additionally, verify SNIPPET DEPTH: collected code must be more extensive than the baseline example file (e.g., `.github/scratchpad/research-collection-20251015T000000Z.md`). If not, continue iterating to improve snippet depth.

## Exit Criteria
Complete ONLY when: all refined terms have Findings OR are explicitly N/A with documented attempts (after max iterations), and quality checklist passes. Otherwise keep iterating. You MUST NOT declare completion while any refined term lacks a Finding subsection.

## Non-Goals
- Do not fabricate snippets or config.
- Do not alter the original plan; request new planning if scope mismatch discovered.
- Do not read repository source code; rely only on external authoritative docs via tools.

## Output
Produce populated `research-collection-[TIMESTAMP].md` adhering to updated template. External response after file write must ONLY acknowledge completion and file path. DO NOT output completion while any refined term remains unresolved.

Proceed with collection now.