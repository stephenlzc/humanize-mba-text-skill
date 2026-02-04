#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多方案融合 AI 特征检测器
结合规则匹配、统计分析和机器学习模型

使用方法:
    python multi_detector.py input.txt
    python multi_detector.py input.txt --interactive
    python multi_detector.py input.txt --output suggestions.json
"""

import re
import sys
import json
import math
import argparse
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple, Optional
from collections import Counter
from enum import Enum


class DetectionMethod(Enum):
    """检测方法类型"""

    RULE_BASED = "rule_based"  # 规则匹配
    STATISTICAL = "statistical"  # 统计分析
    LINGUISTIC = "linguistic"  # 语言特征
    HYBRID = "hybrid"  # 混合检测


@dataclass
class DetectionResult:
    """单个检测结果"""

    method: DetectionMethod
    ai_probability: float  # 0-1 的 AI 生成概率
    confidence: float  # 检测置信度
    features: Dict  # 检测到的特征
    issues: List[Dict]  # 具体问题
    suggestions: List[str]  # 修改建议


@dataclass
class FusionResult:
    """融合后的最终结果"""

    final_probability: float
    method_results: List[DetectionResult]
    consensus_level: str  # high/medium/low
    dominant_features: List[str]
    priority_fixes: List[Dict]


class RuleBasedDetector:
    """基于规则的检测器"""

    def __init__(self):
        self.patterns = {
            "exaggerated_emphasis": {
                "patterns": [
                    r"关键[的是|在于|作用|意义]",
                    r"重要[的是|意义|价值|作用]",
                    r"核心[竞争力|要素|能力|优势]",
                    r"灵魂人物",
                    r"绝对[是|的]",
                    r"至关重要",
                ],
                "weight": 0.8,
                "suggestion": "删除价值判断词汇，直接陈述事实",
            },
            "ai_buzzwords": {
                "patterns": [
                    r"赋能",
                    r"抓手",
                    r"闭环",
                    r"落地",
                    r"痛点",
                    r"打法",
                    r"赛道",
                    r"生态[系统|圈|链]?",
                    r"迭代",
                    r"协同",
                ],
                "weight": 1.0,
                "suggestion": "使用传统学术词汇替代",
            },
            "vague_attribution": {
                "patterns": [
                    r"[有|据|相关]研究[表明|指出|显示|发现]",
                    r"专家[指出|认为|表示|强调]",
                    r"学者[普遍认为|研究发现]",
                    r"普遍[认为|看来|认同]",
                ],
                "weight": 0.9,
                "suggestion": "明确引用具体文献或删除此类表述",
            },
            "surface_analysis": {
                "patterns": [
                    r"凸显[了|出][^，。]*[重要性|价值|意义]",
                    r"反映[了|出][^，。]*[问题|趋势|特征]",
                    r"体现[了|出][^，。]*[价值|意义|作用]",
                ],
                "weight": 0.7,
                "suggestion": "提供具体机制解释或数据支撑",
            },
            "excessive_connectors": {
                "patterns": [
                    r"首先[^，。]*其次[^，。]*最后",
                    r"第一[^，。]*第二[^，。]*第三",
                    r"此外[^，。]*另外[^，。]*与此同时",
                ],
                "weight": 0.6,
                "suggestion": "减少连接词，使用更自然的过渡",
            },
            "spacing_issues": {
                "patterns": [
                    r"[\u4e00-\u9fff]\s+[a-zA-Z0-9]",
                    r"[a-zA-Z0-9]\s+[\u4e00-\u9fff]",
                ],
                "weight": 0.5,
                "suggestion": "删除中英文/数字之间的空格",
            },
        }

    def detect(self, text: str) -> DetectionResult:
        """执行规则检测"""
        issues = []
        total_weight = 0
        matched_weight = 0
        lines = text.split("\n")

        for pattern_id, pattern_info in self.patterns.items():
            weight = pattern_info["weight"]
            total_weight += weight

            for pattern in pattern_info["patterns"]:
                regex = re.compile(pattern)
                for line_num, line in enumerate(lines, 1):
                    for match in regex.finditer(line):
                        matched_weight += weight
                        issues.append(
                            {
                                "type": pattern_id,
                                "line": line_num,
                                "content": match.group(0)[:30],
                                "weight": weight,
                                "suggestion": pattern_info["suggestion"],
                            }
                        )

        # 计算概率
        ai_probability = min(1.0, matched_weight / max(total_weight * 0.3, 1.0))
        confidence = 0.8 if issues else 0.5

        # 生成建议
        suggestions = list(set(issue["suggestion"] for issue in issues))

        return DetectionResult(
            method=DetectionMethod.RULE_BASED,
            ai_probability=ai_probability,
            confidence=confidence,
            features={
                "total_issues": len(issues),
                "issue_types": len(set(i["type"] for i in issues)),
            },
            issues=issues,
            suggestions=suggestions,
        )


class StatisticalDetector:
    """基于统计特征的检测器"""

    def detect(self, text: str) -> DetectionResult:
        """执行统计检测"""
        features = {}
        issues = []

        # 1. 句子长度均匀度（AI 文本通常更均匀）
        sentences = re.split(r"[。！？]", text)
        sentences = [s.strip() for s in sentences if s.strip()]
        if sentences:
            lengths = [len(s) for s in sentences]
            avg_len = sum(lengths) / len(lengths)
            variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)
            uniformity = 1 / (1 + math.sqrt(variance) / avg_len) if avg_len > 0 else 0
            features["sentence_uniformity"] = uniformity

            if uniformity > 0.7:
                issues.append(
                    {
                        "type": "uniform_sentence_length",
                        "line": 0,
                        "content": f"句子长度过于均匀（变异系数: {variance / avg_len:.2f}）",
                        "weight": 0.6,
                        "suggestion": "调整句子长度，增加长短句变化",
                    }
                )

        # 2. 词汇多样性（AI 文本多样性较低）
        words = re.findall(r"[\u4e00-\u9fff]+", text)
        if words:
            unique_words = len(set(words))
            total_words = len(words)
            diversity = unique_words / total_words if total_words > 0 else 0
            features["vocabulary_diversity"] = diversity

            if diversity < 0.4:
                issues.append(
                    {
                        "type": "low_vocabulary_diversity",
                        "line": 0,
                        "content": f"词汇多样性较低（{diversity:.2f}）",
                        "weight": 0.5,
                        "suggestion": "使用更多同义词，避免重复表达",
                    }
                )

        # 3. 标点符号分布
        punctuation = text.count("，") + text.count("。") + text.count("、")
        if len(text) > 0:
            punct_ratio = punctuation / len(text)
            features["punctuation_ratio"] = punct_ratio

        # 4. 段落长度分布
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        if paragraphs:
            para_lengths = [len(p) for p in paragraphs]
            para_variance = sum(
                (l - sum(para_lengths) / len(para_lengths)) ** 2 for l in para_lengths
            ) / len(para_lengths)
            features["paragraph_variance"] = para_variance

        # 计算 AI 概率
        uniformity_val = features.get("sentence_uniformity", 0)
        diversity_val = features.get("vocabulary_diversity", 0.5)
        punct_ratio_val = features.get("punctuation_ratio", 0)
        para_variance_val = features.get("paragraph_variance", 0)

        ai_probability = (
            uniformity_val * 0.3
            + (1 - diversity_val) * 0.3
            + (0.1 if punct_ratio_val > 0.15 else 0) * 0.2
            + (0.5 if para_variance_val < 100 else 0) * 0.2
        )

        return DetectionResult(
            method=DetectionMethod.STATISTICAL,
            ai_probability=min(1.0, ai_probability),
            confidence=0.7,
            features=features,
            issues=issues,
            suggestions=list(set(issue["suggestion"] for issue in issues)),
        )


class LinguisticDetector:
    """基于语言学特征的检测器"""

    def __init__(self):
        self.connectives = [
            "首先",
            "其次",
            "最后",
            "此外",
            "另外",
            "因此",
            "综上所述",
            "值得注意的是",
            "需要指出的是",
            "由此可见",
        ]
        self.formal_patterns = [
            r"本文[研究|分析|探讨|旨在]",
            r"基于[^，。]*分析",
            r"通过[^，。]*发现",
            r"结果表明",
        ]

    def detect(self, text: str) -> DetectionResult:
        """执行语言特征检测"""
        issues = []
        features = {}

        # 1. 连接词密度
        connective_count = sum(text.count(c) for c in self.connectives)
        total_chars = len(text)
        connective_density = (
            connective_count / (total_chars / 100) if total_chars > 0 else 0
        )
        features["connective_density"] = connective_density

        if connective_density > 0.8:
            issues.append(
                {
                    "type": "high_connective_density",
                    "line": 0,
                    "content": f"连接词密度过高（每百字{connective_density:.1f}个）",
                    "weight": 0.7,
                    "suggestion": "减少逻辑连接词，使用更自然的段落过渡",
                }
            )

        # 2. 正式表达模式
        formal_count = 0
        for pattern in self.formal_patterns:
            formal_count += len(re.findall(pattern, text))
        formal_density = formal_count / (total_chars / 100) if total_chars > 0 else 0
        features["formal_pattern_density"] = formal_density

        if formal_density > 1.5:
            issues.append(
                {
                    "type": "excessive_formal_patterns",
                    "line": 0,
                    "content": f"正式表达模式过多（每百字{formal_density:.1f}个）",
                    "weight": 0.5,
                    "suggestion": "适当使用口语化表达，增加文本自然度",
                }
            )

        # 3. 句式复杂度
        complex_patterns = [
            r"不仅[^，。]*而且[^，。]*",
            r"虽然[^，。]*但是[^，。]*",
            r"既然[^，。]*就[^，。]*",
            r"即使[^，。]*也[^，。]*",
        ]
        complex_count = sum(len(re.findall(p, text)) for p in complex_patterns)
        # 计算句子数量
        sentences = re.split(r"[。！？]", text)
        sentences = [s.strip() for s in sentences if s.strip()]
        features["complex_sentence_ratio"] = (
            complex_count / len(sentences) if sentences else 0
        )

        # 计算 AI 概率
        ai_probability = (
            min(1.0, connective_density / 1.5) * 0.4
            + min(1.0, formal_density / 2.0) * 0.3
            + min(1.0, complex_count / 5) * 0.3
        )

        return DetectionResult(
            method=DetectionMethod.LINGUISTIC,
            ai_probability=ai_probability,
            confidence=0.75,
            features=features,
            issues=issues,
            suggestions=list(set(issue["suggestion"] for issue in issues)),
        )


class FusionEngine:
    """融合多个检测器结果"""

    def __init__(self):
        self.detectors = {
            "rule": RuleBasedDetector(),
            "statistical": StatisticalDetector(),
            "linguistic": LinguisticDetector(),
        }
        self.weights = {"rule": 0.4, "statistical": 0.3, "linguistic": 0.3}

    def detect(self, text: str) -> FusionResult:
        """执行融合检测"""
        results = []

        # 运行所有检测器
        for name, detector in self.detectors.items():
            try:
                result = detector.detect(text)
                results.append(result)
            except Exception as e:
                print(f"Warning: {name} detector failed: {e}", file=sys.stderr)

        # 计算融合概率
        weighted_prob = sum(
            r.ai_probability
            * self.weights.get(r.method.value.replace("_based", ""), 0.3)
            for r in results
        )

        # 计算一致性
        probs = [r.ai_probability for r in results]
        consensus = 1 - (max(probs) - min(probs)) if probs else 0

        if consensus > 0.7:
            consensus_level = "high"
        elif consensus > 0.4:
            consensus_level = "medium"
        else:
            consensus_level = "low"

        # 提取主要特征
        all_issues = []
        for r in results:
            all_issues.extend(r.issues)

        # 按权重排序
        all_issues.sort(key=lambda x: x.get("weight", 0.5), reverse=True)
        dominant_features = list(set(issue["type"] for issue in all_issues[:10]))

        # 生成优先修复列表
        priority_fixes = self._generate_priority_fixes(all_issues)

        return FusionResult(
            final_probability=round(weighted_prob, 3),
            method_results=results,
            consensus_level=consensus_level,
            dominant_features=dominant_features,
            priority_fixes=priority_fixes,
        )

    def _generate_priority_fixes(self, issues: List[Dict]) -> List[Dict]:
        """生成优先修复列表"""
        # 按类型分组
        type_groups = {}
        for issue in issues:
            issue_type = issue["type"]
            if issue_type not in type_groups:
                type_groups[issue_type] = []
            type_groups[issue_type].append(issue)

        # 生成修复建议
        fixes = []
        for issue_type, group in sorted(
            type_groups.items(),
            key=lambda x: sum(i.get("weight", 0) for i in x[1]),
            reverse=True,
        )[:5]:
            fixes.append(
                {
                    "issue_type": issue_type,
                    "count": len(group),
                    "example": group[0]["content"][:50] if group else "",
                    "suggestion": group[0]["suggestion"] if group else "",
                    "priority": "high"
                    if sum(i.get("weight", 0) for i in group) > 2
                    else "medium",
                }
            )

        return fixes


def generate_modification_plan(fusion_result: FusionResult, text: str) -> Dict:
    """生成修改计划"""
    plan = {
        "ai_score": fusion_result.final_probability,
        "risk_level": "high"
        if fusion_result.final_probability > 0.7
        else "medium"
        if fusion_result.final_probability > 0.4
        else "low",
        "modification_strategy": "",
        "steps": [],
        "estimated_time": "",
    }

    if fusion_result.final_probability > 0.7:
        plan["modification_strategy"] = "深度改写 - 需要全面重构"
        plan["estimated_time"] = "2-3小时"
        plan["steps"] = [
            "1. 识别并删除所有 AI 特征词汇",
            "2. 重组段落结构，打破僵化模式",
            "3. 补充具体数据和案例",
            "4. 检查并修正所有中英文混排空格",
            "5. 通读润色，确保语言自然流畅",
        ]
    elif fusion_result.final_probability > 0.4:
        plan["modification_strategy"] = "中度修改 - 针对性优化"
        plan["estimated_time"] = "1-2小时"
        plan["steps"] = [
            "1. 修复高优先级的 AI 特征问题",
            "2. 调整明显的套话和模板化表达",
            "3. 补充关键数据支撑",
            "4. 修正空格和标点问题",
        ]
    else:
        plan["modification_strategy"] = "轻度润色 - 细节优化"
        plan["estimated_time"] = "30分钟-1小时"
        plan["steps"] = ["1. 检查并修复少量 AI 痕迹", "2. 优化语言表达", "3. 最终校对"]

    # 添加具体修改建议
    plan["priority_fixes"] = fusion_result.priority_fixes

    return plan


def format_enhanced_report(fusion_result: FusionResult, text: str) -> str:
    """生成增强版 Markdown 报告"""
    plan = generate_modification_plan(fusion_result, text)

    md = f"""# AI 特征多维度检测报告

