"""Dimension 8a — Inter-paragraph structural uniformity.

A paragraph's "structure" can be summarised as a coarse 4-tuple:

    (lead_bucket, body_cv_bucket, tail_bucket, sentence_count_bucket)

where each bucket is a categorical value rather than raw numbers. Two
adjacent paragraphs whose 4-tuples match tend to feel mechanical, even if
their actual words are different. We catch *runs* of identical or near-
identical tuples.

"Bucket" definitions live in `_segments.length_bucket`. The grouping is
deliberately coarse so a natural-looking variation still slips through
without being flagged.
"""

from __future__ import annotations

from scripts.analyzers._segments import (
    cjk_chars,
    is_short_text,
    leading_phrase,
    length_bucket,
    safe_cv,
    split_paragraphs,
    split_sentences,
    trailing_phrase,
)
from scripts.analyzers._types import AnalyzerIssue, AnalyzerReport


ID = "paragraph_structure_uniformity"

LEADING_N = 6
WINDOW = 3  # consecutive paragraphs sharing the same bucket tuple

# Within-bucket similarity: the body length-bucket sequence for a paragraph.
# Two paragraphs sharing the same lead/tail and very similar body lengths is
# the strongest "mechanical" signal we have.


def _structure_tuple(paragraph: str) -> tuple:
    sentences = [s for s in split_sentences(paragraph) if cjk_chars(s) > 0]
    if not sentences:
        return ()
    length_buckets = tuple(length_bucket(cjk_chars(s)) for s in sentences)
    if not length_buckets:
        return ()
    body_cv = round(safe_cv([cjk_chars(s) for s in sentences]), 1)
    return (
        leading_phrase(sentences[0], LEADING_N),
        trailing_phrase(sentences[-1], LEADING_N),
        length_buckets,
        body_cv,
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
            if run_length >= 3:
                runs.append((start, run_length, prev))
            start = i
            prev = values[i]
    run_length = len(values) - start
    if run_length >= 3:
        runs.append((start, run_length, prev))
    return runs


def analyze(text: str) -> AnalyzerReport:
    if is_short_text(text):
        return AnalyzerReport(issues=[], metrics={"structure_uniform_runs": 0.0})

    paragraphs = [p for p in split_paragraphs(text) if cjk_chars(p) >= 60]
    if len(paragraphs) < WINDOW:
        return AnalyzerReport(
            issues=[],
            metrics={"structure_uniform_runs": 0.0, "structure_paragraph_count": float(len(paragraphs))},
        )

    tuples = [_structure_tuple(p) for p in paragraphs]
    runs = _consecutive_runs(tuples)

    issues: list[AnalyzerIssue] = []
    for start_index, run_length, _tuple in runs:
        if run_length >= 6:
            severity = "high"
            confidence = 0.85
        elif run_length >= WINDOW:
            severity = "medium"
            confidence = 0.55
        else:
            continue
        end_index = start_index + run_length - 1
        issues.append(
            AnalyzerIssue(
                analyzer_id=ID,
                severity=severity,
                confidence=confidence,
                location=f"paragraph:{start_index}-{end_index}",
                evidence=(
                    f"段间句式指纹连续 {run_length} 段相同：开头/结尾/句长分布近似"
                ),
                suggestion="让相邻段落切换开场词、收束方式或句长组合，避免章法复制。",
            )
        )

    return AnalyzerReport(
        issues=issues,
        metrics={
            "structure_uniform_runs": float(len(issues)),
            "structure_paragraph_count": float(len(paragraphs)),
        },
    )
