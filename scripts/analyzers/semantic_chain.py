"""Semantic-chain analyzers — dimensions 3, 4, 5.

These analyzers look *across* paragraphs and *between* chapters to catch
machine-like patterns that the per-paragraph regex rules miss. Each analyzer
shares the same data contract as the prose-structure analyzers:
``analyze(text) -> AnalyzerReport``.

Public surface (consumed by ``scripts.analyzers.__init__``):

- ``ANALYZERS`` — tuple of analyzer modules, each with ``ID`` and ``analyze``
- ``chain_analyze(text)`` — run all 10 in one call (preferred)
- ``run_semantic_chain_analyzers(text)`` — alias of ``chain_analyze``
"""

from __future__ import annotations

import re
from collections import Counter

from scripts.analyzers._regex_categories import count_by_category, find_hits
from scripts.analyzers._segments import (
    is_short_text,
    split_chapters,
    split_paragraphs,
)
from scripts.analyzers._types import AnalyzerIssue, AnalyzerReport


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

# Source / method markers used to decide whether a quantified claim is anchored.
# Loaded fresh from evidence.toml via the shared rule document.
_SOURCE_MARKER_HINTS = (
    "根据", "数据来源", "样本", "N=", "（N=", "(N=",
    "公司年报", "财务部", "国家统计局", "行业协会",
    "调研报告", "记录已编码",
)


def _has_source_marker_within(text: str, position: int, radius: int = 80) -> bool:
    """Return True when any source-marker hint appears within ``radius`` chars.

    Looks both forward and backward from ``position`` so a claim that itself
    cites its source in the same sentence still counts as supported. A claim
    that floats in the document with no nearby anchor returns False.
    """
    start = max(0, position - radius)
    end = min(len(text), position + radius)
    window = text[start:end]
    return any(marker in window for marker in _SOURCE_MARKER_HINTS)


def _has_digit_within(text: str, position: int, radius: int = 30) -> bool:
    """Loose check: does the local neighborhood (radius chars) contain a digit?"""
    start = max(0, position - radius)
    end = min(len(text), position + radius)
    return bool(re.search(r"\d", text[start:end]))


_CN_STOPWORDS = frozenset(
    "的 是 在 和 与 及 或 对 为 有 也 这 那 但 而 并且 但是 所以 因此 由于 关于 "
    "通过 对于 之一 方面 一个 一种 一些 这项 该".split()
)


def _tokenize_keywords(text: str, min_len: int = 2) -> list[str]:
    """Return CJK keyword tokens of length >= ``min_len``.

    Pure CJK-only is enough for keyword overlap; this is not a tokenizer,
    just a fingerprint helper for ``cross_section_problem_trace``.
    """
    if not text:
        return []
    out: list[str] = []
    buf: list[str] = []
    for ch in text:
        if "一" <= ch <= "鿿":
            buf.append(ch)
            if len(buf) >= 4:  # 4-char windows to reduce noise
                token = "".join(buf)
                if token not in _CN_STOPWORDS and len(token) >= min_len:
                    out.append(token)
                buf.pop(0)
        else:
            buf = []
    return out


# ---------------------------------------------------------------------------
# Dimension 3 — template chains
# ---------------------------------------------------------------------------

ID_THREE_PART = "chain_three_part_rule"

# Matches the 一是...二是...三是 (or "一方面...另一方面"/"第一...第二...第三") pattern
# inside a single paragraph. The trailing "。" allows multi-sentence paragraphs.
_THREE_PART_RE = re.compile(
    r"(?:"
    r"一(?:是|方面|来|则|者|要)[^。]*。"
    r"[^。]*二(?:是|方面|来|则|者|要)[^。]*。"
    r"[^。]*三(?:是|方面|来|则|者|要)[^。]*。"
    r"|第一[^。]*。[^。]*第二[^。]*。[^。]*第三[^。]*。"
    r"|首先[^。]*。[^。]*(?:然后|其次|再次)[^。]*。[^。]*最后[^。]*。"
    r")"
)


