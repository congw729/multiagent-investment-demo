# AAPL Fundamental Analysis Report (Real Data)
**Analyst**: fundamental-analyst
**Data Sources**:
- Financials: SEC EDGAR (Apple Inc. Form 10-K, FY2022–FY2025; filing dates 2022-10-28 / 2023-11-03 / 2024-11-01 / 2025-10-31; XBRL companyfacts; retrieved 2026-09-04) — `.team/demo-data/financials_real.csv`
- Market data: Yahoo Finance chart API (weekly OHLCV, 1y range; retrieved 2026-09-04) — `.team/demo-data/stock_history_real.csv`
- Units: amounts in USD millions; ratios in percent; PE/PB based on fiscal-year-end close price; latest close: **328.21 USD (2026-09-03)**

---

## 1. Revenue Growth Trend

| FY | Revenue (USD mn) | YoY | FY-end Close (USD) |
|---|---|---|---|
| FY2022 | 394,328 | — | 150.43 |
| FY2023 | 383,285 | -2.80% | 171.21 |
| FY2024 | 391,035 | +2.02% | 227.79 |
| FY2025 | 416,161 | +6.43% | 255.46 |

- Revenue bottomed in FY2023 (-2.80%) and recovered in FY2024 (+2.02%), then **accelerated to +6.43% in FY2025 to a record 416,161 mn**.
- 3-year revenue CAGR (FY2022→FY2025): **+1.81%** — still low single-digit; this is a mature compounder, not a hyper-growth name.
- Stock: FY-end close rose from 150.43 to 255.46 (+69.8% over 3 years), far outpacing revenue/profit growth — the re-rating came largely from **valuation expansion**, not fundamentals alone.
- Latest weekly close 328.21 (2026-09-03) is **+36.9% above the 2025-09-01 close of 239.69** (first bar of the real series), vs FY2025 EPS growth of ~22% — price ran well ahead of earnings.

## 2. Profitability (Gross Margin / Net Margin / ROE)

| FY | Gross Margin | Net Margin | ROE | Net Income (mn) |
|---|---|---|---|---|
| FY2022 | 43.31% | 25.31% | 197.0% | 99,803 |
| FY2023 | 44.13% | 25.31% | 156.1% | 96,995 |
| FY2024 | 46.21% | 23.97% | 164.6% | 93,736 |
| FY2025 | 46.91% | 26.92% | 151.9% | 112,010 |

- **Gross margin improved for four straight years** to a record 46.91% (from 43.31%), signaling a favorable product mix (services, Pro hardware).
- **Net margin rose to a record 26.92% in FY2025** (from 25.31%/23.97%), and net income hit a record 112,010 mn.
- **ROE remains exceptionally high** at 151.9% (FY2025), though it has moderated from 197.0% (FY2022) as the equity base normalized. ROE this high is partly a function of elevated leverage (see below).

## 3. Financial Health (Leverage / Liquidity)

| FY | Debt Ratio (Liab/Assets) | Current Ratio |
|---|---|---|
| FY2022 | 85.6% | 0.88 |
| FY2023 | 82.4% | 0.99 |
| FY2024 | 84.4% | 0.87 |
| FY2025 | 79.5% | 0.89 |

