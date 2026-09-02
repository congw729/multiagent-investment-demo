# JiuWen Multi-Agent Development Handbook

> Using the "US Equity Research Multi-Agent Teaching Demo" as a complete case study, this handbook teaches you how to design and run a multi-agent project from scratch.
> Version: v1.0 | Companion team: task-3e864b925b "US Equity Research Multi-Agent Teaching Demo"
> Statement: All data and analyses referenced in this handbook are **teaching samples**, used only to demonstrate JiuwenSwarm platform capabilities, and **do NOT constitute investment advice**.

---

## Table of Contents

1. [What This Handbook Teaches](#1-what-this-handbook-teaches)
2. [Step 1: Decompose the Project Goal](#2-step-1-decompose-the-project-goal)
3. [Step 2: Design the Team and Agent Roles](#3-step-2-design-the-team-and-agent-roles)
4. [Step 3: Design the Task DAG and Dependencies](#4-step-3-design-the-task-dag-and-dependencies)
5. [Step 4: Design Data and File Handoffs](#5-step-4-design-data-and-file-handoffs)
6. [Step 5: Design the Member Collaboration Mechanism](#6-step-5-design-the-member-collaboration-mechanism)
7. [Step 6: Design the Acceptance Process (QA Gate + Leader Arbitration)](#7-step-6-design-the-acceptance-process-qa-gate--leader-arbitration)
8. [Platform Capability & Demo Stage Mapping Table](#8-platform-capability--demo-stage-mapping-table)
9. [5-Minute Quick Start: Reproduce Your First Multi-Agent Project](#9-5-minute-quick-start-reproduce-your-first-multi-agent-project)
10. [Appendix: Full Workflow Diagram of This Demo](#10-appendix-full-workflow-diagram-of-this-demo)

---

## 1. What This Handbook Teaches

After seeing a multi-agent demo, many learners are most puzzled by one thing: **"It looks impressive, but how do I start when I have my own requirements?"**

This handbook dissects the "US Equity Research Multi-Agent Teaching Demo" — a complete project that actually ran end-to-end — to thoroughly explain the **six-step design method** for multi-agent projects:

| Step | Question It Answers | Section |
|---|---|---|
| Goal decomposition | How does a vague user request become an executable task tree? | §2 |
| Role design | Who is each agent, what can it do, and where are its boundaries? | §3 |
| DAG design | What runs first/later among tasks, and what can run in parallel? | §4 |
| Handoff design | How does data flow safely between agents? | §5 |
| Collaboration design | How do members communicate and align? | §6 |
| Acceptance design | Who checks the output, and what counts as done? | §7 |

Finally, it provides the **platform capability × demo stage mapping table** (§8) and **5-minute reproduction steps** (§9) so you can build your own project by following along.

> Engineering design principle: **the success of a multi-agent project depends not on the number of agents, but on "clear division of labor + explicit task dependencies + standardized handoffs"**. This demo applies all three at every step.

---

## 2. Step 1: Decompose the Project Goal

### 2.1 From a One-Line Request to a Goal Tree

The user's original words (raw requirement):

> "Help me analyze a US-listed company, give a future stock price forecast, and produce an investment research report. I want to learn how to develop multi-agent systems."

This sentence contains multiple layers of information. The first-level decomposition (**goal decomposition, not task decomposition**):

| Requirement Keyword | Implicit Goal | Derived Sub-Goal |
|---|---|---|
| "analyze a company" | needs **data** support | prepare financial + price sample data |
| "stock price forecast" | needs **multi-dimensional analysis inputs** | three-track analysis: fundamental / technical / risk & sentiment |
| "investment research report" | needs **combined conclusions** | forecast synthesis + report integration |
| "learn multi-agent" | needs **teaching output** | reproducible process + teaching handbook |

This yields the **goal tree**:

```
Project goal: deliver "US equity research conclusions + multi-agent development teaching"
├── Data layer goal: standardized sample data (offline reproducible)
├── Analysis layer goal: three parallel analyses (fundamental / technical / risk)
├── Synthesis layer goal: target price range + scenario projection + scorecard
└── Delivery layer goal: investment research report + teaching handbook (with disclaimer)
```

### 2.2 From Goals to Tasks (inputs written into `create_task` at design time)

Each sub-goal maps to a **task**; the task description states what to do, what to produce, and the acceptance criteria. This demo's task list is as follows (verifiable on the task board via `view_task`):

| Task ID | Sub-Goal | Deliverable | Dependencies |
|---|---|---|---|
| task-data | Data ready | financial + price CSV under demo-data/ | none (first stage) |
| task-fundamental | Fundamental analysis | fundamental analysis under analysis/ | task-data |
| task-technical | Technical analysis | technical analysis under analysis/ | task-data |
| task-risk | Risk & sentiment | risk & sentiment analysis under analysis/ | task-data |
| task-qa | QA verification (independent gate) | pass/fail + evidence list for the three analyses | task-fundamental, task-technical, task-risk |
| task-forecast | Combined forecast | outputs/ target price + scenarios + scorecard | task-qa |
| task-report | Final delivery | deliverables/ two final documents | task-forecast |

> Design insight: the **goal → task** mapping should satisfy "one goal corresponds to one verifiable deliverable". If a goal has no clear output file, the decomposition is not thorough enough.

---

## 3. Step 2: Design the Team and Agent Roles

### 3.1 Team Skeleton: Leader + Dedicated Agents

A multi-agent project needs a **Leader (controller)** responsible for task decomposition, coordination, and acceptance; the remaining members are set up on the **domain-independence** principle.

This demo's team structure (created via `build_team` / `spawn_teammate`):

```
                ┌─────────────────────────┐
                │  team-leader Project Lead│  controller + teaching
                └────────────┬────────────┘
        ┌───────────┬────────┼────────┬───────────┐
        ▼           ▼        ▼        ▼           ▼
   data-researcher fundamental technical risk-sentinel
   Data Researcher  Fundamental  Technical  Risk & Sentiment
        (first)   (parallel) (parallel) (parallel)
                    │           │        │
                    └──► qa-tester (independent QA gate) ◄──┘
                             │  verify analyses vs. source data
                             ▼
                      forecaster (convergence)
                             ▼
                  report-synthesizer (final delivery)
```

### 3.2 How to Write the Role Description (desc) — This Demo's Template

Each agent is created via `spawn_teammate`; the **description (desc / persona) determines the agent's positioning, expertise, and boundaries**. The golden formula for writing a desc:

```
[Who you are] + [your domain of expertise] + [what output you are responsible for] + [what you are explicitly NOT responsible for]
```

Using this demo's seven roles as examples:

| Role | display_name | Desc Essentials (who + expertise + responsibilities + non-responsibilities) |
|---|---|---|
| data-researcher | Data Researcher | Data engineer; expertise in structured data design, CSV generation/validation, definition notes; responsible for producing standardized sample data to .team/demo-data/; **NOT responsible for** investment analysis and forecasts |
| fundamental-analyst | Fundamental Analyst | Focus on financial reports: revenue growth, margins, ROE, debt ratio, cash flow, valuation; outputs fundamental score + highlights/risks + valuation judgment; **NOT responsible for** candlestick/sentiment/macro |
| technical-analyst | Technical Analyst | Quantitative technical analysis: candlestick patterns, MAs, RSI/MACD, volume, support/resistance; outputs trend rating + key price levels; **NOT responsible for** fundamentals/sentiment |
| risk-sentinel | Risk & Sentiment Analyst | Non-financial risks from news, policy, regulation, competition, macro; outputs risk rating + sentiment judgment + scenario stress; **NOT responsible for** financial statement calculations |
| forecaster | Forecaster | Synthesizes the three analysis tracks; uses LLM reasoning + simplified valuation models to output 3-6 month target range, probability scorecard, bullish/base/bearish scenarios; **NOT responsible for** redoing the three specialists' analyses |
| report-synthesizer (me) | Report Synthesizer | Integrates all upstream deliverables, produces the *Investment Research Report* + *Teaching Handbook*; responsible for disclaimers and teaching explanation; **NOT responsible for** recomputing data / re-forecasting |
| qa-tester | Independent QA Tester | Independent quality gate: verifies each analysis deliverable against the source data (`.team/demo-data/`) and the task acceptance criteria — numbers match the source, disclaimer present, structure complete, no fabrication; outputs pass/fail with an evidence list; **NOT responsible for** writing analyses, generating data, or integrating reports |

**Why the QA role matters**: a tester who is **independent of the implementers** can catch fabrication, mismatched numbers, or missing disclaimers impartially. It is the **first independent gate** before the forecast; the Leader remains the **final arbiter** for overall delivery (see §7).

**Why boundaries matter**: with clear role boundaries, the task DAG is naturally conflict-free (§4). Writing "what I am NOT responsible for" in the desc prevents agents from grabbing each other's work or producing duplicate/contradictory outputs.

### 3.3 Role Design Checklist

- [ ] Does each role have a line "I am responsible for producing X"?
- [ ] Does each role have a line "I am explicitly NOT responsible for Y"?
- [ ] Do any roles have overlapping responsibility domains? (If so, trim by priority)
- [ ] Is there a "synthesizer/editor" role responsible for final consolidation? (to avoid everyone saying different things)
- [ ] Is there an **independent QA/tester role** (separate from the implementers) to verify deliverables against source data?

---

## 4. Step 3: Design the Task DAG and Dependencies

### 4.1 Expressing Dependencies with `create_task`

In JiuwenSwarm, tasks are automatically organized into a DAG (directed acyclic graph) via `blocked_by` (prerequisite dependencies).

**This demo's task DAG**:

```
task-data (1, first stage)
   ├── task-fundamental (2, parallel)
   ├── task-technical   (3, parallel)
   └── task-risk        (4, parallel)
            │  ← the three analysis tracks run in parallel after data is ready
            ▼
      task-qa (5, independent QA gate)
            │  ← pass → forecast unlocks; fail → back to the analysts
            ▼
      task-forecast (6, convergence point)
            ▼
      task-report (7, terminal delivery)
```

Dependency table (the `blocked_by` field when calling `create_task`):

| Task | Prerequisites | Note |
|---|---|---|
| task-data | — | Starting point, first stage |
| task-fundamental / technical / risk | task-data | **Three parallel tracks** (blocked until data is ready) |
| task-qa | three analyses | **Independent QA gate** (verifies the three analyses against source data before the forecast) |
| task-forecast | task-qa | **Convergence point** (unlocks only after the analyses pass QA) |
| task-report | task-forecast | **Terminal state** (unlocks only when the forecast is done) |

### 4.2 Three Insights for Dependency Design

1. **One-way flow**: data → analysis → synthesis → delivery; avoid cycles (A waits for B, B waits for A).
2. **Parallel decoupling**: don't serialize sub-tasks that can run in parallel (the three analyses); mark the same prerequisite and they run in parallel.
3. **Single convergence point**: all analyses first converge into one "synthesis" task (forecast), which then feeds the terminal state (report), avoiding many-to-many confusion.

> Platform mechanism: tasks with `blocked_by` cannot be claimed; they unlock automatically once prerequisites complete. The `[blocked by ...]` you see in `view_task` is the live rendering of the DAG.

---

## 5. Step 4: Design Data and File Handoffs

### 5.1 Handoff Convention (this project's agreement)

| Directory | What It Holds | Who Writes | Who Reads |
|---|---|---|---|
| `demo-data/` | financial CSV, price CSV | Data Researcher | three analysts |
| `analysis/` | three analysis md/scores | three analysts | QA Tester (verify) → Forecaster (synthesize) |
| `outputs/` | target price / scenarios / scorecard | Forecaster | Report Synthesizer |
| `deliverables/` | report + handbook | Report Synthesizer | user / whole team |

> Handoff contract rule: directory and file names are **hard-coded in the `create_task` task description**; downstream depends only on fixed paths; a missing file pinpoints a DAG break. All paths share the `.team/` prefix.

### 5.1b This Demo's Actual Deliverable List (reproduce against the real files)

After this project actually ran, the handoff files generated under `.team/` (learners can compare directly):

| Stage | Actual File | Producer | Consumer |
|---|---|---|---|
| Data | `demo-data/financials.csv` (FY2022-FY2025 four fiscal years, 14 fields) | data-researcher | three analysts |
| Data | `demo-data/stock_history.csv` (53-week weekly OHLCV) | data-researcher | three analysts |
| Analysis | `analysis/fundamental.md` (fundamental 72/100) | fundamental-analyst | forecaster |
| Analysis | `analysis/technical.md` (trend bullish, key price levels) | technical-analyst | forecaster |
| Analysis | `analysis/risk.md` (risk medium-high, sentiment neutral-to-bullish) | risk-sentinel | forecaster |
| Forecast | `outputs/forecast.md` (target 215-310, mid-point 262, three scenarios 300/270/205) | forecaster | report-synthesizer |
| Delivery | `deliverables/investment-research-report.md` | report-synthesizer | user / whole team |
| Delivery | `deliverables/jiuwen-multiagent-dev-manual.md` | report-synthesizer | user / whole team |

### 5.2 How to Design Handoff Files (Key!)

File handoff is the "contract" of multi-agent collaboration. This demo's conventions:

- **Semantic file names**: this demo's actual file names are `financials.csv` (financials), `stock_history.csv` (weekly prices), `fundamental.md` (fundamental analysis)...
- **Definitions in the file header**: `fundamental.md` states the data source, as-of date, and indicators used — downstream doesn't need to guess.
- **One task, one deliverable**: downstream depends only on fixed paths; a missing file means upstream didn't do its job (this pinpoints DAG breaks).

> Tip: the most common failure point in multi-agent projects is "implicitly agreed handoff formats". **Whether file or message, put the format into the task description or the file header**.

---

## 6. Step 5: Design the Member Collaboration Mechanism

### 6.1 Three Collaboration Channels (`send_message`)

| Scenario | Usage | Example |
|---|---|---|
| Task instructions / kickoff notice | Leader broadcast | `to="*"` → "Data task starts first; other tasks wait for data to be ready" |
| Member alignment | point-to-point unicast | Analyst → Data Researcher "confirm whether the financial definition is quarterly or annual" |
| Completion report | point-to-point | Member → Leader: `to="team-leader"` |

### 6.2 Collaboration Protocol (this project's agreement)

- **Kickoff signal**: Leader broadcasts the task list and assigns tasks ⇒ members check `view_task` → claim via `claim_task(status=claimed)`.
- **Completion signal**: member writes the deliverable to the corresponding `.team/` directory → `claim_task(status=completed)` → report to Leader (with deliverable path).
- **Question channel**: data-definition questions go directly via `send_message` to the relevant member; if unresolvable → escalate to Leader.
- **No polling**: dependencies unlock and notify automatically; members don't need to repeatedly refresh `view_task`.

### 6.3 Key Behaviors for Successful Collaboration

- [ ] Dependent parties proactively sync "I'm done, here's where the deliverable is"
- [ ] Dependent-on parties respond to questions promptly
- [ ] Deliverable path + summary go through the message channel; full text goes to `.team/` files (messages carry paths, not content)

---

## 7. Step 6: Design the Acceptance Process (QA Gate + Leader Arbitration)

### 7.0 Two-Layer Acceptance: Independent QA Tester + Leader

This demo uses a **two-layer quality model**:

| Layer | Who | Role | Independence |
|---|---|---|---|
| **First gate** | qa-tester (Independent QA Tester) | Verifies each analysis deliverable against the **source data** (`.team/demo-data/`) and the **task acceptance criteria**: numbers match the source, disclaimer present, structure complete, no fabrication. Outputs pass/fail + evidence list. | **Independent of the implementers** — catches errors impartially |
| **Final arbiter** | team-leader | Reviews the QA verdict plus the overall pipeline, resolves disputes, and makes the **final accept/reject decision** for delivery | Owns the overall project |

> **Why two layers?** The QA tester is independent of the three analysts, so it can objectively check whether a number in `fundamental.md` really comes from `financials.csv` (no fabrication, no mismatch). The Leader is the final authority who decides whether the whole pipeline is ready to deliver to the user. One layer without the other is weaker: implementer self-checks are biased, and a Leader without an independent check may accept errors too easily.

### 7.1 The Acceptance Tools (Tester + Leader perspective)

| Action | Tool | Who | When |
|---|---|---|---|
| View the full task board | `view_task(action=list)` | Tester / Leader | anytime, to identify bottlenecks/broken links |
| View a single task | `view_task(action=get, task_id=...)` | Tester / Leader | before claiming / before acceptance |
| Read deliverable files | read files under `.team/` | Tester / Leader | when verifying quality |
| Rule pass/fail (gate) | `verify_task(decision=pass/fail)` | **qa-tester** | after a task enters in_review |
| Final arbitration | `verify_task(decision=pass/fail)` | **Leader** | final review of the whole pipeline |

### 7.2 This Demo's Acceptance Examples

- Data task: `view_task(get)` to check task-data → read the CSV → verify field definitions → `pass`.
- Analysis tasks (QA gate): the **qa-tester** reads the three analyses under `analysis/` and **cross-checks every cited number against `demo-data/financials.csv` / `stock_history.csv`** → numbers match, disclaimer present, structure complete → `pass`. Any mismatch, missing disclaimer, or fabricated figure → `fail` with an evidence list.
- Forecast and report: read the two final deliverables under `deliverables/` → "disclaimer present" and "structure complete" → Leader rules `pass` → deliver.

> Acceptance red line: **missing deliverable, wrong definitions, no disclaimer, or fabricated/mismatched numbers = reject**.

---

## 8. Platform Capability & Demo Stage Mapping Table

The table below is for **you who want to learn the platform**: where each JiuwenSwarm capability is used in this demo.

| Platform Capability | Corresponding Stage in This Demo | How You Can Use It in Your Own Project |
|---|---|---|
| `build_team` | Creates the "US Equity Research Multi-Agent Teaching Demo" team | Use the team display_name to set the project theme; enable worktree / shared workspace |
| `spawn_teammate` | Creates the 7 role agents in sequence (each with a desc = "who + expertise + boundaries") | Create roles one by one against the goal tree; each role faces one sub-goal |
| `create_task` | Builds task-data → 3 analyses → QA gate → forecast → report, weaving the DAG with `blocked_by` | Turn "sub-goals" into tasks; use dependencies to express sequencing and parallelism |
| `claim_task` | Members claim autonomously (`status=claimed`), mark `completed` when done | Let members claim their own work — collaboration rather than assignment |
| `view_task` | Everyone's anytime board: `[pending/blocked/in_progress/...]` | Use task states to schedule the DAG and identify bottlenecks |
| `send_message` | Kickoff broadcast, member alignment, completion reports | Broadcast (for direction) / unicast (point-to-point); messages carry paths, not content |
| `.team/` file sharing | Handoff of CSV/analysis/forecast/report; writes to deliverables | Standardize directories and file names for data handoff |
| `workspace_meta` lock/unlock | Lock before multiple members edit the same file (used when writing final deliverables in this demo) | Prevent overwrites, keep shared files consistent |
| `verify_task` / reviewer | qa-tester rules pass/fail on analyses (independent first gate); Leader makes final arbitration | Assign a reviewer (e.g. the QA tester) to tasks via the reviewer field; first verdict wins — pass completes, fail sends back for rework |

> This mapping is also key for the deliverables: learners who want to verify platform capabilities can find ready-made usage in the demo by following the table item by item.

---

## 9. 5-Minute Quick Start: Reproduce Your First Multi-Agent Project

> Goal: build a minimal closed loop of "input company → data → three analyses → combined report" within 5 minutes.

**Step 1 (~30 seconds): clarify what you want**
- Write your raw requirement in one line → decompose it into 3-5 sub-goals using the method in 2.1.

**Step 2 (~1 minute): build the team + roles**
```text
build_team(display_name="My Multi-Agent Project")
spawn_teammate(name="data-1", desc="Data engineer: responsible for sample data; NOT responsible for analysis")
spawn_teammate(name="analyst-1", desc="Analyst: responsible for analysis; NOT responsible for data")
spawn_teammate(name="synth-1", desc="Synthesizer: responsible for aggregating into a report")
```
> desc template: **who + expertise + output responsibility + what you are NOT responsible for**.

**Step 3 (~1 minute): build the DAG**
```text
create_task(task-data,    blocked_by=none)
create_task(task-analyst, blocked_by=task-data)
create_task(task-report,   blocked_by=task-analyst)
```
> Three lines express "data first → then analysis → then report".

**Step 4 (~1 minute): define the handoff directories**
```text
.team/input/     ← upstream writes
.team/output/    ← downstream reads
```
> In each task description, state "which directory the output goes to and what the file name is".

**Step 5 (~1.5 minutes): kick off + final acceptance**
```text
send_message(to="*", content="Data task starts first; others wait for unlock")
# after members finish:
view_task() → check blocks status → verify_task(pass)
```

**Done!** You now have a minimal runnable, reproducible multi-agent project. Afterwards, enrich the roles and DAG step by step following §3-§7 of this handbook.

---

## 10. Appendix: Full Workflow Diagram of This Demo

```text
 User submits requirement (single company)
        │
        ▼
 ┌─ build_team: US Equity Research Multi-Agent Teaching Demo ─┐
 │ spawn_teammate ×7 (data / three analysts / QA tester / forecaster / synthesizer) │
 │ create_task ×7 (data→three analyses→QA gate→forecast→report)      │
 └──────────────────────────────────────────────────────────────┘
        │ kickoff broadcast send_message(to="*")
        ▼
 data-researcher claims task-data → writes demo-data/*.csv → completed
        │ (DAG: downstream unlocks)
        ▼
 ┌────────────────────────────────────────────────────────────┐
 │ fundamental-analyst  → fundamental analysis               │
 │ technical-analyst    → technical analysis                 │  ← three parallel tracks
 │ risk-sentinel        → risk & sentiment analysis          │
 └────────────────────────────────────────────────────────────┘
        │
        ▼
 qa-tester → independent QA gate (numbers match source data? disclaimer? structure? no fabrication?)
        │ pass → forecast unlocks; fail → back to analysts for rework
        ▼
 forecaster → target price range / three scenarios / scorecard → outputs/
        │
        ▼
 report-synthesizer (me) → deliverables/ investment report + teaching handbook
        │
        ▼
 Leader acceptance (verify_task, final arbitration) → deliver to user (with disclaimer)
```

---

*This handbook is a teaching demo deliverable; all case data and conclusions are teaching samples and do not constitute investment advice.*