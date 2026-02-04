#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 检测反馈与修改建议生成器
将检测结果转换为具体的修改操作指南

使用方法:
    python feedback_generator.py detection_result.json --apply
    python feedback_generator.py detection_result.json --export modifications.json
"""

import json
import re
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class ModificationRule:
    """修改规则"""

    issue_type: str
    pattern: str
    replacement: str
    description: str
    priority: str


class FeedbackGenerator:
    """反馈生成器"""

    def __init__(self):
        self.modification_rules = self._load_modification_rules()
        self.chapter_templates = self._load_chapter_templates()

    def _load_modification_rules(self) -> Dict[str, ModificationRule]:
        """加载修改规则库"""
        return {
            "exaggerated_emphasis": ModificationRule(
                issue_type="过度强调",
                pattern=r"(关键|重要|核心|至关重要)[的是|在于|作用|意义]?",
                replacement="",
                description="删除价值判断词汇，改为客观陈述",
                priority="high",
            ),
            "ai_buzzwords": ModificationRule(
                issue_type="AI词汇",
                pattern=r"(赋能|抓手|闭环|落地|痛点|打法|赛道|生态)",
                replacement="",
                description="替换为传统学术词汇",
                priority="high",
            ),
            "vague_attribution": ModificationRule(
                issue_type="模糊归因",
                pattern=r"([有|据|相关]研究[表明|指出|显示|发现]|专家[指出|认为|表示])",
                replacement="",
                description="明确引用具体文献或删除",
                priority="high",
            ),
            "surface_analysis": ModificationRule(
                issue_type="表面分析",
                pattern=r"(凸显|反映|体现|表明)[了|出][^，。]*[重要性|价值|意义|问题|趋势]",
                replacement="",
                description="提供具体数据或机制解释",
                priority="medium",
            ),
            "excessive_connectors": ModificationRule(
                issue_type="连接词过多",
                pattern=r"(首先|其次|最后|此外|另外|因此|综上所述)[^，。]*",
                replacement="",
                description="减少逻辑连接词，使用自然过渡",
                priority="medium",
            ),
            "spacing_issues": ModificationRule(
                issue_type="中英文混排空格",
                pattern=r"([\u4e00-\u9fff])\s+([a-zA-Z0-9])|([a-zA-Z0-9])\s+([\u4e00-\u9fff])",
                replacement=r"\1\2\3\4",
                description="删除中英文/数字之间的空格",
                priority="high",
            ),
            "uniform_sentence_length": ModificationRule(
                issue_type="句子长度均匀",
                pattern="",
                replacement="",
                description="调整句子长度，增加长短句变化",
                priority="low",
            ),
            "low_vocabulary_diversity": ModificationRule(
                issue_type="词汇多样性低",
                pattern="",
                replacement="",
                description="使用同义词替换重复词汇",
                priority="low",
            ),
            "high_connective_density": ModificationRule(
                issue_type="连接词密度高",
                pattern=r"(首先|其次|最后|此外|另外|因此|综上所述|值得注意的是|需要指出的是)",
                replacement="",
                description="删除冗余连接词，重构段落",
                priority="medium",
            ),
            "excessive_formal_patterns": ModificationRule(
                issue_type="正式表达模式过多",
                pattern=r"(本文[研究|分析|探讨|旨在]|基于[^，。]*分析|通过[^，。]*发现)",
                replacement="",
                description="适当使用口语化表达",
                priority="low",
            ),
        }

    def _load_chapter_templates(self) -> Dict[str, Dict]:
        """加载章节特定模板"""
        return {
            "literature_review": {
                "name": "文献综述",
                "common_issues": ["罗列式综述", "缺乏批判性", "时间线堆砌"],
                "improvement_strategy": "按主题组织，进行比较分析，指出研究空白",
            },
            "case_analysis": {
                "name": "案例分析",
                "common_issues": ["描述过多", "结论先行", "缺乏数据", "模板化结构"],
                "improvement_strategy": "精简背景，提供数据，分析因果机制",
            },
            "strategy": {
                "name": "战略建议",
                "common_issues": ["空泛建议", "忽视约束", "套用模板", "缺乏优先级"],
                "improvement_strategy": "具体可操作，考虑约束，分阶段实施",
            },
        }

    def generate_feedback(self, detection_result: Dict, text: str) -> Dict:
        """生成综合反馈"""
        fusion_result = detection_result.get("fusion_result", {})
        modification_plan = detection_result.get("modification_plan", {})

        feedback = {
            "summary": {
                "ai_probability": fusion_result.get("final_probability", 0),
                "risk_level": modification_plan.get("risk_level", "unknown"),
                "total_issues": sum(
                    r.get("issues_count", 0)
                    for r in fusion_result.get("method_results", [])
                ),
                "estimated_time": modification_plan.get("estimated_time", ""),
            },
            "modifications": [],
            "chapter_specific": {},
            "before_after_examples": [],
            "quick_fixes": [],
            "deep_rewrites": [],
        }

        # 生成具体修改项
        priority_fixes = modification_plan.get("priority_fixes", [])
        for fix in priority_fixes:
            modification = self._create_modification(fix, text)
            if modification:
                feedback["modifications"].append(modification)

        # 生成章节特定建议
        chapter_type = self._detect_chapter_type(text)
        if chapter_type in self.chapter_templates:
            feedback["chapter_specific"] = self._generate_chapter_feedback(
                chapter_type, text
            )

        # 生成修改示例
        feedback["before_after_examples"] = self._generate_examples(
            text, priority_fixes
        )

        # 分类修改难度
        feedback["quick_fixes"] = [
            m
            for m in feedback["modifications"]
            if m.get("priority") == "high" and m.get("auto_fixable", False)
        ]
        feedback["deep_rewrites"] = [
            m
            for m in feedback["modifications"]
            if m.get("priority") == "high" and not m.get("auto_fixable", False)
        ]

        return feedback

    def _create_modification(self, fix: Dict, text: str) -> Dict:
        """创建单个修改项"""
        issue_type = fix.get("issue_type", "")
        rule = self.modification_rules.get(issue_type)

        if not rule:
            return {
                "issue_type": issue_type,
                "description": fix.get("suggestion", ""),
                "priority": fix.get("priority", "medium"),
                "auto_fixable": False,
                "manual_steps": [fix.get("suggestion", "")],
            }

        # 查找文本中的匹配项
        matches = []
        if rule.pattern:
            pattern = re.compile(rule.pattern)
            for line_num, line in enumerate(text.split("\n"), 1):
                for match in pattern.finditer(line):
                    matches.append(
                        {
                            "line": line_num,
                            "original": match.group(0),
                            "context": line[
                                max(0, match.start() - 10) : min(
                                    len(line), match.end() + 10
                                )
                            ],
                        }
                    )

        return {
            "issue_type": issue_type,
            "description": rule.description,
            "priority": rule.priority,
            "auto_fixable": bool(rule.pattern and rule.replacement),
            "pattern": rule.pattern if rule.pattern else None,
            "replacement": rule.replacement if rule.replacement else None,
            "matches": matches[:5],  # 最多显示5个匹配
            "manual_steps": self._generate_manual_steps(issue_type),
        }

    def _generate_manual_steps(self, issue_type: str) -> List[str]:
        """生成手动修改步骤"""
        steps_map = {
            "exaggerated_emphasis": [
                '1. 识别文本中的"关键"、"重要"、"核心"等词汇',
                "2. 删除这些词汇，保留客观事实陈述",
                "3. 用具体数据替代价值判断",
            ],
            "ai_buzzwords": [
                '1. 识别"赋能"、"抓手"、"闭环"等 AI 词汇',
                "2. 替换为传统学术表达",
                '3. 例如："赋能"→"促进"、"抓手"→"切入点"',
            ],
            "vague_attribution": [
                '1. 找到"有研究指出"、"专家认为"等模糊表述',
                "2. 查找原始文献，替换为具体引用",
                "3. 或删除此类表述，直接陈述事实",
            ],
            "surface_analysis": [
                '1. 识别"凸显了"、"反映了"等表面分析',
                "2. 补充具体机制解释",
                "3. 添加数据支撑",
            ],
            "excessive_connectors": [
                "1. 统计每段的连接词数量",
                "2. 删除冗余的逻辑连接词",
                "3. 通过段落结构体现逻辑关系",
            ],
            "spacing_issues": [
                "1. 使用查找替换功能",
                "2. 查找：中文 + 空格 + 英文/数字",
                "3. 替换为：中文 + 英文/数字（无空格）",
            ],
        }
        return steps_map.get(issue_type, ["根据具体情况手动修改"])

    def _detect_chapter_type(self, text: str) -> str:
        """检测章节类型"""
        indicators = {
            "literature_review": ["文献综述", "相关研究", "理论基础", "研究现状"],
            "case_analysis": ["案例分析", "案例研究", "实证分析", "企业分析"],
            "strategy": ["战略建议", "对策建议", "实施方案", "改进措施"],
        }

        scores = {}
        for chapter_type, keywords in indicators.items():
            score = sum(text.count(kw) for kw in keywords)
            scores[chapter_type] = score

        if scores:
            return str(max(scores.items(), key=lambda x: x[1])[0])
        return "general"

    def _generate_chapter_feedback(self, chapter_type: str, text: str) -> Dict:
        """生成章节特定反馈"""
        template = self.chapter_templates.get(chapter_type, {})

        # 检测章节常见问题
        detected_issues = []
        if chapter_type == "literature_review":
            if len(re.findall(r"\w+\(\d{4}\)", text)) > 5:
                detected_issues.append("罗列式综述")
            if "但是" not in text and "然而" not in text:
                detected_issues.append("缺乏批判性")

        elif chapter_type == "case_analysis":
            if "该公司" in text and text.count("年") > 3:
                detected_issues.append("背景描述过多")
            if not re.search(r"\d+%", text):
                detected_issues.append("缺乏数据支撑")

        elif chapter_type == "strategy":
            if text.count("建议") > 3:
                detected_issues.append("建议空泛")
            if "约束" not in text and "限制" not in text:
                detected_issues.append("忽视约束条件")

        return {
            "chapter_name": template.get("name", "一般文本"),
            "detected_issues": detected_issues,
            "improvement_strategy": template.get("improvement_strategy", ""),
            "specific_suggestions": self._generate_chapter_suggestions(
                chapter_type, detected_issues
            ),
        }

    def _generate_chapter_suggestions(
        self, chapter_type: str, issues: List[str]
    ) -> List[str]:
        """生成章节特定建议"""
        suggestions = {
            "literature_review": {
                "罗列式综述": "按主题组织文献，例如：理论基础、实证研究、研究空白",
                "缺乏批判性": "对比不同研究的观点差异，指出方法局限",
            },
            "case_analysis": {
                "背景描述过多": "精简背景，聚焦与研究问题相关的关键信息",
                "缺乏数据支撑": "补充具体数字、百分比、时间节点",
            },
            "strategy": {
                "建议空泛": "明确行动主体、具体措施、预期效果",
                "忽视约束条件": "分析资源、能力、环境的限制",
            },
        }

        result = []
        for issue in issues:
            if chapter_type in suggestions and issue in suggestions[chapter_type]:
                result.append(f"{issue}: {suggestions[chapter_type][issue]}")
        return result

    def _generate_examples(self, text: str, fixes: List[Dict]) -> List[Dict]:
        """生成修改前后示例"""
        examples = []

        # 常见 AI 特征示例映射
        example_map = {
            "exaggerated_emphasis": {
                "before": "数字化转型是推动企业高质量发展的关键抓手",
                "after": "本研究探讨数字化转型对企业绩效的影响",
            },
            "ai_buzzwords": {
                "before": "通过赋能业务创新，为企业创造显著价值",
                "after": "通过促进业务创新，提升企业竞争力",
            },
            "vague_attribution": {
                "before": "有研究指出，企业文化对组织绩效具有重要影响",
                "after": "Schein(2010)的研究表明，强势企业文化与组织绩效存在正相关关系(r=0.42, p<0.05)",
            },
            "surface_analysis": {
                "before": "这凸显了管理的重要性",
                "after": "管理效率提升使运营成本下降8%",
            },
            "excessive_connectors": {
                "before": "首先，本文回顾了相关文献。其次，构建了理论模型。最后，进行了实证检验。",
                "after": "本文首先回顾相关文献，在此基础上构建理论模型，并通过实证数据检验研究假设。",
            },
            "spacing_issues": {
                "before": "MBA 论文写作需要关注 AI 痕迹问题。2023 年的研究表明，15 % 的企业存在此类问题。",
                "after": "MBA论文写作需要关注AI痕迹问题。2023年的研究表明，15%的企业存在此类问题。",
            },
        }

        for fix in fixes[:3]:  # 最多显示3个示例
            issue_type = fix.get("issue_type", "")
            if issue_type in example_map:
                examples.append({"issue_type": issue_type, **example_map[issue_type]})

        return examples

    def apply_auto_fixes(
        self, text: str, modifications: List[Dict]
    ) -> Tuple[str, List[Dict]]:
        """应用自动修复"""
        fixed_text = text
        applied_fixes = []

        for mod in modifications:
            if mod.get("auto_fixable") and mod.get("pattern"):
                pattern = mod["pattern"]
                replacement = mod.get("replacement", "")

                # 执行替换
                new_text = re.sub(pattern, replacement, fixed_text)

                if new_text != fixed_text:
                    applied_fixes.append(
                        {
                            "issue_type": mod["issue_type"],
                            "pattern": pattern,
                            "count": len(re.findall(pattern, fixed_text)),
                        }
                    )
                    fixed_text = new_text

        return fixed_text, applied_fixes

    def export_modifications(self, feedback: Dict, output_path: str):
        """导出修改建议"""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(feedback, ensure_ascii=False, indent=2, fp=f)

    def format_feedback_report(self, feedback: Dict) -> str:
        """格式化反馈报告"""
        summary = feedback["summary"]

        report = f"""# AI 检测反馈与修改建议报告

