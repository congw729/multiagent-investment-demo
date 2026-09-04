# Student Lab Worksheet — Reproducing the 7-Agent US Equity Research Pipeline

> Companion to the repository: **US Equity Research Multi-Agent Teaching Demo** (`repo/`)
> Time needed: **45 minutes** | Level: Beginner-friendly | Mode: Individual or pair work
>
> ⚠️ **Disclaimer**: This worksheet is part of a teaching demo built on the JiuwenSwarm platform. All data, analyses, and forecasts used in this lab are **locally generated teaching samples** — **for teaching demonstration only, NOT investment advice**.

---

## 1. Lab Overview

### 1.1 Goal

By the end of this lab, you will have **reproduced the complete 7-agent investment research pipeline** (6 worker agents + 1 independent QA tester) on the JiuwenSwarm platform, exactly like the demo in this repository:

```
data → three parallel analyses (fundamental / technical / risk) → combined forecast → final report + handbook
```

You will learn, hands-on:

| # | Skill | Where |
|---|---|---|
| 1 | Build a team and write agent role descriptions (desc) | Step 1 |
| 2 | Design a task DAG with dependencies | Step 2 |
| 3 | Prepare sample data | Step 3 |
| 4 | Run three parallel analyses | Step 4 |
| 5 | Synthesize a forecast and integrate a report | Step 5 |
| 6 | Accept deliverables as Leader | Step 6 |

### 1.2 Prerequisites

- [ ] A **JiuwenSwarm account** with permission to create teams (`build_team`) and spawn members (`spawn_teammate`)
- [ ] **Python 3.8+** installed locally (to run the sample-data generation script, or skip if your data agent generates the files)
- [ ] **Git** installed (optional, only if you clone the repository)
- [ ] This repository cloned locally (recommended) or open in your editor: `repo/`
- [ ] 45 minutes of uninterrupted time (approx. 5-10 min per step)

> **Tip**: Before you start, skim `deliverables/jiuwen-multiagent-dev-manual.md` §3 (roles) and §4 (DAG) — you will copy from them in Steps 1-2.

---

## 2. Step-by-Step Instructions

### Step 1 — Build the Team: `build_team` + 7 Agents (≈ 5 min)

**What to do**

1. Call `build_team` to create your own team. Give it a clear display name, e.g. `My US Equity Research Lab`.
2. Spawn **7 agents** (6 workers + 1 independent QA tester, plus yourself as Leader) using `spawn_teammate`. Copy the role descriptions (`desc`) from handbook §3.2 — the golden formula is:

```
[Who you are] + [your domain of expertise] + [what output you are responsible for] + [what you are explicitly NOT responsible for]
```

| Agent name (member_name) | Role (display_name) | desc must include… (copy from handbook §3.2) |
|---|---|---|
| data-researcher | Data Researcher | structured data design; produce CSV sample data to `.team/demo-data/`; NOT responsible for analysis |
| fundamental-analyst | Fundamental Analyst | financial statements: revenue, margins, ROE, debt, cash flow, valuation; output score + valuation judgment; NOT responsible for candlesticks/sentiment |
| technical-analyst | Technical Analyst | candlestick patterns, MAs, RSI/MACD, volume, support/resistance; output trend rating + key levels; NOT responsible for fundamentals |
| risk-sentinel | Risk & Sentiment Analyst | news, policy, regulation, competition, macro; output risk rating + sentiment; NOT responsible for financial calculations |
| forecaster | Forecaster | synthesize three tracks; output target range + probability scorecard + bullish/base/bearish scenarios; NOT responsible for redoing the analyses |
| report-synthesizer | Report Synthesizer | integrate all deliverables into report + handbook; responsible for disclaimer; NOT responsible for recomputing data |
| qa-tester | Independent QA Tester | independent quality gate: verify each analysis against source data & acceptance criteria (numbers match, disclaimer present, structure complete, no fabrication); output pass/fail + evidence list; NOT responsible for writing analyses or generating data |

**Expected result**

- You can see 8 members in your team (Leader + 7 agents), each with a distinct desc stating both responsibility and non-responsibility.

**Common issues**

| Issue | Fix |
|---|---|
| I can't call `build_team` / `spawn_teammate` | Check your account permissions; you need team-creation rights |
| Two agents seem to do the same thing | Review their descs — the "NOT responsible for" part is missing; add clear boundaries |
| Member name already taken | Use a unique `member_name` (e.g. add your initials) |

---