## 综合评估

- **AI 生成概率**: {fusion_result.final_probability * 100:.1f}%
- **风险等级**: {"🔴 高风险" if plan["risk_level"] == "high" else "🟡 中风险" if plan["risk_level"] == "medium" else "🟢 低风险"}
- **检测器一致性**: {fusion_result.consensus_level.upper()}
- **建议修改策略**: {plan["modification_strategy"]}
- **预计修改时间**: {plan["estimated_time"]}

## 各检测器结果

"""

    for result in fusion_result.method_results:
        md += f"""### {result.method.value.replace("_", " ").title()}
- AI 概率: {result.ai_probability * 100:.1f}%
- 置信度: {result.confidence * 100:.1f}%
- 发现问题: {len(result.issues)}
"""
        if result.features:
            md += "- 关键特征:\n"
            for k, v in result.features.items():
                if isinstance(v, float):
                    md += f"  - {k}: {v:.3f}\n"
                else:
                    md += f"  - {k}: {v}\n"
        md += "\n"

    md += """## 优先修复项

| 优先级 | 问题类型 | 出现次数 | 示例 | 修改建议 |
|-------|---------|---------|------|---------|
"""

    for fix in plan["priority_fixes"]:
        priority_icon = "🔴" if fix["priority"] == "high" else "🟡"
        example = fix["example"][:30].replace("|", "\\|")
        suggestion = fix["suggestion"][:40].replace("|", "\\|")
        md += f"| {priority_icon} | {fix['issue_type']} | {fix['count']} | {example}... | {suggestion}... |\n"

    md += f"""
