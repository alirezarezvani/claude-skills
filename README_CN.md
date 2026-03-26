# Claude Code 技能与插件 — 适用于所有编码工具的智能体技能

**205 个生产就绪的 Claude Code 技能、插件和智能体技能，支持 11 种 AI 编码工具。**

最全面的开源 Claude Code 技能与智能体插件库 —— 同时支持 OpenAI Codex、Gemini CLI、Cursor 等 7 种编码智能体。可复用的专业知识包，涵盖工程、DevOps、营销、合规、C 级顾问等领域。

**支持工具：** Claude Code · OpenAI Codex · Gemini CLI · OpenClaw · Cursor · Aider · Windsurf · Kilo Code · OpenCode · Augment · Antigravity

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Skills](https://img.shields.io/badge/Skills-205-brightgreen?style=for-the-badge)](#技能概览)
[![Agents](https://img.shields.io/badge/Agents-16-blue?style=for-the-badge)](#智能体)
[![Personas](https://img.shields.io/badge/Personas-3-purple?style=for-the-badge)](#角色)
[![Commands](https://img.shields.io/badge/Commands-19-orange?style=for-the-badge)](#命令)
[![Stars](https://img.shields.io/github/stars/alirezarezvani/claude-skills?style=for-the-badge)](https://github.com/alirezarezvani/claude-skills/stargazers)
[![SkillCheck Validated](https://img.shields.io/badge/SkillCheck-Validated-4c1?style=for-the-badge)](https://getskillcheck.com)

> **5,200+ GitHub Stars** — 最全面的 Claude Code 技能与智能体插件开源库。

---

## 什么是 Claude Code 技能与智能体插件？

Claude Code 技能（也称为智能体技能或编码智能体插件）是模块化的指令包，为 AI 编码智能体提供其原本不具备的领域专业知识。每个技能包含：

- **SKILL.md** — 结构化指令、工作流程和决策框架
- **Python 工具** — 268 个 CLI 脚本（全部仅使用标准库，零 pip 依赖）
- **参考文档** — 模板、检查清单和领域特定知识

**一个仓库，十一个平台。** 原生支持 Claude Code 插件、Codex 智能体技能、Gemini CLI 技能，并通过 `scripts/convert.sh` 转换为其他 8 种工具。所有 268 个 Python 工具可在任何 Python 环境中运行。

### 技能 vs 智能体 vs 角色

|  | 技能 | 智能体 | 角色 |
|---|---|---|---|
| **目的** | 如何执行任务 | 执行什么任务 | 谁在思考 |
| **范围** | 单一领域 | 单一领域 | 跨领域 |
| **语调** | 中性 | 专业 | 个性化 |
| **示例** | "按照这些步骤进行 SEO 优化" | "运行安全审计" | "像创业公司 CTO 一样思考" |

三者协同工作。参见 [编排](#编排) 了解如何组合使用。

---

## 快速安装

### Gemini CLI（新增）

```bash
# 克隆仓库
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills

# 运行安装脚本
./scripts/gemini-install.sh

# 开始使用技能
> activate_skill(name="senior-architect")
```

### Claude Code（推荐）

```bash
# 添加市场
/plugin marketplace add alirezarezvani/claude-skills

# 按领域安装
/plugin install engineering-skills@claude-code-skills          # 24 个核心工程技能
/plugin install engineering-advanced-skills@claude-code-skills  # 25 个 POWERFUL 级别
/plugin install product-skills@claude-code-skills               # 12 个产品技能
/plugin install marketing-skills@claude-code-skills             # 43 个营销技能
/plugin install ra-qm-skills@claude-code-skills                 # 12 个法规/质量
/plugin install pm-skills@claude-code-skills                    # 6 个项目管理
/plugin install c-level-skills@claude-code-skills               # 28 个 C 级顾问（完整 C 套件）
/plugin install business-growth-skills@claude-code-skills       # 4 个业务与增长
/plugin install finance-skills@claude-code-skills               # 2 个财务（分析师 + SaaS 指标）

# 或安装单个技能
/plugin install skill-security-auditor@claude-code-skills       # 安全扫描器
/plugin install playwright-pro@claude-code-skills                  # Playwright 测试工具包
/plugin install self-improving-agent@claude-code-skills         # 自动记忆整理
/plugin install content-creator@claude-code-skills              # 单个技能
```

### OpenAI Codex

```bash
npx agent-skills-cli add alirezarezvani/claude-skills --agent codex
# 或：git clone + ./scripts/codex-install.sh
```

### OpenClaw

```bash
bash <(curl -s https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/scripts/openclaw-install.sh)
```

### 手动安装

```bash
git clone https://github.com/alirezarezvani/claude-skills.git
# 将任意技能文件夹复制到 ~/.claude/skills/（Claude Code）或 ~/.codex/skills/（Codex）
```

---

## 多工具支持（新增）

**使用单一脚本将所有 156 个技能转换为 7 种 AI 编码工具：**

| 工具 | 格式 | 安装 |
|------|--------|---------|
| **Cursor** | `.mdc` 规则 | `./scripts/install.sh --tool cursor --target .` |
| **Aider** | `CONVENTIONS.md` | `./scripts/install.sh --tool aider --target .` |
| **Kilo Code** | `.kilocode/rules/` | `./scripts/install.sh --tool kilocode --target .` |
| **Windsurf** | `.windsurf/skills/` | `./scripts/install.sh --tool windsurf --target .` |
| **OpenCode** | `.opencode/skills/` | `./scripts/install.sh --tool opencode --target .` |
| **Augment** | `.augment/rules/` | `./scripts/install.sh --tool augment --target .` |
| **Antigravity** | `~/.gemini/antigravity/skills/` | `./scripts/install.sh --tool antigravity` |

**工作原理：**

```bash
# 1. 将所有技能转换为所有工具格式（约 15 秒）
./scripts/convert.sh --tool all

# 2. 安装到您的项目（带确认）
./scripts/install.sh --tool cursor --target /path/to/project

# 或使用 --force 跳过确认：
./scripts/install.sh --tool aider --target . --force

# 3. 验证
find .cursor/rules -name "*.mdc" | wc -l  # 应显示 156
```

**每个工具获得：**
- ✅ 所有 156 个技能转换为原生格式
- ✅ 每个工具的专属 README，包含安装/验证/更新步骤
- ✅ 支持脚本、参考资料、模板（如适用）
- ✅ 零手动转换工作

运行 `./scripts/convert.sh --tool all` 在本地生成工具特定输出。

---

## 技能概览

**205 个技能，涵盖 9 个领域：**

| 领域 | 技能数 | 亮点 | 详情 |
|--------|--------|------------|---------|
| **🔧 工程 — 核心** | 26 | 架构、前端、后端、全栈、QA、DevOps、SecOps、AI/ML、数据、Playwright、自改进智能体、Google Workspace CLI、a11y 审计 | [engineering-team/](engineering-team/) |
| **🎭 Playwright Pro** | 9+3 | 测试生成、不稳定测试修复、Cypress/Selenium 迁移、TestRail、BrowserStack、55 个模板 | [engineering-team/playwright-pro](engineering-team/playwright-pro/) |
| **🧠 自改进智能体** | 5+2 | 自动记忆整理、模式推广、技能提取、记忆健康 | [engineering-team/self-improving-agent](engineering-team/self-improving-agent/) |
| **⚡ 工程 — POWERFUL** | 30 | 智能体设计器、RAG 架构师、数据库设计器、CI/CD 构建器、安全审计器、MCP 构建器、AgentHub、Helm charts、Terraform | [engineering/](engineering/) |
| **🎯 产品** | 14 | 产品经理、敏捷 PO、策略师、UX 研究员、UI 设计、落地页、SaaS 脚手架、分析、实验设计、发现、路线图沟通、代码转 PRD | [product-team/](product-team/) |
| **📣 营销** | 43 | 7 个模块：内容（8）、SEO（5）、CRO（6）、渠道（6）、增长（4）、情报（4）、销售（2）+ 上下文基础 + 编排路由器。32 个 Python 工具。 | [marketing-skill/](marketing-skill/) |
| **📋 项目管理** | 6 | 高级 PM、Scrum Master、Jira、Confluence、Atlassian 管理、模板 | [project-management/](project-management/) |
| **🏥 法规与质量管理** | 12 | ISO 13485、MDR 2017/745、FDA、ISO 27001、GDPR、CAPA、风险管理 | [ra-qm-team/](ra-qm-team/) |
| **💼 C 级顾问** | 28 | 完整 C 套件（10 个角色）+ 编排 + 董事会会议 + 文化与协作 | [c-level-advisor/](c-level-advisor/) |
| **📈 业务与增长** | 4 | 客户成功、销售工程师、收入运营、合同与提案 | [business-growth/](business-growth/) |
| **💰 财务** | 2 | 财务分析师（DCF、预算、预测）、SaaS 指标教练（ARR、MRR、流失、LTV、CAC） | [finance/](finance/) |

---

## 角色

预配置的智能体身份，包含精心策划的技能加载、工作流程和独特的沟通风格。角色超越"使用这些技能"——它们定义了智能体如何思考、优先级排序和沟通。

| 角色 | 领域 | 最适合 |
|---------|--------|----------|
| [**创业公司 CTO**](agents/personas/startup-cto.md) | 工程 + 策略 | 架构决策、技术栈选择、团队建设、技术尽职调查 |
| [**增长营销师**](agents/personas/growth-marketer.md) | 营销 + 增长 | 内容驱动增长、发布策略、渠道优化、自力更生营销 |
| [**独立创始人**](agents/personas/solo-founder.md) | 跨领域 | 一人创业公司、副业项目、MVP 构建、身兼数职 |

**使用方法：**
```bash
# Claude Code
cp agents/personas/startup-cto.md ~/.claude/agents/

# 任意工具
./scripts/convert.sh --tool cursor  # 同时转换角色
```

详见 [agents/personas/](agents/personas/)。使用 [TEMPLATE.md](agents/personas/TEMPLATE.md) 创建您自己的角色。

---

## 编排

一种轻量级协议，用于协调跨越领域边界的角色、技能和智能体。无需框架。

**四种模式：**

| 模式 | 内容 | 场景 |
|---------|------|------|
| **单人冲刺** | 在项目阶段间切换角色 | 副业项目、MVP、独立创始人 |
| **领域深潜** | 一个角色 + 多个堆叠技能 | 架构评审、合规审计 |
| **多智能体交接** | 角色互相评审输出 | 高风险决策、发布准备 |
| **技能链** | 顺序技能，无需角色 | 内容流水线、可重复检查清单 |

**示例：6 周产品发布**
```
第 1-2 周：startup-cto + aws-solution-architect + senior-frontend → 构建
第 3-4 周：growth-marketer + launch-strategy + copywriting + seo-audit → 准备
第 5-6 周：solo-founder + email-sequence + analytics-tracking → 发布与迭代
```

完整协议和示例见 [orchestration/ORCHESTRATION.md](orchestration/ORCHESTRATION.md)。

---

## POWERFUL 级别

25 个高级技能，具有深度的生产级能力：

| 技能 | 功能 |
|-------|-------------|
| **agent-designer** | 多智能体编排、工具模式、性能评估 |
| **agent-workflow-designer** | 顺序、并行、路由、编排和评估模式 |
| **rag-architect** | RAG 管道构建器、分块优化器、检索评估器 |
| **database-designer** | 模式分析器、ERD 生成、索引优化、迁移生成 |
| **database-schema-designer** | 需求 → 迁移、类型、种子数据、RLS 策略 |
| **migration-architect** | 迁移规划、兼容性检查、回滚生成 |
| **skill-security-auditor** | 🔒 安全门 — 在安装前扫描技能中的恶意代码 |
| **ci-cd-pipeline-builder** | 分析技术栈 → 生成 GitHub Actions / GitLab CI 配置 |
| **mcp-server-builder** | 从 OpenAPI 规范构建 MCP 服务器 |
| **pr-review-expert** | 影响半径分析、安全扫描、覆盖率增量 |
| **api-design-reviewer** | REST API 检查器、破坏性变更检测、设计评分卡 |
| **api-test-suite-builder** | 扫描 API 路由 → 生成完整测试套件 |
| **dependency-auditor** | 多语言扫描器、许可证合规、升级规划 |
| **release-manager** | 变更日志生成、语义版本控制、准备检查 |
| **observability-designer** | SLO 设计器、告警优化、仪表板生成 |
| **performance-profiler** | Node/Python/Go 性能分析、包分析、负载测试 |
| **monorepo-navigator** | Turborepo/Nx/pnpm 工作区管理与影响分析 |
| **changelog-generator** | 常规提交 → 结构化变更日志 |
| **codebase-onboarding** | 从代码库分析自动生成入职文档 |
| **runbook-generator** | 代码库 → 运维手册与命令 |
| **git-worktree-manager** | 并行开发与端口隔离、环境同步 |
| **env-secrets-manager** | .env 管理、泄露检测、轮换工作流 |
| **incident-commander** | 事件响应手册、严重性分类、PIR 生成 |
| **tech-debt-tracker** | 代码库债务扫描、优先级排序、趋势仪表板 |
| **interview-system-designer** | 面试流程设计、题库、校准器 |

---

## 🔒 技能安全审计器

v2.0.0 新增 — 在安装前审计任何技能的安全风险：

```bash
python3 engineering/skill-security-auditor/scripts/skill_security_auditor.py /path/to/skill/
```

扫描：命令注入、代码执行、数据外泄、提示注入、依赖供应链风险、权限提升。返回 **PASS / WARN / FAIL** 及修复指导。

**零依赖。** 可在任何 Python 环境运行。

---

## 最近增强的技能

为以下技能添加了生产级升级：

- `engineering/git-worktree-manager` — worktree 生命周期 + 清理自动化脚本
- `engineering/mcp-server-builder` — OpenAPI -> MCP 脚手架 + 清单验证器
- `engineering/changelog-generator` — 发布说明生成器 + 常规提交检查器
- `engineering/ci-cd-pipeline-builder` — 技术栈检测器 + 管道生成器
- `marketing-skill/prompt-engineer-toolkit` — 提示 A/B 测试器 + 提示版本/差异管理器

每个现在都包含 `scripts/`、提取的 `references/` 和以使用为中心的 `README.md`。

---

## 使用示例

### 架构评审
```
使用 senior-architect 技能，审查我们的微服务架构
并识别前 3 个可扩展性风险。
```

### 内容创作
```
使用 content-creator 技能，撰写一篇关于 AI 增强
开发的博客文章。针对 "Claude Code 教程" 进行 SEO 优化。
```

### 合规审计
```
使用 mdr-745-specialist 技能，审查我们的技术文档
是否符合 MDR 附件 II 的合规差距。
```

---

## Python 分析工具

254 个 CLI 工具随技能提供（全部经过验证，仅使用标准库）：

```bash
# SaaS 健康检查
python3 finance/saas-metrics-coach/scripts/metrics_calculator.py --mrr 80000 --customers 200 --churned 3 --json

# 品牌声音分析
python3 marketing-skill/content-production/scripts/brand_voice_analyzer.py article.txt

# 技术债务评分
python3 c-level-advisor/cto-advisor/scripts/tech_debt_analyzer.py /path/to/codebase

# RICE 优先级
python3 product-team/product-manager-toolkit/scripts/rice_prioritizer.py features.csv

# 安全审计
python3 engineering/skill-security-auditor/scripts/skill_security_auditor.py /path/to/skill/

# 落地页（TSX + Tailwind）
python3 product-team/landing-page-generator/scripts/landing_page_scaffolder.py config.json --format tsx
```

---

## 相关项目

| 项目 | 描述 |
|---------|-------------|
| [**Claude Code Skills & Agents Factory**](https://github.com/alirezarezvani/claude-code-skills-agents-factory) | 大规模构建技能的方法论 |
| [**Claude Code Tresor**](https://github.com/alirezarezvani/claude-code-tresor) | 生产力工具包，包含 60+ 提示模板 |
| [Product Manager Skills](https://github.com/Digidai/product-manager-skills) | 高级 PM 智能体，包含 6 个知识领域、12 个模板、30+ 框架 — 发现、策略、交付、SaaS 指标、职业辅导、AI 产品工艺 |

---

## 常见问题

**如何安装 Claude Code 插件？**
使用 `/plugin marketplace add alirezarezvani/claude-skills` 添加市场，然后用 `/plugin install <name>@claude-code-skills` 安装任意技能包。

**这些技能是否适用于 OpenAI Codex / Cursor / Windsurf / Aider？**
是的。技能原生支持 11 种工具：Claude Code、OpenAI Codex、Gemini CLI、OpenClaw、Cursor、Aider、Windsurf、Kilo Code、OpenCode、Augment 和 Antigravity。运行 `./scripts/convert.sh --tool all` 为所有工具转换，然后用 `./scripts/install.sh --tool <name>` 安装。详见 [多工具集成](https://alirezarezvani.github.io/claude-skills/integrations/)。

**更新会破坏我的安装吗？**
不会。我们遵循语义版本控制，在补丁版本内保持向后兼容。现有的脚本参数、插件源路径和 SKILL.md 结构在补丁版本中不会改变。详见 [更新日志](CHANGELOG.md)。

**Python 工具是否无依赖？**
是的。所有 254 个 Python CLI 工具仅使用标准库 —— 零 pip 安装需求。每个脚本都经过 `--help` 验证。

**如何创建自己的 Claude Code 技能？**
每个技能是一个文件夹，包含 `SKILL.md`（前置元数据 + 指令）、可选的 `scripts/`、`references/` 和 `assets/`。详见 [Skills & Agents Factory](https://github.com/alirezarezvani/claude-code-skills-agents-factory) 获取分步指南。

---

## 贡献

我们欢迎贡献！详见 [CONTRIBUTING.md](CONTRIBUTING.md) 了解指南。

**快速想法：**
- 在服务不足的领域添加新技能
- 改进现有 Python 工具
- 为脚本添加测试覆盖
- 为非英语市场翻译技能

---

## 许可证

MIT — 详见 [LICENSE](LICENSE)。

---

## Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=alirezarezvani/claude-skills&type=Date)](https://star-history.com/#alirezarezvani/claude-skills&Date)

---

**由 [Alireza Rezvani](https://alirezarezvani.com) 构建** · [Medium](https://alirezarezvani.medium.com) · [Twitter](https://twitter.com/nginitycloud)