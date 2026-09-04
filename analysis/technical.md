# AAPL Technical Analysis Report (Real Market Data)

> **Disclaimer**: This document is generated for **educational / teaching demonstration purposes only**. It is based on real market data fetched from Yahoo Finance (chart API, weekly interval) for a classroom demo of multi-agent investment research. **It does NOT constitute investment advice.** Always conduct your own due diligence before making any investment decision.

---

## 0. Data Source & Provenance

| Item | Detail |
|---|---|
| Instrument | AAPL (Apple Inc.) |
| Data source | Yahoo Finance chart API (`interval=1wk, range=1y`) |
| Fetch date | 2026-09-04 |
| Sample window | 2025-09-01 ~ 2026-09-03 (54 weekly bars) |
| Latest close | **328.21 USD** (2026-09-03) |
| Units | OHLC in USD; volume in shares |
| Computation | Reproducible via script `calc_technical_real.py` (Wilder RSI, standard EMA-based MACD) |

---

## 1. Trend Assessment

### 1.1 Medium-Term Trend (26-week to full window): **Strong Uptrend**

| Window | Start Close | End Close | Change |
|---|---|---|---|
| Full period (54w) | 239.69 | 328.21 | **+36.93%** |
| Last 26w | 250.12 | 328.21 | **+31.22%** |
| Last 13w | 291.13 | 328.21 | +12.74% |

- The stock has advanced from ~240 to ~328 over the past year, forming a clear **ascending channel** with higher lows (Jun pullback low 273.75 → Aug low 300–301 → recent low 312.8).
- Medium-term trend is **bullish and intact**.

### 1.2 Short-Term Trend (4–8 weeks): **Rebound after correction, neutral-to-bullish**

| Window | Start Close | End Close | Change |
|---|---|---|---|
| Last 8w | 333.74 | 328.21 | **-1.66%** |
| Last 4w | 305.93 | 328.21 | **+7.28%** |

- July printed the cycle high (344.57 on 2026-07-27) followed by a sharp one-week pullback (-7.2%, close 308.91) on heavy volume (365M shares).
- August consolidated in the 301–320 range, and the last 4 weeks show a **strong rebound (+7.28%)**, with the latest week (2026-09-03) closing at 328.21 near the round level of 330.

**Conclusion: medium-term uptrend intact; short-term rebound in progress with overhead resistance at 330–345.**

---

## 2. Moving Average System (MA20 / MA53)

### Computation Notes
- **MA20** = simple mean of the last 20 weekly closes.
- **MA53** = simple mean of the last 53 weekly closes (used in place of MA60 because the sample has only 54 bars; approximation explicitly noted).

### MA Values & Slope

| MA | Value (USD) | Prev | Direction |
|---|---|---|---|
| MA10 | 319.25 | — | — |
| MA20 | **308.80** | 305.94 | ↑ (+2.86) |
| MA30 | 292.23 | — | — |
| MA53 | **279.49** | 277.82 | ↑ (+1.67) |

### Alignment
- **Bullish alignment confirmed**: close 328.21 > MA20 308.80 > MA53 279.49.
- Both MA20 and MA53 are rising; price has traded above MA20 since the June pullback recovered in early July.
- MA20 (≈309) is the key dynamic support; MA53 (≈279) is the medium-term trend anchor.

**Conclusion: bullish MA stack; pullbacks toward MA20 (≈309) would be the first technical support zone.**

---

## 3. Momentum Indicators (RSI14 / MACD)

### RSI14 (Wilder smoothing)

| Metric | Value |
|---|---|
| RSI14 latest | **62.92** |
| RSI14 previous week | 61.88 |

- RSI is in the **strong zone (60–70) but NOT overbought (<70)**.
- Momentum has been recovering since the August consolidation; room remains before the overbought threshold.

### MACD (12, 26, 9)

| Metric | Value |
|---|---|
| DIF | +12.985 (above zero, rising) |
| DEA | +12.708 |
| MACD histogram | **+0.554** (prev -0.038; prev2 -0.685) |

- **Note on MACD histogram**: value +0.554 uses EMA seed = first close (as implemented in `calc_technical_real.py`); using the alternative seed convention (EMA seed = SMA of first window) yields approx. +0.277. Both conventions are reproducible and directionally identical (fresh bullish crossover); the script default is retained for consistency.

- DIF > DEA (**bullish**) and both are above the zero line.
- The histogram has **just flipped positive** (-0.685 → -0.038 → +0.554), signaling a **fresh bullish momentum crossover** after a brief consolidation.
- Momentum bias: **bullish**, with an early-stage acceleration signal.

