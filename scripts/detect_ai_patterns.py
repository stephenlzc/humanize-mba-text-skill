#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 写作特征检测工具
用于检测中文文本中的 AI 生成特征，特别是 MBA 论文风格的文本。

使用方法:
    python detect_ai_patterns.py input.txt
    python detect_ai_patterns.py input.txt --output report.json
    python detect_ai_patterns.py input.txt --format markdown
"""

import re
import sys
import json
import argparse
import math
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Tuple, Optional
from collections import Counter


@dataclass
class PatternMatch:
    """匹配到的 AI 特征"""

    pattern_name: str
    pattern_type: str
    line_number: int
    content: str
    suggestion: str
    severity: str  # high, medium, low


@dataclass
class DetectionMetrics:
    """检测指标数据类"""

    parallel_structure_count: int = 0  # 并列结构数量
    connector_density: float = 0.0  # 逻辑连接词密度（每百字）
    sentence_length_std: float = 0.0  # 平均句长标准差
    first_person_ratio: float = 0.0  # 第一人称使用比例


class AIPatternDetector:
    """AI 写作特征检测器"""

    def __init__(self):
        # 定义检测规则
        self.patterns = {
            # 1. 过度强调类
            "exaggerated_emphasis": {
                "name": "过度强调",
                "patterns": [
                    r"关键[的是|在于|作用|意义]",
                    r"重要[的是|意义|价值|作用]",
                    r"核心[竞争力|要素|能力|优势]",
                    r"灵魂人物",
                    r"绝对[是|的]",
                    r"至关重要",
                    r"不可或缺",
                ],
                "suggestion": "删除价值判断词汇，直接陈述事实",
                "severity": "medium",
            },
            # 2. 宏观叙事类
            "macro_narrative": {
                "name": "宏观叙事",
                "patterns": [
                    r"推动[^，。]+变革",
                    r"时代[的|背景|意义]",
                    r"历史[的|进程|意义]",
                    r"趋势[表明|显示|说明]",
                    r"战略[高度|意义|价值]",
                ],
                "suggestion": "聚焦具体研究对象和实证数据",
                "severity": "medium",
            },
            # 3. 表面分析类 (-ing 结尾)
            "surface_analysis": {
                "name": "表面分析",
                "patterns": [
                    r"凸显[了|出][^，。]*[重要性|价值|意义]",
                    r"反映[了|出][^，。]*[问题|趋势|特征]",
                    r"体现[了|出][^，。]*[价值|意义|作用]",
                    r"表明[了|][^，。]*[重要性|必要性]",
                    r"揭示[了|出][^，。]*[规律|本质]",
                ],
                "suggestion": "提供具体机制解释或数据支撑",
                "severity": "high",
            },
            # 4. 模糊归因类
            "vague_attribution": {
                "name": "模糊归因",
                "patterns": [
                    r"[有|据|相关]研究[表明|指出|显示|发现]",
                    r"专家[指出|认为|表示|强调]",
                    r"学者[普遍认为|研究发现]",
                    r"数据[显示|表明]",
                    r"普遍[认为|看来|认同]",
                    r"分析[指出|认为]",
                ],
                "suggestion": "明确引用具体文献或删除此类表述",
                "severity": "high",
            },
            # 5. AI 词汇类（已增强）
            "ai_buzzwords": {
                "name": "AI 词汇",
                "patterns": [
                    # 原有词汇
                    r"赋能",
                    r"抓手",
                    r"闭环",
                    r"落地",
                    r"痛点",
                    r"打法",
                    r"赛道",
                    r"生态[系统|圈|链]",
                    r"迭代",
                    r"协同",
                    r"整合",
                    r"优化",
                    r"升级",
                    r"转型[升级]?",
                    # 新增词汇（来自参考仓库策略）
                    r"重构",
                    r"解耦",
                    r"调制",
                    r"嵌入",
                    r"聚合",
                    r"瓶颈",
                    r"挑战",
                    r"机制",
                    r"架构",
                    r"框架",
                    r"显著",
                    r"优异",
                    r"高效",
                    r"精准",
                ],
                "suggestion": "使用传统学术词汇替代",
                "severity": "high",
            },
            # 6. 连接词过多
            "excessive_connectors": {
                "name": "连接词过多",
                "patterns": [
                    r"首先[^，。]*其次[^，。]*最后",
                    r"第一[^，。]*第二[^，。]*第三",
                    r"此外[^，。]*另外[^，。]*与此同时",
                    r"综上所述[^，。]*因此",
                    r"值得注意的是[^，。]*",
                    r"需要指出的是[^，。]*",
                    r"由此可见[^，。]*",
                ],
                "suggestion": "减少连接词，使用更自然的过渡",
                "severity": "medium",
            },
            # 7. 否定式排比
            "negative_parallelism": {
                "name": "否定式排比",
                "patterns": [
                    r"不仅[^，。]*而且[^，。]*",
                    r"既不是[^，。]*也不是[^，。]*",
                    r"不仅[^，。]*还[^，。]*",
                    r"无论[^，。]*还是[^，。]*",
                ],
                "suggestion": "拆分为简单句或直接陈述",
                "severity": "low",
            },
            # 8. 破折号过度使用
            "dash_overuse": {
                "name": "破折号过度使用",
                "pattern": r"——",
                "suggestion": "使用逗号或括号替代破折号",
                "severity": "low",
                "count_threshold": 3,  # 超过3个才报告
            },
            # 9. 宣传性语言
            "promotional_language": {
                "name": "宣传性语言",
                "patterns": [
                    r"卓越[的|性能|表现]",
                    r"显著[的|成效|提升|改善]",
                    r"突出[的|贡献|成绩]",
                    r"优秀[的|表现|成果]",
                    r"巨大[的|成功|成就]",
                ],
                "suggestion": "使用客观描述性词汇",
                "severity": "medium",
            },
            # 10. 套话式表达
            "cliche_phrases": {
                "name": "套话式表达",
                "patterns": [
                    r"尽管[^，。]*面临挑战[^，。]*但[^，。]*前景",
                    r"在[^，。]*背景下",
                    r"随着[^，。]*的发展",
                    r"基于以上分析[^，。]*",
                    r"通过[^，。]*可以发现",
                ],
                "suggestion": "具体问题具体分析，避免套话",
                "severity": "medium",
            },
            # 11. 列表式行文
            "list_style": {
                "name": "列表式行文",
                "pattern": r"^[\s]*[•\-\*·]\s+\*\*[^*]+\*\*[:：]",
                "suggestion": "将列表转化为连贯的叙述性段落",
                "severity": "medium",
                "multiline": True,
            },
            # 12. 新增：句式特征检测
            "sentence_patterns": {
                "name": "规整句式特征",
                "patterns": [
                    # 过度规整的并列结构
                    r"主要贡献包括[^：]*：\s*\(?1\)?[^，。]*\(?2\)?[^，。]*\(?3\)?",
                    r"主要工作如下[^：]*：\s*\(?1\)?[^，。]*\(?2\)?[^，。]*\(?3\)?",
                    # 过于完美的逻辑闭环
                    r"问题[^，。]*存在[^，。]*方法[^，。]*解决[^，。]*因此[^，。]*提出[^，。]*实验[^，。]*证明",
                    # 缺乏推导过程
                    r"本文直接提出了",
                    r"本研究直接采用",
                    # 规整的段落结构
                    r"为了[^，。]*，本文[^，。]*。具体而言[^，。]*",
                ],
                "suggestion": "打破规整结构，使用长短句交替，添加推理过程",
                "severity": "high",
            },
            # 13. 新增：学术表达检测
            "academic_formality": {
                "name": "学术表达问题",
                "patterns": [
                    # 纯客观陈述模式（缺乏作者视角）
                    r"实验结果显示[^。]*(?:MSE|MAE|准确率|精度|召回率|F1)[^为]*为[\d.]+",
                    r"结果表明[^，。]*达到[\d.]+%",
                    # 过度使用被动语态标记
                    r"被[用于|应用于|证明|验证|用来]",
                ],
                "suggestion": "添加作者视角，使用'我们发现'等主观表述，解释数据意义",
                "severity": "medium",
            },
        }

        # 章节特定规则（已增强）
        self.chapter_patterns = {
            "literature_review": {
                "name": "文献综述特征",
                "patterns": [
                    r"\w+\(\d{4}\)[^，。]*认为[^，。]*",
                    r"\w+\(\d{4}\)[^，。]*指出[^，。]*",
                    r"大量研究[表明|显示|证明]",
                    r"现有研究[主要|多|大多]",
                ],
                "suggestion": "按主题组织，进行比较分析，指出研究空白",
                "severity": "medium",
            },
            "case_analysis": {
                "name": "案例分析特征",
                "patterns": [
                    r"该公司成立于\d+年",
                    r"总部位于[^，。]+",
                    r"员工\d+人",
                    r"年营收[^，。]*亿元",
                    r"由此可见[^，。]*",
                ],
                "suggestion": "精简背景，聚焦研究问题，提供具体数据",
                "severity": "medium",
            },
            "strategy": {
                "name": "战略建议特征",
                "patterns": [
                    r"建议[^，。]*加强[^，。]*",
                    r"建议[^，。]*优化[^，。]*",
                    r"建议[^，。]*提升[^，。]*",
                    r"通过这些措施[^，。]*",
                ],
                "suggestion": "建议具体可操作，考虑约束条件，明确优先级",
                "severity": "high",
            },
            # 新增：摘要章节检测
            "abstract": {
                "name": "摘要AI特征",
                "patterns": [
                    r"本文针对[^，。]*问题[^，。]*提出了",
                    r"本文研究了[^，。]*",
                    r"结果表明[^，。]*",
                    r"本文的主要贡献",
                    r"实验结果表明[^，。]*",
                ],
                "suggestion": "摘要应简洁明了，避免模板化表述，突出核心创新",
                "severity": "medium",
            },
            # 新增：方法论章节检测
            "methodology": {
                "name": "方法描述模板化",
                "patterns": [
                    r"该模块包含[^，。]*组件",
                    r"本方法分为[^，。]*步骤",
                    r"首先[^，。]*然后[^，。]*最后[^，。]*",
                    r"第一阶段[^，。]*第二阶段[^，。]*第三阶段",
                    r"输入[^，。]*经过[^，。]*输出",
                ],
                "suggestion": "方法描述应突出创新点，解释设计决策原因，避免纯流程化叙述",
                "severity": "medium",
            },
        }

        # 逻辑连接词列表（用于计算密度）
        self.connector_words = [
            "首先", "其次", "最后", "第一", "第二", "第三", "此外", "另外",
            "与此同时", "综上所述", "因此", "值得注意的是", "需要指出的是",
            "由此可见", "然而", "但是", "因此", "所以", "由于", "因为",
            "虽然", "尽管", "即使", "不过", "可是", "因而", "从而",
            "进而", "继而", "于是", "然后", "接着", "随后", "最终",
        ]

        # 第一人称表述（用于检测作者视角）
        self.first_person_patterns = [
            r"本文",
            r"我们",
            r"本研究",
            r"笔者",
            r"我发现",
            r"我们认为",
        ]

    def detect_spacing_issues(self, text: str) -> List[PatternMatch]:
        """检测中英文/数字混排空格问题"""
        matches = []
        lines = text.split("\n")

        # 中文后接英文/数字有空格
        pattern1 = re.compile(r"([\u4e00-\u9fff])\s+([a-zA-Z0-9])")
        # 英文/数字后接中文有空格
        pattern2 = re.compile(r"([a-zA-Z0-9])\s+([\u4e00-\u9fff])")

        for line_num, line in enumerate(lines, 1):
            # 检查中文后空格
            for match in pattern1.finditer(line):
                matches.append(
                    PatternMatch(
                        pattern_name="中英文混排空格",
                        pattern_type="spacing",
                        line_number=line_num,
                        content=match.group(0),
                        suggestion=f"删除空格：{match.group(1)}{match.group(2)}",
                        severity="high",
                    )
                )

            # 检查英文后空格
            for match in pattern2.finditer(line):
                matches.append(
                    PatternMatch(
                        pattern_name="中英文混排空格",
                        pattern_type="spacing",
                        line_number=line_num,
                        content=match.group(0),
                        suggestion=f"删除空格：{match.group(1)}{match.group(2)}",
                        severity="high",
                    )
                )

        return matches

    def detect_patterns(self, text: str) -> List[PatternMatch]:
        """检测所有 AI 写作特征"""
        matches = []
        lines = text.split("\n")

        # 检测通用模式
        for pattern_id, pattern_info in self.patterns.items():
            if "pattern" in pattern_info:
                # 单个模式
                pattern = re.compile(pattern_info["pattern"])
                for line_num, line in enumerate(lines, 1):
                    for match in pattern.finditer(line):
                        # 检查阈值
                        if "count_threshold" in pattern_info:
                            count = len(pattern.findall(text))
                            if count <= pattern_info["count_threshold"]:
                                continue

                        matches.append(
                            PatternMatch(
                                pattern_name=pattern_info["name"],
                                pattern_type=pattern_id,
                                line_number=line_num,
                                content=match.group(0)[:50],
                                suggestion=pattern_info["suggestion"],
                                severity=pattern_info["severity"],
                            )
                        )
            else:
                # 多个模式
                for sub_pattern in pattern_info["patterns"]:
                    pattern = re.compile(sub_pattern)
                    for line_num, line in enumerate(lines, 1):
                        for match in pattern.finditer(line):
                            matches.append(
                                PatternMatch(
                                    pattern_name=pattern_info["name"],
                                    pattern_type=pattern_id,
                                    line_number=line_num,
                                    content=match.group(0)[:50],
                                    suggestion=pattern_info["suggestion"],
                                    severity=pattern_info["severity"],
                                )
                            )

        # 检测空格问题
        spacing_matches = self.detect_spacing_issues(text)
        matches.extend(spacing_matches)

        return matches

    def calculate_metrics(self, text: str) -> DetectionMetrics:
        """
        计算检测指标
        
        新增指标：
        - 并列结构数量
        - 逻辑连接词密度（每百字）
        - 平均句长标准差
        - 第一人称使用比例
        """
        metrics = DetectionMetrics()
        
        # 1. 计算并列结构数量
        parallel_patterns = [
            r"不仅[^，。]*而且",
            r"既[^，。]*又",
            r"一边[^，。]*一边",
            r"一方面[^，。]*另一方面",
            r"首先[^，。]*其次",
            r"第一[^，。]*第二",
            r"首先[^，。]*然后[^，。]*最后",
        ]
        parallel_count = 0
        for pattern in parallel_patterns:
            parallel_count += len(re.findall(pattern, text))
        metrics.parallel_structure_count = parallel_count
        
        # 2. 计算逻辑连接词密度（每百字）
        total_chars = len(text.replace(" ", "").replace("\n", ""))
        connector_count = 0
        for connector in self.connector_words:
            connector_count += len(re.findall(connector, text))
        if total_chars > 0:
            metrics.connector_density = round((connector_count / total_chars) * 100, 2)
        
        # 3. 计算平均句长标准差
        sentences = re.split(r'[。！？；]', text)
        sentence_lengths = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                length = len(sentence)
                sentence_lengths.append(length)
        
        if len(sentence_lengths) > 1:
            mean_length = sum(sentence_lengths) / len(sentence_lengths)
            variance = sum((x - mean_length) ** 2 for x in sentence_lengths) / len(sentence_lengths)
            metrics.sentence_length_std = round(math.sqrt(variance), 2)
        
        # 4. 计算第一人称使用比例
        first_person_count = 0
        for pattern in self.first_person_patterns:
            first_person_count += len(re.findall(pattern, text))
        
        # 估算总句数
        total_sentences = len([s for s in sentences if s.strip()])
        if total_sentences > 0:
            metrics.first_person_ratio = round((first_person_count / total_sentences) * 100, 2)
        
        return metrics

    def analyze_chapter_type(self, text: str) -> str:
        """分析文本最可能属于哪个章节"""
        scores = {}

        for chapter_type, chapter_info in self.chapter_patterns.items():
            score = 0
            for pattern in chapter_info["patterns"]:
                matches = re.findall(pattern, text)
                score += len(matches)
            scores[chapter_type] = score

        if not scores or max(scores.values()) == 0:
            return "general"

        return str(max(scores.items(), key=lambda x: x[1])[0])

    def generate_report(self, text: str, matches: List[PatternMatch]) -> Dict:
        """生成检测报告"""
        # 统计各类问题数量
        severity_counts = Counter([m.severity for m in matches])
        type_counts = Counter([m.pattern_name for m in matches])

        # 检测章节类型
        chapter_type = self.analyze_chapter_type(text)
        chapter_names = {
            "general": "一般文本",
            "literature_review": "文献综述",
            "case_analysis": "案例分析",
            "strategy": "战略建议",
            "abstract": "摘要",
            "methodology": "方法论",
        }
        
        # 计算新增指标
        metrics = self.calculate_metrics(text)

        report = {
            "summary": {
                "total_issues": len(matches),
                "high_severity": severity_counts.get("high", 0),
                "medium_severity": severity_counts.get("medium", 0),
                "low_severity": severity_counts.get("low", 0),
                "detected_chapter": chapter_names.get(chapter_type, "一般文本"),
                "ai_score": self._calculate_ai_score(matches, len(text)),
            },
            "metrics": {
                "parallel_structure_count": metrics.parallel_structure_count,
                "connector_density": metrics.connector_density,
                "sentence_length_std": metrics.sentence_length_std,
                "first_person_ratio": metrics.first_person_ratio,
            },
            "issue_types": dict(type_counts.most_common(10)),
            "matches": [asdict(m) for m in matches],
            "chapter_specific_advice": self._get_chapter_advice(chapter_type),
        }

        return report

    def _calculate_ai_score(
        self, matches: List[PatternMatch], text_length: int
    ) -> float:
        """计算 AI 特征分数 (0-100)"""
        if text_length == 0:
            return 0

        # 基于问题密度和严重程度计算
        severity_weights = {"high": 3, "medium": 2, "low": 1}
        weighted_count = sum(severity_weights.get(m.severity, 1) for m in matches)

        # 归一化到 0-100
        score = min(100, (weighted_count / (text_length / 100)) * 10)
        return round(score, 1)

    def _get_chapter_advice(self, chapter_type: str) -> str:
        """获取章节特定建议"""
        advice = {
            "literature_review": "本文本疑似文献综述章节。建议：1)按主题组织而非按作者罗列；2)进行比较分析而非简单陈述；3)明确指出研究空白。",
            "case_analysis": "本文本疑似案例分析章节。建议：1)精简背景信息，聚焦研究问题；2)提供具体数据和时间节点；3)分析因果机制。",
            "strategy": "本文本疑似战略建议章节。建议：1)确保建议具体可操作；2)考虑资源和能力约束；3)明确实施阶段和优先级。",
            "abstract": "本文本疑似摘要章节。建议：1)避免'本文针对...问题...提出了'等模板化表述；2)直接陈述研究内容和核心发现；3)控制字数，突出创新点。",
            "methodology": "本文本疑似方法论章节。建议：1)突出方法创新点而非流程描述；2)解释设计决策的原因；3)使用自然语言描述算法步骤。",
            "general": "请根据实际章节类型参考相应的改写规则。",
        }
        return advice.get(chapter_type, advice["general"])


def format_markdown_report(report: Dict) -> str:
    """格式化为 Markdown 报告"""
    summary = report["summary"]
    metrics = report.get("metrics", {})

    md = f"""# AI 写作特征检测报告

