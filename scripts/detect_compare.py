#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 写作特征改写前后对比工具

对同一份文本的「改写前」和「改写后」版本分别检测，输出中文 Markdown 对比报告，
重点展示段落级句长 CV 的变化。

使用方法:
    python scripts/detect_compare.py before.txt after.txt --output compare.md
    python scripts/detect_compare.py before.txt after.txt --json compare.json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Allow running this script directly from the project root while still importing
# the `scripts` namespace package used throughout the codebase.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

try:
    from detect_ai_patterns import AIPatternDetector
    from analyzers.sentence_length import analyze as analyze_sentence_length
    from analyzers.cv_report import render_markdown as render_cv_report
except ImportError:  # imported as package during tests
    from scripts.detect_ai_patterns import AIPatternDetector
    from scripts.analyzers.sentence_length import analyze as analyze_sentence_length
    from scripts.analyzers.cv_report import render_markdown as render_cv_report


CV_METRIC_KEYS = {
    "n_paragraphs_analyzed",
    "n_sentences_analyzed",
    "sentence_cv",
    "paragraph_cv_mean",
    "paragraph_cv_median",
    "paragraph_cv_min",
    "paragraph_cv_max",
    "uniform_paragraph_count",
    "uniform_paragraph_ratio",
    "section_mean_cv",
    "sentence_length_histogram",
    "cv_distribution",
    "uniform_paragraphs",
    "sections",
    "language",
    "length_unit",
}


def _extract_cv_metrics(report: dict[str, Any]) -> dict[str, Any]:
    """Extract CV-specific metrics from a full detection report."""
    metrics = report.get("metrics", {})
    cv_metrics = {k: metrics.get(k) for k in CV_METRIC_KEYS}
    # Fallback: if the full detector did not run the new sentence_length analyzer,
    # the keys may be missing. Return empty-like values.
    if cv_metrics.get("n_paragraphs_analyzed") is None:
        cv_metrics["n_paragraphs_analyzed"] = 0
        cv_metrics["n_sentences_analyzed"] = 0
        cv_metrics["sentence_cv"] = 0.0
        cv_metrics["paragraph_cv_mean"] = 0.0
        cv_metrics["uniform_paragraph_ratio"] = 0.0
        cv_metrics["length_unit"] = "字"
    return cv_metrics


def _delta(after: float, before: float) -> str:
    diff = after - before
    if abs(diff) < 0.001:
        return "→ 持平"
    direction = "↑" if diff > 0 else "↓"
    return f"{direction} {abs(diff):.3f}"


def _pct_delta(after: float, before: float) -> str:
    diff = after - before
    if abs(diff) < 0.0001:
        return "→ 持平"
    direction = "↑" if diff > 0 else "↓"
    return f"{direction} {abs(diff):.1%}"


