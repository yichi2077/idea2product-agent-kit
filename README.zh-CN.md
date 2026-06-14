# idea2product-agent-kit

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)
![Agents](https://img.shields.io/badge/Agents-Claude%20Code%20%7C%20Codex%20%7C%20Cursor%20%7C%20OpenCode%20%7C%20Hermes%20%7C%20OpenClaw%20%7C%20Generic-purple.svg)
![Version](https://img.shields.io/badge/Version-v1.0.0-orange.svg)

**一套可移植的 AI 驱动工作流，带你从一个模糊的想法走到产品上线——9 个阶段、4 个人工决策门，全程有章可循。** 专为同时扮演策略、产品、工程三重角色的独立建造者设计，兼容你正在使用的任何编程智能体。

---

## 目录

- [流程总览](#流程总览)
- [安装指南](#安装指南)
- [快速上手](#快速上手)
- [阶段参考](#阶段参考)
- [决策门机制](#决策门机制)
- [实用工具技能](#实用工具技能)
- [项目架构](#项目架构)
- [常见问题](#常见问题)
- [参与贡献](#参与贡献)
- [开源协议](#开源协议)

---

## 流程总览

整条流水线由三个「先发散、再收敛」的漏斗组成。每个阶段先扩展信息与选项，再收束为一个决策或产出物：

```
 ══════════════════════════════════════════════════════════════════════
  idea2product-agent-kit v1.0.0 — 9 个阶段 · 4 道决策门
 ══════════════════════════════════════════════════════════════════════

  ┌──────────────────────────────────────────────────────────────────┐
  │                    漏斗一：想法 → 策略                            │
  │             市场 / 财务 / 风险证据 → 策略决策                      │
  ├──────────────────────────────────────────────────────────────────┤
  │                                                                  │
  │   ┌─────┐        ┌─────┐        ┌─────┐                         │
  │   │ P1  │───────▶│ P2  │───────▶│ P3  │                         │
  │   │想法 │        │策略 │        │策略 │                         │
  │   │简报 │        │调研 │        │决策 │                         │
  │   └─────┘        └─────┘        └─────┘                         │
  │                                  ▼                               │
  │                           ╔═══════════╗                          │
  │                           ║  决策门一  ║  ← 策略决策门            │
  │                           ║  策略审批  ║    人工确认              │
  │                           ╚═══════════╝                          │
  └──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │                    漏斗二：策略 → 产品                            │
  │                 选项空间 → 明确的产品定义                          │
  ├──────────────────────────────────────────────────────────────────┤
  │                                                                  │
  │   ┌─────┐        ┌─────┐        ┌─────┐                         │
  │   │ P4  │───────▶│ P5  │───────▶│ P6  │                         │
  │   │产品 │        │产品 │        │架构 │                         │
  │   │发现 │        │定义 │        │交接 │                         │
  │   └─────┘        └─────┘        └─────┘                         │
  │                                  ▼                               │
  │                           ╔═══════════╗                          │
  │                           ║  决策门二  ║  ← 产品决策门            │
  │                           ║  产品审批  ║    人工确认              │
  │                           ╚═══════════╝                          │
  └──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │                    漏斗三：产品 → 交付                            │
  │                 技术选型 → 上线的产品                              │
  ├──────────────────────────────────────────────────────────────────┤
  │                                                                  │
  │   ┌─────┐        ┌─────┐        ┌─────┐                         │
  │   │ P7  │───────▶│ P8  │───────▶│ P9  │                         │
  │   │功能 │        │构建 │        │成果 │                         │
  │   │规格 │        │发布 │        │复盘 │                         │
  │   └─────┘        └─────┘        └─────┘                         │
  │           ▼                   ▼        ▼                         │
  │    ╔═══════════╗       ╔═══════════╗                             │
  │    ║  决策门三  ║       ║  决策门四  ║  ← 发布决策门              │
  │    ║  架构审批  ║       ║  发布审批  ║    人工确认                │
  │    ╚═══════════╝       ╚═══════════╝                             │
  └──────────────────────────────────────────────────────────────────┘
```

---

## 安装指南

### 前置条件

- **Python 3.10+**（仅使用标准库，无需 pip 安装任何依赖）
- **Git**
- 一个编程智能体（从下方列表中选择一个或多个）

### 为你的智能体安装

```bash
# 克隆仓库
git clone https://github.com/yichi2077/idea2product-agent-kit.git
cd idea2product-agent-kit
```

> **提示：** macOS/Linux 使用 `python3`，Windows 使用 `python`。

#### Claude Code

```bash
python3 scripts/install.py skills --target claude-code
python3 scripts/install.py adapters /path/to/your-project --agent claude-code
```

将技能安装到 `~/.claude/skills`，并在项目根目录生成 `CLAUDE.md`。

#### Codex（OpenAI）

```bash
python3 scripts/install.py skills --target codex
python3 scripts/install.py adapters /path/to/your-project --agent codex
```

将技能安装到 `~/.agents/skills`。每个技能会生成对应的 `openai.yaml` 配置。项目根目录生成包含智能体指令的 `README.md`。

#### Cursor

```bash
python3 scripts/install.py adapters /path/to/your-project --agent cursor
```

生成 `README.md` + `.cursor/rules`，适配 Cursor 的规则系统。

#### OpenCode

```bash
python3 scripts/install.py adapters /path/to/your-project --agent opencode
```

在项目根目录生成 `AGENTS.md`。

#### Hermes

```bash
python3 scripts/install.py adapters /path/to/your-project --agent hermes
```

在项目根目录生成 `AGENTS.hermes.md`。如需同时将技能镜像到 `~/.hermes/skills/`：

```bash
python3 scripts/install.py adapters /path/to/your-project --agent hermes --install-user-skills
```

#### OpenClaw

```bash
python3 scripts/install.py adapters /path/to/your-project --agent openclaw
```

生成 `AGENTS.openclaw.md`、`SOUL.md`、`TOOLS.md`，并将技能复制到项目中。

#### 通用方案（任意智能体）

```bash
python3 scripts/install.py adapters /path/to/your-project --agent generic
```

生成通用的 `AGENTS.generic.md`，适用于任何支持 Markdown 指令文件的智能体。

### 脚手架：初始化新项目

```bash
python3 scripts/install.py scaffold /path/to/new-project
```

在目标仓库中创建完整的 `.pipeline/` 目录结构，包含状态文件、模板和配方。

---

## 快速上手

### 第一步 — 安装工具包

```bash
git clone https://github.com/yichi2077/idea2product-agent-kit.git
cd idea2product-agent-kit
python3 scripts/install.py skills --target claude-code    # 将技能安装到智能体
python3 scripts/install.py scaffold /path/to/my-project   # 在项目中创建 .pipeline/
python3 scripts/install.py adapters /path/to/my-project --agent claude-code  # 生成智能体指令
```

### 第二步 — 描述你的想法

在智能体中运行：

```
run p1
```

智能体会引导你创建 `docs/00-idea/idea-brief.md`——将你的原始想法填入结构化模板。

### 第三步 — 运行流水线

```
next
```

智能体会告诉你下一步该做什么。也可以直接指定阶段：

```
run p2
```

### 第四步 — 随时查看进度

```
status
```

显示当前阶段、已完成的阶段、待处理的决策门和需要验证的假设。

### 第五步 — 申请决策门审批

当到达需要决策门的阶段（P3、P6、P8）时，智能体会提示你。决策门审批必须在**真实操作系统终端**中进行（不能用智能体的内置终端）：

```bash
python scripts/pipeline_gate.py request strategy --confidence high --rationale "市场已验证，财务模型成立"
```

系统会给你一个随机挑战字符串，需要准确输入——这能防止误操作。

### 第六步 — 继续推进

```
run p4
run p5
...
run p9
```

每个阶段都有专属配方、模板和领域技能来引导你完成工作。

---

## 阶段参考

| 阶段 | 名称 | 做什么 | 关键产出 |
|------|------|--------|----------|
| **P1** | 想法简报 | 将你的原始想法结构化为一份简洁的简报 | `docs/00-idea/idea-brief.md` |
| **P2** | 策略调研 | 扫描现有方案，分析市场、财务和风险证据 | 市场扫描、财务模型、风险登记、假设登记 |
| **P3** | 策略决策 | 对比自建/购买/合作/放弃方案，结合红队推演 | 决策备忘录、产品纲领 |
| **P4** | 产品发现 | 定义目标用户、待办任务、机会图谱 | JTBD 画布、机会树、精益画布 |
| **P5** | 产品定义 | 撰写 PRD、验收标准、用户故事、边界场景 | PRD、验收标准、用户故事、边界场景文档 |
| **P6** | 架构交接 | 评估技术方案，形成架构决策记录 | ADR、设计推演、架构规格 |
| **P7** | 功能规格 | 以测试先行的方式定义 MVP 功能 | 功能规格、测试计划、TDD 规格 |
| **P8** | 构建发布 | 执行开发、代码审查、验证、发布准备 | 可运行代码、上线清单、GTM 计划 |
| **P9** | 成果复盘 | 将实际结果与假设对比，决定后续方向 | 成果复盘报告、转型/坚持决策 |

> **注意：** P2 和 P3 会被阻塞，直到 `docs/00-idea/idea-brief.md` 中存在真实的想法。P2 必须以现有方案扫描作为第一步。

---

## 决策门机制

决策门是**仅限人工操作的决策点**，防止你在关键时刻草率推进。智能体无法代替你审批决策门。

### 四道决策门

| 决策门 | 位于阶段之后 | 你在决定什么 |
|--------|------------|-------------|
| **策略决策门** | P3 | 这个想法值得做吗？应该自建、购买、合作还是放弃？ |
| **产品决策门** | P6 | 产品定义是否足够扎实，可以进入架构设计？ |
| **架构决策门** | P7 | 技术方案是否可行，可以开始编码？ |
| **发布决策门** | P8 | 产品是否准备就绪，可以交付给真实用户？ |

### 如何审批决策门

1. 打开一个**真实操作系统终端**（不是智能体的内置终端）
2. 执行审批命令：

```bash
python scripts/pipeline_gate.py request <决策门名称> --confidence high --rationale "你的判断依据"
```

3. 系统会显示一个**随机挑战字符串**——准确输入以确认
4. 添加一条**备注**说明你的决策理由
5. 决策门审批结果记录到 `.pipeline/state/pipeline-state.yaml`

### 信心指标

申请决策门时，需要指定你的信心水平：

- **high（高）** — 证据充分，不确定性低，可以全力推进
- **medium（中）** — 证据合理，但仍有部分问题待解
- **low（低）** — 存在重大未知因素（允许但会记录在案）

### 反确认偏误机制

P3 策略决策阶段要求对比**自建 / 购买 / 合作 / 放弃**四种选项。在你到达策略决策门之前，系统会通过跨模型红队推演（使用 `red-team-strategy.md`）对你的推理进行挑战。

---

## 实用工具技能

| 技能 | 命令 | 用途 |
|------|------|------|
| **状态查看** | `status` | 显示当前阶段、进度、待处理决策门和需要验证的假设 |
| **恢复续跑** | `resume` | 从保存的状态恢复中断的流水线 |
| **回退阶段** | `rollback` | 回退到之前的阶段（重新打开该阶段，保留历史记录） |
| **健康诊断** | `doctor` | 检查流水线健康状况——验证状态文件、产出物完整性、引用有效性 |
| **优雅退役** | `retire --reason "..."` | 带原因记录地优雅终止流水线 |
| **上下文交接** | `handoff` | 生成交接文档，用于将项目移交给另一个智能体或人员 |

### 其他实用命令

```bash
run p4              # 运行指定阶段
stage complete p4   # 手动标记某阶段为已完成
reopen p3 --reason "新发现的市场数据"  # 重新打开已完成的阶段
assumptions due     # 列出需要验证的假设
```

---

## 项目架构

### 目录结构

```
idea2product-agent-kit/
├── scripts/
│   ├── install.py             # 主安装器（技能、适配器、脚手架）
│   └── *.ps1                  # Windows 便捷脚本
│
├── skills/                    # 15 个流水线技能
│   ├── p0-guided-flow/        # 端到端引导式流程
│   ├── p0-status/             # 流水线状态
│   ├── p0-resume/             # 恢复中断的流水线
│   ├── p0-rollback/           # 回退阶段
│   ├── p0-doctor/             # 流水线健康诊断
│   ├── p0-retire/             # 优雅终止流水线
│   ├── p1-idea-brief/         # 阶段一：想法采集
│   ├── p2-strategy-research/  # 阶段二：市场/财务/风险调研
│   ├── p3-strategy-decision/  # 阶段三：策略决策（含红队推演）
│   ├── p4-product-discovery/  # 阶段四：用户/需求/机会图谱
│   ├── p5-product-definition/ # 阶段五：PRD 与规格
│   ├── p6-architecture-handoff/ # 阶段六：技术架构
│   ├── p7-feature-specification/ # 阶段七：功能规格
│   ├── p8-build-release/      # 阶段八：开发与上线
│   └── p9-outcome-review/     # 阶段九：成果度量
│
├── pipeline-template/         # 脚手架到目标仓库后变为 .pipeline/
│   ├── .pipeline/
│   │   ├── scripts/
│   │   │   ├── pipeline.py        # 流水线引擎——阶段执行与状态管理
│   │   │   ├── pipeline_gate.py   # 决策门审批——挑战/应答机制
│   │   │   ├── link_skills.py     # 将技能链接到智能体的技能目录
│   │   │   └── review_due.py      # 检查待审核项和假设到期情况
│   │   ├── state/                 # 流水线状态文件
│   │   ├── pipeline-state.yaml
│   │   ├── assumption-register.yaml
│   │   ├── risk-register.yaml
│   │   └── decision-log.md
│   ├── templates/             # 10 个文档模板
│   │   ├── idea-brief.md
│   │   ├── decision-memo.md
│   │   ├── hypothesis-tree.md
│   │   ├── issue-tree.md
│   │   ├── product-thesis.md
│   │   ├── red-team-strategy.md
│   │   ├── red-team-architecture.md
│   │   ├── strategy-research-note.md
│   │   ├── launch-gtm-checklist.md
│   │   └── outcome-review.md
│   ├── recipes/               # 9 个阶段配方（YAML）
│   │   ├── p1.yaml ... p9.yaml
│   └── vendor/                # 内置领域技能
│       ├── strategy/          # 市场调研、财务分析、CEO 顾问、
│       │                      # 商业投资顾问、产品发现
│       ├── product/           # 精益画布、JTBD、PRD、验收标准、
│       │                      # 边界场景、用户故事、上线清单、
│       │                      # 假设、实验设计、埋点规格、
│       │                      # 优先级排序、问题定义、机会树、
│       │                      # 设计推演、ADR、Spike 总结、
│       │                      # 访谈综合、PM 评审员
│       └── engineering/       # TDD、系统化调试、代码审查、
│                              # 完成分支、验证、执行计划
│
└── agent-adapters/            # 各智能体配置生成器
    ├── claude-code/           # → CLAUDE.md
    ├── codex/                 # → README.md + 每个技能的 openai.yaml
    ├── cursor/                # → README.md + .cursor/rules
    ├── opencode/              # → AGENTS.md
    ├── hermes/                # → AGENTS.md + 技能镜像
    ├── openclaw/              # → AGENTS.md + SOUL.md + TOOLS.md + 技能镜像
    └── generic/               # → AGENTS.md
```

### 工作原理

1. **配方**（`.pipeline/recipes/p*.yaml`）定义每个阶段——执行哪些步骤、使用哪些模板、调用哪些领域技能
2. **技能**（`skills/p*`）包含智能体指令（`SKILL.md`）和智能体专属配置（`agents/` 目录）
3. **领域技能**（`.pipeline/vendor/`）是流水线在运行过程中调用的专业技能——策略分析、产品文档、工程实践
4. **状态文件**（`.pipeline/state/`）跨会话追踪进度、假设、风险和决策
5. **适配器**为你的智能体生成对应的指令文件，让它知道如何运行流水线
6. **脚本**处理状态流转、决策门审批和维护任务

---

## 常见问题

### 我需要安装全部 15 个技能吗？

不需要。只安装你需要的阶段即可。流水线虽然是按序推进的，但每个阶段在前置条件满足后都可以独立运行。

### 我可以跳过某些阶段吗？

可以，但决策门会强制要求最低程度的完整性。例如，不通过 P3 的策略决策门，就无法进入 P4（产品发现）。

### 如果我想回到之前的阶段怎么办？

使用 `reopen p3 --reason "发现了新信息"` 或 `rollback`。之前的工作会保留在决策日志中——不会丢失任何内容。

### 没有网络能用吗？

可以。工具包仅依赖 Python 标准库和 Git。领域技能和模板全部是本地文件。智能体自身的 API 调用可能需要网络，但流水线基础设施完全离线可用。

### 同一个项目能用多个智能体吗？

可以。对不同的 `--agent` 参数运行 `python3 scripts/install.py adapters /path/to/your-project`。每个适配器生成自己的指令文件，不会覆盖其他适配器的内容。

### 如果智能体会话中途崩溃怎么办？

使用 `resume` 从断点继续。流水线状态在每个关键步骤后都会保存到 `.pipeline/state/`。你也可以运行 `doctor` 检查是否存在不一致。

### 为什么决策门审批必须在真实终端中进行？

决策门是不可逆的决策点。随机挑战字符串 + 备注的机制能防止误操作，确保你是在做一次深思熟虑的、有记录的选择——而不是在智能体的提示中随手点过。

### 我能自定义模板吗？

当然可以。`.pipeline/templates/` 中的模板都是普通 Markdown 文件。修改它们来适配你的工作流即可。配方通过名称引用模板，你的自定义内容会自动生效。

### 反确认偏误机制是怎么工作的？

P3（策略决策）阶段会强制智能体对比所有可行方案——自建、购买、合作和放弃——而不是先有结论再找理由。在你到达策略决策门之前，系统会通过跨模型红队推演（使用 `red-team-strategy.md`）对推理过程进行挑战。

---

## 参与贡献

欢迎参与贡献！以下是参与方式：

1. **Fork** 本仓库
2. **创建**功能分支（`git checkout -b feature/amazing-improvement`）
3. **提交**你的修改，附上清晰的提交信息
4. **推送**到你的分支并发起 **Pull Request**

### 贡献方向建议

- 新的智能体适配器（Windsurf、Aider 等）
- 额外的模板或领域技能
- README 和模板的翻译
- Bug 修复和文档改进
- 流水线配方优化

重大变更请先开 issue 讨论方案。

---

## 开源协议

本项目基于 **MIT 协议** 开源——详见 [LICENSE](LICENSE) 文件。

Copyright (c) 2026 [yichi2077](https://github.com/yichi2077)

---

<p align="center">
  为每一个独立建造者而生 ❤️
</p>
