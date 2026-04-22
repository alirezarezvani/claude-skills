---
name: "command-guide"
description: >
  Claude Code 命令选择指南 - 自动推荐和选择 Claude Code 中的命令、agents、skills。
  Use when: (1) 用户不确定该用哪个命令或工具, (2) 需要决策哪个 agent/skill 最适合当前任务,
  (3) 查询 /plan, /tdd, /compact, /loop 等命令的使用场景, (4) 了解何时调用 planner, code-reviewer,
  build-error-resolver 等 agents, (5) 需要命令速查表或决策流程图。
  Triggers: "该用什么命令", "哪个 agent", "命令选择", "怎么用 /plan", "/compact 什么时候用",
  "agent 选择指南", "命令速查表", "skill 推荐".
---

# Claude Code 命令选择指南

此 skill 帮助你在不同场景下选择最合适的命令、agent 或 skill。

## 快速决策流程图

```mermaid
graph TD
    A[用户请求] --> B{请求类型?}
    B -->|开发新功能| C[/plan]
    B -->|修复bug| D[/tdd 或 build-error-resolver]
    B -->|代码审查| E[/code-review 或 code-reviewer agent]
    B -->|测试| F[/e2e 或 tdd-guide agent]
    B -->|上下文过长| G[/compact]
    B -->|需要文档| H[/docs 或 docs-lookup agent]
    B -->|循环任务| I[/loop]
    B -->|安全审查| J[security-reviewer agent]
    
    C --> K[planner agent]
    D --> L{构建失败?}
    L -->|是| M[build-error-resolver]
    L -->|否| N[tdd-guide]
    E --> O[code-reviewer]
    F --> P[e2e-runner]
```

## 一、内置 Slash 命令

### 会话管理命令

| 命令 | 使用场景 | 示例 |
|------|----------|------|
| `/compact` | 上下文过长(>150K tokens)、响应变慢、切换任务阶段 | `/compact` 或自动触发 |
| `/clear` | 开始全新对话、清除历史 | `/clear` |
| `/loop` | 需要定期执行任务、自动循环工作 | `/loop 5m 检查构建状态` |
| `/help` | 查看帮助、了解命令 | `/help` |
| `/fast` | 需要更快响应（仅 Opus 4.6） | `/fast` |
| `/model` | 切换模型 | `/model sonnet` |

### 开发流程命令

| 命令 | 使用场景 | 激活时机 |
|------|----------|----------|
| `/plan` | 开始新功能、架构重构、复杂任务 | **进入 Plan Mode** |
| `/tdd` | 写测试、TDD 开发流程 | 需要测试指导时 |
| `/e2e` | E2E 测试、关键用户流程验证 | 需要浏览器测试时 |
| `/code-review` | 代码质量审查 | 写完代码后 |
| `/build-fix` | 构建失败、类型错误 | 构建出错时 |
| `/learn` | 从当前会话提取模式、学习 | 会话结束前 |
| `/skill-create` | 从 git 历史创建新 skill | 发现重复模式时 |

### 文档与查询命令

| 命令 | 使用场景 | 示例 |
|------|----------|------|
| `/docs` | 更新项目文档 | `/docs` |
| `/update-codemaps` | 更新代码地图 | `/update-codemaps` |
| `/remember` | 保存记忆到 memory 系统 | `/remember 用户偏好简洁输出` |
| `/tasks` | 查看任务列表 | `/tasks` |

---

## 二、Agents（子代理）选择

### 开发流程 Agents

| Agent | 触发条件 | 用途 |
|-------|----------|------|
| `planner` | 复杂功能请求、架构决策 | 创建实现计划 |
| `architect` | 系统设计、技术选型 | 架构分析和决策 |
| `tdd-guide` | 新功能、bug修复 | TDD 流程指导 |
| `code-reviewer` | **写完代码后立即调用** | 代码质量审查 |
| `security-reviewer` | 处理认证、API、敏感数据 | 安全漏洞检测 |

