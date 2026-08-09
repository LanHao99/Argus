---
name: research-workflow
description: Deep multi-role research agent that iteratively plans, researches, executes, reviews, and synthesizes. Unlike simple task-execution workflows, this skill enforces depth-gated iteration — each round goes deeper, external information is gathered between rounds, and the Reviewer-Challenger actively pushes for richer analysis. Use when the user needs multi-step research, survey writing, feasibility analysis, or any task requiring iterative deepening rather than one-pass execution.
---

# Research Workflow Skill v2 — Deep Iteration

This skill transforms Pi into a multi-role research agent that **learns and deepens across rounds** rather than just executing and fixing.

## Philosophy

v1 (old): "Do the task. Reviewer checks. Fix if wrong. Next task." — shallow, mechanical.

v2 (new): "Learn before doing. Do the baseline. Challenge yourself to go deeper. Bring in external knowledge. Go deeper again. Only then move on." — research-grade iteration.

## When to Activate

- "研究一下...", "分析这个方向...", "写一篇survey..."
- Any task where shallow one-pass analysis would be insufficient
- Tasks requiring multi-source synthesis, critical evaluation, or iterative refinement

## Architecture

### Five Roles + Two Gates

```
User Request
  │
  ├─ [Planner] ──────────── break into tasks, define depth expectations
  │
  ├─ [Researcher] ───────── gather external info BEFORE executing (NEW)
  │
  ├─ [Engineer R1] ──────── baseline: meet acceptance criteria at surface level
  │     │
  ├─ [Reviewer-Challenger] ─ verify + CHALLENGE: "go deeper on X" (UPGRADED)
  │     │
  ├─ [Engineer R2] ──────── deep dive: address challenges, add insight
  │     │
  ├─ [Reviewer-Challenger] ─ verify + CHALLENGE: "what does external source say?"
  │     │
  ├─ [Engineer R3+] ─────── external enrichment: bring in new knowledge (NEW)
  │     │
  ├─ [Cross-Task Reflector] ─ what did we learn? how does this change remaining tasks? (NEW)
  │     │
  ├─ [Planner Replan Gate] ─ adjust remaining tasks based on new knowledge (NEW)
  │
  └─ [Synthesis] ────────── compile, connect, conclude
```

### Role Definitions

