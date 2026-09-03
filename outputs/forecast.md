# AAPL — Consolidated Price Forecast (Real Data Edition)

**Analyst**: forecaster (Prediction Synthesizer)
**Date**: 2026-09-04
**Data sources**: SEC EDGAR (Apple 10-K FY2022–FY2025, XBRL companyfacts) + Yahoo Finance (weekly OHLCV, 1y); latest close **328.21 USD (2026-09-03)**. Upstream inputs: `.team/analysis/fundamental.md`, `technical.md`, `risk.md` (real-data editions).

> **Disclaimer**: Educational / teaching demonstration only. Real market data, but all forward estimates are analyst assumptions illustrating methodology. **Not investment advice.**

---

## 0. Executive Summary

| Item | Value |
|---|---|
| Target range (3–6 months) | **215 – 365 USD**; core band **275 – 345** |
| Central value (weighted) | **≈ 310 USD** (-5.5% vs 328.21) |
| Advance / decline probability | **45% / 55%** |
| Confidence | **Moderate (~60%)** |
| Scenarios | Bull ≈ **350** (340–365) · Base ≈ **318** (300–335) · Bear ≈ **240** (215–260) |
| Verdict | Great company, rich valuation, intact uptrend — expect high-level consolidation, mildly negative skew; watch 334/344.6 gate vs 305–309 (MA20) support |

---

## 1. Inputs: Three-Analyst Conclusions

| Dimension | Analyst | Conclusion | Key numbers |
|---|---|---|---|
| Fundamental | fundamental-analyst | Quality 66/100, good quality / expensive; no margin of safety | Implied PE 44.0x; fair band 215–295 (center ≈250); FY2026E EPS 7.68 (g=3%) / 7.91 (g=6%) / 8.21 (g=10%) |
| Technical | technical-analyst | **BULLISH**; medium-term uptrend intact | Resistance 330.8–334 / 344.6 (ATH); support 320 → 305–309 (MA20) → 300 → 287–292; RSI 62.92; MACD fresh bullish cross |
| Risk & sentiment | risk-sentinel | **MEDIUM-HIGH**; macro/valuation risk raised to HIGH; cautiously optimistic | ~44x PE; regulatory + supply-chain HIGH; "do not chase strength" |

**Consensus**: excellent quality + strong uptrend + rich valuation → high sensitivity to negative catalysts.

---

## 2. Model 1: PEG Check — Is the Multiple Justified?

**Inputs**: close 328.21; FY2025 EPS 7.46 → trailing P/E 44.0x; FY2026E base EPS 7.91 → forward P/E ≈ 41.5x; visible base growth ≈ 6% (FY2025 rev +6.43%, 3-yr CAGR +1.81%).

| PEG target | Implied required growth (41.5 / PEG) | vs visible 6% |
|---|---|---|
| 1.0 | 41.5% | ~7x higher |
| 1.5 | 27.7% | ~4.6x higher |
| 2.0 (cap) | 20.7% | ~3.5x higher |

- Even bull EPS (8.21, g=10%): forward P/E 40.0x → PEG ≈ 4.0 > 2.
- **Actual PEG (base) = 41.5 / 6 ≈ 6.9** — clearly overvalued zone.

**Conclusion**: the ~41.5x forward multiple embeds 20–40% annual growth expectations vs mid-single-digit fundamentals; the +69.8% (FY22→FY25) / +36.9% (54w) re-rating is **multiple expansion, not earnings growth** — confirms "no margin of safety" (fundamental) and "44x = catalyst-sensitive" (risk).

---

## 3. Model 2: PE × EPS Scenario Weighting

| Scenario | Prob | Triggers | EPS | PE | Target = EPS×PE | Range / center |
|---|---|---|---|---|---|---|
| **Bull** | 25% | Volume-confirmed close above **334** → break **344.6 ATH**; AI/services narrative delivers; benign regulation | 8.21 (g=10%) | 40–42x | 328–345 | **340–365** (≈**350**) |
| **Base** | 50% | No systemic shock; EPS ~+6%; consolidation 305–335 digesting valuation; no decisive break of 334 or 305 | 7.91 (g=6%) | 36–40x | 285–316 | **300–335** (≈**318**) |
| **Bear** | 25% | Weekly close < 320 → below **305–309 (MA20)**; adverse regulatory ruling / supply disruption / sharp rates; EPS <3% | 7.68 (g=3%) | 28–30x | 215–230 | **215–260** (≈**240**) |

**Weighted center** = 350×0.25 + 318×0.50 + 240×0.25 = 87.5 + 159 + 60 = **306.5 ≈ 310 USD** (-5.5% vs spot).

**Target summary**: wide band **215–365** (~90%); core band **275–345** (~60–70%); center **≈310**. Upside from center +17.7% (365) vs downside -30.6% (215) → risk/reward ≈ 1:1.7, **negatively skewed** (matches "above fair band by 11–53%" and "high-level distribution" warnings).

---

## 4. Probability & Confidence