## 摘要

- **检测文本类型**: {summary["detected_chapter"]}
- **AI 特征分数**: {summary["ai_score"]}/100 (分数越高 AI 痕迹越明显)
- **发现问题总数**: {summary["total_issues"]}
  - 严重: {summary["high_severity"]}
  - 中等: {summary["medium_severity"]}
  - 轻微: {summary["low_severity"]}

## 新增检测指标

| 指标 | 数值 | 说明 |
|-----|------|------|
| 并列结构数量 | {metrics.get("parallel_structure_count", "N/A")} | 规整并列句式计数 |
| 逻辑连接词密度 | {metrics.get("connector_density", "N/A")}% | 每百字连接词数量 |
| 句长标准差 | {metrics.get("sentence_length_std", "N/A")} | 句式多样性指标(>8为佳) |
| 第一人称比例 | {metrics.get("first_person_ratio", "N/A")}% | 作者视角使用频率 |

## 章节特定建议

{report["chapter_specific_advice"]}

## 问题类型分布

| 问题类型 | 出现次数 |
|---------|---------|
"""

    for issue_type, count in report["issue_types"].items():
        md += f"| {issue_type} | {count} |\n"

    md += """
## 详细问题列表

| 行号 | 严重程度 | 问题类型 | 内容片段 | 修改建议 |
|-----|---------|---------|---------|---------|
"""

    for match in report["matches"][:50]:  # 最多显示50条
        content = match["content"][:30].replace("|", "\\|")
        suggestion = match["suggestion"][:40].replace("|", "\\|")
        md += f"| {match['line_number']} | {match['severity']} | {match['pattern_name']} | {content}... | {suggestion}... |\n"

    if len(report["matches"]) > 50:
        md += f"\n*还有 {len(report['matches']) - 50} 条未显示*\n"

    md += """