**Conclusion: momentum is bullish; the histogram's fresh positive crossover supports continued upside, provided price clears 330–334.**

---

## 4. Volume-Price Relationship

| Metric | Value |
|---|---|
| Full-window avg volume | 232.7M shares |
| Last 10w avg volume | 209.9M (vs 271.1M prior 10w, **-22.6%**) |
| Latest week volume | 36.4M (partial week, fetch date 09-04) |
| Up-week avg volume (n=30) | 226.9M |
| Down-week avg volume (n=23) | 242.9M |

- **Watch item**: volume is contracting (-22.6%) as price rallies — the rebound is running on lighter volume, so upside needs volume confirmation above 334.
- Down weeks carry slightly higher average volume than up weeks (242.9M vs 226.9M); notable high-volume down weeks occurred on 2025-09-08, 2025-12-15, **2026-06-22 (518.8M, big red week)**, and **2026-07-27 (364.9M, -7.2%)** — these mark distribution zones that acted as resistance.
- No extreme blow-off volume at the current close; the last full week (2026-08-31) closed +1.6% on 128M shares.

**Conclusion: price-volume relationship is broadly healthy, but the rally is modestly under-confirmed by volume; a volume-confirmed break above 334 would strengthen the bullish case.**

---

## 5. Key Support & Resistance Levels

### Resistance
| Level | Basis |
|---|---|
| **330.8 – 334** | 2026-09-03 high (330.81); July high cluster (334.37–334.99) |
| **344.6** | Cycle high 344.57 (2026-07-27) — primary upside target/cap |

### Support
| Level | Basis |
|---|---|
| **312.8 – 320** | Aug consolidation floor (Aug 10 low 305.93 → recent low 312.8); round 320 + Aug 24 close 319.70 |
| **305 – 309** | MA20 (308.80) + Aug 10 low (305.93) + Aug 3 low (301.32) — key dynamic support |
| **300** | Round number + 2026-07-27 intraday low (300.00) |
| **287 – 292** | Jun 8 low (287.38) / MA30 (292.23) — medium-term support if deeper pullback |

---

## 6. Trend Rating

### Rating: **BULLISH** (medium-term uptrend intact; short-term neutral-to-bullish rebound)

| Dimension | Assessment | Evidence |
|---|---|---|
| Medium-term trend | ✅ Bullish | +36.93% over 54w; higher lows structure |
| MA system | ✅ Bullish | close > MA20 > MA53, both rising |
| Momentum | ✅ Bullish | RSI 62.9 strong, not overbought; MACD fresh bullish crossover |
| Volume-price | ⚠️ Mild caution | Rally on lighter volume; down-week volume slightly higher |
| Short-term | ✅ Neutral-to-bullish | +7.28% rebound off 301–306 support zone |

Overall the chart favors upside, but the path is gated by the **330–334 resistance shelf** and the **344.6 cycle high**. A volume-confirmed break above 334 would open the run toward 344+; failure to hold 320–324 could see a retest of 305–309 (MA20).

---

## 7. Key Levels Summary (for cross-agent handoff)

- **Upside targets / resistance**: 330.8 → 334.0–335.0 → 344.6 (ATH)
- **Downside supports**: 320 → 312.8 → 305–309 (MA20) → 300 → 287–292 (MA30/Jun low)
- **Primary pivot**: **334** — above it, bullish acceleration; below **320**, short-term weakness toward MA20.

---

## 8. Risk Notes

1. **Teaching sample disclaimer**: real market data used only for a classroom demo; **not investment advice**; no guarantee of accuracy or timeliness of the data.
2. **Indicator approximations**: MA53 substitutes for MA60 due to 54-bar sample; RSI uses Wilder smoothing with a simple-average seed; MACD uses standard EMA coefficients.
3. **Short-term risk**: rally volume is contracting; a rejection at 330–334 could trigger a pullback to 320 or 305–309.
4. **Correction risk**: the 2026-06-22 and 2026-07-27 high-volume down weeks highlight elevated volatility; a break below 300 would signal a deeper medium-term correction.
5. **Scope limit**: technical analysis only — must be combined with fundamental and risk/sentiment analyses for a full view.

---

*Generated: 2026-09-04 | Analyst: technical-analyst | Data: .team/demo-data/stock_history_real.csv (Yahoo Finance weekly, fetched 2026-09-04) | Educational demo only — not investment advice.*