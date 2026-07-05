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
from dataclasses import dataclass, asdict
from typing import List, Dict
from collections import Counter

try:
    from rule_loader import iter_regex_categories, load_rules  # noqa: F401
    from analyzers import (  # noqa: F401
        run_prose_analyzers,
        run_semantic_chain_analyzers,
        build_modify_plan,
    )
    from analyzers._types import AnalyzerIssue  # noqa: F401
except ImportError:  # imported as package during tests
    from scripts.rule_loader import iter_regex_categories, load_rules  # noqa: F401
    from scripts.analyzers import (
        run_prose_analyzers,
        run_semantic_chain_analyzers,
        build_modify_plan,
    )
    from scripts.analyzers._types import AnalyzerIssue


# Title shown in the matches table / feedback report for issues produced by
# the prose-structure analyzers (dimensions 6, 8, 9, 10, chapter-template).
PROSE_ANALYZER_LABEL = "结构统计"
# Title used for issues raised by the semantic-chain analyzers (dimensions 3, 4, 5).
CHAIN_ANALYZER_LABEL = "语义链统计"


# Translate an AnalyzerIssue into a PatternMatch so it flows through the
# existing report and scoring pipeline. Defined lazily as a plain function;
# PatternMatch itself is defined below.
def _prose_issue_to_match(issue):  # type: ignore[no-untyped-def]
    from dataclasses import asdict  # noqa: F401  (kept for compatibility)

    # Late import to avoid forwarding reference; the dataclass is defined next.
    return _PATTERN_MATCH_FACTORY(
        pattern_name=PROSE_ANALYZER_LABEL,
        pattern_type=issue.analyzer_id,
        line_number=0,
        content=issue.evidence[:60],
        suggestion=issue.suggestion,
        severity=issue.severity,
    )


def _chain_issue_to_match(issue):  # type: ignore[no-untyped-def]
    """Translate a semantic-chain AnalyzerIssue into the same PatternMatch shape.

    Chain issues cover cross-paragraph / cross-chapter patterns (dimensions 3,
    4, 5). They flow through the same scoring pipeline as prose issues but use
    a separate label so the matches table distinguishes the two stages.
    """
    return _PATTERN_MATCH_FACTORY(
        pattern_name=CHAIN_ANALYZER_LABEL,
        pattern_type=issue.analyzer_id,
        line_number=0,
        content=issue.evidence[:60],
        suggestion=issue.suggestion,
        severity=issue.severity,
    )


# Forward declaration: bound below once PatternMatch exists. Using a small
# factory indirection keeps the import order clean.
_PATTERN_MATCH_FACTORY = None  # set after PatternMatch class is defined.


@dataclass
class PatternMatch:
    """匹配到的 AI 特征"""

    pattern_name: str
    pattern_type: str
    line_number: int
    content: str
    suggestion: str
    severity: str  # high, medium, low


# Now that PatternMatch exists, bind the factory used by _prose_issue_to_match.
_PATTERN_MATCH_FACTORY = PatternMatch


@dataclass
class DetectionMetrics:
    """检测指标数据类"""

    parallel_structure_count: int = 0  # 并列结构数量
    connector_density: float = 0.0  # 逻辑连接词密度（每百字）
    sentence_length_std: float = 0.0  # 平均句长标准差
    first_person_ratio: float = 0.0  # 第一人称使用比例