## 改写建议

1. **优先处理严重问题**: 先修改标记为"严重"的 AI 特征
2. **关注空格问题**: 中英文/数字混排空格最容易修复
3. **按章节规则改写**: 参考章节特定规则进行针对性修改
4. **提升句式多样性**: 参考句长标准差指标，增加长短句交替
5. **添加作者视角**: 适当增加"本文""我们"等第一人称表述
6. **通读润色**: 修改后通读全文，确保语言自然流畅

---
*报告生成时间: 自动检测*
"""

    return md


def main():
    parser = argparse.ArgumentParser(
        description="检测中文文本中的 AI 写作特征",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python detect_ai_patterns.py input.txt
    python detect_ai_patterns.py input.txt --output report.json
    python detect_ai_patterns.py input.txt --format markdown --output report.md
        """,
    )

    parser.add_argument("input_file", help="输入文本文件路径")
    parser.add_argument("--output", "-o", help="输出报告文件路径")
    parser.add_argument(
        "--format",
        "-f",
        choices=["json", "markdown"],
        default="json",
        help="输出格式 (默认: json)",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细信息")

    args = parser.parse_args()

    # 读取输入文件
    try:
        with open(args.input_file, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"错误: 文件不存在 - {args.input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: 无法读取文件 - {e}")
        sys.exit(1)

    # 检测
    detector = AIPatternDetector()
    matches = detector.detect_patterns(text)
    report = detector.generate_report(text, matches)

    # 格式化输出
    if args.format == "markdown":
        output = format_markdown_report(report)
    else:
        output = json.dumps(report, ensure_ascii=False, indent=2)

    # 输出结果
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"报告已保存至: {args.output}")
        except Exception as e:
            print(f"错误: 无法保存报告 - {e}")
            sys.exit(1)
    else:
        print(output)

    # 简要统计
    if args.verbose or not args.output:
        summary = report["summary"]
        metrics = report.get("metrics", {})
        print(f"\n检测完成:")
        print(f"  - AI 特征分数: {summary['ai_score']}/100")
        print(f"  - 检测文本类型: {summary['detected_chapter']}")
        print(
            f"  - 发现问题: {summary['total_issues']} (严重: {summary['high_severity']}, 中等: {summary['medium_severity']}, 轻微: {summary['low_severity']})"
        )
        print(f"\n新增指标:")
        print(f"  - 并列结构数量: {metrics.get('parallel_structure_count', 'N/A')}")
        print(f"  - 逻辑连接词密度: {metrics.get('connector_density', 'N/A')}%")
        print(f"  - 句长标准差: {metrics.get('sentence_length_std', 'N/A')} (>8为佳)")
        print(f"  - 第一人称比例: {metrics.get('first_person_ratio', 'N/A')}%")


if __name__ == "__main__":
    main()