### Step 2 — Create the Task DAG: 7 Tasks + Dependencies (≈ 5 min)

**What to do**

Using `create_task`, create the following 7 tasks. Set the `blocked_by` field exactly as in handbook §4.1:

| Task ID | Description | `blocked_by` |
|---|---|---|
| task-data | Prepare local sample datasets (financial + price CSV) | — (none, first) |
| task-fundamental | Fundamental analysis: financial report & quality score | task-data |
| task-technical | Technical analysis: trend / momentum / key levels | task-data |
| task-risk | Risk & sentiment analysis: non-financial dimensions | task-data |
| task-qa | Independent QA gate: verify the three analyses against source data | task-fundamental, task-technical, task-risk |
| task-forecast | Combined forecast: target range + scenarios + scorecard | task-qa |
| task-report | Final delivery: report + handbook | task-forecast |

**Expected result**

- The task board (`view_task`) shows `task-data` as the only `pending` task; the other six show `blocked by ...`, forming a one-way DAG: data → three parallel analyses → QA gate → forecast → report.

**Common issues**

| Issue | Fix |
|---|---|
| `task-forecast` won't unlock | Check that ALL three analyses AND `task-qa` are `completed`; a single missing one keeps it blocked |
| Tasks claimable too early | You forgot `blocked_by` on the downstream tasks — add the prerequisite |
| I see a loop (A waits B, B waits A) | DAG must be acyclic: data → analysis → QA → synthesis → delivery; never point upstream back |

---

### Step 3 — Prepare the Sample Data (≈ 5 min)

**What to do — Option A (recommended, data agent)**

1. Ask your `data-researcher` agent to claim `task-data`.
2. Have it generate the two CSVs into `.team/demo-data/` (it can reuse `scripts/generate_sample_data.py` or write equivalent logic).
3. Verify the files exist before moving on.

**Option B (manual, local)**

```bash
cd repo
python3 scripts/generate_sample_data.py
# output:
#   data/financials.csv      (FY2022-FY2025, 14 fields)
#   data/stock_history.csv   (53 weeks weekly OHLCV)
```

**Expected result**

- `.team/demo-data/financials.csv` — 4 rows (FY2022-FY2025), 14 columns, with English comment header
- `.team/demo-data/stock_history.csv` — 53 rows of weekly OHLCV from 2025-09-15
- (Optional, real-data edition) `.team/demo-data/quarterly_real.csv` — FY2025 Q1-Q3 + FY2026 Q1-Q3 quarterly results (10-Q), used for the FY2026 quarterly trend section
- `task-data` marked `completed`

**Common issues**

| Issue | Fix |
|---|---|
| CSV is empty or missing columns | Re-run the script; check the script prints "financials.csv written:" and "stock_history.csv written:" |
| Column values look wrong (e.g. ratios) | Definition header: amounts in USD millions, EPS USD/share, ratios as percentages (43.31 = 43.31%) |
| Downstream analysts say files not found | Files must be in the **shared workspace** `.team/demo-data/`, not your private directory |

---

### Step 4 — Run the Three Parallel Analyses (≈ 10 min)

**What to do**

1. Ask each analyst to claim its own task: `fundamental-analyst` → `task-fundamental`, `technical-analyst` → `task-technical`, `risk-sentinel` → `task-risk`. (They can run in parallel once `task-data` is done.)
2. Each analyst reads the CSVs from `.team/demo-data/` and writes one markdown report to `.team/analysis/`:
   - `analysis/fundamental.md` — revenue, profitability, financial health, cash flow, valuation + a 0-100 quality score
   - `analysis/technical.md` — trend rating, MA system, RSI/MACD, support/resistance, volume
   - `analysis/risk.md` — non-financial risk list, market sentiment, overall risk rating
3. Each analyst reports completion (file path + one-line summary) via `send_message` to the Leader.

**Expected result**

- Three files exist: `analysis/fundamental.md`, `analysis/technical.md`, `analysis/risk.md`
- Each file header states its data source, as-of date, and indicator definitions
- All three tasks marked `completed`; `task-forecast` unlocks automatically

**Common issues**

| Issue | Fix |
|---|---|
| Analyst says "data not found" | Data must be in `.team/demo-data/` (shared workspace), not a private folder; re-check Step 3 |
| Two analysts write to the same file | Each task must write its own file name; enforce "one task, one deliverable" |
| Analysis conclusions look inconsistent | That's normal and useful — the QA step and the forecast step will cross-validate them (see handbook §8) |

