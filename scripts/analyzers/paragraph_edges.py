"""Dimension 10 — Paragraph-edge (lead-in / lead-out) template repetition.

AI loves to start paragraphs with the same handful of phrases ("综上所述",
"值得注意的是", "通过分析"), and end them with another small bag ("取得
显著效果", "具有重要意义", "需要进一步研究"). Human writers reuse these
phrases too, but rarely back-to-back for many paragraphs in a row.

We fingerprint each paragraph's first non-punctuation sentence prefix and
its last non-punctuation sentence suffix, then flag runs of identical
fingerprints. To avoid false positives on a single reused phrase, we look
for *consecutive* matches at minimum length 3 (medium) / 5 (high).
"""

from __future__ import annotations

from scripts.analyzers._segments import (
    cjk_chars,
    is_short_text,
    leading_phrase,
    split_paragraphs,
    split_sentences,
    trailing_phrase,
)
from scripts.analyzers._types import AnalyzerIssue, AnalyzerReport


ID = "paragraph_edge_template_repeat"

LEAD_RUN_MEDIUM = 3
LEAD_RUN_HIGH = 5
LEADING_N_CHARS = 6


def _consecutive_runs(values):
    """Return list of (start_index, length) for runs of identical values."""
    runs = []
    if not values:
        return runs
    start = 0
    prev = values[0]
    for i in range(1, len(values)):
        if values[i] != prev:
            if i - start >= 2:
                runs.append((start, i - start, prev))
            start = i
            prev = values[i]
    if len(values) - start >= 2:
        runs.append((start, len(values) - start, prev))
    return runs


def _first_sentence(paragraph):
    sentences = split_sentences(paragraph)
    return sentences[0] if sentences else ""


def _last_sentence(paragraph):
    sentences = split_sentences(paragraph)
    return sentences[-1] if sentences else ""


def _runs_to_issues(runs, run_id, location_kind, side_label, suggestion):
    issues = []
    for start_index, run_length, phrase in runs:
        if not phrase:
            continue
        end_index = start_index + run_length - 1
        if run_length >= LEAD_RUN_HIGH:
            severity = "high"
        elif run_length >= LEAD_RUN_MEDIUM:
            severity = "medium"
        else:
            continue
        confidence = min(1.0, 0.4 + (run_length - 2) * 0.1)
        issues.append(
            AnalyzerIssue(
                analyzer_id=run_id,
                severity=severity,
                confidence=round(confidence, 3),
                location=f"{location_kind}:{start_index}-{end_index}",
                evidence=(
                    f"{side_label}模板连续 {run_length} 段重复：「{phrase}」"
                ),
                suggestion=suggestion,
            )
        )
    return issues


def analyze(text: str) -> AnalyzerReport:
    if is_short_text(text):
        return AnalyzerReport(issues=[], metrics={"edge_repeat_runs": 0.0})

    paragraphs = [p for p in split_paragraphs(text) if cjk_chars(p) >= 30]
    if len(paragraphs) < 3:
        return AnalyzerReport(
            issues=[],
            metrics={"edge_repeat_runs": 0.0, "edge_paragraph_count": float(len(paragraphs))},
        )

    leading = [
        leading_phrase(_first_sentence(p), LEADING_N_CHARS) for p in paragraphs
    ]
    trailing = [
        trailing_phrase(_last_sentence(p), LEADING_N_CHARS) for p in paragraphs
    ]

    lead_runs = _consecutive_runs(leading)
    trail_runs = _consecutive_runs(trailing)

    issues: list[AnalyzerIssue] = []
    issues.extend(
        _runs_to_issues(
            lead_runs,
            ID,
            "paragraph",
            "段首",
            "为每段尝试不同的开头，避免连续段落使用同一开场词组。",
        )
    )
    issues.extend(
        _runs_to_issues(
            trail_runs,
            ID,
            "paragraph",
            "段尾",
            "段尾应有不同收束方式（数据、问题、对比），避免连续段落套用同一结句。",
        )
    )

    return AnalyzerReport(
        issues=issues,
        metrics={
            "edge_repeat_runs": float(len(issues)),
            "edge_paragraph_count": float(len(paragraphs)),
        },
    )
