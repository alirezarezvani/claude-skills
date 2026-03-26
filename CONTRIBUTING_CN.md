# 贡献 Claude Skills 库

感谢您有兴趣为 Claude Skills 库做贡献！本仓库旨在通过可复用、生产就绪的技能包为 Claude AI 普及专业知识。

## ⚠️ 重要：始终针对 `dev` 分支

**所有 PR 必须针对 `dev` 分支。** 针对 `main` 的 PR 将被自动关闭。

```bash
# Fork 仓库后：
git checkout -b feat/my-new-skill origin/dev
# ... 进行修改 ...
# 创建 PR → 基础分支：dev（而非 main）
```

`main` 分支保留用于发布，由项目维护者管理。

## 🎯 贡献方式

### 1. 创建新技能

在您的领域添加专业知识：
- 营销、销售、客户成功
- 工程专业化
- 业务职能（财务、人力资源、运营）
- 行业特定技能（金融科技、教育科技等）

### 2. 增强现有技能

改进当前技能：
- 更好的框架和模板
- 额外的 Python 自动化工具
- 更新的最佳实践
- 更多参考资料
- 真实示例和案例研究

### 3. 改进文档

帮助他人有效使用技能：
- 更清晰的操作指南
- 更多使用示例
- 更好的 README 文件
- 翻译成其他语言

### 4. 修复 Bug

报告或修复以下问题：
- Python 脚本
- 文档错误
- 损坏的链接
- 过时的信息

---

## 🚀 入门指南

### 先决条件

- Python 3.7+（用于运行/测试脚本）
- Git 和 GitHub 账户
- Claude AI 或 Claude Code 账户（用于测试技能）
- 熟悉您要贡献的技能领域

### Fork 和 Clone

```bash
# 首先在 GitHub 上 Fork 仓库
git clone https://github.com/YOUR_USERNAME/claude-skills.git
cd claude-skills

# 添加上游远程仓库
git remote add upstream https://github.com/alirezarezvani/claude-skills.git
```

### 创建分支

```bash
# 创建功能分支
git checkout -b feature/my-new-skill

# 或用于改进
git checkout -b improvement/enhance-content-creator
```

---

## 📝 技能创建指南

### 遵循 Anthropic 官方规范

所有技能必须遵循 [Anthropic 的智能体技能规范](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview)。

### 必需结构

```
your-skill-name/
├── SKILL.md（必需）
│   ├── YAML 前置元数据（name、description、license、metadata）
│   └── Markdown 内容（指令、示例、工作流程）
├── scripts/（可选但推荐）
│   ├── tool1.py
│   ├── tool2.py
│   └── tool3.py
├── references/（可选但推荐）
│   ├── framework.md
│   ├── best-practices.md
│   └── examples.md
└── assets/（可选）
    └── templates/
```

### SKILL.md 要求

**YAML 前置元数据（必需）：**
```yaml
---
name: your-skill-name
description: 功能描述和使用场景。包含特定触发器和关键词。
license: MIT
metadata:
  version: 1.0.0
  author: Your Name
  category: domain-category
  updated: 2025-10-28
---
```

**Markdown 内容（必需）：**
- 清晰的标题和概述
- 用于发现的关键词部分
- 快速入门指南
- 核心工作流程
- 脚本文档（如适用）
- 参考指南（如适用）
- 最佳实践
- 示例

**目标长度：** SKILL.md 100-200 行
- 保持核心指令精简
- 将详细内容移至 references/
- 遵循渐进披露原则

### Python 脚本标准

**质量要求：**
- 生产就绪代码（非占位符）
- 优先使用标准库（最小依赖）
- CLI 优先设计，支持 --help
- JSON 输出选项用于自动化
- 清晰的文档字符串和注释
- 错误处理和验证

**示例：**
```python
#!/usr/bin/env python3
"""
工具名称 - 简要描述

用法：
    python tool.py input.txt [--output json]
"""

def main():
    # 实现
    pass

if __name__ == "__main__":
    main()
```

### 文档标准

- 清晰、可操作的指导
- 真实世界示例
- 具体指标和基准
- 不提供通用建议
- 专业语调
- 正确的格式

---

## 🔄 贡献流程

### 第 1 步：先讨论（推荐）

对于重大贡献：
1. 开启一个 issue 描述您的想法
2. 与维护者讨论方法
3. 在投入时间前获得反馈
4. 避免重复工作

### 第 2 步：开发您的贡献

按照上述指南：
- 新技能
- Python 工具
- 文档
- Bug 修复

### 第 3 步：彻底测试

**对于新技能：**
- [ ] YAML 前置元数据有效（无语法错误）
- [ ] 描述正确触发 Claude
- [ ] 所有 Python 脚本使用 --help 正常工作
- [ ] 所有参考链接有效
- [ ] 技能按预期激活
- [ ] 已使用 Claude AI 或 Claude Code 测试

**对于 Python 工具：**
- [ ] 无错误运行
- [ ] 处理边界情况
- [ ] 提供有帮助的错误消息
- [ ] JSON 输出正常工作（如适用）
- [ ] 依赖已文档化

### 第 4 步：提交 Pull Request

