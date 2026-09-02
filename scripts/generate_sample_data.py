#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JiuWenSwarm Teaching Demo - Local sample data generation script (AAPL Apple)
For teaching demonstration only: data magnitudes are consistent with publicly
reported corporate financials/market data, but the data is constructed samples,
not live market data, and not investment advice. Running this script generates
the following files in the same directory:
  1) financials.csv      - annual financial summary for the past 4 fiscal years
  2) stock_history.csv   - weekly OHLCV for the past year (53 weeks)
"""
import csv
import os
import random
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
random.seed(20260820)

# ---------------------------------------------------------------------------
# 1) financials.csv - annual financial summary (amounts in USD millions; EPS in USD per share)
#    Definitions:
#      - roe_pct = net income / end-of-period shareholders' equity
#      - debt_ratio_pct = total liabilities / total assets
#      - current_ratio = current assets / current liabilities
#      - pe_ratio = fiscal year-end price / diluted EPS for the fiscal year; pb_ratio = fiscal year-end price / fiscal year-end book value per share
#      - Ratio fields are expressed as percentages (e.g., 43.31 means 43.31%)
#      - FY2025 is a sample estimate; other years are consistent in magnitude with Apple's public financials
# ---------------------------------------------------------------------------
financial_rows = [
    # fiscal_year, fiscal_year_end, revenue, net_income, gross_margin, net_margin,
    # roe, debt_ratio, current_ratio, ocf, eps, fy_end_price, pe, pb
    ["FY2022", "2022-09-24", 394328, 99803, 43.31, 25.31, 196.9, 85.6, 0.88, 122151, 6.11, 142.0, 23.2, 42.1],
    ["FY2023", "2023-09-30", 383285, 96995, 44.13, 25.31, 156.1, 82.4, 0.99, 110543, 6.44, 171.0, 26.6, 42.4],
    ["FY2024", "2024-09-28", 391035, 97819, 46.21, 24.62, 162.6, 82.0, 1.05, 118254, 6.31, 233.0, 36.9, 60.8],
    ["FY2025", "2025-09-27", 410450, 100180, 46.66, 24.44, 151.8, 81.7, 1.06, 115019, 6.55, 262.0, 40.0, 58.0],
]
fin_headers = [
    "fiscal_year", "fiscal_year_end", "revenue_million_usd", "net_income_million_usd",
    "gross_margin_pct", "net_margin_pct", "roe_pct", "debt_ratio_pct", "current_ratio",
    "operating_cash_flow_million_usd", "eps_usd", "fiscal_year_end_price_usd",
    "pe_ratio", "pb_ratio",
]
fin_path = os.path.join(HERE, "financials.csv")
with open(fin_path, "w", newline="", encoding="utf-8-sig") as f:
    f.write("# AAPL Apple - teaching demo sample financial data (not live market data; not investment advice)\n")
    f.write("# Units: amounts in USD millions; EPS in USD per share; ratios as percentages (43.31=43.31%)\n")
    f.write("# Definitions: ROE=net income/end-of-period equity; debt ratio=total liabilities/total assets; current ratio=current assets/current liabilities\n")
    f.write("# PE=fiscal year-end price/diluted EPS for the fiscal year; PB=fiscal year-end price/book value per share; FY2025 is a sample estimate\n")
    w = csv.writer(f)
    w.writerow(fin_headers)
    w.writerows(financial_rows)
print("financials.csv written:", fin_path)

# ---------------------------------------------------------------------------
# 2) stock_history.csv - weekly OHLCV for the past year (sample window: every Monday from 2025-09-15, 53 weeks)
# Price follows 5 sample trend segments: up -> up -> pullback -> stabilize -> up again;
# geometric interpolation within each segment + weekly random noise; volume unit: shares
# ---------------------------------------------------------------------------
segments = [
    # (start_price, end_price, weeks, weekly_vol_million)
    (228.00, 243.50, 9, 95),    # 2025-09-15 ~ 2025-11-10
    (243.50, 261.50, 15, 100),  # 2025-11-17 ~ 2026-02-23
    (261.50, 244.00, 8, 88),    # 2026-03-02 ~ 2026-04-20
    (244.00, 254.80, 10, 92),   # 2026-04-27 ~ 2026-06-29
    (254.80, 273.50, 11, 105),  # 2026-07-06 ~ 2026-09-14
]

def seg_factor(st, en, n):
    return (en / st) ** (1.0 / n) if n > 0 else 1.0

stock_rows = []
prev_close = None
cur = date(2025, 9, 15)
for (st, en, n, vol_base) in segments:
    g = seg_factor(st, en, n)
    for i in range(n):
        if prev_close is None:
            close = st
        else:
            close = prev_close * g * (1 + random.gauss(0, 0.012))
        if i == n - 1:
            close = (close + en) / 2.0
        op = prev_close * (1 + random.uniform(-0.008, 0.008)) if prev_close else close * (1 + random.uniform(-0.004, 0.004))
        hi = max(op, close) * (1 + abs(random.gauss(0, 0.006)))
        lo = min(op, close) * (1 - abs(random.gauss(0, 0.006)))
        vol = int(vol_base * 1e6 * (1 + random.gauss(0, 0.25)))
        stock_rows.append([cur.isoformat(), round(op, 3), round(hi, 3), round(lo, 3), round(close, 3), vol])
        prev_close = close
        cur = cur + timedelta(days=7)

stock_headers = ["date", "open", "high", "low", "close", "volume"]
stock_path = os.path.join(HERE, "stock_history.csv")
with open(stock_path, "w", newline="", encoding="utf-8-sig") as f:
    f.write("# AAPL Apple - teaching demo sample weekly price history (not live market data; not investment advice)\n")
    f.write("# Period: every Monday from 2025-09-15, %d weeks; OHLC in USD; volume in shares\n" % len(stock_rows))
    f.write("# Construction: 5 geometric trend segments + random noise, for technical analysis teaching only\n")
    w = csv.writer(f)
    w.writerow(stock_headers)
    w.writerows(stock_rows)
print("stock_history.csv written:", stock_path, "| weeks:", len(stock_rows))