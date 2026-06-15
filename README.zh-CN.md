# idea2product-agent-kit

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)
![Agents](https://img.shields.io/badge/Agents-Claude%20Code%20%7C%20Cursor%20%7C%20Codex%20%7C%20Generic-purple.svg)
![Version](https://img.shields.io/badge/Version-v1.1.0-orange.svg)

`idea2product-agent-kit` 是一个运行在本地的、状态驱动的流程管理器。它引导 AI 编码代理（Claude Code、Cursor、Codex 等）遵循结构化的软件工程生命周期进行开发。

通过在项目中运行一个轻量级的 Python 状态机（`pipeline.py`），它能防止 AI 代理过早、盲目地编写代码，强迫其在代码生成开始前，先在本地生成并完善调研报告、产品规格书（PRD）和技术架构设计（ADR）等 Markdown 文档。

---

## 目录

- [背景介绍](#背景介绍)
  - [痛点：代理漂移与盲目写代码](#痛点代理漂移与盲目写代码)
  - [“左移 (Shift-Left)” 核心哲学](#左移-shift-left-核心哲学)
  - [对“即兴编码者”的价值](#对即兴编码者的价值)
- [解决方案：阶段-审批门状态机](#解决方案阶段-审批门状态机)
- [核心对比与技术优势](#核心对比与技术优势)
- [适用边界与典型场景](#适用边界与典型场景)
  - [适用边界 (Scope)](#适用边界-scope)
  - [典型场景](#典型场景)
- [安装与快速上手](#安装与快速上手)
- [核心机制](#核心机制)
  - [人工审批门](#人工审批门)
  - [自动化 Git 提交](#自动化-git-提交)
  - [集成诊断](#集成诊断)
- [延伸文档与自定义](#延伸文档与自定义)
- [参与贡献](#参与贡献)
- [许可证](#许可证)

---

## 背景介绍

### 痛点：代理漂移与盲目写代码
在与 AI 编码代理协作时，缺乏规划是导致项目失败的主要原因：
1. 代理收到原始需求后，立刻开始生成大量代码。
2. 缺乏战略调研，导致重复造轮子或遗漏关键的业务与安全约束。
3. 缺乏明确的产品定义或架构设计，技术债在前期迅速累积。
4. 随着项目变大，代理的上下文窗口崩溃，陷入无休止的 Bug 修复与重构死循环，最终代码库彻底报废。

### “左移 (Shift-Left)” 核心哲学
绝大多数 Agent 辅助开发工具都极度聚焦于 **“怎么做 (How)”**（包括 TDD 测试编写、代码生成与验证）。而 `idea2product` 倡导的是 **“向左移动 (Shift-Left)”**，强迫用户和 Agent 在做任何工程实现决定之前，先标准化地厘清 **“为什么做 (Why)”** 与 **“做什么 (What)”**。

通过前置地定义商业战略与产品范围，你可以在早期直接过滤掉不可行或重复的想法，从源头上减少无效的开发工时。

```
     为什么做? (WHY)            做什么? (WHAT)             怎么做? (HOW)
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────────┐
│  P1 - P3        │────▶│  P4 - P6        │────▶│  P7 - P10           │
│  战略研究与        │     │  产品定义与         │     │  技术架构、           │
│  可行性决策       │     │  规格设计        │     │  特性 Specs 与构建  │
└─────────────────┘     └─────────────────┘     └─────────────────────┘
```

### 对“即兴编码者”的价值
如果你平时主要依赖直觉和大模型快速聊天来凑出代码（即 Vibe Coding），这套流程将是你的最佳稳定器：
*   **平抑需求蔓延**：通过 P4 机会树将用户核心需求具象化，通过 P2 财务和风险模型框定边界，防止功能无节制蔓延（Scope Creep）。
*   **沉淀 Agent 的“信息真理源 (Source of Truth)”**：大模型在开发阶段写错代码，90% 都是由于上下文缺乏对“真实业务意图”的定义所致。通过 P1-P5 阶段沉淀的本地 Markdown 文档（PRD、竞品扫描、风险登记册等）为 Agent 提供了最精准的规则库。当进入 P9 代码构建时，Agent 能够随时调阅本地的这些设计文件作为参考，从而在根本上减少逻辑漂移与 AI 幻觉。

---

## 解决方案：阶段-审批门状态机

`idea2product-agent-kit` 将开发工作流划分为 **10 个线性阶段** 和 **4 道人工审批门 (Gates)**。状态机引擎在关键设计和架构阶段会强制拦截，直到你手动予以批准，代理才能解锁下一阶段的写代码任务。

### 10 阶段工作流

| 阶段 | 阶段描述 | 主要产出 | 闸门拦截 |
|-------|---------|---------|----------|
| **P1** | 构思备忘 (Idea Brief) | `docs/00-idea/idea-brief.md` | - |
| **P2** | 战略调研 (Strategy Research) | 竞品扫描、市场分析、风险登记册 | - |
| **P3** | 战略决策 (Strategy Decision) | 自建/外购/合作备忘录、产品论文 | **战略之门 (Strategy Gate)** |
| **P4** | 产品发现 (Product Discovery) | JTBD 画布、机会树、精益画布 | - |
| **P5** | 产品定义 (Product Definition) | PRD、用户故事、验收标准 | **产品之门 (Product Gate)** |
| **P6** | 验证原型 (Validation Prototype) | 单一核心交互的最小原型 + ~5 位目标用户实测（可豁免） | - |
| **P7** | 架构交付 (Architecture Handoff)| 技术决策记录 (ADR)、技术 Spike、追溯矩阵 | **架构之门 (Architecture Gate)** |
| **P8** | 特性规约 (Feature Spec) | 测试驱动的特性规格包 (TDD Specs) | - |
| **P9** | 构建发布 (Build & Release) | 经验证的代码实现、发布清单 | **发布之门 (Release Gate)** |
| **P10** | 效果复盘 (Outcome Review) | 投产后假设验证与复盘 | - |

---

## 核心对比与技术优势

| 维度 / 方面 | `idea2product` 状态机流 | 裸用 Agent (如 Aider, Claude Code, Cursor) | 多智能体框架 (如 CrewAI, AutoGen) |
| :--- | :--- | :--- | :--- |
| **执行路径** | **确定性状态机**。强制先完成调研、设计文档再写代码。 | **即兴生成 (Ad-hoc)**。直接生成代码，缺乏规格约束。 | **自主循环**。容易发生代理漂移，代码质量难以预期。 |
| **上下文开销** | **极低**。代理的上下文仅聚焦于当前活跃的阶段与交付物。 | **极高**。混合了大量的历史修改记录，上下文容易崩溃。 | **非常高**。多个代理之间大量冗余对话，消耗巨大 Token 成本。 |
| **质量控制** | **人类介入审批门 (HITL Gate)**。硬拦截，直到人类签署审批意见。 | **代码生成后人工审查**。架构缺陷较难在早期捕获。 | **自我校验**。依靠 AI 审 AI，极易遗漏边缘情况。 |
| **隐私与成本** | **本地优先 (Zero SaaS)**。YAML 状态和 Markdown 报告完全存放在 Git 中。 | **本地优先**。 | **通常依赖云端**。长递归运行可能会产生高昂的 API 账单。 |

---

## 适用边界与典型场景

### 适用边界 (Scope)
*   **In-Scope (适用范围):**
    *   **0 到 1 新项目开发：** 从头搭建结构清晰、架构合理且假设经过验证的项目仓库。
    *   **大型特性迭代 (1 到 N)：** 隔离复杂的独立功能（如接入支付或 OAuth），在编写代码前先进行竞品扫描与规格设计。
    *   **技术探路与可行性研究：** 利用 P7 阶段运行独立的 Spike 代码探路。
*   **Out-of-Scope (不适用范围):**
    *   **紧急修复与微调 (Hotfixes)：** 仅仅修改一两行 CSS 或修复错别字，走完 9 阶段流水线开销过大。
    *   **超大型遗留单体系统：** 模块耦合度极高，难以强行套用线性的阶段-审批门模型。
    *   **全自动无人值守生成：** 本工具绝不追求无人看管的代码生成；它本质上是一个人机协作的受控流水线。

### 典型场景
*   **独立开发者与 Indie Hackers：** 约束自己不为了没有经过用户定位 (P4) 和单位经济学 (P2) 验证的伪需求编写代码。
*   **技术产品经理：** 自动在本地生成规范的 PRD、验收标准和架构 handoff，可直接导出并交付给人类开发团队。
*   **团队技术负责人 (TL)：** 在开发流程中强制落地 TDD（测试驱动开发）和设计优先 of AI 协作规范。

---

## 安装与快速上手

### 前置条件
- **Python 3.10+** (仅依赖标准库，无需 pip 安装)
- **Git**
- 兼容的代码代理（Claude Code、Cursor 等）

### 1. 安装
运行安装脚本来初始化项目中的 `.pipeline` 文件夹，并生成适配你所用代理的配置：

```bash
# 克隆仓库
git clone https://github.com/yichi2077/idea2product-agent-kit.git

# 在你的目标项目目录中初始化状态机架子
python3 idea2product-agent-kit/scripts/install.py scaffold /path/to/your-project

# 为你的代理安装指令适配器 (例如 Claude Code)
python3 idea2product-agent-kit/scripts/install.py adapters /path/to/your-project --agent claude-code
```

*若使用其他代理（如 Cursor, Codex, Hermes, OpenClaw, Generic），请参考 [技术操作手册 (英文)](docs/TECHNICAL-DEEP-DIVE.md#1-installation-details-per-agent)。*

### 2. 启动项目
在你的代码代理中，导航至项目目录并启动引导流程：

```bash
# 启动第一阶段
python3 .pipeline/scripts/pipeline.py run p1
```
*(或者，如果你已连接适配器指令，直接对你的代理打字说：`run p1` 或 `next` 即可。)*

---

## 核心机制

### 人工审批门 (Human-in-the-Loop Gates)
状态机通过拦截后续阶段来强制执行人工审批，审批记录保存在本地的 `.pipeline/state/pipeline-state.yaml` 中。
- **Light 模式 (默认)**：你可以直接在代理的聊天框里审阅它生成的 Markdown 文档，然后打字指示代理批准（例如：`"approve the strategy gate with rationale: economics validated"`），代理会在后台调用 `pipeline_gate.py` 进行登记。
- **Strict 模式**：防代理伪造。引擎要求你必须在独立的物理终端中输入随机生成的 Challenge Code 才能放行。可通过以下命令切换模式：
  ```bash
  python3 .pipeline/scripts/pipeline.py gate mode strict
  ```

### 自动化 Git 提交
为了保持干净的审计追踪，状态机在每个阶段顺利完成时，都会自动对修改过的文档和状态文件进行 Git Commit 提交，提交信息格式统一为：
`[pipeline] complete P2: Strategy Research`

### 集成诊断
运行健康检查命令，可自动检测状态文件一致性、缺失的交付物或尚未解决的假设登记：
```bash
python3 .pipeline/scripts/pipeline.py doctor
```

---

## 延伸文档与自定义

- **进阶操作**：如需定制 Adapter、升级现有项目状态机或接入 GitHub Spec Kit 运行 Spec 驱动的实现循环，请查阅 **[技术深潜与用户指南 (英文)](docs/TECHNICAL-DEEP-DIVE.md)**。
- **模板与步骤定制**：你可以随意定制 `.pipeline/recipes/p*.yaml` 中的 YAML 步骤，或者修改 `.pipeline/templates/` 下的 Markdown 交付物模版来符合你自己的团队规范。

---

## 参与贡献

我们非常欢迎社区的贡献，无论是优化状态机引擎、编写新的 Adapter，还是打磨流程模板。

1. **Fork** 仓库。
2. **创建** 特性分支 (`git checkout -b feature/amazing-feature`)。
3. **提交** 你的修改说明。
4. **推送** 分支并提交 **Pull Request**。

如果是较大的功能修改，建议先提一个 Issue 一起讨论。

---

## 许可证
本项目采用 [MIT 许可证](LICENSE) 开源。Copyright (c) 2026 [yichi2077](https://github.com/yichi2077).
