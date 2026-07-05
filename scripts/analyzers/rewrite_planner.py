"""Rewrite planner — turn ``AnalyzerIssue`` lists into structured modify plans.

Designed for humanizers (LLM or human) to act on. The planner is *not* a
rewriter itself; it only produces a location-aware skeleton with the AI-trace
pattern, the targeted rewrite direction, and recommended replacements
extracted from the shared TOML rule document.

Public surface:

- ``build_modify_plan(issues)`` → ``list[ModifyEntry]``
- ``ModifyEntry`` dataclass with the fields callers may serialize
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Iterable, Sequence

from scripts.analyzers._types import AnalyzerIssue, AnalyzerReport
from scripts.rule_loader import load_rules


@dataclass
class ModifyEntry:
    """One row of a rewrite plan.

    Fields:
    - ``analyzer_id`` — matches ``AnalyzerIssue.analyzer_id``
    - ``severity`` — ``high`` / ``medium`` / ``low``
    - ``location`` — ``global`` / ``paragraph:#`` / ``chapter:...``
    - ``evidence`` — short string from the analyzer (≤80 chars)
    - ``suggestion`` — original rewrite direction
    - ``rewrite_template`` — short template phrase the humanizer should follow
    - ``recommended_replacements`` — derived from the shared TOML
    - ``target_word_count_range`` — recommended length window
    - ``before_after_example`` — concrete rewrite pair sourced from
      ``[[categories.examples]]`` in the shared TOML; ``None`` when the rule
      has no example attached.
    """

    analyzer_id: str
    severity: str
    location: str
    evidence: str
    suggestion: str
    rewrite_template: str
    recommended_replacements: list[str]
    target_word_count_range: tuple[int, int]
    before_after_example: dict | None = None

    def to_dict(self) -> dict:
        data = asdict(self)
        # tuples do not serialize as JSON arrays in some callers; force list.
        data["target_word_count_range"] = list(self.target_word_count_range)
        return data


# Per-analyzer skeleton definitions. Word ranges chosen to balance "long
# enough for concrete evidence" against "short enough to stay focused".
_SKELETONS: dict[str, dict] = {
    "chain_three_part_rule": {
        "template": "在长段论述之间插入不同句式：对比、案例、因果或数据各 1-2 句，避免每段都按 '一是…二是…三是…' 展开。",
        "replacements": [
            "案例锚点：插入 '以 XYZ 公司 2023 年的实践为例……'",
            "因果链：插入 '导致该问题的原因是……'",
            "对比基线：插入 '与 2022 年同期相比……'",
        ],
        "word_range": (60, 140),
    },
    "chain_author_listing": {
        "template": "按主题分组综述作者观点，加入比较、归类与本研究的取舍。",
        "replacements": [
            "主题归类：'关于激励机制，张三(2019)与李四(2020)均指出……'",
            "比较分析：'与张三(2019)的结论相比，本研究在样本上做出 …… 的调整'",
            "研究空白：'既有研究主要关注大型国企，较少讨论中小制造企业 ……'",
        ],
        "word_range": (80, 160),
    },
    "chain_method_name": {
        "template": "挑选最贴近研究问题的 1-2 个方法/理论，逐个说明分析维度与适用点。",
        "replacements": [
            "保留一个方法：'本文只采用 STP 模型，分别分析细分市场、目标市场与定位'",
            "删除并列方法名：把 '运用 X 和 Y 和 Z' 改为 '运用 X，辅以 Y 进行校核'",
            "补充方法适用点：'选择 X 是因为 ……'",
        ],
        "word_range": (60, 130),
    },
    "chain_abstract_template": {
        "template": "摘要/开篇段合并为 2-3 句：研究问题与企业案例 → 方法 → 核心发现。",
        "replacements": [
            "第一句：'本研究以 XYZ 公司为案例，回答 …… 问题'",
            "第二句：'采用 …… 方法，分析 …… 数据'",
            "第三句：'研究发现 ……（具体数值或机制）'",
        ],
        "word_range": (120, 240),
    },
    "chain_conclusion_echo": {
        "template": "结论章给出核心发现、对策建议、局限与展望，避免对绪论做逐句复述。",
        "replacements": [
            "核心发现：'本研究发现 ……（列出 2-3 条具体结论）'",
            "对策建议：'基于以上发现，建议 XYZ 公司从 …… 方面着手'",
            "局限展望：'本文受 …… 限制，未来可从 …… 进一步研究'",
        ],
        "word_range": (200, 400),
    },
    "chain_vague_problem_statement": {
        "template": "把 '存在诸多问题/亟需优化' 改成具体指标差：对象、时间、度量、改善幅度。",
        "replacements": [
            "具体指标：'XYZ 公司 2023 年客户投诉率 8.6%，高于行业均值 3.1 个百分点'",
            "覆盖范围：'主要集中在售后响应环节'",
            "对比基线：'2022 年同期为 5.2%'",
        ],
        "word_range": (40, 100),
    },
    "chain_unsupported_quantification": {
        "template": "为每个量化断言补齐来源：样本、时间、统计口径。",
        "replacements": [
            "来源模板：'根据 2023 年 12 月客户问卷（N=120），满意度从 3.8 升至 4.5 分'",
            "样本说明：'问卷采用 5 分制李克特量表'",
            "无法核实时标注：'该指标需要进一步核实，本文未取得第三方数据'",
        ],
        "word_range": (60, 130),
    },
    "chain_macro_narrative": {
        "template": "把宏观背景限缩到与企业案例直接相关的 1-2 句。",
        "replacements": [
            "政策影响：'双碳政策使该公司高耗能产线面临能耗考核压力'",
            "行业拐点：'2022 年区域内新增 3 家竞争者，价格平均下降 15%'",
            "删除 '数字化浪潮''战略高度' 等宏大判断",
        ],
        "word_range": (40, 100),
    },
    "evidence_chain_completeness": {
        "template": "对每个量化结论补齐三件套：方法、来源、口径。",
        "replacements": [
            "方法标记：'问卷（N=120）''访谈 6 人'",
            "来源标记：'公司年报''国家统计局表号 B604-1'",
            "口径说明：'样本范围为该厂一线员工''指标定义为季度出货量'",
        ],
        "word_range": (60, 140),
    },
    "cross_section_problem_trace": {
        "template": "对策章逐条对应问题章，每个问题名词都给出对应改进动作，并用同一关键词回扣。",
        "replacements": [
            "问题章：'售后响应慢' → 对策章：'售后响应：24 小时首次响应，48 小时闭环'",
            "问题章：'库存周转天数偏高' → 对策章：'库存周转：从 45 天降至 32 天'",
            "问题章关键词与对策章关键词一一对照",
        ],
        "word_range": (80, 200),
    },
    # Prose-structure analyzers also benefit from rewrite direction:
    "uniform_sentence_length": {
        "template": "长短句交替：连续 3 个相似句长后插入短句或长句，提升节奏感。",
        "replacements": [
            "短句插入：'这一点至关重要。'",
            "复合长句：'……的过程同时涉及 …… 和 ……，因此需要综合权衡'",
        ],
        "word_range": (10, 60),
    },
    "uniform_paragraph_length": {
        "template": "在长论述段之间插入短过渡段或单句段，模仿自然写作节奏。",
        "replacements": [
            "单句过渡：'基于以上分析，'",
            "短小结段：'小结：本节验证了 ……'",
            "长段后留白：'……这一现象值得进一步研究。'",
        ],
        "word_range": (8, 40),
    },
    "paragraph_edge_template_repeat": {
        "template": "段首/段末用不同句式收束，避免连续多段都是'首先……最后……'。",
        "replacements": [
            "段首改写：'值得注意的是，''从 XYZ 实践来看，''另一项证据来自 ……'",
            "段末改写：'值得在下一节进一步验证。''这与本章开头的判断保持一致。'",
        ],
        "word_range": (10, 50),
    },
    "paragraph_structure_uniformity": {
        "template": "跨段使用不同的句式指纹：长短、转折、举例、对比、引用交替进行。",
        "replacements": [
            "举例段：以具体案例开篇",
            "对比段：以基准对比开篇",
            "结论段：以判断句收束",
        ],
        "word_range": (15, 60),
    },
    "chapter_template_repeat": {
        "template": "章节内部小节使用不同章法，避免每节都按'背景-问题-对策-小结'展开。",
        "replacements": [
            "首节直接给结论 + 证据",
            "末节给出局限与展望",
            "中间节允许'案例 → 数据 → 解读'结构",
        ],
        "word_range": (40, 120),
    },
}


_DEFAULT_SKELETON = {
    "template": "根据问题位置改写：用具体对象、方法、数据替换空泛表述。",
    "replacements": [
        "把模板词换成具体数字或案例",
        "把 '研究表明' 换成 '张三(2019) 在 N=120 样本中发现'",
    ],
    "word_range": (40, 120),
}


# ---------------------------------------------------------------------------
# Plan construction
# ---------------------------------------------------------------------------

# Cache the rule document so the planner does not re-read TOML on every call.
_RULES_CACHE: dict | None = None


def _get_rules() -> dict:
    global _RULES_CACHE
    if _RULES_CACHE is None:
        _RULES_CACHE = load_rules()
    return _RULES_CACHE


def _lookup_rule_suggestion(analyzer_id: str) -> list[str]:
    """Find rewrite_principles for the rule that matches ``analyzer_id``.

    The chain analyzers reuse the regex category ids defined in
    ``references/rules/`` so we can map them back to suggestion bullets.
    """
    rules = _get_rules()
    bucket: list[str] = []
    for category in rules.get("categories", []):
        if category.get("id") == analyzer_id:
            bucket.extend(category.get("rewrite_principles", []))
    if not bucket:
        for category in rules.get("categories", []):
            rewrites = category.get("rewrite_principles", [])
            if rewrites:
                bucket = list(rewrites)
                break
    return bucket


def _lookup_before_after_example(analyzer_id: str) -> dict | None:
    """Return the first concrete rewrite pair attached to ``analyzer_id``.

    Reads the shared TOML rule document via ``_get_rules()`` and looks up
    ``[[categories.examples]]`` for the matching category. Returns a plain
    ``{before, after}`` dict, or ``None`` if the rule has no usable example.

    The first example wins; downstream callers wanting a sentence-matched
    example should use ``scripts.analyzers.high_risk_annotator`` instead.
    """
    rules = _get_rules()
    for category in rules.get("categories", []):
        if category.get("id") != analyzer_id:
            continue
        for example in category.get("examples") or []:
            if (
                isinstance(example, dict)
                and "before" in example
                and "after" in example
            ):
                return {"before": example["before"], "after": example["after"]}
    return None


def _build_entry(issue: AnalyzerIssue) -> ModifyEntry:
    skeleton = _SKELETONS.get(issue.analyzer_id, _DEFAULT_SKELETON)
    replacements = list(skeleton["replacements"])
    rule_replacements = _lookup_rule_suggestion(issue.analyzer_id)
    if rule_replacements:
        replacements.extend(rule_replacements[:2])
    return ModifyEntry(
        analyzer_id=issue.analyzer_id,
        severity=issue.severity,
        location=issue.location,
        evidence=issue.evidence[:80],
        suggestion=issue.suggestion,
        rewrite_template=skeleton["template"],
        recommended_replacements=replacements,
        target_word_count_range=tuple(skeleton["word_range"]),
        before_after_example=_lookup_before_after_example(issue.analyzer_id),
    )


def build_modify_plan(issues: Sequence[AnalyzerIssue] | AnalyzerReport) -> list[ModifyEntry]:
    """Convert an AnalyzerIssue sequence (or report) into a sorted plan.

    High severity comes first; the rest keep analyzer order so writers can
    walk through the document region-by-region.
    """
    if isinstance(issues, AnalyzerReport):
        items = list(issues.issues)
    else:
        items = list(issues)
    severity_rank = {"high": 0, "medium": 1, "low": 2}
    items.sort(key=lambda issue: (severity_rank.get(issue.severity, 3), issue.location))
    return [_build_entry(issue) for issue in items]


def merge_plans(plans: Iterable[Sequence[AnalyzerIssue] | AnalyzerReport]) -> list[ModifyEntry]:
    """Merge multiple inputs into one plan; useful when several detectors ran."""
    collected: list[AnalyzerIssue] = []
    for plan in plans:
        if isinstance(plan, AnalyzerReport):
            collected.extend(plan.issues)
        else:
            collected.extend(plan)
    return build_modify_plan(collected)


__all__ = [
    "ModifyEntry",
    "build_modify_plan",
    "merge_plans",
]
