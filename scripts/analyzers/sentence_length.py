"""Dimension 6 — Sentence-length distribution uniformity (paragraph-level CV).

AI-generated prose typically exhibits low variation in sentence length within a
paragraph: sentences cluster around the same length, producing a low coefficient
of variation (CV = std / mean). Human prose mixes short punchy sentences with
longer explanatory ones, yielding higher CV.

This analyzer computes paragraph-level sentence-length CV for Chinese (CJK
characters) or English (words) prose. It returns both diagnostic issues and a
rich metrics bundle that can be rendered into a human-readable CV report or used
for before/after comparisons.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Literal

from scripts.analyzers._segments import (
    cjk_chars,
    is_short_text,
    safe_cv,
    split_chapters,
    split_paragraphs,
    split_sentences,
    split_sentences_english,
    word_count,
)
from scripts.analyzers._types import AnalyzerIssue, AnalyzerReport


ID = "uniform_sentence_length"

# Thresholds aligned with AI_artifact_detection methodology, calibrated for
# paragraph-level sentence-length CV.
CV_VERY_UNIFORM = 0.20
CV_UNIFORM = 0.30
CV_BORDERLINE = 0.45
CV_HEALTHY = 0.65

# Backward-compatible hard/soft thresholds used by legacy callers/tests.
CV_HARD = 0.18
CV_SOFT = 0.28

MIN_SENTENCES_PER_PARAGRAPH = 3
MIN_PARAGRAPHS = 3
MIN_ZH_CHARS_PER_PARAGRAPH = 30
MIN_EN_WORDS_PER_PARAGRAPH = 20

Language = Literal["zh", "en"]


@dataclass
class ParagraphStats:
    """Per-paragraph sentence-length statistics."""

    index: int
    chapter: str
    line_start: int
    line_end: int
    preview: str
    n_sentences: int
    mean: float
    std: float
    cv: float
    min: int
    max: int
    range: int
    lengths: list[int] = field(default_factory=list)


@dataclass
class SectionStats:
    """Per-chapter/section aggregate statistics."""

    name: str
    n_paragraphs: int
    n_sentences: int
    mean_sentence_length: float
    mean_cv: float
    min_cv: float
    max_cv: float


def _split_sentences_for_language(paragraph: str, language: Language) -> list[str]:
    if language == "en":
        return split_sentences_english(paragraph)
    return split_sentences(paragraph)


def _length_for_language(sentence: str, language: Language) -> int:
    if language == "en":
        return word_count(sentence)
    return cjk_chars(sentence)


def _paragraph_min_length(language: Language) -> int:
    return MIN_EN_WORDS_PER_PARAGRAPH if language == "en" else MIN_ZH_CHARS_PER_PARAGRAPH


def _length_unit(language: Language) -> str:
    return "词" if language == "en" else "字"


def _chapter_heading_re() -> re.Pattern[str]:
    return re.compile(r"^第\s*[一二三四五六七八九十0-9]+\s*[章节][^。！？]*$")


def _analyze_paragraph(
    index: int,
    paragraph: str,
    chapter: str,
    line_offset: int,
    language: Language,
) -> ParagraphStats | None:
    """Compute sentence-length CV for one paragraph."""
    sentences = [
        s
        for s in _split_sentences_for_language(paragraph, language)
        if _length_for_language(s, language) > 0
    ]
    if len(sentences) < MIN_SENTENCES_PER_PARAGRAPH:
        return None

    lengths = [_length_for_language(s, language) for s in sentences]
    total = sum(lengths)
    if total < _paragraph_min_length(language):
        return None

    mean = total / len(lengths)
    std = (sum((x - mean) ** 2 for x in lengths) / len(lengths)) ** 0.5
    cv = safe_cv(lengths)

    line_start = line_offset + 1  # 1-based line numbers
    line_end = line_start + paragraph.count("\n")

    preview = paragraph[:80].replace("\n", " ").strip()
    if len(paragraph) > 80:
        preview += "..."

    return ParagraphStats(
        index=index,
        chapter=chapter,
        line_start=line_start,
        line_end=line_end,
        preview=preview,
        n_sentences=len(sentences),
        mean=round(mean, 2),
        std=round(std, 2),
        cv=round(cv, 3),
        min=min(lengths),
        max=max(lengths),
        range=max(lengths) - min(lengths),
        lengths=lengths,
    )


def _collect_paragraphs(text: str, language: Language) -> list[ParagraphStats]:
    """Parse text into chapters and paragraphs, computing per-paragraph stats."""
    chapters = split_chapters(text)
    stats: list[ParagraphStats] = []
    para_index = 0
    global_line = 0  # 0-based line cursor in the original text

    heading_re = _chapter_heading_re()

    for chapter in chapters:
        chapter_lines = chapter.split("\n")

        # Identify chapter heading, if present.
        chapter_name = "(正文)"
        body_start_line = 0
        for i, raw_line in enumerate(chapter_lines):
            line = raw_line.strip()
            if line:
                if heading_re.match(line):
                    chapter_name = line
                    body_start_line = i + 1
                break

        body = "\n".join(chapter_lines[body_start_line:])
        paragraphs = split_paragraphs(body)
        local_line = body_start_line

        for para in paragraphs:
            stat = _analyze_paragraph(
                index=para_index,
                paragraph=para,
                chapter=chapter_name,
                line_offset=global_line + local_line,
                language=language,
            )
            if stat:
                stats.append(stat)
                para_index += 1

            # Advance cursor past this paragraph plus its trailing blank line.
            local_line += para.count("\n") + 2

        global_line += len(chapter_lines) + 1

    return stats


def _section_stats(paragraphs: list[ParagraphStats]) -> list[SectionStats]:
    """Aggregate per-chapter statistics from paragraph stats."""
    by_section: dict[str, list[ParagraphStats]] = {}
    for p in paragraphs:
        by_section.setdefault(p.chapter, []).append(p)

    sections: list[SectionStats] = []
    for name, paras in by_section.items():
        cvs = [p.cv for p in paras]
        all_lengths: list[int] = []
        for p in paras:
            all_lengths.extend(p.lengths)
        sections.append(
            SectionStats(
                name=name,
                n_paragraphs=len(paras),
                n_sentences=sum(p.n_sentences for p in paras),
                mean_sentence_length=round(sum(all_lengths) / len(all_lengths), 2) if all_lengths else 0.0,
                mean_cv=round(sum(cvs) / len(cvs), 3) if cvs else 0.0,
                min_cv=round(min(cvs), 3) if cvs else 0.0,
                max_cv=round(max(cvs), 3) if cvs else 0.0,
            )
        )
    return sections


def _histogram(lengths: list[int], language: Language) -> dict[str, int]:
    """Return sentence-length histogram buckets."""
    if language == "en":
        buckets = [(0, 10), (10, 15), (15, 20), (20, 25), (25, 30), (30, 40), (40, 60), (60, 100), (100, 9999)]
    else:
        buckets = [(0, 10), (10, 15), (15, 20), (20, 25), (25, 30), (30, 40), (40, 60), (60, 100), (100, 9999)]

    labels = [f"{lo}-{hi}" for lo, hi in buckets]
    counts = {label: 0 for label in labels}
    for length in lengths:
        for i, (lo, hi) in enumerate(buckets):
            if lo <= length < hi:
                counts[labels[i]] += 1
                break
    return counts


def _cv_bucket_counts(paragraphs: list[ParagraphStats]) -> dict[str, int]:
    """Count paragraphs by CV bucket."""
    buckets = {
        "< 0.20 非常均匀": 0,
        "0.20-0.30 均匀": 0,
        "0.30-0.45 边缘": 0,
        "0.45-0.65 健康": 0,
        ">= 0.65 变化较大": 0,
    }
    for p in paragraphs:
        cv = p.cv
        if cv < 0.20:
            buckets["< 0.20 非常均匀"] += 1
        elif cv < 0.30:
            buckets["0.20-0.30 均匀"] += 1
        elif cv < 0.45:
            buckets["0.30-0.45 边缘"] += 1
        elif cv < 0.65:
            buckets["0.45-0.65 健康"] += 1
        else:
            buckets[">= 0.65 变化较大"] += 1
    return buckets


def analyze(text: str, language: Language = "zh") -> AnalyzerReport:
    """Analyze sentence-length uniformity at the paragraph level.

    Args:
        text: The input prose to analyze.
        language: "zh" for Chinese (CJK characters) or "en" for English (words).

    Returns:
        AnalyzerReport with issues and a rich metrics bundle.
    """
    if is_short_text(text):
        return AnalyzerReport(issues=[], metrics={"sentence_cv": 0.0})

    paragraphs = _collect_paragraphs(text, language)
    if len(paragraphs) < MIN_PARAGRAPHS:
        return AnalyzerReport(issues=[], metrics={"sentence_cv": 0.0})

    all_lengths: list[int] = []
    for p in paragraphs:
        all_lengths.extend(p.lengths)

    overall_cv = safe_cv(all_lengths)
    paragraph_cvs = [p.cv for p in paragraphs]
    paragraph_cv_mean = sum(paragraph_cvs) / len(paragraph_cvs)
    paragraph_cvs_sorted = sorted(paragraph_cvs)
    mid = len(paragraph_cvs) // 2
    if len(paragraph_cvs) % 2 == 0:
        paragraph_cv_median = (paragraph_cvs_sorted[mid - 1] + paragraph_cvs_sorted[mid]) / 2
    else:
        paragraph_cv_median = paragraph_cvs_sorted[mid]

    uniform_paragraphs = [p for p in paragraphs if p.cv < CV_UNIFORM]
    uniform_paragraph_count = len(uniform_paragraphs)
    uniform_paragraph_ratio = uniform_paragraph_count / len(paragraphs)

    sections = _section_stats(paragraphs)
    section_mean_cv = {s.name: s.mean_cv for s in sections}
    histogram = _histogram(all_lengths, language)
    cv_buckets = _cv_bucket_counts(paragraphs)

    unit = _length_unit(language)

    metrics = {
        "sentence_cv": round(overall_cv, 3),
        "paragraph_cv_mean": round(paragraph_cv_mean, 3),
        "paragraph_cv_median": round(paragraph_cv_median, 3),
        "paragraph_cv_min": round(min(paragraph_cvs), 3),
        "paragraph_cv_max": round(max(paragraph_cvs), 3),
        "n_paragraphs_analyzed": len(paragraphs),
        "n_sentences_analyzed": len(all_lengths),
        "sentence_mean": round(sum(all_lengths) / len(all_lengths), 2) if all_lengths else 0.0,
        "sentence_std": round(
            (sum((x - (sum(all_lengths) / len(all_lengths))) ** 2 for x in all_lengths) / len(all_lengths)) ** 0.5, 2
        ) if all_lengths else 0.0,
        "uniform_paragraph_count": uniform_paragraph_count,
        "uniform_paragraph_ratio": round(uniform_paragraph_ratio, 3),
        "section_mean_cv": section_mean_cv,
        "sentence_length_histogram": histogram,
        "cv_distribution": cv_buckets,
        "uniform_paragraphs": [
            {
                "index": p.index,
                "chapter": p.chapter,
                "line_start": p.line_start,
                "line_end": p.line_end,
                "preview": p.preview,
                "cv": p.cv,
                "mean": p.mean,
                "std": p.std,
                "min": p.min,
                "max": p.max,
                "n_sentences": p.n_sentences,
            }
            for p in sorted(uniform_paragraphs, key=lambda x: x.cv)
        ],
        "sections": [
            {
                "name": s.name,
                "n_paragraphs": s.n_paragraphs,
                "n_sentences": s.n_sentences,
                "mean_sentence_length": s.mean_sentence_length,
                "mean_cv": s.mean_cv,
                "min_cv": s.min_cv,
                "max_cv": s.max_cv,
            }
            for s in sections
        ],
        "language": language,
        "length_unit": unit,
    }

    issues: list[AnalyzerIssue] = []

    # Issue 1: overall high uniformity (worst paragraph CV is very low).
    worst_cv = min(paragraph_cvs)
    if worst_cv < CV_HARD:
        issues.append(
            AnalyzerIssue(
                analyzer_id=ID,
                severity="high",
                confidence=round(min(1.0, max(0.0, 1.0 - worst_cv)), 3),
                location="global",
                evidence=(
                    f"句子长度高度均匀：最低段落 CV={worst_cv:.2f}<{CV_HARD}，"
                    f"{uniform_paragraph_count}/{len(paragraphs)} 段 CV<{CV_UNIFORM}"
                ),
                suggestion="混合长短句，避免同一段内句子长度过于接近。",
            )
        )

    # Issue 2: too many uniform paragraphs (AI_artifact_detection empirical ratio).
    if uniform_paragraph_ratio > 0.35:
        issues.append(
            AnalyzerIssue(
                analyzer_id=ID,
                severity="high",
                confidence=round(min(1.0, max(0.0, uniform_paragraph_ratio)), 3),
                location="global",
                evidence=(
                    f"uniform 段落占比过高：{uniform_paragraph_ratio:.1%} 的段落 CV<{CV_UNIFORM}，"
                    f"建议重点改写这些段落"
                ),
                suggestion="打断平行句式、拆分复合句、插入短句，提升段落内节奏变化。",
            )
        )
    elif uniform_paragraph_ratio >= 0.20:
        issues.append(
            AnalyzerIssue(
                analyzer_id=ID,
                severity="medium",
                confidence=round(min(1.0, max(0.0, uniform_paragraph_ratio + 0.2)), 3),
                location="global",
                evidence=(
                    f"uniform 段落占比较高：{uniform_paragraph_ratio:.1%} 的段落 CV<{CV_UNIFORM}"
                ),
                suggestion="增加长短句变化，让段落节奏更像人写。",
            )
        )
    elif uniform_paragraph_ratio >= 0.10:
        issues.append(
            AnalyzerIssue(
                analyzer_id=ID,
                severity="low",
                confidence=round(min(1.0, max(0.0, uniform_paragraph_ratio + 0.3)), 3),
                location="global",
                evidence=(
                    f"少量 uniform 段落：{uniform_paragraph_ratio:.1%} 的段落 CV<{CV_UNIFORM}"
                ),
                suggestion="检查这些段落是否需要更多句式变化。",
            )
        )

    # Issue 3: flag individual uniform paragraphs so they appear in high-risk
    # annotations and the modify plan.
    for p in sorted(uniform_paragraphs, key=lambda x: x.cv)[:20]:
        issues.append(
            AnalyzerIssue(
                analyzer_id=ID,
                severity="medium" if p.cv < CV_VERY_UNIFORM else "low",
                confidence=round(min(1.0, max(0.0, 1.0 - p.cv)), 3),
                location=f"paragraph:{p.line_start}-{p.line_end}",
                evidence=(
                    f"{p.preview[:50]} | 段落句长均匀：CV={p.cv:.3f}，"
                    f"平均 {p.mean:.0f}{unit}，范围 [{p.min},{p.max}]{unit}"
                ),
                suggestion="在该段落内插入短句或拆分长句，打破均匀节奏。",
            )
        )

    return AnalyzerReport(issues=issues, metrics=metrics)
