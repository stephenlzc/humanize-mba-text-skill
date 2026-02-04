# Humanize MBA Text - 去除 AI 写作痕迹

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python 3.7+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/Claude-Skill-orange.svg" alt="Claude Skill">
</p>

<p align="center">
  <b>专门针对中国 MBA 毕业论文的 AI 写作痕迹检测与去除工具</b>
</p>

## 🎯 项目简介

这是一个专门为**中国 MBA 毕业论文**设计的 AI 写作痕迹检测与去除工具。通过多维度检测方法，识别文本中的 AI 生成特征，并提供具体的修改建议，帮助你将 AI 生成的文本改写为自然、人类化的学术写作风格。

### 核心功能

- ✅ **多维度 AI 检测**：结合规则匹配、统计分析和语言特征三种检测方法
- ✅ **章节特定规则**：针对文献综述、案例分析、战略建议等不同章节的优化策略
- ✅ **自动修复**：自动处理中英文混排空格等简单问题
- ✅ **智能反馈**：生成详细的修改建议和前后对比示例
- ✅ **Claude Skill 集成**：可作为 Claude Code 的 Skill 直接使用

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

## 📊 检测维度

### 1. 规则匹配检测

识别以下 AI 写作特征：

- **AI 词汇**：赋能、抓手、闭环、痛点、赛道等
- **模糊归因**："有研究指出"、"专家认为"等
- **过度强调**："关键"、"核心"、"至关重要"等
- **表面分析**："凸显了"、"反映了"等 -ing 结尾分析
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

## 🎓 章节特定规则

### 文献综述

**常见问题**：
- ❌ 罗列式综述：简单罗列作者和观点
- ❌ 缺乏批判性：只陈述不评价
- ❌ 时间线堆砌：按时间顺序简单罗列

**改进策略**：
- ✅ 按主题组织而非按作者罗列
- ✅ 进行比较分析而非简单陈述
- ✅ 指出研究空白和本研究定位

### 案例分析

**常见问题**：
- ❌ 描述过多分析不足
- ❌ 结论先行
- ❌ 缺乏数据支撑
- ❌ 模板化结构

**改进策略**：
- ✅ 精简背景，聚焦研究问题
- ✅ 提供具体数据和时间节点
- ✅ 分析因果机制而非描述现象

### 战略建议

**常见问题**：
- ❌ 空泛建议
- ❌ 忽视约束条件
- ❌ 套用模板
- ❌ 缺乏优先级

**改进策略**：
- ✅ 建议具体可操作
- ✅ 考虑资源和能力约束
- ✅ 明确实施阶段和优先级

## 📈 检测结果解读

检测报告包含以下维度：

- **AI 生成概率**：0-100%，分数越高 AI 痕迹越明显
- **风险等级**：🔴 高风险 / 🟡 中风险 / 🟢 低风险
- **检测器一致性**：三种检测方法的结果一致性
- **优先修复项**：按严重程度排序的修改建议

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

### 示例 3：修复中英文混排空格

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

## 📁 项目结构

```
humanize-mba-text-skill/
├── SKILL.md                          # Claude Skill 主文件
├── README.md                         # 本文件
├── LICENSE                           # MIT 许可证
├── references/
│   ├── ai-writing-patterns.md        # AI写作特征详细指南
│   └── chapter-specific-rules.md     # 章节特定规则
└── scripts/
    ├── detect_ai_patterns.py         # 基础规则检测
    ├── multi_detector.py             # 多方案融合检测器
    └── feedback_generator.py         # 反馈生成器
```

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

## ⚠️ 注意事项

1. **学术诚信**：改写时保持学术诚信，不编造数据
2. **引用核实**：对于不确定的引用，建议用户核实
3. **人工审核**：改写后的文本仍需用户根据具体要求调整
4. **范围限制**：本工具专注于去除 AI 痕迹，不涉及学术内容审查

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

## 📝 更新日志

### v1.0.0 (2024-02-04)

- ✨ 初始版本发布
- 🎯 支持多维度 AI 特征检测
- 📚 添加章节特定规则
- 🔧 实现自动修复功能
- 🎓 集成 Claude Skill

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE) - 详见 LICENSE 文件

## 🙏 致谢

- 感谢 Claude Code 提供的 Skill 框架
- 感谢所有提供反馈和建议的用户

## 📮 联系方式

- GitHub Issues: [https://github.com/stephenlzc/humanize-mba-text-skill/issues](https://github.com/stephenlzc/humanize-mba-text-skill/issues)
- 作者：stephenlzc

---

<p align="center">
  如果这个项目对你有帮助，请给个 ⭐ Star！
</p>