### 问题解决 Agents

| Agent | 触发条件 | 用途 |
|-------|----------|------|
| `build-error-resolver` | **构建失败时立即调用** | 修复构建/类型错误 |
| `e2e-runner` | 关键用户流程、PR 前 | E2E 测试执行 |
| `refactor-cleaner` | 代码维护、清理死代码 | 死代码检测和清理 |
| `doc-updater` | 更新文档、codemaps | 文档同步 |

### 研究与探索 Agents

| Agent | 触发条件 | 用途 |
|-------|----------|------|
| `Explore` | 代码库探索、查找文件 | 快速探索代码库 |
| `general-purpose` | 复杂多步骤任务 | 通用任务处理 |
| `docs-lookup` | 查询库/框架文档 | 获取最新 API 文档 |

---

## 三、Skills（技能）选择

### 流程 Skills

| Skill | 触发时机 | 用途 |
|-------|----------|------|
| `tdd-workflow` | 开发新功能/修复 bug | TDD 完整流程指导 |
| `verification-loop` | 功能完成后、PR 前 | 综合验证（build/test/lint/security） |
| `strategic-compact` | 长会话、上下文压力大 | 指导何时手动 `/compact` |

### 架构与模式 Skills

| Skill | 触发时机 | 用途 |
|-------|----------|------|
| `frontend-patterns` | 前端开发 | React/Next.js/Vue 最佳实践 |
| `backend-patterns` | 后端开发 | API/服务架构模式 |
| `api-design` | API 设计 | RESTful/API 设计规范 |
| `mcp-server-patterns` | MCP 服务器开发 | MCP 配置和模式 |

### 测试 Skills

| Skill | 触发时机 | 用途 |
|-------|----------|------|
| `e2e-testing` | E2E 测试需求 | Playwright 测试生成 |
| `security-review` | 安全审查需求 | OWASP Top 10 检测 |

### 研究 Skills

| Skill | 触发时机 | 用途 |
|-------|----------|------|
| `deep-research` | 需要深度研究 | 多轮搜索和研究 |
| `exa-search` | 需要 Web 搜索 | 网络内容搜索 |
| `documentation-lookup` | 查库文档 | Context7 文档查询 |

---

## 四、场景决策矩阵

### 按任务阶段选择

| 阶段 | 推荐工具组合 | 原因 |
|------|--------------|------|
| **需求分析** | `planner` + `Explore` | 先规划后探索 |
| **架构设计** | `architect` + `api-design` skill | 专业架构指导 |
| **开发前** | `tdd-guide` + `tdd-workflow` skill | 测试先行 |
| **开发中** | 直接编辑 + 快速迭代 | 保持流畅 |
| **开发后** | `code-reviewer` + `verification-loop` | 质量把关 |
| **测试阶段** | `e2e-runner` + `e2e-testing` skill | 完整测试覆盖 |
| **PR 前** | `security-reviewer` + `verification-loop` | 最终验证 |
| **构建失败** | `build-error-resolver` | 专注修复 |

### 按问题类型选择

| 问题 | 立即调用 | 说明 |
|------|----------|------|
| 构建失败 | `build-error-resolver` | 最小修改，快速修复 |
| 类型错误 | `build-error-resolver` | TypeScript 专项 |
| Bug 修复 | `tdd-guide` | 写测试再修复 |
| 安全漏洞 | `security-reviewer` | OWASP 检测 |
| 代码质量差 | `code-reviewer` | 立即审查 |
| 文档缺失 | `doc-updater` | 自动更新 |
| 死代码多 | `refactor-cleaner` | 安全清理 |

### 按开发类型选择

