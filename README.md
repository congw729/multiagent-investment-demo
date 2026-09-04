# US Equity Research Multi-Agent Teaching Demo

> A complete teaching project built on the **JiuwenSwarm Multi-Agent Platform**: seven agents collaborate — six workers perform fundamental analysis, technical analysis, and risk/sentiment analysis for a listed company, an independent QA tester verifies the analyses against source data, then the team synthesizes a future price forecast range, producing the *Investment Research Report* and the *JiuWen Multi-Agent Development Handbook*.

> ⚠️ **Disclaimer**: This project is a teaching demonstration built on the JiuwenSwarm platform. It uses **real market data** (SEC EDGAR 10-K filings + Yahoo Finance weekly prices) strictly for teaching; all analysis conclusions and forecast ranges are algorithmic outputs of the multi-agent teaching workflow, **for teaching demonstration only and NOT investment advice**. Any trading based on this project is at your own risk.

---

## 1. Project Overview

This project demonstrates how to design and run a multi-agent collaboration project on the JiuwenSwarm platform. Using "US equity research" as the business scenario, the user inputs a target listed company (this demo uses **AAPL (Apple)** as the teaching sample), and seven agents collaborate according to the task DAG:

> **Course positioning**: this demo maps to the **Risk Management** theme of the *IEDA4000H (Optimization in Financial Engineering)* course — the Risk & Sentiment Analyst (risk-sentinel) outputs a risk checklist with impact ratings and position-sizing suggestions, and the forecast explicitly gives up/down probabilities and a confidence level, demonstrating the teaching point that **risk outputs must include indicators, assumptions, limitations, and evidence**.

1. **Data Researcher** (data-researcher): Generates and validates market datasets (SEC EDGAR 10-K financial CSV + Yahoo Finance historical price CSV)
2. **Fundamental Analyst** (fundamental-analyst): Interprets financial reports, outputs a fundamental score and valuation judgment
3. **Technical Analyst** (technical-analyst): Performs trend and momentum analysis on historical prices, outputs a trend rating and key price levels
4. **Risk & Sentiment Analyst** (risk-sentinel): Assesses risk from non-financial dimensions such as news sentiment, policy, and industry competition
5. **Forecaster** (forecaster): Synthesizes the three analysis tracks, outputs the target price range, probability scorecard, and multi-scenario projection
6. **Report Synthesizer** (report-synthesizer): Integrates all deliverables and produces the *Investment Research Report* and the *Teaching Handbook*
7. **Independent QA Tester** (qa-tester): Independently verifies each analysis against the source data and the task acceptance criteria — a first quality gate before the forecast; the Leader remains the final arbiter

> The project goal is not real investment advice, but to **demonstrate platform capabilities**: `build_team`, `spawn_teammate`, task DAG, autonomous task claiming, `send_message` collaboration, `.team/` file handoffs, and Leader acceptance/delivery. The entire workflow is offline-reproducible with sample data.

### Core Conclusion of This Demo (Real-Data Edition)

| Dimension | Conclusion |
|---|---|
| Fundamental | 66/100 good (solid quality, expensive valuation) |
| Technical | Bullish (mid-term uptrend channel, short-term neutral-to-bullish) |
| Risk & Sentiment | Medium-to-high (regulation + supply chain + high valuation) |
| Combined Forecast | Target range **USD 215-365**, core range 275-345, weighted mid-point approx. **USD 310** (approx. -5.5% vs. latest close 328.21) |
| Three Scenarios | Bullish ~350 / Base ~318 / Bearish ~240 |

---

## 2. Multi-Agent Architecture

### 2.1 Team Members and Responsibilities

| Member | Role | Core Responsibility |
|---|---|---|
| team-leader | Project Lead (Teaching Controller) | Builds the team, decomposes the task DAG, coordinates collaboration, accepts deliverables, delivers teaching |
| data-researcher | Data Researcher | Prepares and cleans local sample datasets (financial/price CSV) |
| fundamental-analyst | Fundamental Analyst | Interprets financial reports, fundamental scoring, valuation judgment |
| technical-analyst | Technical Analyst | Candlestick patterns, trend, momentum indicators, support/resistance levels |
| risk-sentinel | Risk & Sentiment Analyst | Non-financial risk and sentiment assessment: news, policy, industry competition |
| forecaster | Forecaster | Synthesizes three tracks, outputs target price range, scorecard, scenario projection |
| report-synthesizer | Report Synthesizer | Integrates the *Investment Research Report* and the *Teaching Handbook* |
| qa-tester | Independent QA Tester | Verifies analyses against source data and acceptance criteria (first gate); rules pass/fail on analysis tasks |

### 2.2 Task DAG and Dependencies

```
task-data (data ready, first stage)
   ├── task-fundamental (fundamental analysis, depends on data)
   ├── task-technical (technical analysis, depends on data)
   └── task-risk (risk & sentiment analysis, depends on data)
            │  (the three analysis tracks run in parallel)
            ▼
      task-qa (independent QA gate: verify analyses against source data)
            │  (pass → forecast unlocks; fail → back to analysts)
            ▼
      task-forecast (combined forecast, depends on analyses passing QA)
            ▼
      task-report (integrated report + handbook, final delivery)
```

