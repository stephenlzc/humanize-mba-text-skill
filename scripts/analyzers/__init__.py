"""Public entry point for prose-structure and semantic-chain analyzers.

Two related surfaces live here:

- Prose-structure analyzers (dimensions 6, 8, 9, 10, chapter template).
  Call ``run_prose_analyzers(text)`` for one merged ``AnalyzerReport``.
- Semantic-chain analyzers (dimensions 3, 4, 5). Call
  ``run_semantic_chain_analyzers(text)`` for one merged report.

The rewrite planner turns either report into a structured modify plan; call
``build_modify_plan(report)`` to get a list of ``ModifyEntry``.
"""

from __future__ import annotations

from scripts.analyzers._types import AnalyzerIssue, AnalyzerReport
from scripts.analyzers import (
    sentence_length,
    paragraph_length,
    paragraph_edges,
    paragraph_structure,
    chapter_template,
    semantic_chain,
)
from scripts.analyzers.rewrite_planner import ModifyEntry, build_modify_plan, merge_plans


ANALYZERS = (
    sentence_length,
    paragraph_length,
    paragraph_edges,
    paragraph_structure,
    chapter_template,
)


CHAIN_ANALYZER_MODULES = (
    semantic_chain,
)


def run_prose_analyzers(text: str) -> AnalyzerReport:
    """Run every prose-structure analyzer and return a merged report."""
    merged = AnalyzerReport()
    for analyzer in ANALYZERS:
        result = analyzer.analyze(text)
        merged.merge(result)
    return merged


# Backward-compatible alias retained for callers that already use the old name.
run_semantic_chain_analyzers = semantic_chain.chain_analyze


__all__ = [
    "ANALYZERS",
    "CHAIN_ANALYZER_MODULES",
    "AnalyzerIssue",
    "AnalyzerReport",
    "ModifyEntry",
    "build_modify_plan",
    "merge_plans",
    "run_prose_analyzers",
    "run_semantic_chain_analyzers",
    "sentence_length",
    "paragraph_length",
    "paragraph_edges",
    "paragraph_structure",
    "chapter_template",
    "semantic_chain",
]
