#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Load Chinese paper humanization rules.

Supports two layouts:
1. Legacy monolithic TOML with a top-level ``[[categories]]`` list.
2. Progressive split layout:
   ``chinese-paper-humanization-rules.toml`` manifest -> ``references/rules/index.toml``
   -> selected category files.

The split layout lets agents read only the lightweight index first, then load a
single group such as ``formatting`` or selected category IDs on demand.
"""

from __future__ import annotations

from pathlib import Path
import tomllib
from typing import Any, Dict, Iterable, Sequence


DEFAULT_RULES_PATH = (
    Path(__file__).resolve().parents[1]
    / "references"
    / "chinese-paper-humanization-rules.toml"
)

_REQUIRED_CATEGORY_FIELDS = (
    "id",
    "name",
    "severity",
    "description",
    "signals",
    "rewrite_principles",
)


def _read_toml(path: Path) -> Dict[str, Any]:
    with path.open("rb") as fp:
        return tomllib.load(fp)


def _as_set(values: Sequence[str] | None) -> set[str] | None:
    return set(values) if values else None


def _source_path(path: str | Path | None = None) -> Path:
    return Path(path) if path else DEFAULT_RULES_PATH


def _manifest_to_index_path(manifest_path: Path, manifest: Dict[str, Any]) -> Path:
    split = manifest.get("split_rules", {})
    directory = split.get("directory")
    index_name = split.get("index", "index.toml")
    if not directory:
        raise ValueError("split_rules.directory is required in split manifest")
    return manifest_path.parent / directory / index_name


def _resolve_index(path: str | Path | None = None) -> tuple[Path | None, Dict[str, Any] | None, Dict[str, Any] | None]:
    """Return (index_path, index_data, monolithic_data)."""
    source = _source_path(path)
    if source.is_dir():
        index_path = source / "index.toml"
        return index_path, _read_toml(index_path), None

    data = _read_toml(source)
    if "split_rules" in data:
        index_path = _manifest_to_index_path(source, data)
        return index_path, _read_toml(index_path), None
    return None, None, data


def _validate_categories(categories: list[Dict[str, Any]]) -> None:
    if not categories:
        raise ValueError("Rule document must contain at least one category")
    for category in categories:
        missing = [field for field in _REQUIRED_CATEGORY_FIELDS if field not in category]
        if missing:
            category_id = category.get("id", "<unknown>")
            raise ValueError(f"Category {category_id} missing fields: {', '.join(missing)}")


def _filter_categories(
    categories: list[Dict[str, Any]],
    include_category_ids: Sequence[str] | None = None,
) -> list[Dict[str, Any]]:
    ids = _as_set(include_category_ids)
    if not ids:
        return list(categories)
    return [category for category in categories if category.get("id") in ids]


def load_rule_index(path: str | Path | None = None) -> Dict[str, Any]:
    """Load only the lightweight split-rule index; do not load category bodies."""
    index_path, index, monolithic = _resolve_index(path)
    if monolithic is not None:
        return {
            "version": monolithic.get("version"),
            "language": monolithic.get("language"),
            "domain": monolithic.get("domain"),
            "design_principles": monolithic.get("design_principles", {}),
            "user_constraints": monolithic.get("user_constraints", {}),
            "rule_files": [
                {
                    "id": "monolithic",
                    "path": str(_source_path(path)),
                    "category_ids": [c["id"] for c in monolithic.get("categories", [])],
                }
            ],
        }
    assert index is not None and index_path is not None
    # Deliberately omit category bodies to keep this context-light.
    return dict(index)


def _selected_rule_files(
    index: Dict[str, Any],
    include_groups: Sequence[str] | None = None,
    include_category_ids: Sequence[str] | None = None,
) -> list[Dict[str, Any]]:
    groups = _as_set(include_groups)
    ids = _as_set(include_category_ids)
    files = []
    for rule_file in index.get("rule_files", []):
        if groups and rule_file.get("id") not in groups:
            continue
        if ids and not (set(rule_file.get("category_ids", [])) & ids):
            continue
        files.append(rule_file)
    return files


def _load_split_rules(
    index_path: Path,
    index: Dict[str, Any],
    include_groups: Sequence[str] | None = None,
    include_category_ids: Sequence[str] | None = None,
) -> Dict[str, Any]:
    base_dir = index_path.parent
    categories: list[Dict[str, Any]] = []
    for rule_file in _selected_rule_files(index, include_groups, include_category_ids):
        chunk = _read_toml(base_dir / rule_file["path"])
        categories.extend(_filter_categories(chunk.get("categories", []), include_category_ids))

    support_files = index.get("support_files", {})
    chapter_categories: list[Dict[str, Any]] = []
    metrics: Dict[str, Any] = {}
    if not include_groups and not include_category_ids:
        chapter_path = support_files.get("chapter_categories")
        if chapter_path:
            chapter_categories = _read_toml(base_dir / chapter_path).get("chapter_categories", [])
        metrics_path = support_files.get("metrics")
        if metrics_path:
            metrics = _read_toml(base_dir / metrics_path).get("metrics", {})

    rules = {
        "version": index.get("version"),
        "language": index.get("language"),
        "domain": index.get("domain"),
        "design_principles": index.get("design_principles", {}),
        "user_constraints": index.get("user_constraints", {}),
        "categories": categories,
        "chapter_categories": chapter_categories,
        "metrics": metrics,
    }
    _validate_categories(categories)
    return rules


def load_rules(
    path: str | Path | None = None,
    include_groups: Sequence[str] | None = None,
    include_category_ids: Sequence[str] | None = None,
) -> Dict[str, Any]:
    """Load rules, optionally only selected groups or category IDs."""
    index_path, index, monolithic = _resolve_index(path)
    if monolithic is not None:
        categories = _filter_categories(monolithic.get("categories", []), include_category_ids)
        if include_groups:
            # Monolithic files have no group metadata; group filtering is only available in split layout.
            categories = []
        _validate_categories(categories)
        result = dict(monolithic)
        result["categories"] = categories
        return result
    assert index_path is not None and index is not None
    return _load_split_rules(index_path, index, include_groups, include_category_ids)


def iter_regex_categories(
    path: str | Path | None = None,
    include_groups: Sequence[str] | None = None,
    include_category_ids: Sequence[str] | None = None,
) -> Iterable[Dict[str, Any]]:
    """Yield regex-backed categories progressively, loading one split file at a time."""
    index_path, index, monolithic = _resolve_index(path)
    if monolithic is not None:
        for category in _filter_categories(monolithic.get("categories", []), include_category_ids):
            if category.get("regex_patterns"):
                yield category
        return

    assert index_path is not None and index is not None
    base_dir = index_path.parent
    for rule_file in _selected_rule_files(index, include_groups, include_category_ids):
        chunk = _read_toml(base_dir / rule_file["path"])
        for category in _filter_categories(chunk.get("categories", []), include_category_ids):
            if category.get("regex_patterns"):
                yield category
