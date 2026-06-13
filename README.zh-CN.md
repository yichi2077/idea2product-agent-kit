# idea2product Agent Kit（中文说明）

> English version: [README.md](README.md)

一套可移植、由 Agent 驱动的工作流，帮一个人把一个**粗糙的想法**一路推进到
**真正落地的产品**——经过战略、产品定义、技术架构、交付，全程既保持严谨，又
不会陷入文档堆砌。

它面向同时身兼三职的个人开发者：**战略分析者**、**产品经理**、**工程师**。
这个 Kit 把这三个身份桥接起来，让同一个想法从"这事到底值不值得做"顺畅流向
"这是已合并、已测试的功能"，并在中间设下必须由人来拍板的决策点。

它以**技能（skills）**的形式运行在编码 Agent 中（当前支持 Claude Code 与
Codex，并为 Cursor、OpenCode、Hermes、OpenClaw 及任意 AGENTS.md 宿主提供适配）。

---

## 它解决什么问题

一个人单干时，最容易犯的错是爱上某个想法、急着写代码——跳过了本该砍掉或重塑
它的战略与产品思考。另一个极端则是产出无穷无尽、却永远变不成产品的分析文档。

这个 Kit 强制一种有纪律的**扩张 → 收缩**节奏，并让你在真正重要的决策处停下来：

```
想法 ──扩张──▶ 战略 ──决策──▶ 产品 ──定义──▶ 架构 ──构建──▶ 结果
        市场          KILL/HOLD/    PRD、         ADR、功能       发布并
        金融          EXPLORE/      发现、         地图、Spike     度量
        风险          COMMIT        验证
```

三次"扩张→收缩"漏斗：

1. **想法扩张**为市场 / 金融 / 风险证据，再**收缩**为一个战略决策。
2. **战略扩张**为产品选项，再**收缩**为一个明确定义的产品。
3. **产品扩张**为技术选项，再**收缩**为一套架构与交付方案。

---

## 核心概念

**9 个阶段（P1–P9）。** 想法捕获 → 战略分析 → 战略决策 → 产品发现 → 产品定义
→ 架构交接 → 功能规格 → 构建/发布 → 结果复盘。

**4 个门禁（Gate）。** `战略`、`产品`、`架构`、`发布`。门禁是硬性停顿，**只有人
能批准**。Agent 只能"请求"门禁并准备决策上下文，永远无法自行批准。

**3 种模式。** 按风险高低选择相应的流程强度：
- **Light** — 个人小工具、低风险原型（P1 → P7 → P8，门禁最少）。
- **Standard** — 真实产品 MVP（完整 P1–P9，四个门禁全开）。
- **High-Assurance** — 受监管 / 敏感 / 不可逆的工作（追加完整财务模型、安全与隐私
  审查、跨模型红队、供应链审计）。

**单一事实来源。** 战略决策由 Decision Memo 拥有，产品由 PRD 拥有，技术方向由
ADR 拥有，功能由 Spec Kit 规格拥有。幻灯片和 Issue 只是它们的**表达**，绝非
事实源。

**真实想法守卫。** 在 `docs/00-idea/idea-brief.md` 写入真实想法之前，P2 和 P3
始终被阻塞——自带的占位文件会被**故意拒绝**，这样你就无法把一个编造的想法盖章
通过战略门禁。

**反确认偏误的设计。** 战略决策必须对比 build / buy / partner / do-nothing，
Standard 及以上模式还会对推荐结论进行一次跨模型红队审查。

---

## 包里有什么

- **`skills/`** — 12 个可安装的入口技能：
  - `idea2product-p0-guided-flow` — 一站式编排器，读取状态并告诉你下一步该做什么。
  - `idea2product-p1-…` 到 `…-p9-outcome-review` — 每个阶段一个技能。
  - `idea2product-p0-status` / `idea2product-p0-resume` — 报告 / 继续。
- **`pipeline-template/`** — 会被脚手架进你项目的 `.pipeline` 引擎：确定性的
  Python CLI、9 个阶段配方（recipe）、状态登记册（假设、风险、决策）、已 vendor 的
  领域技能、以及面向用户的文档。
