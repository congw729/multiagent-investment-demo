#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_quarterly_data.py —— AAPL 季度真实数据抓取脚本（SEC EDGAR XBRL）
教学演示：使用真实公开数据，不构成投资建议。
输出（写入脚本同目录）：quarterly_real.csv
  - FY2025 Q1-Q4 + FY2026 Q1-Q3 季度财务摘要（单季值）
关键逻辑（v2，Leader 打回修复版）：
  1. 财年归属：同一 end 日期在 XBRL 中会出现多组 fy/fp 记录（后续年度重报），
     必须按 end + fy + fp 三重匹配归属到正确财年季度
  2. 单季判定：duration <= 100 天（Q1 单季=YTD；Q2/Q3 需排除跨季累计记录如 dur=181/272）
  3. FY2025Q4：XBRL 无独立单季记录（仅 10-K 全年 dur=363），按全年减 Q1-Q3 实算
  4. filing_date：取该季度 fy/fp 匹配记录中最早 filed（原始披露日期，非后续重报日期）
可复现：Leader 可独立复跑本脚本验证（需联网访问 data.sec.gov）
"""
import csv
import json
import os
import urllib.request
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
SEC_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json"
UA_SEC = "JiuwenSwarm Teaching Demo research@example.com"

# 目标季度：end 日期 -> (季度标识, 财年, fp, 是否由全年实算)
QUARTERS = {
    # FY2025（对比用）
    "2024-12-28": ("FY2025Q1", 2025, "Q1", False),
    "2025-03-29": ("FY2025Q2", 2025, "Q2", False),
    "2025-06-28": ("FY2025Q3", 2025, "Q3", False),
    "2025-09-27": ("FY2025Q4", 2025, "Q4", True),   # 无独立单季，全年实算
    # FY2026
    "2025-12-27": ("FY2026Q1", 2026, "Q1", False),
    "2026-03-28": ("FY2026Q2", 2026, "Q2", False),
    "2026-06-27": ("FY2026Q3", 2026, "Q3", False),
}

TAGS = {
    "revenue": "RevenueFromContractWithCustomerExcludingAssessedTax",
    "net_income": "NetIncomeLoss",
    "gross_profit": "GrossProfit",
    "eps": "EarningsPerShareDiluted",
}

FY2025_ANNUAL = ("2025-09-27", 2025, "FY")   # FY2025 全年（10-K）


def http_get_json(url, ua):
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def single_quarter_records(usgaap, tag, end, fy, fp, unit=None):
    """按 end+fy+fp 匹配的单季记录（duration<=100天）"""
    if tag not in usgaap:
        return []
    units = usgaap[tag]["units"]
    u = unit or list(units.keys())[0]
    out = []
    for rec in units[u]:
        if rec.get("end") != end or rec.get("fy") != fy or rec.get("fp") != fp:
            continue
        if rec.get("form") not in ("10-Q", "10-K", "10-Q/A"):
            continue
        start = rec.get("start")
        if start:
            dur = (date.fromisoformat(end) - date.fromisoformat(start)).days
            if dur > 100:
                continue
        out.append(rec)
    return out


def quarterly_value(usgaap, tag, end, fy, fp, unit=None):
    """单季值：end+fy+fp 匹配记录中取最新 filed 的 val"""
    recs = single_quarter_records(usgaap, tag, end, fy, fp, unit)
    if not recs:
        return None
    recs.sort(key=lambda r: r["filed"])
    return recs[-1]["val"]


def quarterly_filing_date(usgaap, tag, end, fy, fp, unit=None):
    """该季度原始披露日期（fy/fp 匹配记录中最早 filed）"""
    recs = single_quarter_records(usgaap, tag, end, fy, fp, unit)
    if not recs:
        return None
    recs.sort(key=lambda r: r["filed"])
    return recs[0]["filed"]


def annual_value(usgaap, tag, end, fy, fp="FY", unit=None):
    """全年值：end+fy+fp=FY 匹配、form=10-K、filed 最新"""
    if tag not in usgaap:
        return None
    units = usgaap[tag]["units"]
    u = unit or list(units.keys())[0]
    recs = [r for r in units[u]
            if r.get("end") == end and r.get("fy") == fy and r.get("fp") == fp
            and r.get("form") in ("10-K", "10-K/A")]
    if not recs:
        return None
    recs.sort(key=lambda r: r["filed"])
    return recs[-1]["val"]


def main():
    sec = http_get_json(SEC_URL, UA_SEC)
    usgaap = sec["facts"]["us-gaap"]
    fetch_date = date.today().isoformat()

    rows = []
    for end, (qname, fy, fp, is_computed_q4) in QUARTERS.items():
        note = ""
        if not is_computed_q4:
            r = quarterly_value(usgaap, TAGS["revenue"], end, fy, fp)
            n = quarterly_value(usgaap, TAGS["net_income"], end, fy, fp)
            g = quarterly_value(usgaap, TAGS["gross_profit"], end, fy, fp)
            p = quarterly_value(usgaap, TAGS["eps"], end, fy, fp)
            filing = quarterly_filing_date(usgaap, TAGS["revenue"], end, fy, fp)
            if r is None:
                print("WARN: no revenue for", qname, end, "fy=%d fp=%s" % (fy, fp))
                continue
            gross_margin = g / r * 100 if r and g else None
            rows.append([qname, end, round(r / 1e6), round(n / 1e6) if n else None,
                         round(gross_margin, 2) if gross_margin else None, p, filing, ""])
        else:
            # FY2025Q4 = FY2025 全年(10-K) - FY2025 Q1-Q3 单季
            a_end, a_fy, a_fp = FY2025_ANNUAL
            annual_r = annual_value(usgaap, TAGS["revenue"], a_end, a_fy, a_fp)
            annual_n = annual_value(usgaap, TAGS["net_income"], a_end, a_fy, a_fp)
            annual_g = annual_value(usgaap, TAGS["gross_profit"], a_end, a_fy, a_fp)
            q1q3_rev = sum(quarterly_value(usgaap, TAGS["revenue"], e, 2025, q)
                           for e, q in (("2024-12-28", "Q1"), ("2025-03-29", "Q2"), ("2025-06-28", "Q3")))
            q1q3_ni = sum(quarterly_value(usgaap, TAGS["net_income"], e, 2025, q)
                          for e, q in (("2024-12-28", "Q1"), ("2025-03-29", "Q2"), ("2025-06-28", "Q3")))
            q1q3_gp = sum(quarterly_value(usgaap, TAGS["gross_profit"], e, 2025, q)
                          for e, q in (("2024-12-28", "Q1"), ("2025-03-29", "Q2"), ("2025-06-28", "Q3")))
            q4_rev = annual_r - q1q3_rev
            q4_ni = annual_n - q1q3_ni
            q4_gp = annual_g - q1q3_gp
            q4_gm = q4_gp / q4_rev * 100 if q4_rev else None
            filing = "2025-10-31"  # FY2025 10-K 原始提交日
            rows.append([qname, end, round(q4_rev / 1e6), round(q4_ni / 1e6),
                         round(q4_gm, 2) if q4_gm else None, None, filing,
                         "computed: FY2025 annual - Q1-Q3; EPS n/a (not separately disclosed)"])

    headers = ["fiscal_quarter", "quarter_end", "revenue_million_usd",
               "net_income_million_usd", "gross_margin_pct", "eps_usd",
               "filing_date", "note"]
    out_path = os.path.join(HERE, "quarterly_real.csv")
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        f.write("# ================================================================\n")
        f.write("# AAPL 苹果 真实季度财报数据（教学演示，不构成投资建议）\n")
        f.write("# Data Source & Provenance:\n")
        f.write("#   - 来源机构: SEC EDGAR (公司财报官方数据库 XBRL companyfacts)\n")
        f.write("#   - 具体文件: Apple Inc. 10-Q FY2025 Q1-Q3 / FY2026 Q1-Q3; 10-K FY2025\n")
        for r in rows:
            f.write("#     %s (end=%s) filing date=%s\n" % (r[0], r[1], r[6]))
        f.write("#   - 抓取日期: %s\n" % fetch_date)
        f.write("# 口径: XBRL 单季值(按 end+fy+fp 归属, duration<=100天; Q1单季=YTD);\n")
        f.write("#   FY2025Q4 无独立单季记录, 由 FY2025 全年(10-K) 减 Q1-Q3 实算;\n")
        f.write("#   原始单位美元, 已转换百万美元(÷1e6); gross_margin=GrossProfit/Revenue 实算;\n")
        f.write("#   eps 为摊薄每股收益(USD/shares); filing_date 取原始披露日期(最早 filed)\n")
        f.write("# ================================================================\n")
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)
    print("quarterly_real.csv written:", out_path, "| rows:", len(rows))

    # TTM 营收（截至 FY2026Q3）= FY2025Q4 + FY2026 Q1-Q3 单季
    rev_map = {r[0]: r[2] for r in rows}
    q25q4 = rev_map.get("FY2025Q4")
    q26 = [rev_map.get("FY2026Q%d" % i) for i in (1, 2, 3)]
    if q25q4 and all(q26):
        ttm = q25q4 + sum(q26)
        print("TTM revenue (FY2025Q4 + FY2026Q1-Q3): %d million USD" % ttm)


if __name__ == "__main__":
    main()