def _three_part_consecutive_paragraphs(text: str) -> tuple[int, list[str]]:
    """Return (max_consecutive_run, [evidence snippets])."""
    paragraphs = split_paragraphs(text)
    if not paragraphs:
        return 0, []
    runs: list[tuple[int, list[str]]] = []
    current = 0
    evidence: list[str] = []
    for paragraph in paragraphs:
        if _THREE_PART_RE.search(paragraph):
            current += 1
            evidence.append(paragraph[:60])
        else:
            if current:
                runs.append((current, evidence))
            current = 0
            evidence = []
    if current:
        runs.append((current, evidence))
    if not runs:
        return 0, []
    best_count, best_evidence = max(runs, key=lambda r: r[0])
    return best_count, best_evidence


def analyze_three_part(text: str) -> AnalyzerReport:
    if is_short_text(text):
        return AnalyzerReport()
    run, evidence = _three_part_consecutive_paragraphs(text)
    if run < 3:
        return AnalyzerReport(metrics={ID_THREE_PART: 0.0})
    severity = "high" if run >= 5 else "medium"
    snippet = " | ".join(evidence[:3])
    issue = AnalyzerIssue(
        analyzer_id=ID_THREE_PART,
        severity=severity,
        confidence=round(min(1.0, run / 5), 3),
        location="global",
        evidence=f"连续 {run} 段同时使用三段式结构：{snippet}",
        suggestion=(
            "在长段论述间插入不同句式（对比 / 案例 / 因果 / 数据），避免每段都按 '一是…二是…三是…' "
            "或 '首先…然后…最后…' 展开。"
        ),
    )
    return AnalyzerReport(
        issues=[issue],
        metrics={ID_THREE_PART: float(run)},
    )


ID_AUTHOR_LIST = "chain_author_listing"

_AUTHOR_RE = re.compile(r"\w+\(\d{4}\)[^，。]*?(?:认为|指出|表明|强调|发现|提出)")


def analyze_author_listing(text: str) -> AnalyzerReport:
    if is_short_text(text):
        return AnalyzerReport()
    chapters = split_chapters(text)
    worst_run = 0
    worst_chapter = ""
    for chapter in chapters:
        body = "\n".join(chapter.split("\n")[1:]) if chapter else ""  # skip heading
        count = len(_AUTHOR_RE.findall(body))
        if count > worst_run:
            worst_run = count
            worst_chapter = chapter.split("\n", 1)[0][:30]
    if worst_run < 4:
        return AnalyzerReport(metrics={ID_AUTHOR_LIST: 0.0})
    issue = AnalyzerIssue(
        analyzer_id=ID_AUTHOR_LIST,
        severity="medium",
        confidence=round(min(1.0, worst_run / 6), 3),
        location=f"chapter:{worst_chapter}" if worst_chapter else "global",
        evidence=f"单章出现 {worst_run} 处 '作者(年份)认为/指出' 罗列式引用",
        suggestion=(
            "按主题或方法分组综述作者观点，加入比较与归类（例如'关于激励机制，张三(2019)与李四(2020) "
            "均指出…'），避免 '张三指出…李四指出…' 的并列堆叠。"
        ),
    )
    return AnalyzerReport(
        issues=[issue],
        metrics={ID_AUTHOR_LIST: float(worst_run)},
    )


ID_METHOD_NAME = "chain_method_name"

# Detect a list of 2+ different method/model/theory/framework names piled
# together. The pattern allows ", " / "、" / "和" / "与" between names.
_METHOD_LIST_RE = re.compile(
    r"(?:运用|采用|基于|结合|综合运用)[^。]{0,80}"
    r"(?:模型|理论|框架|方法|分析法|体系)[^。]*"
    r"(?:、|，|和|与|及)[^。]*?"
    r"(?:模型|理论|框架|方法|分析法|体系)"
)


