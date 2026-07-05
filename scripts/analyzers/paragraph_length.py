"""Dimension 9 — Paragraph-length uniformity.

AI tends to lay out paragraphs at a single length (every paragraph is the
"right" answer for the model), while human writers alternate dense analysis
paragraphs with short transitional ones. We compute the coefficient of
variation of CJK character counts across paragraphs.
"""

from __future__ import annotations

from scripts.analyzers._segments import (
    cjk_chars,
    is_short_text,
    safe_cv,
    split_paragraphs,
)
from scripts.analyzers._types import AnalyzerIssue, AnalyzerReport


ID = "uniform_paragraph_length"

CV_HARD = 0.25
CV_SOFT = 0.40
MIN_PARAGRAPHS = 5


def analyze(text: str) -> AnalyzerReport:
    if is_short_text(text):
        return AnalyzerReport(issues=[], metrics={"paragraph_cv": 0.0})

    paragraphs = [p for p in split_paragraphs(text) if cjk_chars(p) >= 30]
    if len(paragraphs) < MIN_PARAGRAPHS:
        return AnalyzerReport(issues=[], metrics={"paragraph_cv": 0.0})

    lengths = [cjk_chars(p) for p in paragraphs]
    cv = safe_cv(lengths)
    issues: list[AnalyzerIssue] = []

    if cv < CV_HARD:
        issues.append(
            AnalyzerIssue(
                analyzer_id=ID,
                severity="high",
                confidence=round(min(1.0, 1.0 - cv / CV_HARD), 3),
                location="global",
                evidence=(
                    f"段落字数高度均匀：CV={cv:.2f}<{CV_HARD}，"
                    f"{len(paragraphs)} 段落的标准差{sum((l - sum(lengths)/len(lengths))**2 for l in lengths)**0.5:.0f}"
                ),
                suggestion="在长论述段之间插入短过渡段或单句段，模仿自然写作节奏。",
            )
        )
    elif cv < CV_SOFT:
        issues.append(
            AnalyzerIssue(
                analyzer_id=ID,
                severity="medium",
                confidence=round(min(1.0, 1.0 - cv / CV_SOFT), 3),
                location="global",
                evidence=(
                    f"段落字数偏均匀：CV={cv:.2f}<{CV_SOFT}，共 {len(paragraphs)} 段"
                ),
                suggestion="让段落长度有明显对比，避免每段都接近同一长度。",
            )
        )

    return AnalyzerReport(
        issues=issues,
        metrics={
            "paragraph_cv": round(cv, 3),
            "paragraph_count": float(len(paragraphs)),
        },
    )