class AIPatternDetector:
    """AI 写作特征检测器"""

    def __init__(self, rule_path=None):
        self.rules = load_rules(rule_path)
        self.patterns = self._load_patterns_from_rules(self.rules)
        self.chapter_patterns = self._load_chapter_patterns(self.rules)
        metrics = self.rules.get("metrics", {})
        self.connector_words = metrics.get("connector_words", [])
        self.first_person_patterns = metrics.get("first_person_patterns", [])
        self.parallel_patterns = metrics.get("parallel_patterns", [])

    def _load_patterns_from_rules(self, rules: Dict) -> Dict:
        """Load all AI-trace regex patterns from the shared TOML rule file."""
        patterns = {}
        for category in rules.get("categories", []):
            if not category.get("regex_patterns"):
                continue
            patterns[category["id"]] = {
                "name": category["name"],
                "patterns": category["regex_patterns"],
                "suggestion": "；".join(category["rewrite_principles"]),
                "severity": category["severity"],
                "weight": category.get("weight", 0.5),
                "count_threshold": category.get("count_threshold"),
                "multiline": category.get("multiline", False),
            }
        return patterns

    def _load_chapter_patterns(self, rules: Dict) -> Dict:
        """Load chapter-specific helper patterns from TOML."""
        patterns = {}
        for category in rules.get("chapter_categories", []):
            patterns[category["id"]] = {
                "name": category["name"],
                "patterns": category.get("regex_patterns", []),
                "suggestion": category.get("suggestion", ""),
                "severity": category.get("severity", "medium"),
            }
        return patterns

    def _match_suggestion(self, pattern_id: str, pattern_info: Dict, match) -> str:
        """Return a contextual suggestion for one regex match."""
        if pattern_id == "mixed_spacing" and match.lastindex and match.lastindex >= 2:
            return f"删除空格：{match.group(1)}{match.group(2)}"
        return pattern_info["suggestion"]

    def detect_patterns(self, text: str) -> List[PatternMatch]:
        """检测所有 AI 写作特征。

        Returns regex matches **plus** issues raised by the prose-structure
        analyzers (sentence length, paragraph length, paragraph edges, paragraph
        structure, chapter template). Both kinds flow into the same report.
        """
        matches = []
        lines = text.split("\n")
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
                # 多个模式（来自 TOML）
                flags = re.MULTILINE if pattern_info.get("multiline") else 0
                for sub_pattern in pattern_info["patterns"]:
                    pattern = re.compile(sub_pattern, flags)
                    count_threshold = pattern_info.get("count_threshold")
                    if count_threshold is not None and len(pattern.findall(text)) <= count_threshold:
                        continue
                    for line_num, line in enumerate(lines, 1):
                        for match in pattern.finditer(line):
                            matches.append(
                                PatternMatch(
                                    pattern_name=pattern_info["name"],
                                    pattern_type=pattern_id,
                                    line_number=line_num,
                                    content=match.group(0)[:50],
                                    suggestion=self._match_suggestion(pattern_id, pattern_info, match),
                                    severity=pattern_info["severity"],
                                )
                            )

        # 统计/结构分析器（dimensions 6, 8, 9, 10, chapter-template）。
        # 在 regex 阶段后注入；它们的 issue 通过 PatternMatch 走同一条管线。
        report = run_prose_analyzers(text)
        for issue in report.issues:
            matches.append(_prose_issue_to_match(issue))

        # 语义链分析器（dimensions 3, 4, 5）。跨段/跨章节模式通过同一条
        # PatternMatch 管线进入评分与报告；modify_plan 由 generate_report
        # 单独组织。
        chain_report = run_semantic_chain_analyzers(text)
        for issue in chain_report.issues:
            matches.append(_chain_issue_to_match(issue))

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
        parallel_count = 0
        for pattern in self.parallel_patterns:
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

        # Prose-structure metrics (sentence cv, paragraph cv, edge runs, structure runs,
        # chapter-template runs). These are surfaced alongside the existing metrics so
        # downstream callers can monitor them without re-running analyzers.
        prose_report = run_prose_analyzers(text)
        prose_metrics = prose_report.metrics

        # Semantic-chain metrics (dimensions 3, 4, 5): the per-analyzer counts the
        # chain layer already produced. Surfaced next to the prose metrics so the
        # downstream dashboards can monitor "chain pressure" alongside prose stats.
        chain_report = run_semantic_chain_analyzers(text)
        chain_metrics = chain_report.metrics

        # Rewrite plan: collect every issue raised by both stages, sort by severity
        # and location, then return a structured skeleton for each row. The plan is
        # plain dicts so callers can JSON-serialise the report end-to-end.
        aggregated_issues = prose_report.issues + chain_report.issues
        modify_plan = [entry.to_dict() for entry in build_modify_plan(aggregated_issues)]

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
                **prose_metrics,
                **chain_metrics,
            },
            "issue_types": dict(type_counts.most_common(10)),
            "matches": [asdict(m) for m in matches],
            "modify_plan": modify_plan,
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