## 检测摘要

- **AI 生成概率**: {summary["ai_probability"] * 100:.1f}%
- **风险等级**: {"🔴 高风险" if summary["risk_level"] == "high" else "🟡 中风险" if summary["risk_level"] == "medium" else "🟢 低风险"}
- **发现问题数**: {summary["total_issues"]}
- **预计修改时间**: {summary["estimated_time"]}

## 快速修复（可自动处理）

"""

        if feedback["quick_fixes"]:
            for fix in feedback["quick_fixes"]:
                report += f"### {fix['issue_type']}\n"
                report += f"- 描述: {fix['description']}\n"
                report += f"- 优先级: {fix['priority']}\n"
                if fix.get("matches"):
                    report += "- 发现位置:\n"
                    for match in fix["matches"][:3]:
                        report += f"  - 第{match['line']}行: {match['context']}\n"
                report += "\n"
        else:
            report += "暂无快速修复项\n\n"

        report += "## 深度改写（需手动处理）\n\n"

        if feedback["deep_rewrites"]:
            for mod in feedback["deep_rewrites"]:
                report += f"### {mod['issue_type']}\n"
                report += f"- 描述: {mod['description']}\n"
                report += f"- 优先级: {mod['priority']}\n"
                report += "- 修改步骤:\n"
                for step in mod.get("manual_steps", []):
                    report += f"  {step}\n"
                report += "\n"

        report += "## 修改示例\n\n"

        for example in feedback["before_after_examples"]:
            report += f"### {example['issue_type']}\n"
            report += f"**原文**: {example['before']}\n\n"
            report += f"**改写**: {example['after']}\n\n"

        if feedback["chapter_specific"]:
            chapter = feedback["chapter_specific"]
            report += f"""## 章节特定建议

