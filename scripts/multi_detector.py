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
from dataclasses import dataclass, asdict, field
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
    humanization_score: float = 0.0  # 人类化分数 (0-1)
    mba_suggestions: List[str] = field(default_factory=list)  # MBA论文特定建议


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
    """基于统计特征的检测器（增强版）"""

    def detect(self, text: str) -> DetectionResult:
        """执行统计检测"""
        features = {}
        issues = []
        
        # 计算总字数和句子数
        total_chars = len(text)
        sentences = re.split(r"[。！？]", text)
        sentences = [s.strip() for s in sentences if s.strip()]
        total_sentences = len(sentences) if sentences else 1

        # 1. 句子长度均匀度（AI 文本通常更均匀）
        if sentences:
            lengths = [len(s) for s in sentences]
            avg_len = sum(lengths) / len(lengths)
            variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)
            std_dev = math.sqrt(variance)
            uniformity = 1 / (1 + std_dev / avg_len) if avg_len > 0 else 0
            features["sentence_uniformity"] = uniformity
            features["sentence_std_dev"] = std_dev  # 句长标准差

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
            
            # 新增：句长标准差目标提示
            if std_dev < 8:
                issues.append(
                    {
                        "type": "low_sentence_variance",
                        "line": 0,
                        "content": f"句长标准差偏低（{std_dev:.2f} < 8）",
                        "weight": 0.5,
                        "suggestion": "增加长短句交替，提升句式变化",
                    }
                )

        # 2. 词汇多样性（AI 文本多样性较低）
        words = re.findall(r"[\u4e00-\u9fff]+", text)
        if words:
            unique_words = len(set(words))
            total_words = len(words)
            diversity = unique_words / total_words if total_words > 0 else 0
            features["vocabulary_diversity"] = diversity
            features["vocabulary_ttr"] = diversity  # TTR (Type-Token Ratio)

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
            
            # 新增：TTR目标提示
            if diversity < 0.6:
                issues.append(
                    {
                        "type": "low_ttr",
                        "line": 0,
                        "content": f"词汇丰富度TTR偏低（{diversity:.2f} < 0.6）",
                        "weight": 0.4,
                        "suggestion": "增加词汇丰富度，使用多样化表达",
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

        # ===== 新增统计特征 =====
        
        # 5. 并列结构密度（每百字中的(1)(2)(3)或首先/其次/最后数量）
        parallel_patterns = [
            r"\([1-9]\)",  # (1)(2)(3) 格式
            r"[①②③④⑤⑥⑦⑧⑨⑩]",  # 圆圈数字
            r"首先.*其次.*最后",  # 首先...其次...最后
            r"第一.*第二.*第三",  # 第一...第二...第三
            r"一方面.*另一方面",  # 一方面...另一方面
        ]
        parallel_count = 0
        for pattern in parallel_patterns:
            parallel_count += len(re.findall(pattern, text))
        parallel_density = parallel_count / (total_chars / 100) if total_chars > 0 else 0
        features["parallel_structure_density"] = parallel_density
        
        if parallel_density > 1.5:
            issues.append(
                {
                    "type": "high_parallel_structure",
                    "line": 0,
                    "content": f"并列结构密度过高（每百字{parallel_density:.1f}个）",
                    "weight": 0.6,
                    "suggestion": "打破并列结构，改用递进关系",
                }
            )

        # 6. 复杂句式比例（包含"尽管...但是"、"不仅...而且"的句子占比）
        complex_patterns = [
            r"尽管[^，。]*但是[^，。]*",
            r"虽然[^，。]*但是[^，。]*",
            r"不仅[^，。]*而且[^，。]*",
            r"不但[^，。]*而且[^，。]*",
            r"即使[^，。]*也[^，。]*",
            r"如果[^，。]*那么[^，。]*",
            r"只要[^，。]*就[^，。]*",
            r"只有[^，。]*才[^，。]*",
            r"无论[^，。]*都[^，。]*",
            r"因为[^，。]*所以[^，。]*",
        ]
        complex_count = 0
        for pattern in complex_patterns:
            complex_count += len(re.findall(pattern, text))
        complex_ratio = complex_count / total_sentences if total_sentences > 0 else 0
        features["complex_sentence_ratio"] = complex_ratio
        
        if complex_ratio < 0.1:
            issues.append(
                {
                    "type": "low_complex_sentences",
                    "line": 0,
                    "content": f"复杂句式比例偏低（{complex_ratio:.2f}）",
                    "weight": 0.4,
                    "suggestion": "增加复杂句式（让步、条件、递进）",
                }
            )

        # 7. 第一人称使用频率（"本文"、"我们"的出现密度）
        first_person_patterns = [
            r"本文",
            r"我们",
            r"笔者认为",
            r"本研究",
        ]
        first_person_count = 0
        for pattern in first_person_patterns:
            first_person_count += len(re.findall(pattern, text))
        first_person_density = first_person_count / (total_chars / 100) if total_chars > 0 else 0
        features["first_person_density"] = first_person_density
        
        if first_person_density < 0.3:
            issues.append(
                {
                    "type": "low_first_person",
                    "line": 0,
                    "content": f"第一人称使用频率偏低（每百字{first_person_density:.1f}个）",
                    "weight": 0.5,
                    "suggestion": "增加第一人称使用（本文、我们、笔者认为）",
                }
            )

        # 计算 AI 概率
        uniformity_val = features.get("sentence_uniformity", 0)
        diversity_val = features.get("vocabulary_diversity", 0.5)
        punct_ratio_val = features.get("punctuation_ratio", 0)
        para_variance_val = features.get("paragraph_variance", 0)
        parallel_density_val = features.get("parallel_structure_density", 0)
        complex_ratio_val = features.get("complex_sentence_ratio", 0)
        first_person_density_val = features.get("first_person_density", 0)

        ai_probability = (
            uniformity_val * 0.25
            + (1 - diversity_val) * 0.25
            + (0.1 if punct_ratio_val > 0.15 else 0) * 0.15
            + (0.5 if para_variance_val < 100 else 0) * 0.15
            + min(1.0, parallel_density_val / 2.0) * 0.1  # 并列结构密度贡献
            + (0.3 if complex_ratio_val < 0.15 else 0) * 0.05  # 缺乏复杂句式贡献
            + (0.4 if first_person_density_val < 0.3 else 0) * 0.05  # 缺少第一人称贡献
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
    """基于语言学特征的检测器（增强版）"""

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
        
        # ===== 新增：过度规整表达检测 =====
        self.overly_regular_patterns = [
            {
                "pattern": r"主要包括[^，。]*",
                "name": "主要包括句式",
                "suggestion": "使用更具体的描述方式，如'核心内容涵盖'、'涉及以下要点'",
            },
            {
                "pattern": r"主要由[^，。]*组成",
                "name": "主要由...组成句式",
                "suggestion": "具体说明组成要素及其关系",
            },
            {
                "pattern": r"核心在于[^，。]*",
                "name": "核心在于句式",
                "suggestion": "直接阐述核心内容，避免'在于'的判断句式",
            },
            {
                "pattern": r"关键在于[^，。]*",
                "name": "关键在于句式",
                "suggestion": "直接说明关键因素及其作用机制",
            },
            {
                "pattern": r"旨在[^，。]*",
                "name": "旨在句式",
                "suggestion": "使用'本文探讨'、'研究目标为'等表达",
            },
            {
                "pattern": r"从[^，。]*角度(看|出发|而言)",
                "name": "从...角度句式",
                "suggestion": "明确研究视角，如'基于XX理论框架'",
            },
            {
                "pattern": r"在[^，。]*背景(下|之下)",
                "name": "在...背景下句式",
                "suggestion": "具体描述背景特征，增强时代感",
            },
        ]
        
        # ===== 新增：缺乏推导过程检测 =====
        self.direct_conclusion_patterns = [
            {
                "pattern": r"由此(可见|可知|得出|可见)[^，。]*(是|为|具有|存在)",
                "name": "直接结论句式",
                "suggestion": "补充推导过程，说明从前提如何得出此结论",
            },
            {
                "pattern": r"因此[^，。]*(?:表明|说明|证明|反映)",
                "name": "因此直接结论",
                "suggestion": "展示因果链条的中间推理步骤",
            },
            {
                "pattern": r"说明[^，。]*(问题|现象|趋势|特征)[^，。]*严重|重要|明显",
                "name": "说明...句式",
                "suggestion": "提供具体数据或案例支撑该说明",
            },
        ]
        
        # ===== 新增：人类化特征检测 =====
        self.humanization_indicators = [
            "我们认为",
            "值得注意的是",
            "令人惊讶的是",
            "有趣的是",
            "不可忽视的是",
            "必须承认",
            "客观地说",
            "从实际情况看",
            "根据经验判断",
            "某种程度上",
            " roughly speaking",
            "一定程度上",
            "或许",
            "可能",
            "似乎",
            "某种程度上而言",
            "基于现有数据",
            "从调研结果看",
            "结合实际案例",
        ]

    def detect(self, text: str) -> DetectionResult:
        """执行语言特征检测"""
        issues = []
        features = {}
        total_chars = len(text)

        # 1. 连接词密度
        connective_count = sum(text.count(c) for c in self.connectives)
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

        # ===== 新增：过度规整表达检测 =====
        overly_regular_count = 0
        overly_regular_issues = []
        for item in self.overly_regular_patterns:
            matches = re.findall(item["pattern"], text)
            count = len(matches)
            if count > 0:
                overly_regular_count += count
                overly_regular_issues.append({
                    "type": "overly_regular_expression",
                    "line": 0,
                    "content": f"检测到{item['name']}：{matches[0][:30] if matches else ''}",
                    "weight": 0.6,
                    "suggestion": item["suggestion"],
                })
        
        overly_regular_density = overly_regular_count / (total_chars / 100) if total_chars > 0 else 0
        features["overly_regular_density"] = overly_regular_density
        
        if overly_regular_count > 0:
            issues.extend(overly_regular_issues[:3])  # 最多显示3个

        # ===== 新增：缺乏推导过程检测 =====
        direct_conclusion_count = 0
        for item in self.direct_conclusion_patterns:
            matches = re.findall(item["pattern"], text)
            count = len(matches)
            if count > 0:
                direct_conclusion_count += count
                issues.append({
                    "type": "lack_of_derivation",
                    "line": 0,
                    "content": f"检测到{item['name']}：{matches[0][:30] if matches else ''}",
                    "weight": 0.5,
                    "suggestion": item["suggestion"],
                })
        
        features["direct_conclusion_count"] = direct_conclusion_count

        # ===== 新增：人类化特征检测 =====
        humanization_count = sum(text.count(indicator) for indicator in self.humanization_indicators)
        humanization_density = humanization_count / (total_chars / 100) if total_chars > 0 else 0
        features["humanization_indicator_density"] = humanization_density
        features["humanization_indicators_found"] = [
            indicator for indicator in self.humanization_indicators 
            if indicator in text
        ]

        # 计算 AI 概率
        ai_probability = (
            min(1.0, connective_density / 1.5) * 0.3
            + min(1.0, formal_density / 2.0) * 0.2
            + min(1.0, complex_count / 5) * 0.2
            + min(1.0, overly_regular_density / 1.0) * 0.2  # 过度规整表达贡献
            + min(1.0, direct_conclusion_count / 3) * 0.1   # 缺乏推导过程贡献
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
    """融合多个检测器结果（优化版）"""

    def __init__(self):
        self.detectors = {
            "rule": RuleBasedDetector(),
            "statistical": StatisticalDetector(),
            "linguistic": LinguisticDetector(),
        }
        # 调整权重：增加 linguistic 检测器权重（0.3 → 0.35）
        self.weights = {"rule": 0.35, "statistical": 0.3, "linguistic": 0.35}

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
        
        # ===== 新增：计算人类化分数 =====
        humanization_score = self._calculate_humanization_score(results, text)
        
        # ===== 新增：生成 MBA 论文特定建议 =====
        mba_suggestions = self._generate_mba_suggestions(results, text)

        return FusionResult(
            final_probability=round(weighted_prob, 3),
            method_results=results,
            consensus_level=consensus_level,
            dominant_features=dominant_features,
            priority_fixes=priority_fixes,
            humanization_score=round(humanization_score, 3),
            mba_suggestions=mba_suggestions,
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
    
    def _calculate_humanization_score(self, results: List[DetectionResult], text: str) -> float:
        """计算人类化分数（0-1，越高越像人类写作）"""
        score = 0.5  # 基础分
        
        # 从统计检测器获取特征
        statistical_features = {}
        linguistic_features = {}
        
        for r in results:
            if r.method == DetectionMethod.STATISTICAL:
                statistical_features = r.features
            elif r.method == DetectionMethod.LINGUISTIC:
                linguistic_features = r.features
        
        # 句长标准差加分（变化越大越像人类）
        std_dev = statistical_features.get("sentence_std_dev", 0)
        if std_dev > 10:
            score += 0.15
        elif std_dev > 8:
            score += 0.1
        elif std_dev > 5:
            score += 0.05
        
        # TTR 词汇丰富度加分
        ttr = statistical_features.get("vocabulary_ttr", 0.5)
        if ttr > 0.7:
            score += 0.15
        elif ttr > 0.6:
            score += 0.1
        elif ttr > 0.5:
            score += 0.05
        
        # 第一人称使用加分
        first_person_density = statistical_features.get("first_person_density", 0)
        if first_person_density > 0.8:
            score += 0.15
        elif first_person_density > 0.5:
            score += 0.1
        elif first_person_density > 0.3:
            score += 0.05
        
        # 复杂句式比例加分
        complex_ratio = statistical_features.get("complex_sentence_ratio", 0)
        if complex_ratio > 0.25:
            score += 0.1
        elif complex_ratio > 0.15:
            score += 0.05
        
        # 人类化指示词加分
        humanization_density = linguistic_features.get("humanization_indicator_density", 0)
        if humanization_density > 0.5:
            score += 0.15
        elif humanization_density > 0.3:
            score += 0.1
        elif humanization_density > 0.1:
            score += 0.05
        
        # 并列结构密度减分（过高是AI特征）
        parallel_density = statistical_features.get("parallel_structure_density", 0)
        if parallel_density > 2:
            score -= 0.15
        elif parallel_density > 1.5:
            score -= 0.1
        
        return min(1.0, max(0.0, score))
    
    def _generate_mba_suggestions(self, results: List[DetectionResult], text: str) -> List[str]:
        """生成 MBA 论文特定建议"""
        suggestions = []
        
        # 获取各检测器特征
        statistical_features = {}
        linguistic_features = {}
        
        for r in results:
            if r.method == DetectionMethod.STATISTICAL:
                statistical_features = r.features
            elif r.method == DetectionMethod.LINGUISTIC:
                linguistic_features = r.features
        
        # MBA论文特定建议
        first_person_density = statistical_features.get("first_person_density", 0)
        if first_person_density < 0.3:
            suggestions.append("建议使用第一人称（本文、我们、笔者认为）增强主观性和研究立场")
        
        parallel_density = statistical_features.get("parallel_structure_density", 0)
        if parallel_density > 1.0:
            suggestions.append("MBA论文建议减少机械式并列结构(1)(2)(3)，改用更有层次感的论述方式")
        
        complex_ratio = statistical_features.get("complex_sentence_ratio", 0)
        if complex_ratio < 0.15:
            suggestions.append("建议增加复杂句式（让步、转折、条件句），体现商业分析的辩证思维")
        
        overly_regular_density = linguistic_features.get("overly_regular_density", 0)
        if overly_regular_density > 0.5:
            suggestions.append("避免'主要包括'、'核心在于'等模板化表达，使用MBA案例分析的实证语言")
        
        humanization_density = linguistic_features.get("humanization_indicator_density", 0)
        if humanization_density < 0.2:
            suggestions.append("增加研究者主观判断表达（如'我们认为'、'值得关注的是'），体现管理洞察")
        
        # 默认建议
        if not suggestions:
            suggestions.append("当前文本符合MBA论文写作风格，建议保持并继续优化实证数据支撑")
        
        return suggestions


def generate_modification_plan(fusion_result: FusionResult, text: str) -> Dict:
    """生成修改计划（增强版）"""
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
        "evaluation_criteria": {},  # 新增：评估标准
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
            # 新增步骤
            "6. 增加第一人称使用（本文、我们、笔者认为）增强主观性",
            "7. 打破并列结构，改用递进关系论述",
            "8. 增加复杂句式（让步、条件、递进）体现辩证思维",
        ]
    elif fusion_result.final_probability > 0.4:
        plan["modification_strategy"] = "中度修改 - 针对性优化"
        plan["estimated_time"] = "1-2小时"
        plan["steps"] = [
            "1. 修复高优先级的 AI 特征问题",
            "2. 调整明显的套话和模板化表达",
            "3. 补充关键数据支撑",
            "4. 修正空格和标点问题",
            # 新增步骤
            "5. 适度增加第一人称表达",
            "6. 优化句式结构，增加复杂句式",
        ]
    else:
        plan["modification_strategy"] = "轻度润色 - 细节优化"
        plan["estimated_time"] = "30分钟-1小时"
        plan["steps"] = [
            "1. 检查并修复少量 AI 痕迹", 
            "2. 优化语言表达", 
            "3. 最终校对",
            # 新增建议
            "4. 可考虑增加个性化表达提升自然度",
        ]

    # 新增：评估标准对照
    plan["evaluation_criteria"] = {
        "ai_detection_rate": {
            "target": "< 20%",
            "current": f"{fusion_result.final_probability * 100:.1f}%",
            "status": "✅ 达标" if fusion_result.final_probability < 0.2 else "⚠️ 未达标",
        },
        "sentence_std_dev": {
            "target": "> 8",
            "description": "句长标准差，反映句式变化程度",
            "status": "检测中",
        },
        "vocabulary_ttr": {
            "target": "> 0.6",
            "description": "词汇丰富度（Type-Token Ratio）",
            "status": "检测中",
        },
        "humanization_score": {
            "target": "> 0.6",
            "current": f"{fusion_result.humanization_score:.2f}",
            "description": "人类化写作特征综合评分",
            "status": "✅ 良好" if fusion_result.humanization_score > 0.6 else "⚠️ 需提升",
        },
    }
    
    # 从检测结果中填充实际值
    for result in fusion_result.method_results:
        if result.method == DetectionMethod.STATISTICAL:
            std_dev = result.features.get("sentence_std_dev", 0)
            ttr = result.features.get("vocabulary_ttr", 0)
            plan["evaluation_criteria"]["sentence_std_dev"]["current"] = f"{std_dev:.2f}"
            plan["evaluation_criteria"]["sentence_std_dev"]["status"] = "✅ 达标" if std_dev > 8 else "⚠️ 未达标"
            plan["evaluation_criteria"]["vocabulary_ttr"]["current"] = f"{ttr:.3f}"
            plan["evaluation_criteria"]["vocabulary_ttr"]["status"] = "✅ 达标" if ttr > 0.6 else "⚠️ 未达标"

    # 添加具体修改建议
    plan["priority_fixes"] = fusion_result.priority_fixes
    
    # 新增：MBA论文特定建议
    plan["mba_specific_suggestions"] = fusion_result.mba_suggestions

    return plan


def format_enhanced_report(fusion_result: FusionResult, text: str) -> str:
    """生成增强版 Markdown 报告"""
    plan = generate_modification_plan(fusion_result, text)

    md = f"""# AI 特征多维度检测报告

## 综合评估

- **AI 生成概率**: {fusion_result.final_probability * 100:.1f}%
- **人类化分数**: {fusion_result.humanization_score * 100:.1f}% {"✅" if fusion_result.humanization_score > 0.6 else "⚠️"}
- **风险等级**: {"🔴 高风险" if plan["risk_level"] == "high" else "🟡 中风险" if plan["risk_level"] == "medium" else "🟢 低风险"}
- **检测器一致性**: {fusion_result.consensus_level.upper()}
- **建议修改策略**: {plan["modification_strategy"]}
- **预计修改时间**: {plan["estimated_time"]}

## 评估标准对照表

| 指标 | 目标值 | 当前值 | 状态 | 说明 |
|------|--------|--------|------|------|
| AI检测率 | < 20% | {plan["evaluation_criteria"]["ai_detection_rate"]["current"]} | {plan["evaluation_criteria"]["ai_detection_rate"]["status"]} | 综合AI生成概率 |
| 句长标准差 | > 8 | {plan["evaluation_criteria"]["sentence_std_dev"].get("current", "N/A")} | {plan["evaluation_criteria"]["sentence_std_dev"]["status"]} | 反映句式变化程度 |
| 词汇丰富度TTR | > 0.6 | {plan["evaluation_criteria"]["vocabulary_ttr"].get("current", "N/A")} | {plan["evaluation_criteria"]["vocabulary_ttr"]["status"]} | Type-Token Ratio |
| 人类化分数 | > 0.6 | {plan["evaluation_criteria"]["humanization_score"]["current"]} | {plan["evaluation_criteria"]["humanization_score"]["status"]} | 人类写作特征综合评分 |

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
                elif isinstance(v, list):
                    md += f"  - {k}: {len(v)} 项\n"
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
## MBA论文特定建议

"""
    for i, suggestion in enumerate(plan["mba_specific_suggestions"], 1):
        md += f"{i}. {suggestion}\n"

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
*报告由多维度 AI 检测系统生成（增强版 v2.0）*
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
                    "humanization_score": fusion_result.humanization_score,
                    "consensus_level": fusion_result.consensus_level,
                    "dominant_features": fusion_result.dominant_features,
                    "priority_fixes": fusion_result.priority_fixes,
                    "mba_suggestions": fusion_result.mba_suggestions,
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
    print(f"  - 人类化分数: {fusion_result.humanization_score * 100:.1f}%")
    print(f"  - 风险等级: {plan['risk_level'].upper()}")
    print(f"  - 检测器一致性: {fusion_result.consensus_level}")
    print(f"  - 建议修改策略: {plan['modification_strategy']}")
    print(f"  - 预计时间: {plan['estimated_time']}")
    
    # 显示MBA建议
    if fusion_result.mba_suggestions:
        print(f"\n💡 MBA论文建议:")
        for suggestion in fusion_result.mba_suggestions[:3]:
            print(f"  • {suggestion}")

    # 交互模式
    if args.interactive and fusion_result.priority_fixes:
        print("\n📝 交互式修改建议:")
        for i, fix in enumerate(fusion_result.priority_fixes[:3], 1):
            print(f"\n{i}. [{fix['priority'].upper()}] {fix['issue_type']}")
            print(f"   示例: {fix['example'][:50]}...")
            print(f"   建议: {fix['suggestion']}")


if __name__ == "__main__":
    main()