def _method_name_count(paragraph: str) -> int:
    """Count the number of distinct method-like tokens in one paragraph."""
    # The thresholds are intentionally narrow: capture multi-method piles
    # without catching every passing reference to a single theory.
    methods = re.findall(
        r"[A-Z]{2,4}|[A-Za-z一-鿿]{2,8}(?:模型|理论|框架|方法|分析法|体系)",
        paragraph,
    )
    return len(set(methods))


def analyze_method_name(text: str) -> AnalyzerReport:
    if is_short_text(text):
        return AnalyzerReport()
    paragraphs = [p for p in split_paragraphs(text) if len(p) >= 20]
    fired: list[str] = []
    for paragraph in paragraphs:
        if _METHOD_LIST_RE.search(paragraph) and _method_name_count(paragraph) >= 2:
            fired.append(paragraph[:80])
    if not fired:
        return AnalyzerReport(metrics={ID_METHOD_NAME: 0.0})
    issue = AnalyzerIssue(
        analyzer_id=ID_METHOD_NAME,
        severity="medium",
        confidence=round(min(1.0, len(fired) / 3), 3),
        location="global",
        evidence=f"有 {len(fired)} 段同时堆叠 2 个以上方法/模型/理论，且未对每个方法单独说明",
        suggestion=(
            "挑选最贴近研究问题的 1-2 个方法/理论，逐个说明其分析维度和本研究的适用点。"
            "删除'综合运用 X 和 Y 和 Z'式的并列堆叠。"
        ),
    )
    return AnalyzerReport(
        issues=[issue],
        metrics={ID_METHOD_NAME: float(len(fired))},
    )


ID_ABSTRACT_TEMPLATE = "chain_abstract_template"

_ABSTRACT_PHRASES = (
    "本文针对",
    "本文研究",
    "本文提出",
    "结果表明",
    "本文的主要贡献",
    "实验结果表明",
)


def analyze_abstract_template(text: str) -> AnalyzerReport:
    if is_short_text(text):
        return AnalyzerReport()
    paragraphs = split_paragraphs(text)
    if not paragraphs:
        return AnalyzerReport(metrics={ID_ABSTRACT_TEMPLATE: 0.0})
    best_count = 0
    best_para = ""
    for paragraph in paragraphs:
        hits = sum(1 for phrase in _ABSTRACT_PHRASES if phrase in paragraph)
        if hits > best_count:
            best_count = hits
            best_para = paragraph[:80]
    if best_count < 3:
        return AnalyzerReport(metrics={ID_ABSTRACT_TEMPLATE: float(best_count)})
    issue = AnalyzerIssue(
        analyzer_id=ID_ABSTRACT_TEMPLATE,
        severity="medium",
        confidence=round(min(1.0, best_count / 4), 3),
        location="paragraph:abstract",
        evidence=f"摘要/开篇段同时命中 {best_count} 个摘要模板短语：{best_para}",
        suggestion=(
            "摘要/开篇段合并为 2-3 句：先写研究问题与企业案例，再写方法和核心发现，"
            "避免 '本文针对…问题…提出了…结果表明…' 的连续堆叠。"
        ),
    )
    return AnalyzerReport(
        issues=[issue],
        metrics={ID_ABSTRACT_TEMPLATE: float(best_count)},
    )


ID_CONCLUSION_ECHO = "chain_conclusion_echo"


def _chapter_signature(paragraphs: list[str], n_chars: int = 60) -> set[str]:
    """Return character-level n-grams used to detect echoing across chapters."""
    bag: set[str] = set()
    for paragraph in paragraphs[:3]:  # first 3 paragraphs carry the framing
        cleaned = re.sub(r"\s+", "", paragraph)
        for index in range(0, max(0, len(cleaned) - n_chars + 1)):
            bag.add(cleaned[index : index + n_chars])
    return bag