### 2.3 Platform Capability Mapping

| Platform Capability | Where It Is Used in This Demo |
|---|---|
| `build_team` / `spawn_teammate` | Forms the seven-agent team (6 workers + 1 independent QA tester) |
| `create_task` task DAG | Data → three parallel analyses → QA gate → synthesis → report |
| Autonomous task claiming | Each analyst claims their own analysis task; qa-tester claims task-qa |
| `send_message` collaboration | Data-ready broadcast, conclusion aggregation, QA feedback, blocker escalation |
| `.team/` file handoff | CSV data, analysis markdown, forecast markdown, reports flow between members |
| `verify_task` / reviewer | qa-tester rules pass/fail on analyses (independent first gate); Leader makes final acceptance |
| Leader acceptance/delivery | Data unlock confirmation, final deliverable acceptance |

---

## 3. Quick Start

### 3.1 Environment Requirements

- Python 3.8+ (to run the sample data generation script)
- Git (for version management)
- JiuwenSwarm platform (to reproduce the multi-agent collaboration workflow)

### 3.2 Data Sources and Generation

The full pipeline runs on **real market data**:

- **Financials (annual)**: SEC EDGAR (XBRL companyfacts) — Apple Inc. Form 10-K FY2022-FY2025 (filing dates 2022-10-28 / 2023-11-03 / 2024-11-01 / 2025-10-31), retrieved 2026-09-04
- **Financials (quarterly)**: SEC EDGAR (XBRL companyfacts) — Apple Inc. Form 10-Q FY2025 Q1-Q3 + FY2026 Q1-Q3 (filing dates 2026-01-30 / 2026-05-01 / 2026-07-31), retrieved 2026-09-04
- **Prices**: Yahoo Finance chart API — weekly OHLCV, 1y range (54 weekly bars, 2025-09-01 ~ 2026-09-03), latest close **328.21 USD**

The repository also ships a local sample-data generator for offline reproduction:

```bash
# Generate offline teaching sample data (financial + historical price CSV)
python scripts/generate_sample_data.py
```

Output is written to the `data/` directory:
- `data/financials.csv`: AAPL financial summary for the last 4 fiscal years (FY2022-FY2025)
- `data/stock_history.csv`: weekly OHLCV for the past year (53 weeks)

The real-data CSVs used by the current pipeline are `demo-data/financials_real.csv`, `demo-data/quarterly_real.csv` and `demo-data/stock_history_real.csv`.

### 3.3 View Analysis Deliverables

```bash
# Three analysis tracks
cat analysis/fundamental.md   # Fundamental analysis
cat analysis/technical.md     # Technical analysis
cat analysis/risk.md          # Risk & sentiment analysis

# Combined forecast
cat outputs/forecast.md       # Target price range and scenario projection

# Final deliverables
cat deliverables/investment-research-report.md   # Investment research report
cat deliverables/jiuwen-multiagent-dev-manual.md # JiuWen multi-agent development handbook
```

### 3.4 Reproduce This Project on JiuwenSwarm

See the *JiuWen Multi-Agent Development Handbook* (`deliverables/jiuwen-multiagent-dev-manual.md`) for the complete step-by-step reproduction tutorial, covering: goal decomposition → role design → DAG design → handoff design → collaboration design → acceptance design, plus a "5-minute quick start" checklist.

---

## 4. Directory Structure

```
repo/
├── README.md                        # Project overview, architecture, quick start, disclaimer
├── LICENSE                          # MIT open-source license
├── .gitignore                       # Excludes temporary files, .DS_Store, etc.
├── data/                            # Offline sample data (real data lives in .team/demo-data/)
│   ├── financials.csv               # Sample financial summary (FY2022-FY2025, 14 fields)
│   └── stock_history.csv            # Sample weekly OHLCV (53 weeks)
│   # real pipeline data: financials_real.csv (10-K) + quarterly_real.csv (10-Q) + stock_history_real.csv (Yahoo)
├── analysis/                        # Three analysis tracks
│   ├── fundamental.md               # Fundamental analysis
│   ├── technical.md                 # Technical analysis
│   └── risk.md                      # Risk & sentiment analysis
├── outputs/                         # Forecast
│   └── forecast.md                  # Combined forecast (target price range + scenario projection)
├── deliverables/                    # Reports and handbook
│   ├── investment-research-report.md    # Investment research report
│   └── jiuwen-multiagent-dev-manual.md  # JiuWen multi-agent development handbook
└── scripts/                         # Generation scripts
    └── generate_sample_data.py      # Sample data generation script
```

---

## 5. Disclaimer

This project and all of its content (data, analysis, forecasts, reports, handbook) are **for teaching demonstration purposes only**:

- All financial and market data are **locally generated constructed samples**, not real-time or real;
- All analysis conclusions, scores, target price ranges, and scenario projections are **algorithmic outputs of the multi-agent teaching workflow** and do not reflect any real investment judgment;
- This project **does NOT constitute investment advice**; do not make real trading decisions based on it. Any trading based on this project is at your own risk.

---

## 6. License

This project is licensed under the [MIT License](LICENSE) and may be freely used, modified, and distributed (for teaching purposes).
