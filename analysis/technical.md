# AAPL Technical Analysis Report (Teaching Sample)

> **Scope Statement**: This report is based on `.team/demo-data/stock_history.csv` (AAPL teaching demo sample weekly price data, 2025-09-15 ~ 2026-09-14, 53 weeks). The data are **constructed teaching sample data, not live market data, and not investment advice**. Indicator calculations are reproducible with the script `calc_technical.py`; calculation assumptions are noted at the end.

---

## 1. Data Overview

| Item | Value |
|---|---|
| Sample period | 2025-09-15 ~ 2026-09-14 (53 weeks, sampled every Monday) |
| First week close | USD 228.00 |
| Latest close (2026-09-14) | **USD 276.11** |
| Full-period change | **+21.10%** |
| Full-period high / low | 282.22 (week of 2026-09-14) / 218.39 (week of 2025-11-10) |

The sample is constructed from 5 trend segments: "up → up → pullback → stabilize → up again", consistent with the data generation script definition.

---

## 2. Trend Assessment

### 1. Short-term trend (last 4-8 weeks): consolidating then re-attacking upward, neutral-to-bullish

| Window | Starting Close | Latest Close | Change |
|---|---|---|---|
| Last 4 weeks | 275.37 | 276.11 | +0.27% |
| Last 8 weeks | 256.35 | 276.11 | **+7.71%** |
| Last 13 weeks | 255.16 | 276.11 | +8.21% |
| Last 26 weeks | 254.54 | 276.11 | +8.47% |

- Over the last 4 weeks, price has consolidated in the 271-282 range (8/17 close 275.37 → 9/14 close 276.11), i.e., **high-level consolidation**;
- However, on the 8-13 week view, price has steadily climbed from around 255 to above 276, with a rising short-term center of gravity. Last week (9/7 close 280.26) briefly broke above 280 before pulling back slightly to close at 276, showing **clear upward intent**.

### 2. Mid-term trend (last 26 weeks to full period): bullish trend intact

- Full period +21.10%, 26 weeks +8.47%, mid-term uptrend channel remains intact;
- Lows kept rising from Feb 2026 (approx. USD 251) and mid-March (approx. USD 254), with highs also rising in tandem, consistent with an **uptrend**;
- Since May, price has been trading above MA20, with pullbacks not breaking the mid-term average — healthy trend structure.

**Conclusion: short-term neutral-to-bullish (consolidation building), mid-term bullish (uptrend channel).**

---

## 3. Moving Average System (MA20 / MA60)

### Calculation Notes
- **MA20** = simple average of the most recent 20 weekly closes;
- **MA60**: since the sample has only 53 weeks (fewer than 60), the **full-sample 53-week average (MA53) is used as a proxy for MA60**, and this assumption is explicitly flagged.

### Moving Average Values and Arrangement

| MA | Value (USD) | vs. Last Week |
|---|---|---|
| MA10 (weekly) | 268.91 | — |
| MA20 (weekly) | **262.33** | 260.80 → 262.33 (↑1.53) |
| MA30 (weekly) | 257.92 | — |
| MA53 (≈MA60) | **246.73** | 246.17 → 246.73 (↑0.56) |

### Arrangement Assessment

- **Bullish alignment confirmed**: latest close 276.11 > MA20 262.33 > MA53(≈MA60) 246.73;
- Both MA20 and MA53 are rising with positive slopes — effective mid-term cost support;
- Price has stayed above MA20 since July, only briefly testing it during the week of 7/6 (251.75) before quickly recovering — **MA20 acts as dynamic support**.

**Conclusion: bullish moving-average alignment; MA20 (approx. 262) and MA53-proxy (approx. 247) are the most important trend supports.**

---

## 4. Momentum Indicators (RSI14 / MACD)

### RSI14 (Wilder smoothing, simplified for teaching)

| Indicator | Value |
|---|---|
| RSI14 latest | **68.66** |
| RSI14 previous | 75.51 |

- Currently in the **strong zone (60-70), not overbought (overbought is >70)**;
- Eased from the prior high of 75.5 to 68.66, meaning short-term overheating has been digested — **momentum remains strong after the repair**;
- If price continues higher, watch for short-term pullback risk as RSI approaches 70.

### MACD (12, 26, 9)

| Indicator | Value |
|---|---|
| DIF | +8.123 (above zero line) |
| DEA | +6.682 |
| MACD histogram | +2.882 (prior 3.417) |

- Both DIF and DEA are above the zero line, and **DIF > DEA (bullish alignment / golden cross persisting)**;
- The red histogram has narrowed slightly (3.417 → 2.882): momentum easing marginally at the edges but not turning green — **mid-term bullish momentum still dominant, short-term momentum cooling slightly**.

**Conclusion: dual-bullish momentum (RSI strong, MACD golden cross above zero line persisting); short-term momentum cooling slightly but trend not broken.**

---

## 5. Volume-Price Relationship

