# Humanize MBA Text - 去除 AI 写作痕迹

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python 3.7+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/Claude-Skill-orange.svg" alt="Claude Skill">
  <img src="https://img.shields.io/badge/Version-1.1-brightgreen.svg" alt="Version: 1.1">
  <img src="https://img.shields.io/badge/Kimi-CLI-blue.svg" alt="Kimi CLI">
  <img src="https://img.shields.io/badge/中文-🇨🇳-red.svg" alt="中文">
  <a href="README_EN.md"><img src="https://img.shields.io/badge/English-🇺🇸-inactive.svg" alt="English"></a>
  <a href="README_KR.md"><img src="https://img.shields.io/badge/한국어-🇰🇷-inactive.svg" alt="한국어"></a>
  <a href="README_JP.md"><img src="https://img.shields.io/badge/日本語-🇯🇵-inactive.svg" alt="日本語"></a>
</p>

<p align="center">
  <b>专门针对中国 MBA 毕业论文的 AI 写作痕迹检测与去除工具</b>
</p>

<p align="center">
  <code>#AI-Detection</code> <code>#Academic-Writing</code> <code>#MBA-Thesis</code> <code>#Claude-Skill</code> <code>#Text-Humanization</code> <code>#ChatGPT-Alternative</code> <code>#LLM-Writing</code> <code>#Research-Tools</code> <code>#Academic-Integrity</code> <code>#Chinese-NLP</code>
</p>

---

## 🎯 项目简介

这是一个专门为**中国 MBA 毕业论文**设计的 AI 写作痕迹检测与去除工具。基于 MBA 论文的学术规范和实践要求，通过多维度检测方法识别文本中的 AI 生成特征，并提供具体的修改建议，帮助你将 AI 生成的文本改写为自然、人类化的学术写作风格。

### ✨ 版本 1.1 新特性

- 📚 **重构章节文档**：将章节规则拆分为 5 个独立文件，更便于查找和使用
- 🎓 **细化 MBA 规范**：新增 MBA 论文核心原则和分章节写作指南
- 📝 **完善格式规范**：独立整理格式标准文档，覆盖中英文混排、图表、引用等
- 🎯 **强化实践导向**：更强调数据支撑、理论应用和具体案例分析

### 核心功能

- ✅ **多维度 AI 检测**：结合规则匹配、统计分析和语言特征三种检测方法
- ✅ **章节特定规则**：针对绪论、理论、分析、建议、结论 5 个章节的优化策略
- ✅ **MBA 论文规范**：符合中国高校 MBA 论文字数、结构、格式要求
- ✅ **自动修复**：自动处理中英文混排空格等简单问题
- ✅ **智能反馈**：生成详细的修改建议和前后对比示例
- ✅ **Claude Skill 集成**：可作为 Claude Code 的 Skill 直接使用

### 技术参考

