"""Lightweight wrapper around ``iter_regex_categories`` for hit-level access.

The chain analyzers (dimensions 3, 4, 5) need more than boolean "did this rule
match" — they need to know *where* and *which exact substring* matched so they
can reason about co-location, distance, and chapter-level patterns.

This module reuses the single regex rule document already declared in
``references/rules/`` (loaded via ``rule_loader.iter_regex_categories``); it does
not introduce a new rule store.
"""

from __future__ import annotations

import re
from typing import Iterable

from scripts.rule_loader import iter_regex_categories


def _build_line_offsets(text: str) -> list[tuple[int, int]]:
    """Return ``[(start_offset, line_no_1based), ...]`` for offset → line lookup."""
    offsets: list[tuple[int, int]] = []
    pos = 0
    for index, line in enumerate(text.split("\n"), start=1):
        offsets.append((pos, index))
        pos += len(line) + 1  # account for the stripped \n
    return offsets


def _line_of(offsets: list[tuple[int, int]], span_start: int) -> int:
    """Find the 1-based line number that contains ``span_start``."""
    last = 1
    for offset, line_no in offsets:
        if offset <= span_start:
            last = line_no
        else:
            break
    return last


def find_hits(
    text: str,
    *,
    include_groups: Iterable[str] | None = None,
    include_category_ids: Iterable[str] | None = None,
) -> list[tuple[str, int, tuple[int, int], str]]:
    """Return ``[(category_id, line_no, (start, end), matched_text), ...]``.

    Walks every regex category the loader yields once, compiles each pattern,
    and emits the matching substrings. The result is a flat list — chain
    analyzers can group by category or scan for repeated counts without
    touching TOML themselves.
    """
    if not text:
        return []
    line_offsets = _build_line_offsets(text)
    hits: list[tuple[str, int, tuple[int, int], str]] = []
    for category in iter_regex_categories(
        include_groups=include_groups,
        include_category_ids=include_category_ids,
    ):
        category_id = category.get("id", "")
        for pattern in category.get("regex_patterns", []):
            try:
                rx = re.compile(pattern, re.MULTILINE)
            except re.error:
                # Skip a malformed entry — the chain layer is best-effort.
                continue
            for match in rx.finditer(text):
                hits.append(
                    (
                        category_id,
                        _line_of(line_offsets, match.start()),
                        (match.start(), match.end()),
                        match.group(0),
                    )
                )
    return hits


def hit_category_set(hits: list[tuple]) -> set[str]:
    """Return the set of distinct category ids present in ``hits``.

    Convenience for analyzers that just want "is this rule present?".
    """
    return {category_id for category_id, _, _, _ in hits}


def count_by_category(hits: list[tuple]) -> dict[str, int]:
    """Return ``{category_id: hit_count}`` for the supplied hits."""
    out: dict[str, int] = {}
    for category_id, _, _, _ in hits:
        out[category_id] = out.get(category_id, 0) + 1
    return out


__all__ = ["find_hits", "hit_category_set", "count_by_category"]