- **Leverage improved to 79.5% in FY2025**, the lowest of the four years (from 85.6%), a genuine deleveraging trend — but the absolute level remains high (>79%), and ROE above 150% is structurally dependent on this leverage.
- **Liquidity stays tight**: current ratio FY2025 = 0.89 (below 1.0, and below FY2023's 0.99). Short-term assets do not cover short-term liabilities; buffer is thin.

## 4. Cash Flow Quality

| FY | Operating Cash Flow (mn) | OCF / Net Income |
|---|---|---|
| FY2022 | 122,151 | 1.22 |
| FY2023 | 110,543 | 1.14 |
| FY2024 | 118,254 | 1.26 |
| FY2025 | 111,482 | 1.00 |

- OCF exceeded 110 bn USD in every year; OCF/Net Income was **>1.0 in all four years (1.00–1.26)**, confirming high earnings quality (profits backed by real cash).
- Note: FY2025 OCF/NI fell to 1.00 — still ≥1, but the cushion narrowed as working-capital dynamics shifted.

## 5. Valuation Assessment

| FY | FY-end Close | PE | PB |
|---|---|---|---|
| FY2022 | 150.43 | 24.6x | 47.2x |
| FY2023 | 171.21 | 27.9x | 42.8x |
| FY2024 | 227.79 | 37.5x | 60.5x |
| FY2025 | 255.46 | 34.2x | 51.2x |

- **Latest close 328.21 (2026-09-03) / FY2025 diluted EPS 7.46 → implied PE ≈ 44.0x**, well above the four-year band (24.6x–37.5x) and far above the 4-year mean of **31.05x**.
- FY-end PE was already rich at 34.2x (FY2025); the current 44.0x implies a further re-rating of ~29% vs. FY2025 year-end.

### Reasonable Value Range (Qualitative + Quantitative)

- **Valuation anchors**: historical PE mean 31x, top of band 37.5x (FY2024). FY2026E EPS scenarios (analyst assumptions on top of real FY2025 EPS 7.46): g=3% → 7.68; g=6% → 7.91; g=10% → 8.21.
- **PE × EPS range**:
  - Bearish (PE 28x × 7.68): ≈ **215 USD**
  - Base (PE 32x × 7.91): ≈ **253 USD**
  - Bullish (PE 36x × 8.21): ≈ **295 USD**
  - Peak scenario (PE 40x × 8.21): ≈ **328 USD** (i.e., the current price itself requires ~40x on 10% EPS growth — the market is pricing the most optimistic case)
- **Qualitative view**: a fair-value band of roughly **215–295 USD (base-case center ≈ 250)** looks defensible for a high-quality compounder with record margins but single-digit revenue growth. At 328.21 (44.0x), the stock sits **above the top of a reasonable band by ~11–53%** — valuation is stretched, and margin of safety is thin.

## 6. Company Quality Score (100 pts)

| Item | Max | Score | Basis (real data) |
|---|---|---|---|
| Revenue growth trend | 20 | 14 | FY2025 +6.43% acceleration; 3-yr CAGR only 1.81% |
| Profitability | 25 | 23 | Record GM 46.91%, NM 26.92%, ROE 151.9%+ |
| Financial health | 20 | 10 | DR 79.5% high; current ratio 0.89 <1 |
| Cash flow quality | 20 | 16 | OCF/NI 1.00–1.26 all years; FY2025 cushion =1.00 |
| Valuation | 15 | 3 | Implied PE 44x at all-time high; no margin of safety |
| **Total** | **100** | **66** | **Rating: Good quality, expensive valuation** |

## 7. Bull Case (3+)

1. **Growth re-accelerating**: FY2025 revenue hit a record 416,161 mn (+6.43%), the fastest pace in 3 years; margins rising into the acceleration.
2. **Record profitability**: gross margin 46.91%, net margin 26.92%, and net income 112,010 mn — all four-year highs; pricing power intact.
3. **High earnings quality**: OCF above 110 bn USD in every year, OCF/NI ≥1.00 throughout (1.00–1.26), profits are real cash.
4. **Deleveraging trend**: debt ratio improved from 85.6% to 79.5% over four years, reducing structural risk.

## 8. Bear Case / Risks (3)

1. **Valuation risk (primary)**: implied PE ≈44x vs. historical mean 31x and band top 37.5x; EPS growth is single-digit — price has run ahead of fundamentals; any disappointment in growth or risk appetite could trigger a 15–35% de-rating back toward 215–280.
2. **Low growth base**: 3-year revenue CAGR only 1.81%; sustained high multiple requires new product cycles/services scaling that are not yet evidenced in the reported data.
3. **Tight liquidity + high leverage**: current ratio 0.89 (<1) with debt ratio 79.5% — limited financial buffer under rising rates or cash-flow volatility.

---

*This report is based on real data sourced from SEC EDGAR 10-K filings (FY2022–FY2025) and Yahoo Finance weekly prices, retrieved 2026-09-04. Forward EPS scenarios are analyst assumptions; all historical figures are quoted directly from the source CSV. For teaching demo only.*<br>
**For educational demonstration only — not investment advice.**