| 开发类型 | Skills 组合 |
|----------|-------------|
| 前端功能 | `frontend-patterns` + `tdd-workflow` |
| 后端 API | `backend-patterns` + `api-design` + `tdd-workflow` |
| MCP 服务器 | `mcp-server-patterns` + `tdd-workflow` |
| 数据库 | `database-reviewer` agent |
| 安全功能 | `security-reviewer` + `security-review` skill |

---

## 五、并行执行策略

### 可并行的场景

```markdown
✅ 推荐：同时启动多个独立任务

场景：代码完成后准备 PR
- Agent 1: code-reviewer（代码质量）
- Agent 2: security-reviewer（安全审查）
- Agent 3: e2e-runner（E2E 测试）

场景：大型重构分析
- Agent 1: architect（架构分析）
- Agent 2: Explore（代码探索）
- Agent 3: refactor-cleaner（死代码检测）
```

### 必须顺序执行的场景

```markdown
❌ 不能并行：存在依赖关系

场景：修复构建错误
- 顺序：build-error-resolver → 测试验证 → code-reviewer

场景：新功能开发
- 顺序：planner → tdd-guide（写测试）→ 实现 → code-reviewer
```

---

## 六、自动触发规则

### 无需用户请求自动调用

| 情况 | 自动动作 |
|------|----------|
| 写完/修改代码 | **立即调用** `code-reviewer` |
| 构建失败 | **立即调用** `build-error-resolver` |
| 复杂功能请求 | **立即调用** `planner` |
| 处理认证/敏感数据 | **立即调用** `security-reviewer` |
| 新功能/bug修复 | **立即调用** `tdd-guide` |
| 架构决策 | **立即调用** `architect` |

---

## 七、上下文管理时机

| 指标 | 触发 `/compact` |
|------|-----------------|
| Token > 150K | 立即压缩 |
| 响应变慢 | 建议压缩 |
| 切换任务阶段 | 在边界压缩 |
| 完成 major milestone | 压缩后继续 |
| 调试结束 → 新任务 | 清除调试痕迹 |

**最佳实践**：
- 研究后、实现前压缩（保留计划）
- 完成里程碑后压缩（清空中间状态）
- 不要在实现中途压缩（丢失变量/路径）

---

## 八、命令速查表

```
开发流程:
/plan        → 进入规划模式（复杂任务）
/tdd         → TDD 工作流
/e2e         → E2E 测试
/code-review → 代码审查
/build-fix   → 修复构建

会话管理:
/compact     → 压缩上下文
/clear       → 清除会话
/loop        → 循环任务
/fast        → 快速模式

文档与记忆:
/docs        → 更新文档
/remember    → 保存记忆
/tasks       → 查看任务

帮助:
/help        → 查看所有命令
```

---

## 九、使用示例

### 示例 1：新功能开发

```
用户：添加用户认证功能

流程：
1. /plan → planner agent 创建计划
2. tdd-guide → 写测试
3. 实现 → 编辑代码
4. code-reviewer → 代码审查
5. security-reviewer → 安全审查（认证敏感）
6. e2e-runner → E2E 测试
7. /compact → 完成 milestone 后压缩
```

### 示例 2：构建失败

```
用户：npm run build 失败

流程：
1. build-error-resolver → 分析错误、最小修复
2. 验证构建成功
3. code-reviewer → 检查修复质量
```

### 示例 3：代码重构

```
用户：重构认证模块

流程：
1. architect → 架构分析
2. planner → 实现计划
3. refactor-cleaner → 死代码检测
4. tdd-guide → 确保测试覆盖
5. 实现 → 重构代码
6. verification-loop → 全面验证
```

---

**核心原则**：
1. **先规划后实现** - complex tasks 用 `/plan`
2. **测试先行** - 新功能用 `tdd-guide`
3. **写完立即审查** - 代码完成用 `code-reviewer`
4. **构建失败立即修复** - 用 `build-error-resolver`
5. **敏感代码必审查** - 认证/API 用 `security-reviewer`
6. **PR 前全面验证** - 用 `verification-loop`