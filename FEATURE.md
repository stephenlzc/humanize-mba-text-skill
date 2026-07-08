# 历史版本特性

本文件归档 Humanize MBA Text 技能的历史版本更新日志。最新版本特性请查看对应语种的 README。

---

## 版本 1.4 新特性（high_risk_annotations）

- 🧭 **按句聚合的高风险标注**：报告新增 `high_risk_annotations[]` 键，每条标注 = 一句话 + 该句触发的所有规则；正则命中（带行号）和结构/链 issue（带 location）合并到同一句
- 🔁 **替换短语字典（TOML `phrase_replacements`）**：为 4 类高频规则提供"短语→学术词"映射：`ai_buzzwords`（赋能→促进/支持 等 11 条）/ `empty_solution_verbs`（加强…管理→…SOP 等 6 条）/ `vague_attribution`（有研究表明→具名作者 等 6 条）/ `unsupported_quantification`（提升X%→含 N=、时间、来源 等 6 条）
- 📐 **真实改写对（TOML `[[categories.examples]]`）**：复用既有 `[[categories.examples]]` 字段，在 `modify_plan` 与 `high_risk_annotations` 中暴露为 `before_after_example`，无需新增数据源
- 🆕 **`scripts/analyzers/high_risk_annotator.py`**：新增 350 行模块负责句子切分（带 char 偏移）+ 双轨桶聚合（regex 按行号 / issue 按 location + evidence 子串）+ 严重度排序

---

## 版本 1.3 新特性

- 🔬 **规则外置**：所有 AI 检测规则改用外部 TOML 文件维护，按 `structure / rhythm_quality / formatting / content / evidence / language / chapter-categories` 七大类拆分；分析与代码解耦，新增规则无需改动代码
- 📊 **散文结构分析器（5 个）**：句长 CV / 段长 CV / 段首末模板重复 / 段间结构均一化 / 章节章法模板重复；每个分析器输出 severity + confidence + location + evidence + suggestion 五个字段
- 🔗 **语义链分析器（10 个）**：三段式 / 作者罗列 / 方法堆叠 / 摘要模板 / 结论回声 / 笼统问题 / 无来源量化 / 宏观叙事 / 证据链完整度 / 问题-对策跨章节追踪；跨段、跨章节模型，捕捉段内看不到的成链模板
- 📋 **结构化改写计划**：报告新增 `modify_plan` 键，每个问题提供位置、改写骨架、推荐替换句式、目标字数区间；按 severity high → medium → low 排序，可直接对接 LLM 或人工改写
- 🎯 **三方统一接入**：`AIPatternDetector`、`StatisticalDetector`、`FeedbackGenerator` 共用同一份 TOML 规则，新增类别一处生效

---

## 版本 1.2 新特性

- 📚 **三维优化策略**：新增 AI 检测率降低 / 查重率降低 / 学术润色三份策略文档
- 🔍 **增强检测能力**：规则匹配、统计分析、语言特征三层全面调优
- 🎓 **细化 MBA 规范**：MBA 论文核心原则和分章节写作指南进一步细化
- 📝 **完善格式规范**：扩展格式标准文档的边界场景覆盖
- 🎯 **强化实践导向**：更强调数据支撑、理论应用和具体案例分析
- 🌐 **多语言 README**：补齐英文 / 日文 / 韩文版本

---

*English / 日本語 / 한국어 version history is kept in sync with this document.*