def analyze_conclusion_echo(text: str) -> AnalyzerReport:
    if is_short_text(text):
        return AnalyzerReport()
    chapters = split_chapters(text)
    if len(chapters) < 2:
        return AnalyzerReport(metrics={ID_CONCLUSION_ECHO: 0.0})
    # First non-empty chapter is treated as the abstract/intro framing;
    # last non-empty chapter is the conclusion. Falling back to paragraphs.
    first_chapter_paras = split_paragraphs(chapters[0])
    last_chapter_paras = split_paragraphs(chapters[-1])
    if not first_chapter_paras or not last_chapter_paras:
        return AnalyzerReport(metrics={ID_CONCLUSION_ECHO: 0.0})
    first_sig = _chapter_signature(first_chapter_paras)
    last_sig = _chapter_signature(last_chapter_paras)
    if not first_sig or not last_sig:
        return AnalyzerReport(metrics={ID_CONCLUSION_ECHO: 0.0})
    overlap = len(first_sig & last_sig)
    union = len(first_sig | last_sig)
    jaccard = overlap / union if union else 0.0
    if jaccard < 0.30:
        return AnalyzerReport(metrics={ID_CONCLUSION_ECHO: round(jaccard, 3)})
    severity = "medium" if jaccard < 0.55 else "high"
    issue = AnalyzerIssue(
        analyzer_id=ID_CONCLUSION_ECHO,
        severity=severity,
        confidence=round(jaccard, 3),
        location="chapter:last",
        evidence=(
            f"结论章首段与开篇章首段字符级别 Jaccard 重叠={jaccard:.2f}，"
            f"重复片段数 {overlap}/{union}，疑似只复述绪论而无新结论"
        ),
        suggestion=(
            "结论章必须写出本研究的核心发现、对策建议、局限与展望，避免对绪论做逐句复述。"
            "若结论确实需要回扣研究意义，可只保留一句即可。"
        ),
    )
    return AnalyzerReport(
        issues=[issue],
        metrics={ID_CONCLUSION_ECHO: round(jaccard, 3)},
    )


# ---------------------------------------------------------------------------
# Dimension 4 — vague content chains
# ---------------------------------------------------------------------------

ID_VAGUE_PROBLEM = "chain_vague_problem_statement"

_VAGUE_PROBLEM_RE = re.compile(
    r"(?:存在(?:诸多|一些|很多|较多)(?:问题|不足|挑战)|"
    r"面临(?:诸多|严峻|复杂)(?:挑战|问题|压力)|"
    r"亟需(?:优化|提升|完善|改进)|"
    r"有待(?:进一步)?(?:优化|提升|完善))"
)


def analyze_vague_problem(text: str) -> AnalyzerReport:
    if is_short_text(text):
        return AnalyzerReport()
    matches = list(_VAGUE_PROBLEM_RE.finditer(text))
    if len(matches) < 2:
        return AnalyzerReport(metrics={ID_VAGUE_PROBLEM: float(len(matches))})
    # A "supported" statement has a digit nearby (some metric within 30 chars).
    supported = [m for m in matches if _has_digit_within(text, m.start(), radius=30)]
    unsupported = [m for m in matches if m not in supported]
    if len(unsupported) < 2:
        return AnalyzerReport(metrics={ID_VAGUE_PROBLEM: float(len(matches))})
    issue = AnalyzerIssue(
        analyzer_id=ID_VAGUE_PROBLEM,
        severity="medium",
        confidence=round(min(1.0, len(unsupported) / 4), 3),
        location="global",
        evidence=(
            f"出现 {len(matches)} 处笼统问题表述，其中 {len(unsupported)} 处 30 字内无任何度量支撑"
        ),
        suggestion=(
            "把 '存在诸多问题 / 亟需优化' 改成具体指标差：'XYZ 公司 2023 年客户投诉率 8.6%，"
            "高于行业均值 3.1 个百分点，主要集中在售后响应。'"
        ),
    )
    return AnalyzerReport(
        issues=[issue],
        metrics={ID_VAGUE_PROBLEM: float(len(matches))},
    )


ID_UNSUPPORTED_NUMBER = "chain_unsupported_quantification"