---

### Step 4.5 — Independent QA Verification: the Quality Gate (≈ 5 min)

**What to do**

Before letting the forecast start, add an **independent QA gate** — this is a core teaching point ("independent Tester quality gate"):

1. Ask the `qa-tester` agent to claim `task-qa`. Its prerequisites are the three analyses.
2. The QA tester **independently verifies** each analysis deliverable against the source data and the task acceptance criteria:
   - Numbers match the source files (`demo-data/financials.csv`, `demo-data/stock_history.csv`) — no fabrication, no mismatch
   - Disclaimer present in each analysis
   - Structure complete (data source, as-of date, indicator definitions in the header)
3. It rules `verify_task(decision=pass/fail)` with an evidence list:
   - `pass` → the forecast task unlocks
   - `fail` → the analyses go back to the analysts for rework, then QA re-checks

**Why this matters**

The QA tester is **independent of the three analysts** — it cannot "agree with itself" the way an implementer can. This is the **first independent gate**; the Leader remains the **final arbiter** (Step 6). One layer without the other is weaker: analyst self-checks are biased, and a Leader without an independent check may accept errors too easily.

**Expected result**

- `task-qa` marked `completed` with a pass verdict + evidence list
- `task-forecast` unlocked **only after** the QA pass

**Common issues**

| Issue | Fix |
|---|---|
| QA and the analysts are the same person/agent | The QA role must be a **separate, independent** agent — see Step 1 |
| QA passes without reading the files | Pass/fail must be based on **reading the files and comparing numbers**, not on trust |
| Forecast starts before QA | Check the DAG: `task-forecast` must have `blocked_by = task-qa` |

---

### Step 5 — Combined Forecast + Report Integration (≈ 10 min)

**What to do**

1. Ask `forecaster` to claim `task-forecast`. It reads the three analyses and produces `.team/outputs/forecast.md`:
   - a transparent method (e.g. PEG valuation test + PE×EPS three-scenario weighting)
   - a target price range with probability scorecard (bullish / base / bearish)
2. Ask `report-synthesizer` to claim `task-report`. It reads all upstream outputs and produces, under `.team/deliverables/`:
   - `investment-research-report.md` — executive summary, scorecard, target range & three scenarios, risk warnings, disclaimer
   - `jiuwen-multiagent-dev-manual.md` — teaching handbook (already present in this repo; you may regenerate or reuse)

**Expected result**

- `outputs/forecast.md` exists with: target range (wide + core), weighted mid-point, three scenarios with probabilities, confidence level
- `deliverables/investment-research-report.md` exists with a **disclaimer** (teaching demo only, not investment advice)
- `task-forecast` and `task-report` marked `completed`

**Common issues**

| Issue | Fix |
|---|---|
| Forecast numbers don't match the analyses | Forecast must derive from upstream inputs, not new assumptions; cite which number came from which analysis |
| Report has no disclaimer | The report MUST contain the disclaimer — acceptance will reject it otherwise (see Step 6) |
| `task-report` won't unlock | `task-forecast` must be `completed` first; check the DAG in Step 2 |

---

### Step 6 — Leader Acceptance: Final Arbitration (≈ 5 min)

**What to do**

The QA tester ran the first gate on the analyses (Step 4.5). Now the **Leader acts as the final arbiter** for the whole pipeline:

1. `view_task(action=list)` — confirm all 7 tasks are `completed`
2. Read each deliverable under `.team/` and check quality:
   - CSV files exist and parse correctly
   - Three analyses are present with definitions in the header, and the **QA evidence list** confirms numbers match the source
   - Forecast contains target range + scenarios + probabilities
   - Report contains executive summary, scorecard, target range, risk warnings, **disclaimer**
3. For each task, rule `verify_task(decision=pass/fail)`. If any deliverable is missing, has wrong definitions, lacks a disclaimer, or failed QA → `fail` and send feedback for rework.

> **QA Tester vs. Leader**: the QA tester is the **independent first gate** (checks analyses against source data); the Leader is the **final arbiter** (reviews the QA verdict plus the whole pipeline and makes the final accept/reject decision for delivery). Both use `verify_task` — the QA tester on the analysis tasks, the Leader on the final acceptance.

**Expected result**

- All tasks `completed` after passing both gates (QA + Leader)
- A complete, reproducible pipeline record: data → analyses → QA gate → forecast → report → Leader-accepted

**Common issues**

