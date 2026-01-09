---
description: "Collection template – iterate refined search terms -> library docs -> structured findings with code/config emphasis"
---

# Research Collection Log: [TOPIC]

Plan File Used: [plan filename]
Date: [DATE]
Collector: [Agent/User]
Initial Prompt (verbatim): [original question]
Referenced Research Plan: [plan filename]

## 1. Plan Validation
IMPORTANT (REPEAT RULE): DO NOT STOP COLLECTION UNTIL EVERY REFINED SEARCH TERM HAS A COMPLETED FINDING (or explicit N/A with documented attempts). This rule applies throughout the template. If any term remains unchecked, continue iterating.
| Check | Result | Notes |
|-------|--------|-------|
| Plan File Found | [Y/N] |  |
| Refined Terms Present | [Y/N] | Count: [n] |
| Libraries Present | [Y/N] | Count: [n] |
| Scope Items Parsed | [Y/N] |  |
| Proceed? | [YES/NO] | If NO, reason |

Blocking Clarifications (if any): [none or list]

## 2. Refined Search Term Checklist
REPEAT RULE: Every refined search term must progress to a completed Finding section. No early termination allowed. Iterate until all rows show Completed.
For each term below, a mandatory tool call sequence must be executed. Check when Finding section completed.

| # | Refined Search Term | Paired Library (resolved id) | Completed? |
|---|---------------------|------------------------------|------------|
| 1 | [term] | [library_id] | [ ] |
| 2 | [term] | [library_id] | [ ] |
| 3 | [term] | [library_id] | [ ] |
| 4 | [term] | [library_id] | [ ] |
| 5 | [term] | [library_id] | [ ] |
| 6 | [term] | [library_id] | [ ] |
| .. | ... | ... | ... |

## 3. Findings (One Subsection Per Refined Search Term)
REPEAT RULE: Create a Finding subsection for EVERY refined search term. Do not omit any. If information truly unavailable after required attempts, mark N/A but still include the subsection and attempts log.
Repeat the structure below for EACH refined search term in the plan (DO NOT SKIP). Number sequentially. Continue iterations until all terms completed.

### Finding 1: [Refined Search Term]
Paired Library: [resolved library id]
Original Broad Topic Mapping: [broad topic]

#### Summary
- [Concise synthesized outcome (≤30 words)]

#### Code Snippet (Minimal)
```[language]
// minimal snippet showing core concept
```
> Sources: [citation(s)]

#### Code Snippet (Advanced / Edge)
```[language]
// optional advanced pattern (omit section if none)
```
> Sources: [citation(s)]

#### Config / Env / Schema
| Type | Name / Key | Purpose | Placeholder / Example | Citation |
|------|------------|---------|-----------------------|----------|
| ENV  | EXAMPLE_VAR | Purpose desc | <VALUE> | [link] |

#### Commands / Provisioning
```bash
# CLI / infra commands with placeholders
```
> Sources: [citation]

#### Integration / Registration
```json
{ "example": "integration fragment" }
```
> Sources: [citation]

#### Other Relevant Info
- [Misc implementation insight + citation]

Add / remove sub-sections as needed to capture scope, e.g. if "Commands / Provisioning" not relevant, omit that sub-section.
---

### Finding 2: [Refined Search Term]
... (repeat identical structure for each term) ...
Add / remove sub-sections as needed to capture scope, e.g. if "Commands / Provisioning" not relevant, omit that sub-section.

## 4. Consolidated Environment Variables
| Name | Purpose | Used In Findings | Required (Y/N) | Default / Placeholder | Citation |
|------|---------|------------------|----------------|-----------------------|----------|

## 5. Consolidated Commands / Infra
```bash
# Aggregate essential commands (deduplicated)
```
```bicep
// Key infra snippets
```

## 6. Consolidated requirements.txt
pandas
openai
numpy
requests
etc..

## 7. Outstanding Gaps
NOTE: Gaps listed here must not include un-researched refined terms; if a term is not yet fully researched, continue collection instead of listing it as a gap. Only record genuine absence after exhaustive attempts.
- [Gap] (Attempts: [tools/queries])

## 8. Errors (If Occurred)
| Tool | Query | Error | Retry Outcome | Impact |
|------|-------|-------|---------------|--------|

## 9. Quality Checklist
REPEAT RULE: Validation fails if ANY refined search term lacks a completed Finding subsection.
- [ ] Every refined search term has a Finding subsection (REQUIRED – if not, DO NOT STOP)
- [ ] Each Finding minimal code snippet present (or explicitly N/A + attempt logged)
- [ ] Every snippet & factual line cited
- [ ] Environment variables consolidated
- [ ] Commands/provisioning consolidated without duplication
- [ ] Consolidated requirements.txt included
- [ ] No unresolved blocking clarifications
- [ ] Deprecations / preview flags captured or confirmed none
- [ ] Open Notes from plan addressed (each item either satisfied or logged as gap)
- [ ] Status correctly reflects completeness

## 10. Status Summary
Status: [Complete / Incomplete]
Completion Rationale: [brief]
Missing (if Incomplete): [list]
Next Actions: [list]

---
*End of Research Collection Template*