## 修改计划

### 修改步骤
"""

    for step in plan["steps"]:
        md += f"- {step}\n"

    md += """
### 主要 AI 特征类型
"""

    for feature in fusion_result.dominant_features[:5]:
        md += f"- {feature}\n"

    md += """
---
*报告由多维度 AI 检测系统生成*
"""

    return md


def main():
    parser = argparse.ArgumentParser(
        description="多方案融合 AI 特征检测",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python multi_detector.py input.txt
    python multi_detector.py input.txt --interactive
    python multi_detector.py input.txt --plan modification_plan.json
        """,
    )

    parser.add_argument("input_file", help="输入文本文件路径")
    parser.add_argument("--output", "-o", help="输出报告文件路径")
    parser.add_argument("--plan", "-p", help="输出修改计划 JSON")
    parser.add_argument(
        "--interactive", "-i", action="store_true", help="交互模式，逐条确认修改"
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["json", "markdown"],
        default="markdown",
        help="输出格式",
    )

    args = parser.parse_args()

    # 读取输入文件
    try:
        with open(args.input_file, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        print(f"错误: 无法读取文件 - {e}")
        sys.exit(1)

    # 执行融合检测
    print("正在进行多维度 AI 特征检测...")
    engine = FusionEngine()
    fusion_result = engine.detect(text)

    # 生成修改计划
    plan = generate_modification_plan(fusion_result, text)

    # 格式化输出
    if args.format == "json":
        output = json.dumps(
            {
                "fusion_result": {
                    "final_probability": fusion_result.final_probability,
                    "consensus_level": fusion_result.consensus_level,
                    "dominant_features": fusion_result.dominant_features,
                    "priority_fixes": fusion_result.priority_fixes,
                    "method_results": [
                        {
                            "method": r.method.value,
                            "ai_probability": r.ai_probability,
                            "confidence": r.confidence,
                            "features": r.features,
                            "issues_count": len(r.issues),
                        }
                        for r in fusion_result.method_results
                    ],
                },
                "modification_plan": plan,
            },
            ensure_ascii=False,
            indent=2,
        )
    else:
        output = format_enhanced_report(fusion_result, text)

    # 输出结果
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ 检测报告已保存至: {args.output}")
    else:
        print(output)

    # 保存修改计划
    if args.plan:
        with open(args.plan, "w", encoding="utf-8") as f:
            json.dump(plan, ensure_ascii=False, indent=2, fp=f)
        print(f"✅ 修改计划已保存至: {args.plan}")

    # 简要统计
    print(f"\n📊 检测摘要:")
    print(f"  - AI 生成概率: {fusion_result.final_probability * 100:.1f}%")
    print(f"  - 风险等级: {plan['risk_level'].upper()}")
    print(f"  - 检测器一致性: {fusion_result.consensus_level}")
    print(f"  - 建议修改策略: {plan['modification_strategy']}")
    print(f"  - 预计时间: {plan['estimated_time']}")

    # 交互模式
    if args.interactive and fusion_result.priority_fixes:
        print("\n📝 交互式修改建议:")
        for i, fix in enumerate(fusion_result.priority_fixes[:3], 1):
            print(f"\n{i}. [{fix['priority'].upper()}] {fix['issue_type']}")
            print(f"   示例: {fix['example'][:50]}...")
            print(f"   建议: {fix['suggestion']}")


if __name__ == "__main__":
    main()