本项目在优化策略设计上参考了 [thesis-optimizer](https://github.com/Haimbeau1o/thesis-optimizer) 项目的三维协同优化理念：
- 🔍 **降AI检测率**：句式多样化、语气自然化、逻辑人性化
- 📉 **降查重率**：深度语义改写、引用规范化、专业术语处理  
- ✨ **学术润色**：表达精准化、学术规范性、可读性优化

---

## 🎓 MBA 论文核心原则

本工具基于中国 MBA 论文的学术规范设计，遵循以下核心原则：

### 1. 实践导向
- 必须来源于企业管理实际，解决具体管理问题
- 避免纯理论空谈

### 2. 小题大做
- 选题聚焦明确，"小题深做"
- 核心概念不超过 2-3 个
- 避免选题过大、过于宽泛

### 3. 数据溯源
- 所有数据必须注明来源
- 确保准确性和可信度
- 删除"相关数据显示"等模糊表述

### 4. 理论支撑
- 运用 1-2 个相关理论作为分析框架
- 避免就事论事

### 5. 结构规范
- 正文字数 ≥ 3 万字
- 每章至少 4 节（含本章小结）
- 每节内容充实，避免一节不足一页

### 6. 学术诚信
- 复制率 < 15%
- 不编造数据，所有引用可核实

---

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/stephenlzc/humanize-mba-text-skill.git
cd humanize-mba-text-skill

# 安装依赖（如需使用 transformers 模型）
pip install transformers torch
```

### 基础使用

#### 1. 基础检测

```bash
# 使用基础规则检测
python scripts/detect_ai_patterns.py your_text.txt --format markdown --output report.md
```

#### 2. 多维度融合检测（推荐）

```bash
# 使用多维度检测
python scripts/multi_detector.py your_text.txt --format markdown --output report.md --plan plan.json
```

#### 3. 生成修改建议

```bash
# 基于检测结果生成反馈
python scripts/feedback_generator.py detection_result.json --text your_text.txt --output feedback.md
```

#### 4. 应用自动修复

```bash
# 自动修复空格等简单问题
python scripts/feedback_generator.py detection_result.json --text your_text.txt --apply
```

### 作为 Claude Skill 使用

1. 将本仓库克隆到 Claude Code 的 skills 目录：

```bash
cd ~/.config/opencode/skills
git clone https://github.com/stephenlzc/humanize-mba-text-skill.git
```

2. 在 Claude Code 中触发 Skill：

```
去 AI 痕迹：[粘贴你的文本]
```

或

```
帮我去除这段文字的 AI 写作痕迹
```

---

## 📊 检测维度

### 1. 规则匹配检测

识别以下 AI 写作特征：

- **AI 词汇**：赋能、抓手、闭环、痛点、赛道等
- **模糊归因**："有研究指出"、"专家认为"等
- **过度强调**："关键"、"核心"、"至关重要"等
- **宏观叙事**："时代"、"趋势"、"浪潮"等
- **表面分析**："凸显了"、"反映了"等 -ing 结尾分析
- **套话结尾**："综上所述"、"由此可见"等
- **连接词过多**："首先...其次...最后"等
- **中英文混排空格**："MBA 论文" → "MBA论文"

### 2. 统计分析检测

- **句子长度均匀度**：AI 文本通常句子长度更均匀
- **词汇多样性**：AI 文本词汇多样性较低
- **标点符号分布**：分析标点使用模式
- **段落结构**：检测段落长度分布

### 3. 语言特征检测

- **连接词密度**：统计逻辑连接词使用频率
- **正式表达模式**：识别过度正式的学术表达
- **句式复杂度**：分析复杂句式使用情况

---

## 🎓 分章节写作指南

本工具提供针对 MBA 论文 5 个核心章节的详细写作指南：

### 第1章 绪论

**常见问题**：
- ❌ 宏大叙事式开头："随着经济的发展..."
- ❌ 研究意义空泛："具有重要理论意义和实践价值"
- ❌ 文献综述罗列：A说、B说、C说
- ❌ 研究方法简单罗列

**改进策略**：
- ✅ 开门见山：直接点明研究企业、具体问题
- ✅ 意义具体：说明解决什么问题、带来什么价值
- ✅ 综述主题化：按主题组织，有批判性分析
- ✅ 方法具体：说明数据来源、样本、分析工具

📄 **详细指南**：[chapter-1-introduction.md](references/chapter-1-introduction.md)

### 第2章 理论基础

**常见问题**：
- ❌ 教科书式定义堆砌
- ❌ 理论罗列：介绍5-6个理论
- ❌ 理论与实践脱节

**改进策略**：
- ✅ 简洁界定：2-3 个核心概念
- ✅ 精选理论：1-2 个核心理论，说明选择理由
- ✅ 应用导向：理论为后续分析提供框架

📄 **详细指南**：[chapter-2-theory.md](references/chapter-2-theory.md)

### 第3章 现状与问题分析

**常见问题**：
- ❌ 企业概况资料堆砌，与研究关联度低
- ❌ 现状描述定性为主，缺乏数据
- ❌ 问题识别笼统："管理不善"、"效率低下"
- ❌ 成因分析表面化：停留在现象描述

**改进策略**：
- ✅ 聚焦相关：只提供与研究相关的背景
- ✅ 数据说话：用具体指标和时间序列数据
- ✅ 问题具体：每个问题都有衡量指标和调研数据
- ✅ 深入挖掘：用理论框架分析根本原因

📄 **详细指南**：[chapter-3-analysis.md](references/chapter-3-analysis.md)

### 第4章 对策建议

**常见问题**：
- ❌ 建议空泛："加强管理"、"优化流程"
- ❌ 缺乏可操作性
- ❌ 忽视约束条件
- ❌ 套用模板：SWOT 流于形式

**改进策略**：
- ✅ 具体可操作：明确做什么、怎么做、谁来做
- ✅ 分阶段实施：区分短期、中期、长期
- ✅ 考虑约束：分析资源、能力、文化限制
- ✅ 效果量化：预期效果尽可能量化

📄 **详细指南**：[chapter-4-solutions.md](references/chapter-4-solutions.md)

### 第5章 结论

**常见问题**：
- ❌ 重复摘要内容
- ❌ 简单罗列各章内容
- ❌ 创新点空泛："首次研究"、"填补空白"
- ❌ 回避研究局限

**改进策略**：
- ✅ 研究发现：突出核心发现，不与摘要重复
- ✅ 创新具体：客观说明理论、方法、应用创新
- ✅ 诚实局限：具体分析局限和影响
- ✅ 未来展望：提出具体可行的研究方向

📄 **详细指南**：[chapter-5-conclusion.md](references/chapter-5-conclusion.md)

---

## 📝 格式规范

独立的格式规范文档覆盖：

- 中英文/数字混排规范
- 图表编号与排版规范
- 引用与参考文献规范
- 数字与单位规范
- 标点符号规范
- 段落与层级规范

📄 **详细规范**：[format-standards.md](references/format-standards.md)

---

## 📈 检测结果解读

检测报告包含以下维度：

- **AI 生成概率**：0-100%，分数越高 AI 痕迹越明显
- **风险等级**：🔴 高风险 / 🟡 中风险 / 🟢 低风险
- **检测器一致性**：三种检测方法的结果一致性
- **优先修复项**：按严重程度排序的修改建议
- **章节特定建议**：根据检测到的章节类型提供针对性建议

### 修改策略

根据 AI 概率分数采取不同策略：

**🔴 高风险 (>70%)**：深度改写
- 全面重构段落结构
- 删除所有 AI 特征词汇
- 补充具体数据和案例
- 预计时间：2-3小时

**🟡 中风险 (40-70%)**：针对性优化
- 修复高优先级 AI 特征
- 调整套话和模板化表达
- 补充关键数据支撑
- 预计时间：1-2小时

**🟢 低风险 (<40%)**：细节润色
- 修复少量 AI 痕迹
- 优化语言表达
- 最终校对
- 预计时间：30分钟-1小时

---

## 💡 使用示例

### 示例 1：去除 AI 词汇

**原文**：
```
数字化转型已成为推动企业高质量发展的关键抓手，
通过赋能业务创新，为企业创造显著价值。
```

**改写后**：
```
本研究探讨数字化转型对企业绩效的影响。
通过分析XX公司2018-2023年的财务数据，
发现数字化投入与营业收入增长呈正相关关系。
```

### 示例 2：去除模糊归因

**原文**：
```
有研究指出，企业文化对组织绩效具有重要影响。
```

**改写后**：
```
Schein(2010)的研究表明，强势企业文化与组织绩效
存在正相关关系（r=0.42, p<0.05）。
```

### 示例 3：MBA 论文小题大做

**原文**：
```
企业数字化转型研究
```

**改写后**：
```
XX公司生产部门数字化转型中的流程优化研究
```

### 示例 4：数据溯源

**原文**：
```
企业营收增长20%，员工满意度为85%。
```

**改写后**：
```
根据XX公司2023年年报，企业营收同比增长20%。
根据2023年12月开展的问卷调查（N=120），员工满意度为85%。
```

### 示例 5：修复中英文混排空格

**原文**：
```
MBA 论文写作需要关注 AI 痕迹问题。
2023 年的研究表明，15 % 的企业存在此类问题。
```

**改写后**：
```
MBA论文写作需要关注AI痕迹问题。
2023年的研究表明，15%的企业存在此类问题。
```

---

## 📁 项目结构

```
humanize-mba-text-skill/
├── SKILL.md                          # Claude Skill 主文件
├── README.md                         # 本文件
├── LICENSE                           # MIT 许可证
│
├── references/                       # 参考文档
│   ├── ai-writing-patterns.md        # AI写作特征详细指南
│   ├── chapter-1-introduction.md     # 第1章：绪论写作指南
│   ├── chapter-2-theory.md           # 第2章：理论基础写作指南
│   ├── chapter-3-analysis.md         # 第3章：现状与问题分析写作指南
│   ├── chapter-4-solutions.md        # 第4章：对策建议写作指南
│   ├── chapter-5-conclusion.md       # 第5章：结论写作指南
│   ├── format-standards.md           # 格式规范
│   ├── strategy_ai_reduction.md      # 降AI检测率策略 ⭐新增
│   ├── strategy_plagiarism.md        # 降查重率策略 ⭐新增
│   └── strategy_polishing.md         # 学术润色策略 ⭐新增
│
└── scripts/                          # 检测脚本
    ├── detect_ai_patterns.py         # 基础规则检测
    ├── multi_detector.py             # 多方案融合检测器
    └── feedback_generator.py         # 反馈生成器
```

---

## 🔧 高级用法

### 交互式修改

```bash
python scripts/multi_detector.py your_text.txt --interactive
```

### 导出修改计划

```bash
python scripts/multi_detector.py your_text.txt --plan modification_plan.json
```

### 批量处理

```bash
# 处理多个文件
for file in *.txt; do
    python scripts/multi_detector.py "$file" --output "reports/${file%.txt}_report.md"
done
```

---

## ⚠️ 注意事项

1. **学术诚信**：改写时保持学术诚信，不编造数据；所有数据必须有真实来源
2. **数据核实**：对于不确定的引用和数据，建议用户核实原始资料
3. **理论适配**：建议用户根据具体研究问题选择合适的理论框架
4. **企业授权**：如涉及企业内部数据，建议获得企业书面授权或做脱敏处理
5. **查重控制**：改写后建议进行查重，确保复制率 < 15%
6. **个性化调整**：改写后的文本需用户根据具体学校和导师要求调整
7. **范围限制**：本工具专注于去除 AI 痕迹和格式规范，不涉及学术内容深度审查
8. **参考文献**：改写不自动生成参考文献，需用户根据实际引用补充完整

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 提交 Issue

- 描述清楚遇到的问题
- 提供示例文本（可脱敏）
- 说明期望的行为

### 提交 Pull Request

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

---

## 📝 更新日志

### v1.1.0 (2024-02-05)

- 📚 **重构章节文档**：将章节规则拆分为 5 个独立文件
  - chapter-1-introduction.md：绪论详细指南
  - chapter-2-theory.md：理论基础详细指南
  - chapter-3-analysis.md：现状与问题分析详细指南
  - chapter-4-solutions.md：对策建议详细指南
  - chapter-5-conclusion.md：结论详细指南
  - format-standards.md：格式规范独立文档
- 🎓 **细化 MBA 规范**：新增 MBA 论文核心原则章节
- 🎯 **强化实践导向**：更强调数据支撑、理论应用和具体案例
- 📝 **完善格式规范**：独立整理格式标准，覆盖中英文混排、图表、引用等
- 🏗️ **优化项目结构**：更清晰的文件组织和索引

### v1.0.0 (2024-02-04)

- ✨ 初始版本发布
- 🎯 支持多维度 AI 特征检测
- 📚 添加章节特定规则
- 🔧 实现自动修复功能
- 🎓 集成 Claude Skill

---

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE) - 详见 LICENSE 文件

---

## 🙏 致谢

- 感谢 Claude Code 提供的 Skill 框架
- 感谢 Kimi CLI 提供的 Agent 并行执行工具
- 感谢所有提供反馈和建议的用户
- **特别感谢 [Haimbeau1o/thesis-optimizer](https://github.com/Haimbeau1o/thesis-optimizer) 项目**，本项目的三维协同优化策略（降AI检测率、降查重率、学术润色提升）参考了该项目的优秀设计

---

## 📮 联系方式

- GitHub Issues: [https://github.com/stephenlzc/humanize-mba-text-skill/issues](https://github.com/stephenlzc/humanize-mba-text-skill/issues)
- 作者：stephenlzc

---

## 🔗 相关项目

- [thesis-optimizer](https://github.com/Haimbeau1o/thesis-optimizer) - 学术论文智能优化系统（计算机深度学习方向）

---

<p align="center">
  如果这个项目对你有帮助，请给个 ⭐ Star！
</p>