| Item | Value |
|---|---|
| Full-period average weekly volume | 97.3M shares |
| Last-10-week average volume | 99.1M (+0.5% vs. prior 10 weeks' 98.6M) |
| Avg volume up-weeks / down-weeks | 98.4M / 94.4M |
| Latest week volume (9/14) | 134.3M (significantly expanded, near full-period peak of 146M) |

- **Up-week average volume > down-week average volume**: rising price action accompanied by volume confirmation — healthy volume-price relationship;
- Volume expanded during the weeks of 8/3 (+1.9%, 146.1M) and 9/14 (spiked to 282 then closed at 276, 134.3M); the August expansion accompanied a breakout while the September expansion came with stalled gains — worth noting;
- Overall volume is steady with a slight increase (+0.5%), **no obvious divergence of shrinking-volume stall or high-volume sell-off**.

**Conclusion: volume-price cooperation is good, rallies supported by volume; the 9/14 high-volume close with ~1.5% pullback is a high-level divergence signal — track whether it continues.**

---

## 6. Key Support / Resistance Levels

### Key Price Levels (USD)

| Type | Level | Basis |
|---|---|---|
| Resistance 1 | **282-283** | Full-period high 282.22 (high of week 9/14); round-number 280 nearby |
| Resistance 2 | 280.3 | Week of 9/7 high 280.29, first short-term hurdle |
| Support 1 | **273-274** | Dense zone of last-4-week lows 271.3-274.3 + 8/17-8/31 close pullback zone |
| Support 2 | **262-266** | MA20 (262.3) + 8/10 low 261.5 + 8/3 breakout platform, double support |
| Support 3 | **255-256** | MA30 (257.9) + mid-June lows 252.7-255.2 mid-term neckline |

---

## 7. Trend Rating

### Rating: **Bullish (trend up; short-term neutral-to-bullish)**

| Dimension | Conclusion | Basis |
|---|---|---|
| Mid-term trend | ✅ Bullish | Full period +21%, uptrend channel, rising lows |
| MA alignment | ✅ Bullish | Bullish alignment (close > MA20 > MA60), MA20/MA60 rising |
| Momentum | ✅ Bullish-leaning | RSI strong, not overbought; MACD golden cross above zero line persisting |
| Volume-price | ✅ Positive | Rallies on volume, healthy volume-price relationship |
| Short-term | ⚠️ Neutral-to-bullish | Last 4 weeks consolidating, RSI pulled back from highs, MACD red histogram narrowing |

The overall score leans bullish; key uncertainties are the **breakout capability near the short-term high (282) and MACD momentum convergence**.

---

## 8. Buy/Sell Timing Suggestions (Teaching Context, Not Investment Advice)

> The following are strategy illustrations in a technical-analysis teaching context, to help understand the analytical framework — **not investment advice**.

### Buy Scenarios

1. **Buy on support pullback (conservative)**: when price pulls back to **262-266 (MA20 zone)**, stabilizes, and volume shrinks, it can serve as a reference zone for staged entry; stop-loss reference below 258 (below MA30).
2. **Buy on confirmed breakout (aggressive)**: if price **effectively breaks and holds 282.5** on volume (weekly volume >110M), it can be seen as a trend-acceleration signal — enter on confirmation.

### Sell / Take-Profit Scenarios

1. **Reduce at resistance**: when the advance toward **282-283** shows long upper shadows or stalled gains (e.g., a repeat of the 9/14 spike-and-reversal), consider partial profit-taking.
2. **Stop-loss on trend break**: if close falls below **MA20 (262)** and RSI falls below 55, the short-term trend weakens — reduce positions; a break below 255 (MA30) damages the mid-term uptrend channel — stop and wait.

### Risk Monitoring Checklist

- Whether RSI14 enters overbought (>70) with divergence;
- Whether the MACD red histogram keeps narrowing and turns green (momentum turning bearish);
- Whether the 282 resistance breaks on volume;
- Whether volume shows a high-volume decline (distribution signal at highs).

---

## 9. Risk Warnings

1. **Teaching sample nature**: this data is constructed (5 trend segments + random noise), with deliberately engineered technical patterns; conclusions only demonstrate methodology, **not investment advice, and do not indicate real market behavior**.
2. **MA approximation**: MA60 is proxied by the full-sample average due to insufficient data length (53 weeks); the mid-term MA reference has limited meaning.
3. **Short-term pullback risk**: RSI is still in the strong zone and 9/14 spiked then fell; MACD red histogram is narrowing — short-term high-level consolidation is needed.
4. **Technical-only limitation**: this report is based solely on price-volume data and does not consider fundamentals, market sentiment, or macro factors; combine with the *Fundamental Analysis* and *Risk & Sentiment Analysis* reports.
5. **Discrete data frequency**: weekly view smooths intraday fluctuations; short-term support/resistance levels are for teaching reference only.

---

## Appendix: Calculation Methods and Assumptions (Reproducible)

| Indicator | Calculation Method | Assumption / Approximation |
|---|---|---|
| MA20 / MA30 | Simple average of last N weekly closes | — |
| MA60 proxy | Full-sample 53-week average (MA53) | Sample shorter than 60 weeks; explicit proxy and flag |
| RSI14 | Wilder smoothing: simple-average initialization, then `(n-1)/n` recursion | Teaching simplification; no multi-period/divergence validation |
| MACD | EMA12 − EMA26 = DIF; DEA = EMA9(DIF); histogram = 2×(DIF−DEA) | EMA uses standard smoothing coefficients; initialized with first-week close |
| Support/Resistance | Recent swing high/low + MA dynamic support + round numbers | Manual annotation, not automated pivot calculation |

*Generated: 2026-08-20 | Analyst: technical-analyst | Data source: .team/demo-data/stock_history.csv (teaching sample)*
