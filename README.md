# 美股投研多 Agent 教学 Demo

> 基于 **JiuwenSwarm 多 Agent 平台**搭建的完整教学项目：六名 Agent 分工协作，完成一家上市公司的财报基本面分析、技术面分析、风险情绪分析，最终综合给出未来股价预测区间，并产出《投研报告》与《JiuWen 多 Agent 开发教学手册》。

> ⚠️ **免责声明**：本项目全部数据为**本地生成的教学样本数据**（非实时、非真实行情），所有分析结论与预测区间均为多 Agent 教学流程的算法输出，**仅供教学演示、不构成任何投资建议**。据此操作，风险自负。

---

## 一、项目简介

本项目演示了如何在 JiuwenSwarm 平台上设计并落地一个多 Agent 协作项目。以「美股投研」为业务场景，用户输入一家指定上市公司（本 demo 以 **AAPL 苹果**为教学样本标的），六名 Agent 按任务 DAG 分工协作：

1. **数据采集员**（data-researcher）：生成并校验本地样本数据集（财报 CSV + 历史股价 CSV）
2. **基本面分析师**（fundamental-analyst）：解读财务报告，输出基本面评分与估值判断
3. **技术分析师**（technical-analyst）：基于历史价格做趋势与动量分析，输出趋势评级与关键价位
4. **风险与情绪分析师**（risk-sentinel）：从舆情、政策、行业竞争等非财务维度评估风险
5. **预测综合员**（forecaster）：综合三路分析，输出目标价区间、概率评分卡与多情景推演
6. **报告主编**（report-synthesizer）：整合全部交付物，产出《投研报告》与《教学手册》

> 项目目标不是真实投资建议，而是**演示平台能力**：`build_team`、`spawn_teammate`、任务 DAG、成员自主认领、`send_message` 协作、`.team/` 文件交接、Leader 验收交付。全流程离线可复现、样本数据生成。

### 本 demo 核心结论（教学样本输出）

| 维度 | 结论 |
|---|---|
| 基本面 | 72/100 良好（质地优、估值贵） |
| 技术面 | 看多（中期上升通道，短线中性偏多） |
| 风险与情绪 | 中偏高（监管+供应链+估值高位） |
| 综合预测 | 目标区间 **215–310 美元**，核心区间 245–290，中枢约 **262 美元**（较现价约 -5%） |
| 三情景 | 乐观 ~300 / 基准 ~270 / 悲观 ~205 |

---

## 二、多 Agent 架构说明

### 2.1 团队成员分工

| 成员 | 角色 | 核心职责 |
|---|---|---|
| team-leader | 项目负责人（教学总控） | 组建团队、拆解任务 DAG、协调协作、验收交付、教学讲解 |
| data-researcher | 数据采集员 | 准备与清洗本地样本数据集（财报/股价 CSV） |
| fundamental-analyst | 基本面分析师 | 财务报告解读、基本面评分、估值判断 |
| technical-analyst | 技术分析师 | K 线形态、趋势、动量指标、支撑/阻力位 |
| risk-sentinel | 风险与情绪分析师 | 舆情、政策、行业竞争等非财务风险与情绪评估 |
| forecaster | 预测综合员 | 综合三路结论，输出目标价区间、评分卡、情景推演 |
| report-synthesizer | 报告主编 | 整合《投研报告》与《教学手册》 |

### 2.2 任务 DAG 与依赖

```
task-data（数据就绪，第一棒）
   ├── task-fundamental（基本面分析，依赖数据）
   ├── task-technical（技术面分析，依赖数据）
   └── task-risk（风险与情绪分析，依赖数据）
            │  （三路分析可并行）
            ▼
      task-forecast（综合预测，依赖三路分析完成）
            ▼
      task-report（整合报告+教学手册，最终交付）
```

### 2.3 平台能力映射

| 平台能力 | 本 demo 应用环节 |
|---|---|
| `build_team` / `spawn_teammate` | 组建六名 Agent 团队 |
| `create_task` 任务 DAG | 数据 → 三路并行分析 → 综合 → 报告 |
| 成员自主认领 | 各分析师认领各自分析任务 |
| `send_message` 协作 | 数据就绪广播、结论汇总、阻塞升级 |
| `.team/` 文件交接 | CSV 数据、分析 md、预测 md、报告在成员间流转 |
| Leader 验收交付 | 数据解锁确认、最终交付验收 |

---

## 三、快速开始

### 3.1 环境要求

- Python 3.8+（用于运行样本数据生成脚本）
- Git（用于版本管理）
- JiuwenSwarm 平台（用于复现多 Agent 协作流程）

### 3.2 复现数据生成

```bash
# 生成教学样本数据（财报 + 历史股价 CSV）
python scripts/generate_sample_data.py
```

生成结果输出到 `data/` 目录：
- `data/financials.csv`：AAPL 近 4 财年（FY2022–FY2025）财务摘要
- `data/stock_history.csv`：近 1 年周线 OHLCV（53 周）

### 3.3 查看分析产物

```bash
# 三路分析
cat analysis/fundamental.md   # 基本面分析
cat analysis/technical.md     # 技术面分析
cat analysis/risk.md          # 风险与情绪分析

# 综合预测
cat outputs/forecast.md       # 目标价区间与情景推演

# 最终交付物
cat deliverables/investment-research-report.md   # 投研报告
cat deliverables/jiuwen-multiagent-dev-manual.md # 教学手册
```

### 3.4 在 JiuwenSwarm 上复刻本项目

完整的分步复刻教程见《JiuWen 多 Agent 开发教学手册》（`deliverables/jiuwen-multiagent-dev-manual.md`），涵盖：目标拆解 → 角色设计 → DAG 设计 → 交接设计 → 协作设计 → 验收设计，以及「5 分钟上手」快速复刻清单。

---

## 四、目录说明

```
repo/
├── README.md                        # 项目简介、架构说明、快速开始、免责声明
├── LICENSE                          # MIT 开源协议
├── .gitignore                       # 排除临时文件、.DS_Store 等
├── data/                            # 样本数据
│   ├── financials.csv               # 财报摘要（FY2022–FY2025，14 字段）
│   └── stock_history.csv            # 周线 OHLCV（53 周）
├── analysis/                        # 三路分析
│   ├── fundamental.md               # 基本面分析
│   ├── technical.md                 # 技术面分析
│   └── risk.md                      # 风险与情绪分析
├── outputs/                         # 预测
│   └── forecast.md                  # 综合预测（目标价区间+情景推演）
├── deliverables/                    # 报告与手册
│   ├── investment-research-report.md    # 投研报告
│   └── jiuwen-multiagent-dev-manual.md  # JiuWen 多 Agent 开发教学手册
└── scripts/                         # 生成脚本
    └── generate_sample_data.py      # 样本数据生成脚本
```

---

## 五、免责声明

本项目及其全部内容（数据、分析、预测、报告、手册）均为**教学演示用途**：

- 所有财务与行情数据为**本地生成的构造样本**，非实时、非真实；
- 所有分析结论、评分、目标价区间与情景推演均为**多 Agent 教学流程的算法输出**，不反映任何真实投资判断；
- 本项目**不构成任何投资建议**，请勿据此进行真实交易决策。据此操作，风险自负。

---

## 六、License

本项目采用 [MIT License](LICENSE)，可自由使用、修改与分发（教学用途）。