def render_comparison_markdown(
    before_report: dict[str, Any],
    after_report: dict[str, Any],
    before_cv: dict[str, Any],
    after_cv: dict[str, Any],
    before_path: str,
    after_path: str,
) -> str:
    """Render the Chinese before/after comparison Markdown."""
    b_summary = before_report.get("summary", {})
    a_summary = after_report.get("summary", {})
    unit = before_cv.get("length_unit") or after_cv.get("length_unit") or "字"

    lines: list[str] = [
        "# AI 写作特征改写对比报告",
        "",
        f"- 改写前：`{before_path}`",
        f"- 改写后：`{after_path}`",
        "",
        "## 摘要对比",
        "",
        "| 指标 | 改写前 | 改写后 | 变化 |",
        "|------|--------|--------|------|",
    ]

    ai_score_before = b_summary.get("ai_score", 0.0)
    ai_score_after = a_summary.get("ai_score", 0.0)
    lines.append(
        f"| AI 特征分数 | {ai_score_before} | {ai_score_after} | "
        f"{_delta(ai_score_after, ai_score_before)} |"
    )

    issues_before = b_summary.get("total_issues", 0)
    issues_after = a_summary.get("total_issues", 0)
    lines.append(
        f"| 问题总数 | {issues_before} | {issues_after} | "
        f"{_delta(float(issues_after), float(issues_before))} |"
    )

    lines.append(
        f"| 分析段落数 | {before_cv.get('n_paragraphs_analyzed', 0)} | "
        f"{after_cv.get('n_paragraphs_analyzed', 0)} | - |"
    )
    lines.append(
        f"| 分析句子数 | {before_cv.get('n_sentences_analyzed', 0)} | "
        f"{after_cv.get('n_sentences_analyzed', 0)} | - |"
    )
    lines.append(
        f"| 整体句长 CV | {before_cv.get('sentence_cv', 0.0):.3f} | "
        f"{after_cv.get('sentence_cv', 0.0):.3f} | "
        f"{_delta(after_cv.get('sentence_cv', 0.0), before_cv.get('sentence_cv', 0.0))} |"
    )
    lines.append(
        f"| 段落平均 CV | {before_cv.get('paragraph_cv_mean', 0.0):.3f} | "
        f"{after_cv.get('paragraph_cv_mean', 0.0):.3f} | "
        f"{_delta(after_cv.get('paragraph_cv_mean', 0.0), before_cv.get('paragraph_cv_mean', 0.0))} |"
    )
    lines.append(
        f"| Uniform 段落占比 | {before_cv.get('uniform_paragraph_ratio', 0.0):.1%} | "
        f"{after_cv.get('uniform_paragraph_ratio', 0.0):.1%} | "
        f"{_pct_delta(after_cv.get('uniform_paragraph_ratio', 0.0), before_cv.get('uniform_paragraph_ratio', 0.0))} |"
    )

    lines.extend(["", "## 改写前 CV 分布", ""])
    for label, count in (before_cv.get("cv_distribution") or {}).items():
        total = sum((before_cv.get("cv_distribution") or {}).values())
        pct = (100 * count / total) if total else 0.0
        lines.append(f"- {label}：**{count}** 段 ({pct:.1f}%)")

    lines.extend(["", "## 改写后 CV 分布", ""])
    for label, count in (after_cv.get("cv_distribution") or {}).items():
        total = sum((after_cv.get("cv_distribution") or {}).values())
        pct = (100 * count / total) if total else 0.0
        lines.append(f"- {label}：**{count}** 段 ({pct:.1f}%)")

    lines.extend(["", "## 改写前 Uniform 段落", ""])
    before_uniform = before_cv.get("uniform_paragraphs") or []
    if before_uniform:
        for p in before_uniform[:20]:
            preview = (p.get("preview") or "").replace("|", "\\|").replace("\n", " ")
            lines.append(
                f"- CV={p.get('cv', 0.0):.3f} | 平均 {p.get('mean', 0.0):.0f}±{p.get('std', 0.0):.0f}{unit} | "
                f"[{p.get('chapter', '(正文)')[:40]}]: \"{preview}\""
            )
    else:
        lines.append("- 无 CV < 0.30 的段落。")

    lines.extend(["", "## 改写后 Uniform 段落", ""])
    after_uniform = after_cv.get("uniform_paragraphs") or []
    if after_uniform:
        for p in after_uniform[:20]:
            preview = (p.get("preview") or "").replace("|", "\\|").replace("\n", " ")
            lines.append(
                f"- CV={p.get('cv', 0.0):.3f} | 平均 {p.get('mean', 0.0):.0f}±{p.get('std', 0.0):.0f}{unit} | "
                f"[{p.get('chapter', '(正文)')[:40]}]: \"{preview}\""
            )
    else:
        lines.append("- 无 CV < 0.30 的段落。")

    lines.extend(["", "## 章节 CV 对比", "", "| 章节 | 改写前 MeanCV | 改写后 MeanCV | 变化 |", "|------|---------------|---------------|------|"])
    before_sections = {s.get("name"): s for s in (before_cv.get("sections") or [])}
    after_sections = {s.get("name"): s for s in (after_cv.get("sections") or [])}
    all_names = sorted(set(before_sections.keys()) | set(after_sections.keys()))
    for name in all_names:
        b_cv = before_sections.get(name, {}).get("mean_cv", 0.0)
        a_cv = after_sections.get(name, {}).get("mean_cv", 0.0)
        lines.append(
            f"| {(name or '(正文)')[:40].replace('|', '\\|')} | {b_cv:.3f} | {a_cv:.3f} | {_delta(a_cv, b_cv)} |"
        )

    lines.extend(["", "## 改写前句长分布", ""])
    for label, count in (before_cv.get("sentence_length_histogram") or {}).items():
        total = sum((before_cv.get("sentence_length_histogram") or {}).values())
        pct = (100 * count / total) if total else 0.0
        lines.append(f"- {label} {unit}：**{count}** 句 ({pct:.1f}%)")

    lines.extend(["", "## 改写后句长分布", ""])
    for label, count in (after_cv.get("sentence_length_histogram") or {}).items():
        total = sum((after_cv.get("sentence_length_histogram") or {}).values())
        pct = (100 * count / total) if total else 0.0
        lines.append(f"- {label} {unit}：**{count}** 句 ({pct:.1f}%)")

    lines.extend(
        [
            "",
            "## 改写策略总结",
            "",
            "- 打断平行定义段，避免连续多句长度相近。",
            "- 替换三联句，减少 '一是…二是…三是…' 等均匀结构。",
            "- 拆分复合句，把长句拆成若干短句。",
            "- 插入短句，在长篇论述中制造节奏停顿。",
            "- 变换句首，避免每段以相同句式开头。",
            "",
            "---",
            f"*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        ]
    )

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="对比文本改写前后的 AI 写作特征（重点：句长 CV）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python scripts/detect_compare.py before.txt after.txt --output compare.md
    python scripts/detect_compare.py before.txt after.txt --json compare.json
        """,
    )
    parser.add_argument("before_file", help="改写前文本文件路径")
    parser.add_argument("after_file", help="改写后文本文件路径")
    parser.add_argument("--output", "-o", help="输出对比报告文件路径（Markdown）")
    parser.add_argument("--json", "-j", help="输出结构化 JSON 文件路径")
    parser.add_argument("--language", "-l", choices=["zh", "en"], default="zh", help="检测语言（默认中文）")
    args = parser.parse_args()

    before_path = Path(args.before_file)
    after_path = Path(args.after_file)

    if not before_path.exists():
        print(f"错误：文件不存在 - {args.before_file}", file=sys.stderr)
        return 1
    if not after_path.exists():
        print(f"错误：文件不存在 - {args.after_file}", file=sys.stderr)
        return 1

    before_text = before_path.read_text(encoding="utf-8")
    after_text = after_path.read_text(encoding="utf-8")

    detector = AIPatternDetector()
    before_matches = detector.detect_patterns(before_text)
    after_matches = detector.detect_patterns(after_text)
    before_report = detector.generate_report(before_text, before_matches)
    after_report = detector.generate_report(after_text, after_matches)

    # Dedicated CV analysis for richer, focused metrics.
    before_cv = analyze_sentence_length(before_text, language=args.language).metrics
    after_cv = analyze_sentence_length(after_text, language=args.language).metrics

    markdown = render_comparison_markdown(
        before_report=before_report,
        after_report=after_report,
        before_cv=before_cv,
        after_cv=after_cv,
        before_path=str(before_path),
        after_path=str(after_path),
    )

    if args.output:
        Path(args.output).write_text(markdown, encoding="utf-8")
        print(f"对比报告已保存至: {args.output}")

    if args.json:
        json_out = {
            "before": before_report,
            "after": after_report,
            "before_cv": before_cv,
            "after_cv": after_cv,
        }
        Path(args.json).write_text(
            json.dumps(json_out, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"结构化 JSON 已保存至: {args.json}")

    if not args.output and not args.json:
        print(markdown)

    return 0


if __name__ == "__main__":
    sys.exit(main())