| Issue | Fix |
|---|---|
| I'm the Leader but can't `verify_task` | Only the task's assigned reviewer can rule; check the reviewer field on the task |
| A task is stuck `in_review` | If it has a reviewer, wait for their verdict; if you're the reviewer, read the output and rule pass/fail |
| Rework loop | Give specific feedback (which file, what's wrong) so the member can fix it in one pass |

---

## 3. Lab Record Table (fill in during the lab)

Record each stage as you complete it. Leave "Time used" for the end of each step.

| Step | Task ID | Output file path (`.team/...`) | Key conclusion (score / range / rating) | Time used (min) |
|---|---|---|---|---|
| 1 | team build | — | members created: ______ | ______ |
| 2 | DAG | — | tasks created: ______ (blocked_by correct? ☐ yes ☐ no) | ______ |
| 3 | task-data | demo-data/__________________ | rows / fields: ______ | ______ |
| 4 | task-fundamental | analysis/fundamental.md | quality score: ______/100 | ______ |
| 4 | task-technical | analysis/technical.md | trend rating: ______ | ______ |
| 4 | task-risk | analysis/risk.md | risk rating: ______ | ______ |
| 4.5 | task-qa | — (QA evidence list) | verdict: pass ☐ / fail ☐ | ______ |
| 5 | task-forecast | outputs/forecast.md | target range: ______ / mid-point: ______ | ______ |
| 5 | task-report | deliverables/investment-research-report.md | report complete? ☐ yes ☐ no | ______ |
| 6 | acceptance | — | verdicts: pass ______ / fail ______ | ______ |

**Total time used: ______ minutes** (target: ≤ 45)

---

## 4. Advanced Challenges (bonus, optional)

Pick one or more if you finish early.

### Challenge A — Switch the target company (MSFT / TSLA / any ticker)

Replace the AAPL sample with another company. You must (1) regenerate or edit the sample CSVs so the values roughly match the new company's public profile (magnitude only, still sample data), (2) have the analysts re-run all three analyses against the new data, and (3) produce a new forecast and report. Compare: how do the quality score, target range, and risk rating change vs. AAPL, and why? *Remember to keep the disclaimer — sample data only.*

### Challenge B — Add a new agent

Add an 8th agent with a distinct domain, e.g. a **macro-economist** (rates/inflation/currency) or a **compliance auditor** (policy checks). Write its desc with the golden formula, insert a matching task into the DAG (decide: does it run in parallel with the three analyses, or feed the forecast?), and describe how its output flows through `.team/`.

### Challenge C — Improve a desc

Take one existing agent (e.g. `technical-analyst`) and rewrite its desc to be more precise: add 2-3 concrete indicators it is responsible for, and 2 things it explicitly does NOT do. Explain in 2-3 sentences how your change would reduce conflicts or improve quality in a real run.

### Challenge D — Sensitivity Analysis: What If One Assumption Changes?

Forecasts are only as good as their assumptions. This challenge makes the "risk output must include indicators, assumptions, limitations, and evidence" teaching point tangible: change **one** input of the forecast's PE×EPS model and observe how the conclusion moves.

**What to do**

1. Open `outputs/forecast.md` (real-data edition) and go to **§3 "Model 2: PE × EPS Scenario Weighting"** — the *Scenario Design* table (bullish / base / bearish rows with EPS, PE, and target levels) and the *Probability Weighting* formula (weighted mid-point = 350×0.25 + 318×0.50 + 240×0.25 ≈ **310 USD**). *Optional (real-data edition): cross-check the FY2026E EPS assumptions against the quarterly run-rate in `demo-data/quarterly_real.csv` (FY2026 Q1-Q3 diluted EPS sum = 6.87).*
2. Pick **one** assumption to change, and change nothing else:
   - **Option A — raise Base-scenario EPS growth**: FY2026E EPS from **7.91 (+6%)** to **≈8.21 (+10%)**; keep the Base PE band (36-40x, ~40x mid was used to get 318). Recompute the Base target = EPS × PE, then the new weighted mid-point.
   - **Option B — lower Bearish-scenario EPS**: EPS from **7.68** to **7.50** (keep the ~31x PE used to get 240). The Bearish target falls from 240 to ≈233 (7.50 × 31). Recompute the weighted mid-point.
   - **Option C — raise Bearish-scenario probability**: probabilities from **25/50/25** to **25/40/35** (base 50% → 40%, bearish 25% → 35%). Recompute the weighted mid-point — no formula change, only weights.
3. Compare with the original **310** and quantify the change (in USD and in %).

**Expected result hints**

- **Option A**: Base target ≈ 328 (8.21 × 40), mid-point ≈ **312** (350×0.25 + 328×0.50 + 240×0.25) — **+2 USD (+0.6%)**, mild upward drift.
- **Option B**: Bearish target ≈ 233 (7.50 × 31), mid-point ≈ **304** (350×0.25 + 318×0.50 + 233×0.25) — **−6 USD (−1.9%)**, mild downward drift.
- **Option C**: mid-point ≈ **299** (350×0.25 + 318×0.40 + 240×0.35) — **−11 USD (−3.5%)**, the largest move: re-weighting tail risk beats a modest EPS change, because the bearish scenario is the lowest target and its weight doubled its tail influence.
- Sanity check: probabilities must still sum to 100%; only **one** input changes per run. The spread of outcomes (312 / 304 / 299) is the sensitivity surface of the mid-point.
- If you push any assumption far enough (e.g., EPS +20%), the conclusion can flip sign — that sensitivity itself is the finding.

**Why this matters**

Sensitivity is a core risk-management discipline: a single forecast number without its sensitivity surface hides the risk. Showing **which assumption moves the mid-point the most** (here: probability re-weighting of the tail > a ±3% EPS tweak) is exactly the "indicators + assumptions + limitations + evidence" evidence chain the course asks for.

**Observation template (write 3-5 lines)**

```text
- Assumption changed: ___ (e.g., Option C: bearish probability 25% → 35%) in the §3 Scenario Design table.
- New weighted mid-point ≈ ___ USD vs. original 310 → change ≈ ___% (direction: up/down).
- Why: the ___ scenario carries ___% weight (or its target moved from ___ to ___), contributing Δ ≈ (new − old) × weight ≈ ___ USD.
- Insight: the mid-point is most sensitive to ___ (e.g., tail-probability re-weighting), because ___.
- Takeaway: a defensible forecast states its assumptions and shows how the conclusion changes under stress — indicators + assumptions + limitations + evidence.
```

---

## 5. Scoring Rubric (100 pts + 10 bonus)

| Criterion | Weight | Meets expectation (full marks) |
|---|---|---|
| DAG correctness | 20% | 7 tasks created (data → 3 analyses → QA gate → forecast → report); `blocked_by` matches handbook §4.1; downstream blocked until prerequisites done |
| Role description quality | 20% | Each of 7 agents has a desc with: who + expertise + responsible output + explicit non-responsibility |
| Deliverable completeness | 30% | demo-data CSVs (2), analyses (3), forecast (1), report (1) all exist, named correctly, with definitions in headers |
| QA gate & lab record | 20% | QA pass/fail with evidence recorded; record table filled for all steps; output paths and key conclusions match the actual files |
| Disclaimer & structure | 10% | Report/handbook contain the teaching disclaimer; markdown tables render correctly |
| Advanced challenge (bonus) | +10% | At least one challenge completed with correct reasoning |

**Passing threshold: 60/100.** Below that, review the failing rows in the rubric, fix, and re-submit.

---

## 6. Reference File Map (where to find the answers in this repo)

| What you need | Reference file (in this repo) | What it gives you |
|---|---|---|
| Role desc templates (Step 1) | `deliverables/jiuwen-multiagent-dev-manual.md` §3.2 | Golden formula + all 7 role descs |
| DAG design (Step 2) | `deliverables/jiuwen-multiagent-dev-manual.md` §4 | Dependency table + design insights |
| Sample data generator (Step 3) | `scripts/generate_sample_data.py` | Run it to produce both CSVs |
| Sample data (Step 3) | `data/financials.csv`, `data/stock_history.csv` | Expected structure & values (AAPL) |
| Three analyses (Step 4) | `analysis/fundamental.md`, `analysis/technical.md`, `analysis/risk.md` | Expected conclusions & formats |
| Combined forecast (Step 5) | `outputs/forecast.md` | Expected target range & scenario format |
| Final report (Step 5) | `deliverables/investment-research-report.md` | Expected report structure & disclaimer |
| Platform capabilities | `README.md` §2.3 | Capability → demo-stage mapping |
| Full pipeline flow | `deliverables/jiuwen-multiagent-dev-manual.md` §10 | End-to-end workflow diagram |

---

*This worksheet is part of a teaching demo. All referenced data, analyses, and forecasts are locally generated sample data — **teaching demonstration only, NOT investment advice.***
