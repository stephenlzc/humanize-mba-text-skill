"""Dimension 8b — Chapter-template uniformity.

When chapters share a `shape` — same intro section, same body length bucket,
same closing template — the manuscript feels machine-written. We:

1. Split the manuscript into chapters via ``第N章 ...`` markers.
2. For each chapter compute (intro-sentence fingerprint, body sentence count
   bucket, presence of `展望/对策/小结` markers).
3. Look for consecutive chapters whose tuple matches at minimum length 3.

A single reused chapter shape is humanly fine; three in a row is suspicious.
"""

from __future__ import annotations

import re

from scripts.analyzers._segments import (
    cjk_chars,
    is_short_text,
    leading_phrase,
    split_chapters,
    split_paragraphs,
    split_sentences,
)
from scripts.analyzers._types import AnalyzerIssue, AnalyzerReport


ID = "chapter_template_repeat"

CHAPTER_RUN_MEDIUM = 3
CHAPTER_RUN_HIGH = 5
INTRO_N_CHARS = 6

# Strip the "第N章" / "第N节" prefix so the fingerprint reflects the actual
# content, not the chapter number (which would differ for every chapter).
_CHAPTER_MARKER = re.compile(r"^第\s*[一二三四五六七八九十0-9]+\s*[章节]\s*")


_FORWARD_LOOKING = ("展望", "对策", "建议", "小结", "结语")


def _intro_fingerprint(chapter_text):
    paragraphs = [p for p in split_paragraphs(chapter_text) if cjk_chars(p) >= 30]
    if not paragraphs:
        return ""
    sentences = split_sentences(paragraphs[0])
    if not sentences:
        return ""
    first = _CHAPTER_MARKER.sub("", sentences[0])
    return leading_phrase(first, INTRO_N_CHARS)


def _has_forward_looker(chapter_text):
    for marker in _FORWARD_LOOKING:
        if marker in chapter_text:
            return True
    return False


def _body_sentence_count(chapter_text):
    paragraphs = [p for p in split_paragraphs(chapter_text) if cjk_chars(p) >= 30]
    n_sentences = sum(len(split_sentences(p)) for p in paragraphs)
    if n_sentences <= 5:
        return 5
    if n_sentences <= 10:
        return 10
    if n_sentences <= 20:
        return 20
    if n_sentences <= 40:
        return 40
    return 99


def _chapter_shape(chapter_text):
    return (
        _intro_fingerprint(chapter_text),
        _body_sentence_count(chapter_text),
        _has_forward_looker(chapter_text),
    )


def _consecutive_runs(values):
    runs = []
    if not values:
        return runs
    start = 0
    prev = values[0]
    for i in range(1, len(values)):
        if values[i] != prev:
            run_length = i - start
            if run_length >= 2:
                runs.append((start, run_length, prev))
            start = i
            prev = values[i]
    run_length = len(values) - start
    if run_length >= 2:
        runs.append((start, run_length, prev))
    return runs


def analyze(text: str) -> AnalyzerReport:
    if is_short_text(text):
        return AnalyzerReport(issues=[], metrics={"chapter_template_runs": 0.0})

    chapters = [c for c in split_chapters(text) if cjk_chars(c) >= 100]
    if len(chapters) < CHAPTER_RUN_MEDIUM:
        return AnalyzerReport(
            issues=[],
            metrics={"chapter_template_runs": 0.0, "chapter_count": float(len(chapters))},
        )

    shapes = [_chapter_shape(c) for c in chapters]
    # ignore chapters whose intro fingerprint was empty (those would be noise).
    runs = _consecutive_runs([s for s in shapes if s[0]])

    issues: list[AnalyzerIssue] = []
    for start_index, run_length, _shape in runs:
        if run_length >= CHAPTER_RUN_HIGH:
            severity = "high"
            confidence = 0.8
        elif run_length >= CHAPTER_RUN_MEDIUM:
            severity = "medium"
            confidence = 0.5
        else:
            continue
        end_index = start_index + run_length - 1
        issues.append(
            AnalyzerIssue(
                analyzer_id=ID,
                severity=severity,
                confidence=confidence,
                location=f"chapter:{start_index}-{end_index}",
                evidence=(
                    f"章节章法模板连续 {run_length} 章相似：开头/篇幅桶/小节结构近似"
                ),
                suggestion="在章节层面轮换开头措辞、章节长度或小节结构，避免章节套娃。",
            )
        )

    return AnalyzerReport(
        issues=issues,
        metrics={
            "chapter_template_runs": float(len(issues)),
            "chapter_count": float(len(chapters)),
        },
    )