_NUMBER_RE = re.compile(
    r"(?:"
    r"(?:提升|增长|下降|降低|减少|增加|上涨)[^，。]{0,8}\d+(?:\.\d+)?%"
    r"|(?:达到|超过|低于|高于)\d+(?:\.\d+)?%"
    r"|排名第[一二三四五六七八九十1-9]"
    r"|占比(?:达到|为)?\d+(?:\.\d+)?%"
    r")"
)


def analyze_unsupported_quantification(text: str) -> AnalyzerReport:
    if is_short_text(text):
        return AnalyzerReport()
    matches = list(_NUMBER_RE.finditer(text))
    if len(matches) < 2:
        return AnalyzerReport(metrics={ID_UNSUPPORTED_NUMBER: float(len(matches))})
    unsupported = [m for m in matches if not _has_source_marker_within(text, m.start(), radius=80)]
    if len(unsupported) < 2:
        return AnalyzerReport(metrics={ID_UNSUPPORTED_NUMBER: float(len(matches))})
    issue = AnalyzerIssue(
        analyzer_id=ID_UNSUPPORTED_NUMBER,
        severity="high",
        confidence=round(min(1.0, len(unsupported) / 4), 3),
        location="global",
        evidence=(
            f"出现 {len(matches)} 个百分比/排名类断言，其中 {len(unsupported)} 个 80 字内"
            f"没有根据/来源/问卷/N= 标记"
        ),
        suggestion=(
            "为每个量化断言补齐来源：'根据 2023 年 12 月客户问卷（N=120），客户满意度从 3.8 升至 4.5 分。' "
            "无法核实时改为定性描述并标注需补数据。"
        ),
    )
    return AnalyzerReport(
        issues=[issue],
        metrics={ID_UNSUPPORTED_NUMBER: float(len(unsupported))},
    )


ID_MACRO_NARRATIVE = "chain_macro_narrative"

_MACRO_HIT_RE = re.compile(
    r"(?:推动[^，。]+变革|时代(?:的|背景|意义)|历史(?:的|进程|意义)"
    r"|趋势(?:表明|显示|说明)|战略(?:高度|意义|价值)|"
    r"(?:数字化|智能化|绿色化|全球化)?浪潮|新时代)"
)


def analyze_macro_narrative(text: str) -> AnalyzerReport:
    if is_short_text(text):
        return AnalyzerReport()
    # Sliding window of 1000 chars: if 3+ macro-narrative phrases fit inside,
    # that stretch reads like an AI-style preface.
    if len(text) < 1000:
        hits = _MACRO_HIT_RE.findall(text)
        count = len(hits)
        window_size = len(text)
    else:
        best = 0
        best_window = ""
        for match in _MACRO_HIT_RE.finditer(text):
            start = max(0, match.start() - 500)
            end = min(len(text), match.start() + 500)
            window = text[start:end]
            count_in_window = len(_MACRO_HIT_RE.findall(window))
            if count_in_window > best:
                best = count_in_window
                best_window = window[:60]
        count = best
        window_size = 1000
    if count < 3:
        return AnalyzerReport(metrics={ID_MACRO_NARRATIVE: float(count)})
    issue = AnalyzerIssue(
        analyzer_id=ID_MACRO_NARRATIVE,
        severity="medium",
        confidence=round(min(1.0, count / 5), 3),
        location="global",
        evidence=f"在 {window_size} 字窗口内出现 {count} 个宏观叙事短语",
        suggestion=(
            "把宏观背景限缩到与企业案例直接相关的 1-2 句：'双碳政策使该公司高耗能产线面临能耗考核压力'，"
            "避免 '在数字化浪潮的时代背景下……推动行业变革' 这类堆叠。"
        ),
    )
    return AnalyzerReport(
        issues=[issue],
        metrics={ID_MACRO_NARRATIVE: float(count)},
    )


# ---------------------------------------------------------------------------
# Dimension 5 — evidence chain
# ---------------------------------------------------------------------------