| Role | v1 Behavior | v2 Behavior |
|------|------------|-------------|
| **Planner** | Plan once upfront | Plan upfront + replan after each task based on learnings |
| **Researcher** | (didn't exist) | Gather external info, search, read files BEFORE each task |
| **Engineer** | Execute, fix on REVISE | R1=baseline, R2=deep dive, R3+=external enrichment |
| **Reviewer** | Verify criteria only | Verify + CHALLENGE with specific depth-push questions |
| **Cross-Task Reflector** | (didn't exist) | Extract learnings, update knowledge, inform replan |
| **Synthesis** | Compile deliverables | Compile + connect cross-task insights + identify emergent patterns |

---

## Depth-Gated Iteration (Core Innovation)

Each task goes through AT LEAST 2 rounds, and ideally 3+. The Reviewer-Challenger cannot APPROVE on R1 unless the task is genuinely trivial (e.g., creating a directory structure).

### Round Expectations

| Round | Depth Level | What Must Happen | Minimum Output Standard |
|-------|-------------|------------------|------------------------|
| **R1** | Baseline | Meet all acceptance criteria at surface level | All criteria checked; completeness over depth |
| **R2** | Deep Dive | Address at least 2 Reviewer challenges; add analysis beyond original criteria | New insights that weren't in R1; specific examples/evidence |
| **R3** | External Enrichment | Bring in new information from external sources (web, files, data); cross-reference with other tasks | At least 1 external source cited; connection to another task's findings |
| **R4+** | Synthesis Polish | Address remaining edge cases; strengthen weakest sections; prepare for final synthesis | Each round must point to specific R3 gaps being filled |

### Depth Gate Rules

1. **R1→R2 mandatory for all non-trivial tasks**: Reviewer MUST issue at least 2 substantive CHALLENGEs before APPROVE is even possible.
2. **R2→R3 strongly encouraged**: If the topic has discoverable external information, the Reviewer should CHALLENGE the Engineer to find and incorporate it.
3. **Max 6 rounds per task** (up from 5 in v1).
4. **APPROVE on R2 only if** all challenges addressed AND no obvious external enrichment paths exist.
5. **APPROVE on R3+ is the expected norm** for research-grade tasks.

---

## New Phase: Research (Phase 1.5)

### Before Each Task Execution

```
## Researcher: Information Gathering

Before executing Task <T<N>>, gather relevant external information:

1. SEARCH: Use web search (if available) to find:
   - Recent developments related to this task's topic
   - Key papers, benchmarks, or datasets
   - Competing perspectives or criticisms

2. READ: Review relevant files in the project:
   - Existing deliverables that this task builds on
   - Discussion logs from previous tasks
   - Any reference materials provided by the user

3. LOG: Write findings to output/discussion/T<N>_research_brief.md:
   - Key information discovered
   - Gaps in available information
   - How this information changes the approach to the task
   - Specific sources to cite in the deliverable

## Output
Write a concise research brief (1-2 pages) that the Engineer will use.
```

### Research Brief Template

```markdown
# T<N> Research Brief

## Information Gathered
- [Source 1]: [Key finding]
- [Source 2]: [Key finding]

## Knowledge Gaps
- [What we still don't know]

## Approach Adjustments
- [How this changes our plan for this task]

## Sources to Cite
- [Source]: [Relevance]
```

---

## Upgraded: Reviewer → Reviewer-Challenger

### New Reviewer Output Format

```
## Reviewer-Challenger: Independent Verification + Depth Challenge

### Verification
[Check each acceptance criterion against the Engineer's output]

### Depth Assessment
Round: R<N>
Depth expected at this round: [Baseline / Deep Dive / External Enrichment]
Depth achieved: [assessment]

### Challenges (MANDATORY — at least 2 for R1, at least 1 for R2+)
🔍 CHALLENGE 1: <specific aspect the Engineer should explore deeper>
🔍 CHALLENGE 2: <another angle, external source, or cross-connection>
[CHALLENGE 3+: additional depth-push questions]

### Decision
Return EXACTLY ONE of:
- APPROVE: <reason — only valid on R2+ with all challenges addressed>
- REVISE: <specifics — what depth gaps remain + which challenges are unaddressed>
- BLOCKED: <reason — requires Planner replan, e.g., task scope wrong>
```

### Challenge Types (Reviewer Must Vary These)

| Challenge Type | Example | Purpose |
|---------------|---------|---------|
| **Depth-Push** | "You listed the risks but didn't quantify their probability or impact. Go deeper." | Force quantitative/nuanced analysis |
| **External-Connect** | "What would [specific paper/benchmark/expert] say about this? Find and incorporate." | Bring in outside knowledge |
| **Counter-Perspective** | "You argued for X. What's the strongest counterargument? Address it directly." | Avoid one-sided analysis |
| **Cross-Task Link** | "T2 discovered Y. How does Y change your analysis here in T3?" | Build cumulative knowledge |
| **Edge-Case Hunt** | "Under what conditions would your conclusion fail? Describe 2 scenarios." | Test robustness |
| **Practicality Check** | "How would a practitioner actually use this finding? Give a concrete scenario." | Ground in reality |

---

## New Phase: Cross-Task Reflection (Phase 2.5)

After each task is APPROVED, BEFORE starting the next task:

```
## Cross-Task Reflector: Learning Extraction

### What We Learned from T<N>
1. [Key finding that emerged]
2. [Surprising insight]
3. [Methodological lesson]

### Impact on Remaining Tasks
- T<X>: [Adjustment needed based on T<N> finding]
- T<Y>: [New question to address]
- T<Z>: [No change]

### Knowledge to Carry Forward
[Write to output/learning_log.md: accumulated insights across all tasks]

### Replan Recommendation
- [ ] No replan needed — remaining tasks still valid
- [ ] Minor adjustment — tweak T<X> acceptance criteria
- [ ] Major replan — significant scope change needed
```

### Learning Log Format

`output/learning_log.md` accumulates across tasks:

```markdown
# Cross-Task Learning Log

## After T1: [Key learning]
## After T2: [Key learning]
## After T3: [Key learning]

## Emergent Patterns (filled during Synthesis)
[Patterns visible only when looking across all tasks]
```

---

## Planner Replan Gate

After Cross-Task Reflection, the Planner reviews:

```
## Planner: Replan Check

### Current State
- Completed: T1-T<N>
- Remaining: T<X>-T<Z>

### Assessment
[Review learning_log.md and reflection]

### Decision
- [ ] CONTINUE: remaining tasks unchanged
- [ ] ADJUST: modify T<X> as follows: <specific changes>
- [ ] SPLIT: T<X> is too large, split into T<X>a and T<X>b
- [ ] MERGE: T<X> and T<Y> overlap significantly, merge them
- [ ] ADD: New task needed based on learnings
```

---

## Updated State Management

```json
{
  "objective": "user's original request",
  "tasks": [
    {
      "id": "T1",
      "title": "...",
      "objective": "...",
      "acceptance": "checkable criteria",
      "depth_target": "baseline|deep_dive|external_enrichment",
      "status": "pending|running|done|blocked",
      "engineer_rounds": 0,
      "reviewer_verdicts": [],
      "challenges_issued": [],
      "challenges_resolved": [],
      "cross_task_learnings": []
    }
  ],
  "current_phase": "planning|researching|executing|reviewing|reflecting|replanning|synthesis|done",
  "started_at": "ISO timestamp",
  "learning_log": "output/learning_log.md"
}
```

---

## Updated Progress Display

```
📋 [Planner] → 4 tasks defined, depth targets set
🔍 [Researcher T1] → gathered 5 sources, identified 2 knowledge gaps
🔄 [Engineer T1 R1] → baseline complete
🧐 [Reviewer-Challenger T1 R1] → 3 challenges issued
🔄 [Engineer T1 R2] → deep dive: addressed 2/3 challenges
🧐 [Reviewer-Challenger T1 R2] → 1 challenge remains + external enrichment requested
🔄 [Engineer T1 R3] → external enrichment: incorporated 2 papers
✅ [Reviewer-Challenger T1 R3] → APPROVE after 3 rounds
💡 [Cross-Task Reflector T1] → 2 learnings that change T3 approach
🔁 [Planner Replan] → ADJUST: T3 acceptance criteria updated
...
📝 [Synthesis] → 4 tasks, 12 total rounds, 8 external sources, emergent pattern found
```

---

## Updated Output Structure

```
output/
├── deliverables/          ← Final products
├── discussion/
│   ├── T<N>_research_brief.md    ← (NEW) Pre-task research findings
│   ├── T<N>_engineer_discussion.md  ← Per-round decisions and rejected approaches
│   ├── T<N>_reflection.md        ← (NEW) Cross-task reflection for this task
│   └── reviewer_trail.md         ← All reviewer verdicts and challenges
├── learning_log.md               ← (NEW) Accumulated insights across tasks
└── README.md                     ← Final synthesis
```

---

## Updated Workflow Summary

### Phase 0: Intake
(Same as v1)

### Phase 1: Planning
- Planner breaks objective into 2-5 tasks
- **NEW**: Each task gets a `depth_target` (how deep should we go?)
- **NEW**: Planner identifies external information needs for each task

### Phase 1.5: Research (NEW)
- **BEFORE** each task, Researcher gathers external info
- Writes research brief to `output/discussion/T<N>_research_brief.md`
- This phase runs SEPARATELY for each task (not once upfront)

### Phase 2: Deep Execution Loop
For each task in dependency order:
1. **Research** (Phase 1.5) — gather info
2. **Engineer R1** — baseline
3. **Reviewer-Challenger** — verify + issue ≥2 challenges
4. **Engineer R2** — deep dive, address challenges
5. **Reviewer-Challenger** — verify + issue ≥1 challenge (push to R3)
6. **Engineer R3** — external enrichment
7. **Reviewer-Challenger** — APPROVE (normative) or REVISE
8. **Cross-Task Reflector** — extract learnings
9. **Planner Replan Gate** — adjust remaining tasks

### Phase 3: Synthesis
- Compile deliverables + cross-task insights
- Identify emergent patterns (visible only across all tasks)
- Write final README.md

---

## Anti-Regression Guards (v1 + v2 additions)

1. No single-round tasks: R1-only APPROVE requires explicit justification
2. No unchallenged acceptance: Reviewer MUST issue challenges, not just verify
3. No isolated tasks: Cross-Task Reflector connects learnings across tasks
4. No stale plans: Planner replans after each task based on new knowledge
5. (v1 guards retained: no daemon, clear paths, time-boxing, early blocker surfacing, no scope creep)