- **`agent-adapters/`** — Claude Code、Codex、Cursor、OpenCode、Hermes、OpenClaw
  及通用 AGENTS.md Agent 的宿主接线。
- **`scripts/`** — 安装、脚手架、适配器安装等辅助脚本。

流水线的领域专长来自**已 vendor、锁定固定 commit、记录许可证的技能**：战略类
（市场研究、财务分析、CEO 顾问等）、产品类（精益画布、JTBD、PRD、验收标准等）、
工程纪律类（TDD、系统化调试、代码审查）。

---

## 环境要求

- **Python 3.10+** — 唯一需要的东西。安装器和所有流水线命令（`status`、`run`、
  `gate`、`stage`、`mode`）都只用 Python 标准库。不需要 PowerShell、不需要 Node、
  日常使用也不需要 pip 装任何包。Windows / macOS / Linux 通用。
- **Git** — 用于历史记录，以及为门禁批准打 tag。

---

## 安装（一步搞定，任意系统）

安装器是 `scripts/install.py`，在所有平台上命令完全相同。

### Claude Code

```bash
python3 scripts/install.py skills --target claude-code
```

这会把 12 个技能复制到 `~/.claude/skills`，Claude Code 会按名称自动发现它们。
若没有立即出现，新开一个会话即可。

### Codex

```bash
python3 scripts/install.py skills --target codex
```

安装到 `~/.agents/skills`。用 `$技能名` 显式调用。

### 两者一起装

```bash
python3 scripts/install.py skills
```

> Windows 用户也可以用 `scripts/` 里的 `.ps1` 包装脚本（如
> `install_user_skills.ps1`）；它们只是转发到 `install.py`。

---

## 快速上手

1. 打开任意项目目录（空目录也行）。
2. 让 Agent 启动引导流程——例如 *"用 idea2product-p0-guided-flow 开始"*。
   首次使用时，只有在空目录（或仅有 `.git` 的空仓库）里才会自动创建 `.pipeline/`
   和 `docs/`（**不需要测试运行器**）。如果是非空仓库，请显式运行
   `python3 scripts/install.py scaffold /path/to/repo` 或 guided-flow 的 `init .`，
   避免把错误仓库弄脏。
3. 运行 **P1**，把你的真实想法写进 `docs/00-idea/idea-brief.md`。
   （在此之前 P2/P3 保持阻塞。）
4. 逐阶段推进。引导流程始终告诉你下一步该做什么：

```text
idea2product-p0-status     报告你当前在哪一步
idea2product-p0-resume     从已保存状态继续
idea2product-p1-idea-expansion … idea2product-p9-outcome-review
```

### 门禁由你来批

Agent 负责准备并"请求"门禁：

```powershell
python .pipeline/scripts/pipeline.py gate request strategy
```

macOS/Linux 直接运行流水线命令时请使用 `python3`：

```bash
python3 .pipeline/scripts/pipeline.py gate request strategy
```

批准或驳回必须由人在**普通系统终端**中完成（直接打开的 PowerShell/cmd/bash——
**不是** Agent 的集成终端，该命令会故意拒绝集成终端）：

```powershell
python .pipeline/scripts/pipeline_gate.py approve strategy
python .pipeline/scripts/pipeline_gate.py reject strategy
```

批准时需要输入门禁名称、请求时打印的随机 challenge，以及一条说明。批准成功会记录
批准者、时间和 commit，并创建一个带注释的 `i2p-gate-<门禁>-<时间戳>` git tag。
被驳回的门禁可以再次请求以重新打开。

---

## 其他宿主与项目级安装

把宿主适配装进目标仓库（对 Claude Code 还会在仓库内 `.claude/skills` 安装随项目
携带的技能）：

```bash
python3 scripts/install.py adapters /path/to/repo --agent claude-code
python3 scripts/install.py adapters /path/to/repo --agent cursor
python3 scripts/install.py adapters /path/to/repo --agent all
```

若想不经技能、直接在仓库里预先创建 `.pipeline` 引擎：

```bash
python3 scripts/install.py scaffold /path/to/repo
```
