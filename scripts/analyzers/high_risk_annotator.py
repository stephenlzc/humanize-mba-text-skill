"""Sentence-level high-risk annotation aggregator.

Produces ``high_risk_annotations`` rows for the detection report: one entry
per sentence, aggregating every rule that fired inside it. Each entry combines
the sentence anchor (char offset + line number + text), the triggered rules'
phrase-level replacement suggestions (sourced from TOML
``phrase_replacements``), and a concrete rewrite pair (sourced from TOML
``[[categories.examples]]``).

Decoupled from ``scripts.detect_ai_patterns`` on purpose: the module consumes
duck-typed ``PatternMatch``-like objects (anything exposing ``line_number``,
``content``, ``pattern_type``, ``pattern_name``, ``severity``) so the import
graph stays acyclic.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from typing import Any, Iterable

from scripts.analyzers._types import AnalyzerIssue
from scripts.analyzers.rewrite_planner import _SKELETONS, _DEFAULT_SKELETON


# ---------------------------------------------------------------------------
# Constants — mirror what detect_ai_patterns.py emits. Re-declared here to
# avoid a runtime circular import.
# ---------------------------------------------------------------------------

PROSE_ANALYZER_LABEL = "结构统计"
CHAIN_ANALYZER_LABEL = "语义链统计"

PROSE_ANALYZER_IDS = frozenset(
    {
        "uniform_sentence_length",
        "uniform_paragraph_length",
        "paragraph_edge_template_repeat",
        "paragraph_structure_uniformity",
        "chapter_template_repeat",
    }
)

CHAIN_ANALYZER_IDS = frozenset(
    {
        "chain_three_part_rule",
        "chain_author_listing",
        "chain_method_name",
        "chain_abstract_template",
        "chain_conclusion_echo",
        "chain_vague_problem_statement",
        "chain_unsupported_quantification",
        "chain_macro_narrative",
        "evidence_chain_completeness",
        "cross_section_problem_trace",
    }
)

SEVERITY_RANK = {"high": 0, "medium": 1, "low": 2}

# Same terminator set as scripts.analyzers._segments._TERMINATOR_RE so the
# notion of "sentence" stays consistent across the codebase.
_TERMINATOR_RE = re.compile(r"[。！？]")


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class TriggeredRule:
    """One rule that fired inside the enclosing sentence."""

    rule_id: str
    pattern_name: str
    pattern_type: str               # "regex" | "prose" | "chain"
    evidence: str
    confidence: float
    severity: str
    phrase_replacements: list[str] = field(default_factory=list)
    before_after_example: dict | None = None


@dataclass
class HighRiskAnnotation:
    """One row of ``report["high_risk_annotations"]``."""

    sentence_index: int
    char_offset_start: int
    char_offset_end: int
    sentence_text: str
    line_number: int
    severity: str
    triggered_rules: list[TriggeredRule]
    rewrite_template: str
    recommended_replacements: list[str]

    def to_dict(self) -> dict:
        return {
            "sentence_index": self.sentence_index,
            "char_offset_start": self.char_offset_start,
            "char_offset_end": self.char_offset_end,
            "sentence_text": self.sentence_text,
            "line_number": self.line_number,
            "severity": self.severity,
            "triggered_rules": [asdict(r) for r in self.triggered_rules],
            "rewrite_template": self.rewrite_template,
            "recommended_replacements": list(self.recommended_replacements),
        }


SentenceSpan = tuple[int, int, int, str]   # (line_no, char_start, char_end, text)


# ---------------------------------------------------------------------------
# Sentence boundaries
# ---------------------------------------------------------------------------


def _has_real_content(fragment: str) -> bool:
    """Return True when ``fragment`` has at least one non-terminator char.

    ``str.strip()`` treats Chinese terminators like ``。`` as non-whitespace,
    so ``"。".strip()`` still equals ``"。"``. We need to peel off terminators
    explicitly to recognise pure-terminator fragments (``。。``, ``。！``) as
    empty.
    """
    return any(ch not in "。！？" for ch in fragment)


def compute_sentence_spans(text: str) -> list[SentenceSpan]:
    """Return ``[(line_no, char_start, char_end, sentence_text), ...]``.

    ``char_end`` is exclusive and points at the terminator so substring slicing
    is trivial. Empty fragments (e.g. ``。。``) are dropped.

    ``line_no`` is computed by counting ``\\n`` in ``[0, match.end())`` so it
    matches the 1-based line numbers produced by ``text.split("\\n")`` used
    in ``detect_ai_patterns.detect_patterns``. Counting only up to ``cursor``
    (start of the fragment) would under-count newlines that immediately
    follow the previous terminator and mis-align regex buckets.
    """
    if not text:
        return []
    spans: list[SentenceSpan] = []
    cursor = 0
    for match in _TERMINATOR_RE.finditer(text):
        raw = text[cursor:match.end()]
        stripped = raw.strip()
        if stripped and _has_real_content(stripped):
            line_number = text.count("\n", 0, match.end()) + 1
            spans.append((line_number, cursor, match.end(), stripped))
        cursor = match.end()
    tail = text[cursor:].strip()
    if tail and _has_real_content(tail):
        line_number = text.count("\n", 0, len(text)) + 1
        spans.append((line_number, cursor, len(text), tail))
    return spans


# ---------------------------------------------------------------------------
# Bucketing
# ---------------------------------------------------------------------------


def bucket_matches_by_sentence(
    matches: Iterable[Any], spans: list[SentenceSpan]
) -> dict[int, list[tuple[Any, SentenceSpan]]]:
    """Group regex-stage ``PatternMatch``-like objects by their enclosing sentence.

    Regex matches already carry a real ``line_number`` (from
    ``detect_ai_patterns.detect_patterns``). When multiple sentences share a
    line, prefer the one whose ``sentence_text`` contains ``m.content[:30]``;
    otherwise the first sentence on that line wins.
    """
    line_to_indices: dict[int, list[int]] = {}
    for idx, (line_no, *_rest) in enumerate(spans):
        line_to_indices.setdefault(line_no, []).append(idx)

    out: dict[int, list[tuple[Any, SentenceSpan]]] = {}
    for m in matches:
        line_no = getattr(m, "line_number", 0)
        if line_no <= 0:
            continue
        candidates = line_to_indices.get(line_no)
        if not candidates:
            continue
        content = getattr(m, "content", "") or ""
        best: int | None = None
        if content:
            for idx in candidates:
                if content[:30] in spans[idx][3]:
                    best = idx
                    break
        if best is None:
            best = candidates[0]
        out.setdefault(best, []).append((m, spans[best]))
    return out


def _location_candidate_indices(
    location: str, spans: list[SentenceSpan]
) -> list[int]:
    """Narrow candidate sentence indices based on ``AnalyzerIssue.location``."""
    n = len(spans)
    if n == 0:
        return []
    if not location or location == "global":
        return list(range(n))
    if location.startswith("paragraph:"):
        tag = location.split(":", 1)[1]
        if "-" in tag:
            lo, _, hi = tag.partition("-")
            try:
                lo_i, hi_i = int(lo), int(hi)
            except ValueError:
                return list(range(n))
        elif tag.isdigit():
            lo_i = hi_i = int(tag)
        else:  # paragraph:abstract, paragraph:front_matter, ...
            return list(range(n))
        return [i for i, (ln, *_r) in enumerate(spans) if lo_i <= ln <= hi_i]
    if location == "chapter:last":
        last_third = max(0, n - n // 3)
        return list(range(last_third, n))
    if location.startswith("chapter:"):
        return list(range(n))
    return list(range(n))


def bucket_issues_by_sentence(
    issues: Iterable[AnalyzerIssue], spans: list[SentenceSpan]
) -> dict[int, list[tuple[AnalyzerIssue, SentenceSpan]]]:
    """Map ``AnalyzerIssue`` objects (no ``line_number``) into sentence buckets.

    Strategy:
      1. Narrow candidates by parsing ``issue.location``.
      2. Pick the first candidate whose ``sentence_text`` contains
         ``issue.evidence[:30]`` as a substring.
      3. Fall back to ``candidates[0]`` when no substring matches — the
         ``location`` string is still meaningful even when ``evidence`` is
         paraphrased.
      4. Drop issues whose location yields zero candidates.
    """
    out: dict[int, list[tuple[AnalyzerIssue, SentenceSpan]]] = {}
    for issue in issues:
        candidates = _location_candidate_indices(issue.location, spans)
        if not candidates:
            continue
        evidence_fragment = (issue.evidence or "")[:30]
        target_idx: int | None = None
        if evidence_fragment:
            for idx in candidates:
                if evidence_fragment in spans[idx][3]:
                    target_idx = idx
                    break
        if target_idx is None:
            target_idx = candidates[0]
        out.setdefault(target_idx, []).append((issue, spans[target_idx]))
    return out


# ---------------------------------------------------------------------------
# Rule metadata lookups
# ---------------------------------------------------------------------------


def _lookup_phrase_replacements(rule_id: str, rules: dict) -> list[str]:
    """Return the TOML ``phrase_replacements`` list for ``rule_id`` (or ``[]``).

    v2 may insert an LLM fallback here: read the cached list first, otherwise
    call out to a model, otherwise return ``[]``. The dataclass shape already
    accepts an empty list so the upgrade is non-breaking.
    """
    for category in rules.get("categories", []):
        if category.get("id") == rule_id:
            return list(category.get("phrase_replacements") or [])
    return []


def _pick_example_for_rule(
    rule_id: str, rules: dict, sentence_text: str
) -> dict | None:
    """Pick the first ``[[categories.examples]]`` entry that fits the sentence.

    Prefer examples whose ``before`` is a substring of ``sentence_text``; fall
    back to the first well-formed example; return ``None`` if none are usable.
    """
    for category in rules.get("categories", []):
        if category.get("id") != rule_id:
            continue
        examples = category.get("examples") or []
        first_valid: dict | None = None
        for example in examples:
            if not (
                isinstance(example, dict)
                and "before" in example
                and "after" in example
            ):
                continue
            entry = {"before": example["before"], "after": example["after"]}
            if first_valid is None:
                first_valid = entry
            if entry["before"] in sentence_text:
                return entry
        return first_valid
    return None


def _select_skeleton_template(rule_ids: list[str]) -> str:
    """Pick a rewrite template; prefer the first analyzer with a skeleton."""
    for rule_id in rule_ids:
        skeleton = _SKELETONS.get(rule_id)
        if skeleton:
            return skeleton["template"]
    return _DEFAULT_SKELETON["template"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _kind_for_analyzer_id(analyzer_id: str) -> str:
    if analyzer_id in PROSE_ANALYZER_IDS:
        return "prose"
    if analyzer_id in CHAIN_ANALYZER_IDS:
        return "chain"
    return "regex"


def _worst_severity(severities: Iterable[str]) -> str:
    """Return the highest-severity label among ``severities`` (default ``low``)."""
    best = "low"
    best_rank = SEVERITY_RANK.get(best, 2)
    for s in severities:
        rank = SEVERITY_RANK.get(s, 2)
        if rank < best_rank:
            best = s
            best_rank = rank
    return best


# ---------------------------------------------------------------------------
# Public orchestrator
# ---------------------------------------------------------------------------


def build_annotations(
    text: str,
    matches: Iterable[Any],
    prose_issues: Iterable[AnalyzerIssue],
    chain_issues: Iterable[AnalyzerIssue],
    rules: dict,
) -> list[HighRiskAnnotation]:
    """Build the per-sentence annotation list.

    One ``HighRiskAnnotation`` per sentence that fired at least one rule.
    Sorted high→low severity, then by ``char_offset_start`` ascending.
    """
    spans = compute_sentence_spans(text)
    regex_buckets = bucket_matches_by_sentence(matches, spans)
    issue_buckets = bucket_issues_by_sentence(
        list(prose_issues) + list(chain_issues), spans
    )

    annotations: list[HighRiskAnnotation] = []
    for sentence_idx in range(len(spans)):
        line_no, start, end, sentence_text = spans[sentence_idx]
        regex_items = regex_buckets.get(sentence_idx, [])
        issue_items = issue_buckets.get(sentence_idx, [])
        if not regex_items and not issue_items:
            continue

        triggered: list[TriggeredRule] = []
        rec_set: set[str] = set()
        recs: list[str] = []
        rule_ids: list[str] = []

        for m, _span in regex_items:
            rule_id = getattr(m, "pattern_type", "unknown")
            triggered.append(
                TriggeredRule(
                    rule_id=rule_id,
                    pattern_name=getattr(m, "pattern_name", rule_id),
                    pattern_type="regex",
                    evidence=getattr(m, "content", "") or "",
                    confidence=1.0,
                    severity=getattr(m, "severity", "medium"),
                    phrase_replacements=_lookup_phrase_replacements(rule_id, rules),
                    before_after_example=_pick_example_for_rule(
                        rule_id, rules, sentence_text
                    ),
                )
            )
            rule_ids.append(rule_id)
            for rep in triggered[-1].phrase_replacements:
                if rep not in rec_set:
                    rec_set.add(rep)
                    recs.append(rep)

        for issue, _span in issue_items:
            rule_id = issue.analyzer_id
            kind = _kind_for_analyzer_id(rule_id)
            triggered.append(
                TriggeredRule(
                    rule_id=rule_id,
                    pattern_name=(
                        PROSE_ANALYZER_LABEL
                        if kind == "prose"
                        else CHAIN_ANALYZER_LABEL
                    ),
                    pattern_type=kind,
                    evidence=(issue.evidence or "")[:60],
                    confidence=float(getattr(issue, "confidence", 0.5)),
                    severity=issue.severity,
                    phrase_replacements=_lookup_phrase_replacements(rule_id, rules),
                    before_after_example=_pick_example_for_rule(
                        rule_id, rules, sentence_text
                    ),
                )
            )
            rule_ids.append(rule_id)
            for rep in triggered[-1].phrase_replacements:
                if rep not in rec_set:
                    rec_set.add(rep)
                    recs.append(rep)

        annotations.append(
            HighRiskAnnotation(
                sentence_index=sentence_idx,
                char_offset_start=start,
                char_offset_end=end,
                sentence_text=sentence_text,
                line_number=line_no,
                severity=_worst_severity(t.severity for t in triggered),
                triggered_rules=triggered,
                rewrite_template=_select_skeleton_template(rule_ids),
                recommended_replacements=recs,
            )
        )

    annotations.sort(
        key=lambda a: (SEVERITY_RANK.get(a.severity, 3), a.char_offset_start)
    )
    return annotations


__all__ = [
    "TriggeredRule",
    "HighRiskAnnotation",
    "PROSE_ANALYZER_IDS",
    "CHAIN_ANALYZER_IDS",
    "PROSE_ANALYZER_LABEL",
    "CHAIN_ANALYZER_LABEL",
    "compute_sentence_spans",
    "bucket_matches_by_sentence",
    "bucket_issues_by_sentence",
    "build_annotations",
]