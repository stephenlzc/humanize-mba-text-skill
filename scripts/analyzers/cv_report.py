"""CV report renderer for sentence-length uniformity analysis.

Produces the Chinese Markdown report sections requested by users:

1. Overall statistics
2. CV distribution (text bar chart)
3. Most uniform paragraphs (CV < 0.30)
4. Section summary
5. Sentence-length histogram
"""

from __future__ import annotations

from typing import Any


BAR_CHAR = "█"


def _bar(pct: float, width: int = 25) -> str:
    """Return a text bar of fixed maximum width."""
    chars = int(round(pct / 100 * width))
    return BAR_CHAR * max(0, min(width, chars))


def _pct(count: int, total: int) -> float:
    return (100 * count / total) if total else 0.0


def render_overall(metrics: dict[str, Any]) -> list[str]:
    """Render the 'Overall statistics' section."""
    unit = metrics.get("length_unit", "字")
    lines = [
        "## 整体统计",
        "",
        f"- 分析段落数：**{metrics.get('n_paragraphs_analyzed', 0)}**",
        f"- 分析句子数：**{metrics.get('n_sentences_analyzed', 0)}**",
        f"- 平均句长：**{metrics.get('sentence_mean', 0.0):.2f}** {unit}",
        f"- 句长标准差：**{metrics.get('sentence_std', 0.0):.2f}** {unit}",
        f"- 整体句长 CV：**{metrics.get('sentence_cv', 0.0):.3f}**",
        f"- 段落平均 CV：**{metrics.get('paragraph_cv_mean', 0.0):.3f}**",
        f"- 段落 CV 中位数：**{metrics.get('paragraph_cv_median', 0.0):.3f}**",
        f"- 最低/最高段落 CV：**{metrics.get('paragraph_cv_min', 0.0):.3f} / {metrics.get('paragraph_cv_max', 0.0):.3f}**",
        f"- Uniform 段落占比：**{metrics.get('uniform_paragraph_ratio', 0.0):.1%}** "
        f"({metrics.get('uniform_paragraph_count', 0)} / {metrics.get('n_paragraphs_analyzed', 0)})",
    ]
    return lines


def render_cv_distribution(metrics: dict[str, Any]) -> list[str]:
    """Render the 'CV distribution' section with text bars."""
    cv_buckets = metrics.get("cv_distribution", {}) or {}
    if not cv_buckets:
        return []

    total = sum(cv_buckets.values())
    lines = ["## CV 分布", ""]
    for label, count in cv_buckets.items():
        pct = _pct(count, total)
        bar = _bar(pct)
        lines.append(f"- {label}：**{count}** 段 ({pct:.1f}%) {bar}")
    return lines


def render_uniform_paragraphs(metrics: dict[str, Any]) -> list[str]:
    """Render the 'Most uniform paragraphs' section as a full table."""
    unit = metrics.get("length_unit", "字")
    uniform = metrics.get("uniform_paragraphs", []) or []
    lines = [
        f"## Uniform 段落详情（CV < 0.30）— 共 {len(uniform)} 段",
        "",
    ]
    if not uniform:
        lines.append("- 无 CV < 0.30 的段落。")
        return lines

    lines.append(
        f"| CV | 平均句长({unit}) | 范围({unit}) | 句数 | 章节 | 内容片段 |"
    )
    lines.append("|------|------------|----------|------|------|----------|")

    for p in uniform:
        preview = (p.get("preview") or "").replace("|", "\\|").replace("\n", " ")
        chapter = (p.get("chapter") or "(正文)")[:30].replace("|", "\\|")
        lines.append(
            f"| {p.get('cv', 0.0):.3f} | {p.get('mean', 0.0):.0f}±{p.get('std', 0.0):.0f} | "
            f"[{p.get('min', 0)},{p.get('max', 0)}] | {p.get('n_sentences', 0)} | {chapter} | {preview} |"
        )
    return lines


def render_section_summary(metrics: dict[str, Any]) -> list[str]:
    """Render the per-section/chapter summary table."""
    sections = metrics.get("sections", []) or []
    unit = metrics.get("length_unit", "字")
    lines = [
        "## 章节汇总",
        "",
        f"| 章节 | 段落数 | 句子数 | 平均句长({unit}) | MeanCV | MinCV | MaxCV |",
        "|------|--------|--------|------------------|--------|-------|-------|",
    ]
    if not sections:
        lines.append("| - | - | - | - | - | - | - |")
        return lines

    for s in sections:
        name = (s.get("name") or "(正文)")[:40].replace("|", "\\|")
        lines.append(
            f"| {name} | {s.get('n_paragraphs', 0)} | {s.get('n_sentences', 0)} | "
            f"{s.get('mean_sentence_length', 0.0):.2f} | {s.get('mean_cv', 0.0):.3f} | "
            f"{s.get('min_cv', 0.0):.3f} | {s.get('max_cv', 0.0):.3f} |"
        )
    return lines


def render_sentence_histogram(metrics: dict[str, Any]) -> list[str]:
    """Render the sentence-length histogram."""
    histogram = metrics.get("sentence_length_histogram", {}) or {}
    unit = metrics.get("length_unit", "字")
    if not histogram:
        return []

    total = sum(histogram.values())
    lines = [f"## 句长分布（{unit}）", ""]
    for label, count in histogram.items():
        pct = _pct(count, total)
        bar = _bar(pct)
        lines.append(f"- {label:>9} {unit}：**{count}** 句 ({pct:.1f}%) {bar}")
    return lines


def render_markdown(
    metrics: dict[str, Any], title: str = "句长 CV 分析报告", include_footer: bool = True
) -> str:
    """Render a complete Chinese Markdown CV report from sentence_length metrics."""
    from datetime import datetime

    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    parts = [f"# {title}", ""]
    parts.extend(render_overall(metrics))
    parts.append("")
    parts.extend(render_cv_distribution(metrics))
    parts.append("")
    parts.extend(render_uniform_paragraphs(metrics))
    parts.append("")
    parts.extend(render_section_summary(metrics))
    parts.append("")
    parts.extend(render_sentence_histogram(metrics))
    parts.extend(
        [
            "",
            "## 说明",
            "",
            "- CV（变异系数）= 标准差 / 平均值，数值越低说明句长越均匀。",
            "- Uniform 段落（CV < 0.30）是 AI 生成文本的典型信号之一。",
        ]
    )
    if include_footer:
        parts.extend(["", f"---\n*报告生成时间: {generated_at}*"])
    return "\n".join(parts) + "\n"


def render_summary_table(metrics: dict[str, Any]) -> list[str]:
    """Render a compact summary table suitable for before/after comparison."""
    return [
        f"| 分析段落数 | {metrics.get('n_paragraphs_analyzed', 0)} |",
        f"| 分析句子数 | {metrics.get('n_sentences_analyzed', 0)} |",
        f"| 整体句长 CV | {metrics.get('sentence_cv', 0.0):.3f} |",
        f"| 段落平均 CV | {metrics.get('paragraph_cv_mean', 0.0):.3f} |",
        f"| Uniform 段落占比 | {metrics.get('uniform_paragraph_ratio', 0.0):.1%} |",
    ]
