# 《JiuWen 多 Agent 开发教学手册》

> 以「美股投研多 Agent 教学 Demo」为完整案例，教你从零设计并落地一个多 Agent 项目。
> 版本：v1.0 ｜ 配套团队：task-3e864b925b「美股投研多Agent教学Demo」
> 声明：本手册及其引用的全部数据、分析均为**教学样本**，仅用于演示 JiuwenSwarm 平台能力，**不构成任何投资建议**。

---

## 目录

1. [这本手册教什么](#1-这本手册教什么)
2. [第一步：项目目标拆解](#2-第一步项目目标拆解)
3. [第二步：设计团队与 Agent 角色](#3-第二步设计团队与agent角色)
4. [第三步：设计任务 DAG 与依赖](#4-第三步设计任务dag与依赖)
5. [第四步：设计数据与文件交接](#5-第四步设计数据与文件交接)
6. [第五步：设计成员协作机制](#6-第五步设计成员协作机制)
7. [第六步：设计 Leader 验收流程](#7-第六步设计leader验收流程)
8. [平台能力与 demo 环节映射表](#8-平台能力与demo环节映射表)
9. [5 分钟上手：照着复刻你的第一个多 Agent 项目](#9-5分钟上手照着复刻你的第一个多agent项目)
10. [附：本 demo 全程流程示意](#10-附本demo全程流程示意)

---

## 1. 这本手册教什么

很多同学见识过多 Agent 的 demo 后，最大的困惑是：**"看起来热闹，但换成我自己的需求，怎么下手？"**

本手册用「美股投研多 Agent 教学 Demo」这个真实跑通的完整项目做解剖样本，把多 Agent 项目的**设计六步法**讲透：

| 步骤 | 要回答的问题 | 对应章节 |
|---|---|---|
| 目标拆解 | 用户一个模糊需求，怎么变成可执行的任务树？ | §2 |
| 角色设计 | 每个 Agent 是谁、会什么、边界在哪？ | §3 |
| DAG 设计 | 任务之间谁先谁后、谁能并行？ | §4 |
| 交接设计 | 数据在 Agent 之间怎么安全流转？ | §5 |
| 协作设计 | 成员之间怎么沟通、怎么对齐？ | §6 |
| 验收设计 | 谁来检查产出、怎么算完成？ | §7 |

最后给出**平台能力 × demo 环节映射表**（§8）和 **5 分钟复刻步骤**（§9），让你照着就能做出自己的项目。

> 工程设计原则：**多 Agent 项目成败的关键，不在 Agent 数量，而在"分工边界清晰 + 任务依赖明确 + 交接物标准化"**。本 demo 每一步都贯彻这三条。

---

## 2. 第一步：项目目标拆解

### 2.1 从一句话需求到目标树

用户原话（原始需求）：

> 「帮我分析一家美股上市公司，给出未来股价预测，并产出一份投研报告。想学多 Agent 怎么开发。」

这句话包含三层信息，第一层拆解（**目标拆解，不是任务拆解**）：

| 需求关键词 | 隐含目标 | 推导出的子目标 |
|---|---|---|
| "分析一家公司" | 需要**数据**支撑 | 准备财报+股价样本数据 |
| "股价预测" | 需要**多维度分析输入** | 基本面 / 技术面 / 风险情绪三路分析 |
| "投研报告" | 需要**综合结论** | 预测综合 + 报告整合 |
| "想学多 Agent" | 需要**教学产出** | 过程可复现 + 教学手册 |

由此得到**目标树**：

```
项目目标：交付「美股投研分析结论 + 多Agent开发教学」
├── 数据层目标：标准化样本数据（离线可复现）
├── 分析层目标：三路并行分析（基本面/技术面/风险）
├── 综合层目标：目标价区间 + 情景推演 + 评分卡
└── 交付层目标：投研报告 + 教学手册（含免责声明）
```

### 2.2 从目标到任务（design 时写进 create_task 的输入）

每个子目标最终映射为一个**任务**，任务描述里写明：做什么、产出什么、验收标准。本 demo 的任务清单如下（可在任务看板 `view_task` 中核对）：

| 任务 ID | 子目标 | 产出物 | 依赖 |
|---|---|---|---|
| task-data | 数据就绪 | demo-data/ 下财报+股价 CSV | 无（第一棒） |
| task-fundamental | 基本面分析 | analysis/ 基本面分析 | task-data |
| task-technical | 技术面分析 | analysis/ 技术面分析 | task-data |
| task-risk | 风险与情绪 | analysis/ 风险情绪分析 | task-data |
| task-forecast | 综合预测 | outputs/ 目标价+情景+评分卡 | 三路分析 |
| task-report | 最终交付 | deliverables/ 两份终稿 | task-forecast |

> 设计心法：**目标 → 任务** 的映射要"一个目标对应一个可验证的产出物"。如果某目标没有明确的产出文件，说明拆解不到位。

---

## 3. 第二步：设计团队与 Agent 角色

### 3.1 团队骨架：Leader + 专职 Agent

多 Agent 项目需要一个 **Leader（总控）** 负责拆任务、协调、验收；其余成员按**领域独立**原则设置。

本 demo 团队构成（`build_team` / `spawn_teammate` 创建）：

```
                ┌─────────────────────────┐
                │   team-leader 项目负责人  │  总控+教学
                └────────────┬────────────┘
        ┌───────────┬────────┼────────┬───────────┐
        ▼           ▼        ▼        ▼           ▼
   data-researcher fundamental technical risk-sentinel  forecaster
   数据采集员      基本面分析师   技术分析师  风险与情绪分析师  预测综合员
        (第一棒)  (并行)      (并行)     (并行)          (汇合点)

                    report-synthesizer
                       报告主编（最终交付）
```

### 3.2 角色描述（desc）怎么写？——本 demo 角色描述模板

每个 Agent 通过 `spawn_teammate` 创建，**描述（desc / persona）决定这个 Agent 的定位、专长与边界**。写 desc 的黄金公式：

```
[你是谁] + [你的专长域] + [你负责什么输出] + [你明确不负责什么]
```

以本 demo 六角色为样例：

| 角色 | display_name | desc 要点（谁 + 专长 + 负责 + 不负责） |
|---|---|---|
| data-researcher | 数据采集员 | 数据工程师；专长结构化数据设计、CSV 生成校验、口径说明；负责产出标准化样本数据到 .team/demo-data/；**不负责**投资分析和预测 |
| fundamental-analyst | 基本面分析师 | 专注财报：营收增长、利润率、ROE、负债率、现金流、估值；输出基本面评分+亮点风险+估值判断；**不负责**K线/舆情/宏观 |
| technical-analyst | 技术分析师 | 量化技术分析：K线形态、均线、RSI/MACD、量能、支撑阻力；输出趋势评级+关键价位；**不负责**基本面/情绪 |
| risk-sentinel | 风险与情绪分析师 | 新闻舆情、政策监管、竞争、宏观等非财务风险；输出风险评级+情绪判断+情景压力；**不负责**财务报表计算 |
| forecaster | 预测综合员 | 综合三路分析结论，用 LLM 推理+简化估值模型，输出未来3-6月目标区间、概率评分卡、乐观/基准/悲观情景；**不负责**重新做三方专业分析 |
| report-synthesizer（我） | 报告主编 | 整合全部上游产物，产出《投研报告》+《教学手册》；负责免责声明与教学讲解；**不负责**重新算数据/重新预测 |

**边界为什么重要**：角色边界清晰，任务 DAG 才天然不冲突（§4）。desc 里写清"不负责什么"，可以防止 Agent 相互抢活、输出重复或矛盾。

### 3.3 角色设计的检查清单

- [ ] 每个角色是否有一句"我负责产出 X"？
- [ ] 每个角色是否有一句"我明确不负责 Y"？
- [ ] 角色之间是否存在重复的负责域？（若有，根据优先级裁剪）
- [ ] 有没有一个"综合/主编"角色负责最终合稿？（避免各说各话）

---

## 4. 第三步：设计任务 DAG 与依赖

### 4.1 用 `create_task` 表达依赖

JiuwenSwarm 中任务通过 `blocked_by`（前置依赖）自动组织成 DAG（有向无环图）。

**本 demo 的任务 DAG**：

```
                    ┌───────────────────────────────┐
                    ▼                               │
 task-data ──┬──► task-fundamental ──► ┐            │
      (1)    ├──► task-technical  ──► task-forecast ─► task-report (终)
             └──► task-risk       ──►           (汇合)
                    ▲  (2)(3)(4) 可并行              │(6)
                    └───────────────────────────────┘
```

依赖关系表（create_task 时的 `blocked_by` 字段）：

| 任务 | 前置依赖 | 说明 |
|---|---|---|
| task-data | — | 起点，第一棒 |
| task-fundamental / technical / risk | task-data | **三路并行**（阻塞在数据就绪） |
| task-forecast | 三路分析 | **汇合点**（三路都完成才解锁） |
| task-report | task-forecast | **终态**（预测完成才解锁） |

### 4.2 依赖设计的三个心法

1. **单向流动**：数据 → 分析 → 综合 → 交付，不要出现环（A等B、B等A）。
2. **并行解耦**：能并行的子任务（三路分析）不要串行，标注同一个前置即可并行。
3. **汇合点单一**：所有分析先汇入一个"综合"任务（forecast），再由它喂给终态（report），避免多对多混乱。

> 平台机制：被 `blocked_by` 的任务不可认领；前置完成后自动解锁可见。同学们在 `view_task` 里看到的 `[blocked by ...]` 就是 DAG 的实时呈现。

---

## 5. 第四步：设计数据与文件交接

### 5.1 交接规范（本项目约定）

| 目录 | 放什么 | 谁写 | 谁读 |
|---|---|---|---|
| `demo-data/` | 财报 CSV、股价 CSV | 数据采集员 | 三位分析师 |
| `analysis/` | 三路分析 md/评分 | 三位分析师 | 预测综合师 |
| `outputs/` | 目标价/情景/评分卡 | 预测综合师 | 报告主编 |
| `deliverables/` | 报告 + 教学手册 | 报告主编 | 用户/全队 |

> 交接契约铁律：目录与文件名**在 create_task 任务描述中写死**，下游只依赖固定路径；找不到文件即可定位 DAG 断点。所有路径前缀统一 `.team/`。

### 5.1b 本 demo 实际产物清单（对照真实文件复刻）

本项目实际运行后，`.team/` 下生成的交接文件（学员可直接对照）：

| 阶段 | 实际文件 | 生产者 | 消费者 |
|---|---|---|---|
| 数据 | `demo-data/financials.csv`（FY2022-FY2025 四财年 14 字段） | data-researcher | 三路分析师 |
| 数据 | `demo-data/stock_history.csv`（53 周周线 OHLCV） | data-researcher | 三路分析师 |
| 分析 | `analysis/fundamental.md`（基本面 72/100） | fundamental-analyst | forecaster |
| 分析 | `analysis/technical.md`（趋势看多，关键价位） | technical-analyst | forecaster |
| 分析 | `analysis/risk.md`（风险中偏高，情绪中性偏乐观） | risk-sentinel | forecaster |
| 预测 | `outputs/forecast.md`（目标价 215-310，中枢 262，三情景 300/270/205） | forecaster | report-synthesizer |
| 交付 | `deliverables/investment-research-report.md` | report-synthesizer | 用户/全队 |
| 交付 | `deliverables/jiuwen-multiagent-dev-manual.md` | report-synthesizer | 用户/全队 |

### 5.2 交接文件怎么设计（关键！）

文件交接是多 Agent 协作的"契约"。本 demo 约定：

- **文件名语义化**：本 demo 实际文件名为 `financials.csv`（财报）、`stock_history.csv`（周线）、`fundamental.md`（基本面分析）……
- **文件头带口径**：`fundamental.md` 写明数据来源、截止日、所用指标——下游不需要猜。
- **一个任务一个产出物**：下游只依赖固定路径，找不到就说明上游没做（可据此定位 DAG 断点）。

> 小贴士：多 Agent 项目最容易翻车的地方就是"交接格式隐式约定"。**无论文件还是消息，都把格式写进任务描述或文件首部**。

---

## 6. 第五步：设计成员协作机制

### 6.1 三种协作通道（`send_message`）

| 场景 | 用法 | 示例 |
|---|---|---|
| 任务指令/开工通知 | Leader 广播 | `to="*"` →「数据任务先启动，其余任务等待数据就绪」 |
| 成员间对齐 | 点对点 单播 | 分析师→数据员「确认下财报口径是季度还是年度」 |
| 完成汇报 | 点对点 | 成员→Leader：`to="team-leader"` |

### 6.2 协作协议（本项目约定）

- **开工信号**：Leader 广播任务清单，指派各自任务 ⇒ 成员 `view_task` 自查 → `claim_task(status=claimed)` 认领。
- **完成信号**：成员把产物写入 `.team/` 对应目录 → `claim_task(status=completed)` → 汇报 Leader（附产物路径）。
- **疑问通道**：数据口径等疑问直接 `send_message` 给相关成员；无法达成 → 升级 Leader。
- **不轮询**：依赖完成会自动解锁并通知，成员不需要反复刷 `view_task`。

### 6.3 协作成功的关键行为

- [ ] 依赖方主动同步"我已完成、产物在哪"
- [ ] 被依赖方收到疑问及时回
- [ ] 产物路径+摘要走消息通道，全文走 `.team/` 文件（消息传路径，不传正文）

---

## 7. 第六步：设计 Leader 验收流程

### 7.1 验收四件套（Leader 视角）

| 动作 | 工具 | 何时做 |
|---|---|---|
| 查看任务全景 | `view_task(action=list)` | 随时，识别瓶颈/断链 |
| 查看单个任务 | `view_task(action=get, task_id=...)` | 认领前 / 验收前 |
| 阅读产出文件 | read `.team/` 下文件 | 验收质量时 |
| 裁决通过与打回 | `verify_task(decision=pass/fail)` | 任务进入 in_review 后 |

### 7.2 本 demo 验收示例

- 数据任务：`view_task(get)` 核对 task-data → 读 CSV → 校验 5 列口径 → `pass`。
- 分析任务：读 `analysis/` 三份分析 → 核对其引用的批数据指标与数据文件吻嘴 → `pass`。
- 预测与报告：读 `deliverables/` 两份终稿 →「免责声明存在」「结构完整」→ `pass` → 交付。

> 验收红线：**产出物缺失、口径错误、无免责声明 = 打回**。

---

## 8. 平台能力与 demo 环节映射表

下表是**写给想学平台**的你：JiuwenSwarm 每个能力在本 demo 哪一环被用到。

| 平台能力 | 在本 demo 中对应环节 | 你可以在自己项目里怎么用 |
|---|---|---|
| `build_team` | 创建「美股投研多Agent教学Demo」团队 | 用 team display_name 定项目主题，开启 worktree/共享工作区 |
| `spawn_teammate` | 依次创建 6 个角色 Agent（每人带 desc 即"谁+专长+边界"） | 按目标树逐项创建角色，每个角色面对一个子目标 |
| `create_task` | 建 task-data → 3 个分析 → forecast → report，用 `blocked_by` 织 DAG | 把"子目标"变成任务，用依赖表达先后与并行 |
| `claim_task` | 成员自主认领（`status=claimed`），完成标记 `completed` | 让成员自行认领，体现协作而非派发 |
| `view_task` | 全员随时看板：`[pending/blocked/in_progress/...]` | 用任务状态排 DAG 调度、识别瓶颈 |
| `send_message` | 开工广播、成员对齐、完成汇报 | 广播(for-dir)/单播(点对点)，消息传路径不传正文 |
| `.team/` 文件共享 | 交接 CSV/分析/预测/报告；写入deliverables | 规范目录与文件名，实现数据交接 |
| `workspace_meta` lock/unlock | 多成员改同一文件前加锁（本 demo 终稿写入时用） | 防覆盖、保证共享文件一致 |
| `verify_task` | Leader 验收 pass/fail，打回返工 | 建立质量门禁，多 Agent 闭环 |

> 以上映射也是交付物的关键：学员若要验证平台能力，照着映射表逐项在 demo 里能找到现成用法。

---

## 9. 5 分钟上手：复刻你的第一个多 Agent 项目

> 目标：5 分钟内搭起一个「输入公司 → 数据 → 三路分析 → 综报」的最小闭环。

**Step 1（约 30 秒）：想清楚你要什么**
- 写出原始需求一句话 → 用 2.1 的目标拆解方法拆成 3~5 个子目标。

**Step 2（约 1 分钟）：建团队 + 建角色**
```text
build_team(display_name="我的多Agent项目")
spawn_teammate(name="data-1", desc="数据工程师：负责样本数据；不负责分析")
spawn_teammate(name="analyst-1", desc="分析师：负责分析；不负责数据")
spawn_teammate(name="synth-1", desc="综合员：负责汇总出报告")
```
> desc 模板：**谁 + 专长 + 负责输出 + 不负责什么**。

**Step 3（约 1 分钟）：建 DAG**
```text
create_task(task-data,    blocked_by=无)
create_task(task-analyst, blocked_by=task-data)
create_task(task-report,   blocked_by=task-analyst)
```
> 三行代码即表达"先数据 → 再分析 → 后报告"。

**Step 4（约 1 分钟）：定交接目录**
```text
.team/input/     ← 上游写
.team/output/    ← 下游读
```
> 每个任务描述中写明"产出写到哪个目录、文件名是什么"。

**Step 5（约 1.5 分钟）：通知开工 + 尾声验收**
```text
send_message(to="*", content="数据任务先启动，其他等待解锁")
# 等成员完成后：
view_task() → 检查 blocks 状态 → verify_task(pass)
```

**完成！** 你已拥有一个最小可运行、可复课的多 Agent 项目。之后只需按本手册 §3-§7 逐步加丰富的角色与 DAG。

---

## 10. 附：本 demo 全程流程示意

```text
 用户提交需求(单一公司)
        │
        ▼
 ┌─ build_team：美股投研多Agent教学Demo ─┐
 │ spawn_teammate ×6（数据/三分析师/预测/主编）│
 │ create_task ×6（data→三分析→forecast→report）│
 └────────────────────────────────────────┘
        │ 开工广播 send_message(to="*")
        ▼
 data-researcher 认领 task-data → 写 demo-data/*.csv → completed
        │（DAG:下游解锁）
        ▼
 ┌────────────────────────────────────────┐
 │ fundamental-analyst  → 基本面分析     │
 │ technical-analyst   → 技术面分析       │  ← 三路并行
 │ risk-sentinel       → 风险情绪分析     │
 └────────────────────────────────────────┘
        │ 三路都完成后 forecast 解锁
        ▼
 forecaster → 目标价区间 / 三情景 / 分数卡 → outputs/
        │
        ▼
 report-synthesizer（我）→ deliverables/投研报告 + 教学手册
        │
        ▼
 Leader 验收 (verify_task) → 交付用户（含免责声明）
```

---

*本手册为教学 demo 产物，案例数据与结论均为教学样本，不构成投资建议。*