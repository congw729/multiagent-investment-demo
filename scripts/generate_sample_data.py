#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JiuWenSwarm 教学 Demo —— 本地样本数据生成脚本（AAPL 苹果）
仅用于教学演示：数据量级贴近上市公司公开财报/行情常识，但为构造样本，
非实时行情，不构成投资建议。运行本脚本会在同目录生成：
  1) financials.csv      —— 近 4 个财年年度财务摘要
  2) stock_history.csv     —— 近 1 年周线 OHLCV（53 周）
"""
import csv
import os
import random
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
random.seed(20260820)

# ---------------------------------------------------------------------------
# 1) financials.csv —— 年度财务摘要（金额单位：百万美元；EPS 为美元/股）
#    口径：
#      - roe_pct = 净利润 / 期末股东权益
#      - debt_ratio_pct = 总负债 / 总资产
#      - current_ratio = 流动资产 / 流动负债
#      - pe_ratio = 财年末股价 / 当财年摊薄EPS；pb_ratio = 财年末股价 / 财年末每股净资产
#      - 各比率字段以百分数形式给出（如 43.31 表示 43.31%）
#      - FY2025 为样本估算值，其余年份量级贴近苹果公开财报
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
    f.write("# AAPL 苹果 教学演示样本财务数据（非实时行情，不构成投资建议）\n")
    f.write("# 金额单位: 百万美元; EPS: 美元/股; 比率: 百分数(43.31=43.31%)\n")
    f.write("# 口径: ROE=净利/期末权益; 负债率=总负债/总资产; 流动比率=流动资产/流动负债\n")
    f.write("# PE=财年末股价/当财年摊薄EPS; PB=财年末股价/每股净资产; FY2025 为样本估算\n")
    w = csv.writer(f)
    w.writerow(fin_headers)
    w.writerows(financial_rows)
print("financials.csv written:", fin_path)

# ---------------------------------------------------------------------------
# 2) stock_history.csv —— 近 1 年周线 OHLCV（样本窗口：2025-09-15 起，每周一，共 53 周）
# 价格分 5 段样本趋势：升→升→回调→企稳→再升；段内几何插值 + 周随机噪声
# volume 单位：股
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
    f.write("# AAPL 苹果 教学演示样本周线行情（非实时行情，不构成投资建议）\n")
    f.write("# 周期: 2025-09-15 起 每周一 共%d周; OHLC 美元; volume 股\n" % len(stock_rows))
    f.write("# 构造: 5 段几何趋势+随机噪声, 仅用于技术分析教学\n")
    w = csv.writer(f)
    w.writerow(stock_headers)
    w.writerows(stock_rows)
print("stock_history.csv written:", stock_path, "| weeks:", len(stock_rows))