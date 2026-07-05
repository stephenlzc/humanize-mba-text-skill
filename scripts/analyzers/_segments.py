"""Shared segmentation helpers for prose-structure analyzers.

Pure functions only — no file I/O, no globals, no side effects. Each analyzer in
this package uses these helpers so that "sentence", "paragraph", and "chapter"
mean the same thing everywhere.
"""

from __future__ import annotations

import re
from typing import Sequence


# Sentence boundary punctuation for Chinese prose.
# Keep this conservative; adding Latin "." would mis-split bullet lists and decimal
# numbers. Words like "3.5" are common in academic writing.
_SENTENCE_TERMINATORS = ("。", "！", "？")
_TERMINATOR_RE = re.compile("[。！？]")


def is_short_text(text: str) -> bool:
    """Return True when the corpus is too small to be statistically meaningful."""
    # 200 chars covers roughly two short paragraphs; below that hand-waving rules
    # dominate and structural statistics are unreliable.
    return len(text.strip()) < 200


def split_paragraphs(text: str) -> list[str]:
    """Split by blank lines. Drop empty fragments. Preserve original order."""
    if not text:
        return []
    # Normalise Windows line endings first so a "\r\n\r\n" never splits wrong.
    normalised = text.replace("\r\n", "\n").replace("\r", "\n")
    parts = re.split(r"\n\s*\n", normalised)
    return [p.strip() for p in parts if p and p.strip()]


def split_sentences(paragraph: str) -> list[str]:
    """Split a single paragraph into sentences by 。！？ and drop empty strings."""
    if not paragraph:
        return []
    parts = _TERMINATOR_RE.split(paragraph)
    return [p.strip() for p in parts if p and p.strip()]


def split_sentences_global(text: str) -> list[str]:
    """Flatten every paragraph and return a flat sentence list."""
    sentences: list[str] = []
    for paragraph in split_paragraphs(text):
        sentences.extend(split_sentences(paragraph))
    return sentences


def split_chapters(text: str) -> list[str]:
    """Split a manuscript into chapters by leading "第N章 ..." / "第N节 ..." lines.

    Many MBA theses use "第N章" headings; some use plain "章 X". Anything that
    does not start a chapter goes into the "front matter" chapter.
    """
    if not text:
        return []
    normalised = text.replace("\r\n", "\n").replace("\r", "\n")
    boundaries: list[int] = [0]
    chapter_re = re.compile(r"^第\s*[一二三四五六七八九十0-9]+\s*[章节][^。！？]*$", re.MULTILINE)
    for match in chapter_re.finditer(normalised):
        boundaries.append(match.start())
    chunks: list[str] = []
    for i in range(len(boundaries)):
        start = boundaries[i]
        end = boundaries[i + 1] if i + 1 < len(boundaries) else len(normalised)
        chunk = normalised[start:end].strip()
        if chunk:
            chunks.append(chunk)
    return chunks or ([normalised.strip()] if normalised.strip() else [])


def cjk_chars(text: str) -> int:
    """Count CJK characters (the units human readers actually count)."""
    return sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")


def mean(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def stddev(values: Sequence[float]) -> float:
    if len(values) < 2:
        return 0.0
    mu = mean(values)
    variance = sum((v - mu) ** 2 for v in values) / len(values)
    return variance ** 0.5


def safe_cv(values: Sequence[float]) -> float:
    """Coefficient of variation. Returns 0.0 when mean <= 0 to keep callers safe."""
    if not values:
        return 0.0
    mu = mean(values)
    if mu <= 0:
        return 0.0
    return stddev(values) / mu


def leading_phrase(text: str, n_chars: int = 6) -> str:
    """First non-punctuation characters, used as a paragraph-edge fingerprint."""
    if not text:
        return ""
    cleaned = text.lstrip(" \t　,.，、:：;；!?！？")
    if not cleaned:
        return ""
    # Prefer CJK characters for the fingerprint; Latin words are usually noise.
    out: list[str] = []
    for ch in cleaned:
        out.append(ch)
        if len(out) >= n_chars:
            break
    return "".join(out)


def trailing_phrase(text: str, n_chars: int = 6) -> str:
    """Last non-punctuation characters (used together with leading_phrase)."""
    if not text:
        return ""
    cleaned = text.rstrip(" \t　,.，、:：;；!?！？")
    if not cleaned:
        return ""
    return cleaned[-n_chars:]


def length_bucket(char_count: int) -> int:
    """Coarse sentence-length bucket for fingerprinting structure variety."""
    if char_count <= 10:
        return 10
    if char_count <= 20:
        return 20
    if char_count <= 35:
        return 35
    if char_count <= 55:
        return 55
    return 99