ID_EVIDENCE_COMPLETE = "evidence_chain_completeness"


def analyze_evidence_chain(text: str) -> AnalyzerReport:
    """Cross-check number claims against the evidence rule set.

    A claim is "complete" when it carries a method/source/N marker nearby.
    The dimension fires when the corpus has 2+ claims that lack anchors —
    the same text often reads as 'lots of numbers, no source'.
    """
    if is_short_text(text):
        return AnalyzerReport()
    # Per-rule claims: hit both content.toml's quantification rule and the
    # evidence.toml 'data_without_method' rule (they imply missing anchors).
    q_hits = find_hits(text, include_category_ids=["unsupported_quantification"])
    d_hits = find_hits(text, include_category_ids=["data_without_method"])
    targets: list[int] = []
    for _, _, span, _ in q_hits:
        targets.append(span[0])
    for _, _, span, snippet in d_hits:
        # Skip methodless statements that already mentioned data sources inline.
        if any(marker in snippet for marker in _SOURCE_MARKER_HINTS):
            continue
        targets.append(span[0])
    if len(targets) < 2:
        return AnalyzerReport(metrics={ID_EVIDENCE_COMPLETE: float(len(targets))})
    unanchored = [
        position
        for position in targets
        if not _has_source_marker_within(text, position, radius=80)
    ]
    if len(unanchored) < 2:
        return AnalyzerReport(metrics={ID_EVIDENCE_COMPLETE: float(len(targets))})
    issue = AnalyzerIssue(
        analyzer_id=ID_EVIDENCE_COMPLETE,
        severity="high",
        confidence=round(min(1.0, len(unanchored) / 4), 3),
        location="global",
        evidence=(
            f"证据链校验命中 {len(targets)} 处量化/调研断言，其中 {len(unanchored)} 处周围 80 字内"
            f"没有方法/来源/N 标记"
        ),
        suggestion=(
            "对每个量化结论补齐三件套：方法（N=、问卷题项、时间窗）、来源（年报/数据库/访谈编码）、"
            "口径（样本范围、统计指标定义）。"
        ),
    )
    return AnalyzerReport(
        issues=[issue],
        metrics={ID_EVIDENCE_COMPLETE: float(len(unanchored))},
    )


ID_PROBLEM_TRACE = "cross_section_problem_trace"