| Direction | Probability | Basis |
|---|---|---|
| Advance (> 328.21) | ≈ 45% | Bull 25% + upper half of Base |
| Decline (< 328.21) | ≈ 55% | Base center 318 < spot + Bear |

**Confidence moderate (~60%)**: ① genuine bull/bear disagreement (technical vs valuation) widens uncertainty; ② compressed 54-week real-data window; ③ regulatory/macro tails unpriced.

---

## 5. Three-Scenario Walkthrough (3–6 months)

**Bull (25%, 340–365, center ≈350, +4% to +11%)** — Triggers: weekly volume >250M confirms break of 334 → then 344.6 ATH; FY2026 guidance ≥10% EPS; benign rulings; dovish macro. Path: 320–328 → clear 330.8–334 shelf → 344.6 → 350–365. Cross-check: technical breakout scenario; risk upgrade path; fundamental peak 40x×8.21=328 — 350+ requires BOTH technical breakout AND EPS upgrade.

**Base (50%, 300–335, center ≈318, -3% to +2%)** — Triggers: EPS ~6%; no shock; regulation incremental; rates stable. Path: high-level consolidation 305–335; stalls at 330–334; pullbacks hold 320, occasionally test 305–309 (MA20). Cross-check: all technical supports/resistances inside band; fundamental fair band top 295 near band lower edge; risk "buy pullbacks".

**Bear (25%, 215–260, center ≈240, -21% to -27%)** — Triggers: weekly close <320 → loss of 305–309 (MA20) → <300 → 287–292 (MA30/Jun low); adverse regulatory ruling / supply disruption / rate repricing; EPS <3%. Path: 320 → 305–309 → 300 → 287–292; earnings cut to 7.68 + 28–30x → 215–230 zone; losing MA53 (≈279) confirms trend damage (aligns technical stop-loss with risk de-risk trigger). Cross-check: fundamental bear 215; risk HIGH upgrade; technical deeper-correction signal.

---

## 6. Key Assumptions

1. FY2026E EPS: base 7.91 (+6%), bull 8.21 (+10%), bear 7.68 (+3%) — analyst extrapolation on real FY2025 EPS 7.46.
2. Scenario P/E 28x–42x: below 4-yr mean (31.05x) in bear to above FY2024 band top (37.5x) in bull.
3. No systemic black swan; no extreme rate reversal.
4. Regulatory incremental only — sudden adverse ruling shifts distribution to bear (risk → HIGH).
5. Technical: MA20 (308.80) / MA53 (279.49) hold in base; 330.8–334 / 344.6 cap upside until volume break.
6. AI landscape and narrative as-is; no major capital-structure events.

---

## 7. Cross-Validation (Agreements & Disagreements)

**Agreements** (reinforced): ① "great company, rich price" — all three; ② medium-term trend positive (BULLISH channel + cautious optimism + FY2025 acceleration); ③ near-term tension at current price (330–334 resistance, volume caution, peak-multiple pricing) → center placed below spot.

**Disagreements** (→ tail risk):

| Issue | Fundamental | Technical | Risk | My resolution |
|---|---|---|---|---|
| Fair-value anchor | ≈250 | levels only | no target | Blend 250 + 305–309 support → center ≈310 |
| Pullback depth | bear ≈215 | deepest 287–292/279 | refs technical | Two-stage: 305–309, then 287–292/279; extreme 215–230 only if EPS cut |
| Upside space | peak ≈328 | 344.6+ | upgrade if AI delivers | 340–365 requires BOTH break of 344.6 AND EPS upgrade |

**Synthesis**: direction medium-term cautiously positive; 3–6 month view cautious (valuation + overhead shelf) → center ~5.5% below spot. One-liner: *"A great company at a rich price in an intact uptrend"* — high-level consolidation; volume break above 334 opens 344+ (bull); weekly close below 320 opens 305–309 and beyond (bear).

---

## 8. Data Provenance & Limitations

- **Financials**: SEC EDGAR XBRL companyfacts — Apple 10-K FY2022–FY2025 (filing 2022-10-28 / 2023-11-03 / 2024-11-01 / 2025-10-31), fetched 2026-09-04; USD millions.
- **Prices**: Yahoo Finance chart API (1wk, 1y), fetched 2026-09-04; 54 weekly bars; latest close 328.21.
- **Forward EPS/PE are transparent analyst assumptions** on real reported data.
- **Limitations**: 54-bar sample (MA53≈MA60); sentiment/regulatory judgments rely on public common knowledge; teaching-grade models omit DCF/dividends/fx.

---

## 9. Teaching Takeaways

- Demonstrates the **synthesis node** of a multi-agent pipeline: three upstream reports → transparent models (PEG check + PE×EPS scenario weighting) → probability-weighted target → cross-validation.
- **Cross-validation is the most transferable skill**: agreement raises confidence; disagreement becomes explicit tail risk and lowers it.
- Every number is reproducible from the stated inputs and formulas.

---

*Educational demonstration only — not investment advice.*
