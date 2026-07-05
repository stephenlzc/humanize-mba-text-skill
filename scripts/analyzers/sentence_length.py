"""Dimension 6 — Sentence-length distribution uniformity.

AI-generated prose typically has very tight sentence-length distributions.
Human prose mixes short/long sentences in a much wider spread. We compute
the coefficient of variation (CV = std/mean) of sentence length in CJK
characters, both globally and paragraph-by-paragraph.

A paragraph whose sentences all hover around the same length reads like a
machine: short factual paragraphs may legitimately use short sentences, so
the analyzer keeps a soft floor on text length to avoid noisy hits.
"""

from __future__ import annotations

from scripts.analyzers._segments import (
    is_short_text,
    safe_cv,
    split_paragraphs,
    split_sentences,
    cjk_chars,
)
from scripts.analyzers._types import AnalyzerIssue, AnalyzerReport


ID = "uniform_sentence_length"

CV_HARD = 0.18
CV_SOFT = 0.28
MIN_SENTENCES_PER_PARAGRAPH = 3
MIN_PARAGRAPHS = 3


def _cv(values):
    return safe_cv(values)


def analyze(text: str) -> AnalyzerReport:
    if is_short_text(text):
        return AnalyzerReport(issues=[], metrics={"sentence_cv": 0.0})

    paragraphs = [p for p in split_paragraphs(text) if cjk_chars(p) >= 30]
    if len(paragraphs) < MIN_PARAGRAPHS:
        return AnalyzerReport(issues=[], metrics={"sentence_cv": 0.0})

    per_paragraph_cv: list[float] = []
    avg_lengths: list[float] = []
    for p in paragraphs:
        sentences = [s for s in split_sentences(p) if cjk_chars(s) > 0]
        if len(sentences) < MIN_SENTENCES_PER_PARAGRAPH:
            continue
        lengths = [cjk_chars(s) for s in sentences]
        per_paragraph_cv.append(_cv(lengths))
        avg_lengths.append(sum(lengths) / len(lengths))

    if not per_paragraph_cv:
        return AnalyzerReport(issues=[], metrics={"sentence_cv": 0.0})

    uniform_paragraph_count = sum(
        1 for cv in per_paragraph_cv if cv < CV_SOFT
    )
    worst_cv = min(per_paragraph_cv)
    issues: list[AnalyzerIssue] = []
    confidence = 1.0 - worst_cv  # monotone decreasing in uniformity
    if worst_cv < CV_HARD:
        issues.append(
            AnalyzerIssue(
                analyzer_id=ID,
                severity="high",
                confidence=round(min(1.0, max(0.0, confidence)), 3),
                location="global",
                evidence=(
                    f"句子长度高度均匀：CV={worst_cv:.2f}<{CV_HARD}，"
                    f"{uniform_paragraph_count}/{len(per_paragraph_cv)} 段触发规则"
                ),
                suggestion="混合长短句，避免每段都使用相近长度。",
            )
        )
    elif uniform_paragraph_count >= max(3, len(per_paragraph_cv) // 2) and worst_cv < CV_SOFT:
        issues.append(
            AnalyzerIssue(
                analyzer_id=ID,
                severity="medium",
                confidence=round(min(1.0, max(0.0, confidence - 0.1)), 3),
                location="global",
                evidence=(
                    f"句子长度偏向均匀：CV={worst_cv:.2f}，"
                    f"{uniform_paragraph_count}/{len(per_paragraph_cv)} 段触发规则"
                ),
                suggestion="增加长短句变化，让节奏更像人写。",
            )
        )

    return AnalyzerReport(
        issues=issues,
        metrics={
            "sentence_cv": round(worst_cv, 3),
            "uniform_paragraph_ratio": round(
                uniform_paragraph_count / len(per_paragraph_cv), 3
            ),
        },
    )