**检测章节**: {chapter["chapter_name"]}

**发现问题**:
"""
            for issue in chapter["detected_issues"]:
                report += f"- {issue}\n"

            report += f"\n**改进策略**: {chapter['improvement_strategy']}\n\n"

            if chapter.get("specific_suggestions"):
                report += "**具体建议**:\n"
                for suggestion in chapter["specific_suggestions"]:
                    report += f"- {suggestion}\n"

        report += """
---
*报告由 AI 检测反馈系统生成*
"""

        return report


def main():
    import argparse

    parser = argparse.ArgumentParser(description="AI 检测反馈生成器")
    parser.add_argument("detection_result", help="检测结果 JSON 文件")
    parser.add_argument("--text", "-t", help="原始文本文件")
    parser.add_argument("--apply", "-a", action="store_true", help="应用自动修复")
    parser.add_argument("--export", "-e", help="导出修改建议 JSON")
    parser.add_argument("--output", "-o", help="输出报告文件")

    args = parser.parse_args()

    # 加载检测结果
    with open(args.detection_result, "r", encoding="utf-8") as f:
        detection_result = json.load(f)

    # 加载原始文本
    text = ""
    if args.text:
        with open(args.text, "r", encoding="utf-8") as f:
            text = f.read()

    # 生成反馈
    generator = FeedbackGenerator()
    feedback = generator.generate_feedback(detection_result, text)

    # 应用自动修复
    if args.apply and text:
        fixed_text, applied = generator.apply_auto_fixes(
            text, feedback["modifications"]
        )
        print(f"✅ 自动修复完成，修复了 {len(applied)} 类问题")
        for fix in applied:
            print(f"  - {fix['issue_type']}: {fix['count']} 处")

        # 保存修复后的文本
        fixed_path = args.text.replace(".txt", "_fixed.txt")
        with open(fixed_path, "w", encoding="utf-8") as f:
            f.write(fixed_text)
        print(f"✅ 修复后的文本已保存至: {fixed_path}")

    # 导出修改建议
    if args.export:
        generator.export_modifications(feedback, args.export)
        print(f"✅ 修改建议已导出至: {args.export}")

    # 输出报告
    report = generator.format_feedback_report(feedback)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✅ 反馈报告已保存至: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