def _identify_chapters(text: str) -> tuple[str, str]:
    """Return (problem_chapter_text, recommendation_chapter_text).

    Heuristic: the chapter with the highest count of problem nouns (问题/痛点/
    不足/薄弱) is treated as the problem chapter; the one with the highest
    count of recommendation nouns (对策/建议/方案/措施) is treated as the
    recommendation chapter. Falls back to a positional pick when neither
    keyword appears.
    """
    chapters = split_chapters(text)
    if len(chapters) < 2:
        return "", ""
    problem_keywords = ("问题", "痛点", "不足", "薄弱", "挑战", "现状")
    recommend_keywords = ("对策", "建议", "方案", "措施", "实施", "保障")
    problem_chapter = max(
        chapters,
        key=lambda chapter: sum(chapter.count(kw) for kw in problem_keywords),
    )
    recommend_chapter = max(
        chapters,
        key=lambda chapter: sum(chapter.count(kw) for kw in recommend_keywords),
    )
    if problem_chapter == recommend_chapter and len(chapters) >= 2:
        # Last-resort positional pick so a uniform template still yields a trace.
        problem_chapter = chapters[len(chapters) // 3]
        recommend_chapter = chapters[-1]
    return problem_chapter, recommend_chapter


def analyze_problem_trace(text: str) -> AnalyzerReport:
    if is_short_text(text):
        return AnalyzerReport()
    problem_chapter, recommend_chapter = _identify_chapters(text)
    if not problem_chapter or not recommend_chapter:
        return AnalyzerReport(metrics={ID_PROBLEM_TRACE: 1.0})
    problem_tokens = Counter(_tokenize_keywords(problem_chapter))
    recommend_tokens = _tokenize_keywords(recommend_chapter)
    if not problem_tokens or not recommend_tokens:
        return AnalyzerReport(metrics={ID_PROBLEM_TRACE: 1.0})
    problem_set = {tok for tok, count in problem_tokens.items() if count >= 1}
    if not problem_set:
        return AnalyzerReport(metrics={ID_PROBLEM_TRACE: 1.0})
    recommend_set = set(recommend_tokens)
    overlap = problem_set & recommend_set
    overlap_ratio = len(overlap) / len(problem_set)
    if overlap_ratio >= 0.30:
        return AnalyzerReport(metrics={ID_PROBLEM_TRACE: round(overlap_ratio, 3)})
    issue = AnalyzerIssue(
        analyzer_id=ID_PROBLEM_TRACE,
        severity="high",
        confidence=round(1.0 - overlap_ratio, 3),
        location="chapter:problem_vs_recommendation",
        evidence=(
            f"问题章与对策章关键词重叠率仅 {overlap_ratio:.2f}（阈值 0.30），"
            f"问题章有 {len(problem_set)} 个关键词，仅 {len(overlap)} 个出现在对策章"
        ),
        suggestion=(
            "对策章应逐条对应问题章：把每个问题名词（例如'库存周转天数偏高''售后响应慢'）"
            "在对策章明确给出对应的改进动作，并用同一关键词回扣。"
        ),
    )
    return AnalyzerReport(
        issues=[issue],
        metrics={ID_PROBLEM_TRACE: round(overlap_ratio, 3)},
    )


# ---------------------------------------------------------------------------
# Aggregator
# ---------------------------------------------------------------------------

CHAIN_ANALYZERS = (
    (
        ID_THREE_PART,
        analyze_three_part,
        "维度 3：连续三段式模板",
    ),
    (
        ID_AUTHOR_LIST,
        analyze_author_listing,
        "维度 3：作者罗列式综述",
    ),
    (
        ID_METHOD_NAME,
        analyze_method_name,
        "维度 3：方法名堆叠",
    ),
    (
        ID_ABSTRACT_TEMPLATE,
        analyze_abstract_template,
        "维度 3：摘要模板堆叠",
    ),
    (
        ID_CONCLUSION_ECHO,
        analyze_conclusion_echo,
        "维度 3：结论与绪论回声",
    ),
    (
        ID_VAGUE_PROBLEM,
        analyze_vague_problem,
        "维度 4：笼统问题表述成链",
    ),
    (
        ID_UNSUPPORTED_NUMBER,
        analyze_unsupported_quantification,
        "维度 4：无来源量化断言成链",
    ),
    (
        ID_MACRO_NARRATIVE,
        analyze_macro_narrative,
        "维度 4：宏观叙事堆叠",
    ),
    (
        ID_EVIDENCE_COMPLETE,
        analyze_evidence_chain,
        "维度 5：证据链完整度",
    ),
    (
        ID_PROBLEM_TRACE,
        analyze_problem_trace,
        "维度 5：跨章节问题-对策追踪",
    ),
)


def chain_analyze(text: str) -> AnalyzerReport:
    """Run every chain analyzer and merge into one report."""
    merged = AnalyzerReport()
    for _, fn, _ in CHAIN_ANALYZERS:
        merged.merge(fn(text))
    return merged


# Backward-compatible alias for the prose package's naming style.
run_semantic_chain_analyzers = chain_analyze


__all__ = [
    "CHAIN_ANALYZERS",
    "chain_analyze",
    "run_semantic_chain_analyzers",
    "analyze_three_part",
    "analyze_author_listing",
    "analyze_method_name",
    "analyze_abstract_template",
    "analyze_conclusion_echo",
    "analyze_vague_problem",
    "analyze_unsupported_quantification",
    "analyze_macro_narrative",
    "analyze_evidence_chain",
    "analyze_problem_trace",
]