```bash
# 提交您的更改
git add .
git commit -m "feat(domain): add new-skill with [capabilities]"

# 推送到您的 fork
git push origin feature/my-new-skill

# 在 GitHub 上创建 pull request
```

**PR 标题格式：**
- `feat(domain): add new skill for [purpose]`
- `fix(skill-name): correct issue with [component]`
- `docs(domain): improve documentation for [topic]`
- `refactor(skill-name): optimize [component]`

**PR 描述必须包含：**
- What：这添加/更改/修复了什么？
- Why：这有什么价值？
- Testing：如何测试的？
- Documentation：更新了哪些文档？

---

## ✅ 质量标准

### 技能质量检查清单

所有新技能必须满足以下标准：

**文档：**
- [ ] 清晰的 SKILL.md，包含所有必需部分
- [ ] 增强的描述，包含触发器和关键词
- [ ] 用于发现的关键词部分
- [ ] 包含 2-3 个示例的快速入门指南
- [ ] 专业元数据（license、version、author）
- [ ] 领域特定 README 已更新（如适用）

**Python 工具（如包含）：**
- [ ] 生产就绪代码（非占位符）
- [ ] 支持 --help 的 CLI
- [ ] 正确的错误处理
- [ ] 清晰的文档字符串
- [ ] 依赖最小化并已文档化

**参考资料（如包含）：**
- [ ] 可操作的框架和模板
- [ ] 具体指导（非通用建议）
- [ ] 真实世界基准和示例
- [ ] 从 SKILL.md 正确链接

**测试：**
- [ ] 技能使用 Claude 正确激活
- [ ] 所有脚本无错误执行
- [ ] 所有链接有效
- [ ] 无损坏引用

**ROI：**
- [ ] 展示可衡量的价值
- [ ] 时间节省已量化
- [ ] 质量改进已明确
- [ ] 用例已文档化

---

## 🎨 风格指南

### Python 代码

**遵循 PEP 8：**
- 4 空格缩进
- 最大行长：100 字符
- 清晰的变量名
- 函数文档字符串

**示例：**
```python
def analyze_content(text: str, keywords: list) -> dict:
    """
    分析文本内容的关键词密度和可读性。

    参数：
        text: 要分析的内容
        keywords: 要检查的关键词列表

    返回：
        dict: 包含分数和建议的分析结果
    """
    pass
```

### Markdown 文档

- 一致使用标题（H1 用于标题，H2 用于章节）
- 包含语言规范的代码块
- 使用表格进行比较
- 适度使用表情符号建立视觉层次
- 保持段落简洁

### 提交消息

遵循 [Conventional Commits](https://www.conventionalcommits.org/)：

- `feat(domain): add new capability`
- `fix(skill): correct bug in script`
- `docs(readme): update installation guide`
- `refactor(skill): optimize SKILL.md length`
- `test(tool): add test coverage`

---

## 🏆 认可

### 贡献者

所有贡献者将：
- 在 CHANGELOG.md 中列出其贡献
- 在发布说明中提及
- 在 PR 合并消息中致谢
- 在社区中认可

### 重要贡献

重大贡献可能导致：
- 提交中的共同作者署名
- 文档中的功能归属
- README 中突出显示
- 社交媒体认可

---

## 📋 领域特定指南

### 营销技能

- 包含真实基准（CAC、转化率等）
- 平台特定指导（LinkedIn、Google 等）
- 明确说明 B2B 或 B2C 重点
- 国际市场考虑

### 工程技能

- 在元数据中包含技术栈
- 提供架构模式
- 添加代码质量标准
- 性能基准

### 产品技能

- 包含框架（RICE、OKR 等）
- 真实世界指标和 KPI
- 模板丰富且有示例
- 与工具的集成点

### 法规/质量技能

- 引用具体标准（ISO、FDA、EU MDR）
- 合规框架清晰
- 行业特定（健康科技、医疗科技）
- 监管管辖区明确

---

## 🚫 不接受的贡献

**我们将不接受：**
- 没有可操作框架的通用建议
- 占位符脚本（必须是生产就绪）
- 没有明确用例的技能
- 与现有技能功能重复
- 专有或机密信息
- 违反许可证的内容
- 推广不道德实践的技能

---

## 🤝 行为准则

通过参与本项目，您同意遵守我们的 [行为准则](CODE_OF_CONDUCT.md)。

预期行为：
- 尊重和包容
- 提供建设性反馈
- 关注社区最佳利益
- 表现同理心和善意

---

## 📞 问题？

- **一般问题：** 开启一个 [讨论](https://github.com/alirezarezvani/claude-skills/discussions)
- **Bug 报告：** 使用 [bug 报告模板](https://github.com/alirezarezvani/claude-skills/issues/new?template=bug_report.md)
- **功能想法：** 使用 [功能请求模板](https://github.com/alirezarezvani/claude-skills/issues/new?template=feature_request.md)
- **联系：** [alirezarezvani.com](https://alirezarezvani.com) 或 [medium.com/@alirezarezvani](https://medium.com/@alirezarezvani)

---

## 🙏 感谢您！

您的贡献帮助通过 Claude AI 使世界级专业知识对每个人都可访问。每添加一个技能、修复一个 bug 或改进文档都会产生影响。

**祝贡献愉快！** 🚀