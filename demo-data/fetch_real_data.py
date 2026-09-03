#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_real_data.py —— AAPL 真实数据抓取脚本（SEC EDGAR 财报 + Yahoo Finance 行情）
教学演示：使用真实公开数据，不构成投资建议。
输出（写入脚本同目录）：
  1) financials_real.csv      —— FY2022-FY2025 真实财报摘要（单位：百万美元）
  2) stock_history_real.csv   —— 近 1 年真实周线 OHLCV（2025-09-01 ~ 2026-09-03）
可复现：Leader 可独立复跑本脚本验证（需联网访问 data.sec.gov / query1.finance.yahoo.com）
"""
import csv
import json
import os
import urllib.request
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
SEC_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json"
YF_WEEKLY_URL = "https://query1.finance.yahoo.com/v8/finance/chart/AAPL?interval=1wk&range=1y"
YF_DAILY_URL = "https://query1.finance.yahoo.com/v8/finance/chart/AAPL?interval=1d&range=5y"
UA_SEC = "JiuwenSwarm Teaching Demo research@example.com"
UA_APP = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

FYS = {  # 财年 -> (财年末日期, 10-K filing date)
    "FY2022": ("2022-09-24", "2022-10-28"),
    "FY2023": ("2023-09-30", "2023-11-03"),
    "FY2024": ("2024-09-28", "2024-11-01"),
    "FY2025": ("2025-09-27", "2025-10-31"),
}


def http_get_json(url, ua):
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def latest_annual(usgaap, tag, fys, unit=None):
    """取某标签 FY 年度值：按 end 日期取最新 filed（去重）"""
    if tag not in usgaap:
        return {}
    units = usgaap[tag]["units"]
    u = unit or list(units.keys())[0]
    out = {}
    for rec in units[u]:
        end = rec.get("end")
        if end not in {v[0] for v in fys.values()}:
            continue
        if rec.get("form") not in ("10-K", "10-K/A"):
            continue
        if end not in out or rec["filed"] > out[end]["filed"]:
            out[end] = rec
    return out


def latest_shares_by_fy(dei, fys):
    """dei 命名空间股数：end 为 10-K 封面日期，需按 fy + fp=FY 匹配，取最新 filed"""
    tag = "EntityCommonStockSharesOutstanding"
    if tag not in dei:
        return {}
    out = {}
    for rec in dei[tag]["units"]["shares"]:
        fy = rec.get("fy")
        if fy not in (2022, 2023, 2024, 2025):
            continue
        if rec.get("fp") != "FY" or rec.get("form") not in ("10-K", "10-K/A"):
            continue
        if fy not in out or rec["filed"] > out[fy]["filed"]:
            out[fy] = rec
    return out


def main():
    sec = http_get_json(SEC_URL, UA_SEC)
    usgaap = sec["facts"]["us-gaap"]
    fetch_date = date.today().isoformat()

    # ---- SEC 财务事实提取（单位：美元原始值）----
    rev = latest_annual(usgaap, "RevenueFromContractWithCustomerExcludingAssessedTax", FYS)
    ni = latest_annual(usgaap, "NetIncomeLoss", FYS)
    gp = latest_annual(usgaap, "GrossProfit", FYS)
    eps = latest_annual(usgaap, "EarningsPerShareDiluted", FYS)
    ocf = latest_annual(usgaap, "NetCashProvidedByUsedInOperatingActivities", FYS)
    assets = latest_annual(usgaap, "Assets", FYS)
    liab = latest_annual(usgaap, "Liabilities", FYS)
    equity = latest_annual(usgaap, "StockholdersEquity", FYS)
    ca = latest_annual(usgaap, "AssetsCurrent", FYS)
    cl = latest_annual(usgaap, "LiabilitiesCurrent", FYS)
    # 流通股数在 dei 命名空间（EntityCommonStockSharesOutstanding），非 us-gaap
    dei = sec.get("facts", {}).get("dei", {})
    shares_by_fy = latest_shares_by_fy(dei, FYS)
    # 键：财年序号 -> 财年末日期
    shares = {FYS["FY%d" % fy][0]: rec for fy, rec in shares_by_fy.items()}

    # ---- Yahoo 行情 ----
    yf_w = http_get_json(YF_WEEKLY_URL, UA_APP)["chart"]["result"][0]
    yf_d = http_get_json(YF_DAILY_URL, UA_APP)["chart"]["result"][0]

    def fy_end_price(fy_end_iso):
        """财年末（含当日）之前最近交易日的收盘价"""
        from datetime import datetime, timezone
        target = date.fromisoformat(fy_end_iso)
        best, best_i = None, None
        for i, t in enumerate(yf_d["timestamp"]):
            d = datetime.fromtimestamp(t, tz=timezone.utc).date()
            if d <= target and (best is None or d > best):
                best, best_i = d, i
        return yf_d["indicators"]["quote"][0]["close"][best_i], best

    # ---- 汇总成行 ----
    fin_rows = []
    for fy, (end, filing) in FYS.items():
        e = end
        r = rev.get(e, {}).get("val")
        n = ni.get(e, {}).get("val")
        g = gp.get(e, {}).get("val")
        p = eps.get(e, {}).get("val")
        o = ocf.get(e, {}).get("val")
        a = assets.get(e, {}).get("val")
        l = liab.get(e, {}).get("val")
        q = equity.get(e, {}).get("val")
        ca_v = ca.get(e, {}).get("val")
        cl_v = cl.get(e, {}).get("val")
        sh = shares.get(e, {}).get("val")
        price, price_date = fy_end_price(end)

        gross_margin = g / r * 100 if r and g else None
        net_margin = n / r * 100 if r and n else None
        roe = n / q * 100 if q and n else None
        debt_ratio = l / a * 100 if a and l else None
        cur_ratio = ca_v / cl_v if ca_v and cl_v else None
        pe = price / p if p else None
        bvps = q / sh if q and sh else None
        pb = price / bvps if price and bvps else None

        fin_rows.append([
            fy, end,
            round(r / 1e6) if r else None,          # 营收 百万美元
            round(n / 1e6) if n else None,          # 净利 百万美元
            round(gross_margin, 2) if gross_margin else None,
            round(net_margin, 2) if net_margin else None,
            round(roe, 1) if roe else None,
            round(debt_ratio, 1) if debt_ratio else None,
            round(cur_ratio, 2) if cur_ratio else None,
            round(o / 1e6) if o else None,          # 经营现金流 百万美元
            p,                                       # 摊薄 EPS 美元
            round(price, 2),                         # 财年末收盘价 美元
            round(pe, 1) if pe else None,
            round(pb, 1) if pb else None,
        ])

    fin_headers = [
        "fiscal_year", "fiscal_year_end", "revenue_million_usd", "net_income_million_usd",
        "gross_margin_pct", "net_margin_pct", "roe_pct", "debt_ratio_pct", "current_ratio",
        "operating_cash_flow_million_usd", "eps_usd", "fiscal_year_end_price_usd",
        "pe_ratio", "pb_ratio",
    ]
    fin_path = os.path.join(HERE, "financials_real.csv")
    with open(fin_path, "w", newline="", encoding="utf-8-sig") as f:
        f.write("# ================================================================\n")
        f.write("# AAPL 苹果 真实财报数据（非实时行情，教学演示，不构成投资建议）\n")
        f.write("# Data Source & Provenance:\n")
        f.write("#   - 来源机构: SEC EDGAR (公司财报官方数据库 XBRL companyfacts)\n")
        f.write("#   - 具体文件: Apple Inc. 10-K FY2022-FY2025\n")
        f.write("#     filing dates: 2022-10-28 / 2023-11-03 / 2024-11-01 / 2025-10-31\n")
        f.write("#   - 抓取日期: %s\n" % fetch_date)
        f.write("# 口径: XBRL 年度值(10-K); 原始单位美元, 已转换百万美元(÷1e6);\n")
        f.write("#   gross_margin=GrossProfit/Revenue; roe=NetIncome/Equity;\n")
        f.write("#   debt_ratio=Liabilities/Assets; current_ratio=CurrentAssets/CurrentLiabilities;\n")
        f.write("#   pe=财年末收盘价(Yahoo)/摊薄EPS; pb=财年末收盘价/每股净资产(Equity/Shares)\n")
        f.write("# ================================================================\n")
        w = csv.writer(f)
        w.writerow(fin_headers)
        w.writerows(fin_rows)
    print("financials_real.csv written:", fin_path)

    # ---- 周线行情 ----
    stock_rows = []
    for i, t in enumerate(yf_w["timestamp"]):
        from datetime import datetime, timezone
        d = datetime.fromtimestamp(t, tz=timezone.utc).date().isoformat()
        q = yf_w["indicators"]["quote"][0]
        stock_rows.append([
            d,
            round(q["open"][i], 3), round(q["high"][i], 3),
            round(q["low"][i], 3), round(q["close"][i], 3),
            int(q["volume"][i]),
        ])
    stock_headers = ["date", "open", "high", "low", "close", "volume"]
    stock_path = os.path.join(HERE, "stock_history_real.csv")
    with open(stock_path, "w", newline="", encoding="utf-8-sig") as f:
        f.write("# ================================================================\n")
        f.write("# AAPL 苹果 真实周线行情（教学演示，不构成投资建议）\n")
        f.write("# Data Source & Provenance:\n")
        f.write("#   - 来源机构: Yahoo Finance (chart API, interval=1wk, range=1y)\n")
        f.write("#   - 抓取日期: %s\n" % fetch_date)
        f.write("# 口径: OHLC 单位美元; volume 单位股; 每周一根 bar\n")
        f.write("# ================================================================\n")
        w = csv.writer(f)
        w.writerow(stock_headers)
        w.writerows(stock_rows)
    print("stock_history_real.csv written:", stock_path, "| weeks:", len(stock_rows))


if __name__ == "__main__":
    main()