# Humanize MBA Text - Remove AI Writing Traces

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python 3.7+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/Claude-Skill-orange.svg" alt="Claude Skill">
  <img src="https://img.shields.io/badge/Version-1.5-brightgreen.svg" alt="Version: 1.5">
  <img src="https://img.shields.io/badge/Kimi-CLI-blue.svg" alt="Kimi CLI">
  <a href="README.md"><img src="https://img.shields.io/badge/中文-🇨🇳-inactive.svg" alt="中文"></a>
  <img src="https://img.shields.io/badge/English-🇺🇸-red.svg" alt="English">
  <a href="README_KR.md"><img src="https://img.shields.io/badge/한국어-🇰🇷-inactive.svg" alt="한국어"></a>
  <a href="README_JP.md"><img src="https://img.shields.io/badge/日本語-🇯🇵-inactive.svg" alt="日本語"></a>
</p>

<p align="center">
  <b>AI Writing Trace Detection and Removal Tool Specifically for Chinese MBA Theses</b>
</p>

<p align="center">
  <code>#AI-Detection</code> <code>#Academic-Writing</code> <code>#MBA-Thesis</code> <code>#Claude-Skill</code> <code>#Text-Humanization</code> <code>#ChatGPT-Alternative</code> <code>#LLM-Writing</code> <code>#Research-Tools</code> <code>#Academic-Integrity</code> <code>#Chinese-NLP</code>
</p>

---

## 🎯 Project Introduction

This is an AI writing trace detection and removal tool specifically designed for **Chinese MBA theses**. Based on the academic norms and practical requirements of MBA theses, it uses multi-dimensional detection methods to identify AI-generated features in text and provides specific modification suggestions to help you rewrite AI-generated text into natural, humanized academic writing style.

### ✨ Version 1.5 New Features (Paragraph-Level Sentence CV + Report Readability)

- 📐 **Paragraph-level sentence-length CV**: Adapts the `AI_artifact_detection` method, using the coefficient of variation (CV) of sentence length within a paragraph as the core AI signal. Chinese is measured in CJK characters, English in words
- 📊 **Chinese CV report**: Detection Markdown reports now automatically append a five-section CV report — Overall Statistics / CV Distribution / Uniform Paragraph Details / Section Summary / Sentence-Length Histogram
- 🔁 **Before/After comparison**: New `scripts/detect_compare.py` CLI takes before/after texts and outputs a Chinese Before/After comparison Markdown
- 🌐 **Optional English detection mode**: `sentence_length.analyze(text, language="en")` supports sentence-length CV detection for English prose
- 🎯 **Content snippets with context**: The detailed issue list now shows ~20 characters before and after each match for quick location
- 📝 **Full modification suggestions**: Suggestions are no longer truncated; all guidance is displayed in full
- 📋 **Uniform paragraphs as full table**: All paragraphs with CV < 0.30 are listed in a table, no longer capped at 20
- ⏰ **Real generation timestamp**: Report footer now shows the actual generation time (YYYY-MM-DD HH:MM:SS)

> Older versions (1.4 / 1.3 / 1.2) are archived in [`FEATURE.md`](FEATURE.md).

### Core Features

- ✅ **Layered AI Detection**: Regex rules → prose-structure statistics (5 dimensions) → semantic-chain patterns (10 dimensions)
- ✅ **Chapter-specific Rules**: Optimization strategies for 5 chapters: Introduction, Theory, Analysis, Solutions, and Conclusion
- ✅ **MBA Thesis Standards**: Complies with Chinese university MBA thesis word count, structure, and format requirements
- ✅ **Structured Rewrite Plan**: Every issue carries location + skeleton + recommended replacements + target word count
- ✅ **Auto-fix**: Automatically handles simple issues like Chinese-English mixed spacing
- ✅ **Smart Feedback**: Generates detailed modification suggestions and before/after comparison examples
- ✅ **Claude Skill Integration**: Can be used directly as a Claude Code Skill

### Technical Reference

This project's optimization strategy design references the three-dimensional collaborative optimization concept from the [thesis-optimizer](https://github.com/Haimbeau1o/thesis-optimizer) project:

- 🔍 **Dimension 1: AI Detection Rate Reduction**
  - Sentence Structure Diversification
  - Academic Tone Naturalization
  - Logical Chain Humanization

- 📉 **Dimension 2: Plagiarism Rate Reduction**
  - Deep Semantic Rewriting
  - Citation Standardization
  - Professional Terminology Processing

- ✨ **Dimension 3: Academic Polishing Enhancement**
  - Expression Precision
  - Academic Standardization
  - Readability Optimization

---

## 🎓 MBA Thesis Core Principles

This tool is designed based on the academic norms of Chinese MBA theses and follows the following core principles:

### 1. Practice Orientation
- Must originate from actual enterprise management and solve specific management problems
- Avoid pure theoretical discussions

### 2. Focused Deep Research ("Small Topic, Deep Analysis")
- Clear and focused topic selection, "small topic with deep analysis"
- Core concepts should not exceed 2-3
- Avoid overly broad or vague topics

### 3. Data Traceability
- All data must indicate sources
- Ensure accuracy and credibility
- Remove vague expressions like "relevant data shows"

### 4. Theoretical Support
- Apply 1-2 relevant theories as analytical frameworks
- Avoid discussing issues in isolation without theoretical grounding

### 5. Structural Standards
- Main text word count ≥ 30,000 words
- Each chapter must have at least 4 sections (including chapter summary)
- Each section must be substantial, avoid sections shorter than one page

### 6. Academic Integrity
- Plagiarism rate < 15%
- Do not fabricate data; all citations must be verifiable

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/stephenlzc/humanize-mba-text-skill.git
cd humanize-mba-text-skill

# Install dependencies (if using transformers models)
pip install transformers torch
```

### Basic Usage

#### 1. Basic Detection

```bash
# Use basic rule detection
python scripts/detect_ai_patterns.py your_text.txt --format markdown --output report.md
```

#### 2. Multi-dimensional Fusion Detection (Recommended)

```bash
# Use multi-dimensional detection
python scripts/multi_detector.py your_text.txt --format markdown --output report.md --plan plan.json
```

#### 3. Generate Modification Suggestions

```bash
# Generate feedback based on detection results
python scripts/feedback_generator.py detection_result.json --text your_text.txt --output feedback.md
```

#### 4. Apply Auto-fixes

```bash
# Auto-fix simple issues like spacing
python scripts/feedback_generator.py detection_result.json --text your_text.txt --apply
```

### Using as Claude Skill

1. Clone this repository to the Claude Code skills directory:

```bash
cd ~/.config/opencode/skills
git clone https://github.com/stephenlzc/humanize-mba-text-skill.git
```

2. Trigger the Skill in Claude Code:

```
Remove AI traces: [paste your text]
```

Or

```
Help me remove AI writing traces from this text
```

---

## 📊 Detection Dimensions

### 1. Rule Matching Detection

Identifies the following AI writing characteristics:

- **AI Vocabulary**: 赋能 (empower), 抓手 (handle), 闭环 (closed loop), 痛点 (pain point), 赛道 (track), etc.
- **Vague Attribution**: "Studies have shown", "Experts believe", etc.
- **Overemphasis**: "Key", "Core", "Crucial", etc.
- **Macro Narratives**: "Era", "Trend", "Wave", etc.
- **Surface Analysis**: "Highlights", "Reflects", etc. -ing ending analyses
- **Cliché Conclusions**: "In summary", "From this we can see", etc.
- **Excessive Connectives**: "First... Second... Finally", etc.
- **Chinese-English Mixed Spacing**: "MBA 论文" → "MBA论文"

### 2. Statistical Analysis Detection

- **Sentence Length Uniformity**: AI text typically has more uniform sentence lengths
- **Vocabulary Diversity**: AI text has lower vocabulary diversity
- **Punctuation Distribution**: Analyzes punctuation usage patterns
- **Paragraph Structure**: Detects paragraph length distribution

### 3. Linguistic Feature Detection

- **Connective Density**: Statistics on logical connective usage frequency
- **Formal Expression Patterns**: Identifies overly formal academic expressions
- **Sentence Complexity**: Analyzes complex sentence structure usage

### 4. Prose-Structure Analyzers (v1.3)

Each analyzer returns an `AnalyzerIssue` (analyzer_id / severity / confidence / location / evidence / suggestion) plus statistical metrics:

| Dim | analyzer_id | Trigger |
| --- | --- | --- |
| 6 | `uniform_sentence_length` | Sentence-length variance/CV exceeds threshold (paragraph + global) |
| 9 | `uniform_paragraph_length` | Inter-paragraph CJK length CV < 0.25 |
| 10 | `paragraph_edge_template_repeat` | 3+ consecutive paragraphs share identical leading/trailing fingerprint |
| 8a | `paragraph_structure_uniformity` | 3+ consecutive paragraphs share the same 4-tuple structure fingerprint |
| 8b | `chapter_template_repeat` | 3+ sections inside one chapter reuse the same chapter-template |

### 5. Semantic-Chain Analyzers (v1.3)

Cross-paragraph and cross-chapter AI patterns that no per-paragraph rule can catch:

| Dim | analyzer_id | Trigger |
| --- | --- | --- |
| 3 | `chain_three_part_rule` | 3+ consecutive paragraphs all use 「一是…二是…三是」 or 「首先…其次…最后」 |
| 3 | `chain_author_listing` | 4+ 「Author(year) 指出/认为」 references stacked inside one chapter |
| 3 | `chain_method_name` | One paragraph piles 2+ method/model/theory names without per-method elaboration |
| 3 | `chain_abstract_template` | One paragraph hits 3+ abstract-template phrases |
| 3 | `chain_conclusion_echo` | Conclusion chapter's opening duplicates the abstract's character Jaccard ≥ 0.30 |
| 4 | `chain_vague_problem_statement` | 2+ vague problem statements with no metric within 30 chars |
| 4 | `chain_unsupported_quantification` | 2+ percentage/ranking claims with no 「根据/来源/问卷/N=」 anchor within 80 chars |
| 4 | `chain_macro_narrative` | 3+ macro-narrative phrases inside a 1000-char window |
| 5 | `evidence_chain_completeness` | 2+ quantified/research claims lacking method/source/N= anchors (cross-rule) |
| 5 | `cross_section_problem_trace` | Chapter-3 problems ↔ chapter-5 recommendations keyword overlap < 30% |

### 6. Structured Rewrite Plan (v1.3)

`detect_ai_patterns.AIPatternDetector.generate_report()` and `multi_detector.FusionEngine.detect()` now expose a `modify_plan` key — one `ModifyEntry` per issue:

```json
{
  "analyzer_id": "chain_unsupported_quantification",
  "severity": "high",
  "location": "global",
  "evidence": "7 percentage/ranking assertions, 5 lack 「根据/来源/问卷/N=」 anchors within 80 chars",
  "suggestion": "Anchor every quantitative claim with method/source/N marker",
  "rewrite_template": "For each quantified claim, supply sample, time window, and statistical scope.",
  "recommended_replacements": [
    "Per 'per the Dec 2023 customer survey (N=120), …'",
    "Sample description: '5-point Likert scale'",
    "When unverifiable: 'this metric needs further verification'",
  ],
  "target_word_count_range": [60, 140],
  "before_after_example": {
    "before": "客户满意度提升20%。",
    "after": "根据2023年12月客户问卷（N=120），客户满意度从3.8分升至4.5分。"
  }
}
```

### 7. Per-sentence High-Risk Annotations (v1.4)

`report["high_risk_annotations"]` is a new third array — **one entry per sentence** — that bridges the gap between `matches[]` (hundreds of regex hits, each with only a generic `suggestion` string) and `modify_plan[]` (4 aggregated rows with no line numbers):

```json
{
  "sentence_index": 17,
  "char_offset_start": 1287,
  "char_offset_end": 1335,
  "sentence_text": "数字化转型赋能业务创新，形成从生产到服务的完整闭环。",
  "line_number": 24,
  "severity": "high",
  "triggered_rules": [
    {
      "rule_id": "ai_buzzwords",
      "pattern_name": "AI词汇/互联网黑话",
      "pattern_type": "regex",
      "evidence": "赋能",
      "confidence": 1.0,
      "severity": "high",
      "phrase_replacements": [
        "赋能 → 促进/支持",
        "闭环 → 闭合回路/完整流程",
        "抓手 → 切入点/措施"
      ],
      "before_after_example": {
        "before": "数字化转型赋能业务创新，形成从生产到服务的完整闭环。",
        "after": "数字化改造使生产到售后的流程数据打通，订单处理时长从5天缩短至2天。"
      }
    }
  ],
  "rewrite_template": "把互联网黑话替换为传统管理学术语。",
  "recommended_replacements": [
    "赋能 → 促进/支持",
    "闭环 → 闭合回路/完整流程"
  ]
}
```

**Field reference**:

| Field | Meaning |
| --- | --- |
| `sentence_text` | Original sentence as-is |
| `char_offset_start/end` | Char offsets in the original text (inclusive of terminator) |
| `line_number` | 1-based line in the original text |
| `severity` | Worst severity across all rules that fired in this sentence |
| `triggered_rules[].rule_id` | e.g. `ai_buzzwords`, `empty_solution_verbs`, `chain_three_part_rule` |
| `triggered_rules[].phrase_replacements` | From TOML `phrase_replacements` — drop-in copy-paste swaps |
| `triggered_rules[].before_after_example` | From TOML `[[categories.examples]]` — real rewrite pairs |
| `rewrite_template` | From `rewrite_planner._SKELETONS` — the highest-priority skeleton for this sentence |
| `recommended_replacements` | Deduped union of every triggered rule's `phrase_replacements` |

**Guarantees**:

- Sorted high → low severity, then `char_offset_start` ascending — ready to feed an LLM humanizer agent sentence-by-sentence
- Multiple rules hitting the same sentence → one annotation; `triggered_rules[]` aggregates them
- Existing `matches` / `modify_plan` / `summary` / `metrics` fields **completely unchanged**

---

## 🎓 Chapter-specific Writing Guidelines

This tool provides detailed writing guidelines for 5 core chapters of MBA theses:

### Chapter 1: Introduction

**Common Issues**:
- ❌ Grand narrative opening: "With the development of the economy..."
- ❌ Vague research significance: "Has important theoretical and practical value"
- ❌ Literature review listing: A says, B says, C says
- ❌ Simple listing of research methods

**Improvement Strategies**:
- ✅ Get straight to the point: Directly state the research enterprise and specific problem
- ✅ Specific significance: Explain what problem is solved and what value it brings
- ✅ Thematic review: Organize by themes with critical analysis
- ✅ Specific methods: Explain data sources, samples, and analysis tools

📄 **Detailed Guide**: [chapter-1-introduction.md](references/chapter-1-introduction.md)

### Chapter 2: Theoretical Foundation

**Common Issues**:
- ❌ Textbook-style definition stacking
- ❌ Theory listing: Introducing 5-6 theories
- ❌ Disconnect between theory and practice

**Improvement Strategies**:
- ✅ Concise definition: 2-3 core concepts
- ✅ Selective theories: 1-2 core theories, with rationale for selection
- ✅ Application-oriented: Theory provides framework for subsequent analysis

📄 **Detailed Guide**: [chapter-2-theory.md](references/chapter-2-theory.md)

### Chapter 3: Current Situation and Problem Analysis

**Common Issues**:
- ❌ Enterprise overview data stacking with low research relevance
- ❌ Qualitative status description lacking data
- ❌ Vague problem identification: "Poor management", "Low efficiency"
- ❌ Surface-level cause analysis: Remaining at phenomenon description

**Improvement Strategies**:
- ✅ Focus on relevance: Only provide background relevant to the research
- ✅ Data-driven: Use specific indicators and time series data
- ✅ Specific problems: Each problem has measurement indicators and research data
- ✅ Deep exploration: Use theoretical framework to analyze root causes

📄 **Detailed Guide**: [chapter-3-analysis.md](references/chapter-3-analysis.md)

### Chapter 4: Solutions and Recommendations

**Common Issues**:
- ❌ Vague recommendations: "Strengthen management", "Optimize processes"
- ❌ Lack of operability
- ❌ Ignoring constraints
- ❌ Template application: SWOT becomes formalistic

**Improvement Strategies**:
- ✅ Specific and actionable: Clearly define what to do, how to do it, and who will do it
- ✅ Phased implementation: Distinguish short-term, medium-term, and long-term
- ✅ Consider constraints: Analyze resource, capability, and cultural limitations
- ✅ Quantified effects: Expected effects should be quantified where possible

📄 **Detailed Guide**: [chapter-4-solutions.md](references/chapter-4-solutions.md)

### Chapter 5: Conclusion

**Common Issues**:
- ❌ Repetition of abstract content
- ❌ Simple listing of each chapter's content
- ❌ Vague innovation points: "First study", "Fills a gap"
- ❌ Avoiding research limitations

**Improvement Strategies**:
- ✅ Research findings: Highlight core findings without repeating the abstract
- ✅ Specific innovation: Objectively explain theoretical, methodological, and application innovations
- ✅ Honest limitations: Specifically analyze limitations and their impact
- ✅ Future outlook: Propose specific and feasible research directions

📄 **Detailed Guide**: [chapter-5-conclusion.md](references/chapter-5-conclusion.md)

---

## 📝 Format Standards

Independent format standard documentation covers:

- Chinese-English/Number mixed typesetting standards
- Figure and table numbering and layout standards
- Citation and reference standards
- Number and unit standards
- Punctuation standards
- Paragraph and hierarchy standards

📄 **Detailed Standards**: [format-standards.md](references/format-standards.md)

---

## 📈 Detection Results Interpretation

The detection report contains the following dimensions:

- **AI Generation Probability**: 0-100%, higher score indicates more obvious AI traces
- **Risk Level**: 🔴 High Risk / 🟡 Medium Risk / 🟢 Low Risk
- **Detector Consistency**: Results consistency among three detection methods
- **Priority Fix Items**: Modification suggestions sorted by severity
- **Chapter-specific Suggestions**: Targeted suggestions based on detected chapter type

### Modification Strategies

Different strategies based on AI probability score:

**🔴 High Risk (>70%)**: Deep Rewriting
- Comprehensive reconstruction of paragraph structure
- Remove all AI characteristic vocabulary
- Supplement specific data and cases
- Estimated time: 2-3 hours

**🟡 Medium Risk (40-70%)**: Targeted Optimization
- Fix high-priority AI characteristics
- Adjust clichés and template expressions
- Supplement key data support
- Estimated time: 1-2 hours

**🟢 Low Risk (<40%)**: Detail Polishing
- Fix small amounts of AI traces
- Optimize language expression
- Final proofreading
- Estimated time: 30 minutes-1 hour

---

## 💡 Usage Examples

### Example 1: Removing AI Vocabulary

**Original**:
```
Digital transformation has become a key handle for promoting high-quality 
enterprise development, empowering business innovation and creating 
significant value for enterprises.
```

**Rewritten**:
```
This study explores the impact of digital transformation on enterprise 
performance. By analyzing XX Company's financial data from 2018-2023, 
it was found that digital investment is positively correlated with 
revenue growth.
```

### Example 2: Removing Vague Attribution

**Original**:
```
Research has shown that corporate culture has an important impact on 
organizational performance.
```

**Rewritten**:
```
Schein's (2010) research indicates that strong corporate culture is 
positively correlated with organizational performance (r=0.42, p<0.05).
```

### Example 3: MBA Thesis Focused Deep Research

**Original**:
```
Research on Enterprise Digital Transformation
```

**Rewritten**:
```
Research on Process Optimization in Digital Transformation of XX 
Company's Production Department
```

### Example 4: Data Traceability

**Original**:
```
Enterprise revenue increased by 20%, employee satisfaction is 85%.
```

**Rewritten**:
```
According to XX Company's 2023 annual report, enterprise revenue 
increased by 20% year-over-year. Based on a questionnaire survey 
conducted in December 2023 (N=120), employee satisfaction is 85%.
```

### Example 5: Fixing Chinese-English Mixed Spacing

**Original**:
```
MBA thesis writing needs to pay attention to AI trace issues.
Research in 2023 shows that 15% of enterprises have such problems.
```

**Rewritten**:
```
MBA thesis writing needs to pay attention to AI trace issues.
Research in 2023 shows that 15% of enterprises have such problems.
```

---

## 📁 Project Structure

```
humanize-mba-text-skill/
├── SKILL.md                          # Claude Skill main file
├── README.md                         # Chinese README
├── README_EN.md                      # English README (this file)
├── README_JP.md                      # 日本語 README
├── README_KR.md                      # 한국어 README
├── LICENSE                           # MIT License
│
├── references/                       # Reference documents + AI detection rules
│   ├── ai-writing-patterns.md        # AI writing characteristics guide
│   ├── chapter-1-introduction.md     # Chapter 1: Introduction guide
│   ├── chapter-2-theory.md           # Chapter 2: Theory foundation guide
│   ├── chapter-3-analysis.md         # Chapter 3: Analysis guide
│   ├── chapter-4-solutions.md        # Chapter 4: Solutions guide
│   ├── chapter-5-conclusion.md       # Chapter 5: Conclusion guide
│   ├── format-standards.md           # Format standards
│   ├── strategy_ai_reduction.md      # AI Detection Rate Reduction Strategy
│   ├── strategy_plagiarism.md        # Plagiarism Rate Reduction Strategy
│   ├── strategy_polishing.md         # Academic Polishing Strategy
│   ├── chinese-paper-humanization-rules.toml   # monolithic rule entry (fallback)
│   └── rules/                        # ⭐v1.3: progress-loadable AI rules
│       ├── index.toml                #   lightweight manifest
│       ├── categories/
│       │   ├── structure.toml        #   structure category
│       │   ├── rhythm_quality.toml  #   rhythm category
│       │   ├── formatting.toml       #   formatting category
│       │   ├── content.toml          #   content (incl. macro-narrative, vague problem, no-source quantification)
│       │   ├── evidence.toml         #   evidence (incl. data-without-method, causal leap)
│       │   └── language.toml         #   language category
│       ├── chapter-categories.toml  #   chapter-type classifier
│       └── metrics.toml              #   shared metrics wordlists
│
└── scripts/                          # Detection scripts
    ├── rule_loader.py                # ⭐v1.3: progressive TOML loader
    ├── detect_ai_patterns.py         # AIPatternDetector entry (with modify_plan)
    ├── multi_detector.py             # FusionEngine entry
    ├── feedback_generator.py         # Feedback generator
    └── analyzers/                    # ⭐v1.3: analyzer package
        ├── __init__.py               #   exposes run_prose_analyzers / run_semantic_chain_analyzers / build_modify_plan
        ├── _types.py                 #   AnalyzerIssue / AnalyzerReport data contracts
        ├── _segments.py              #   shared segmentation helpers
        ├── _regex_categories.py      #   hit-level wrapper (used by chain layer)
        ├── sentence_length.py        #   dimension 6
        ├── paragraph_length.py       #   dimension 9
        ├── paragraph_edges.py        #   dimension 10
        ├── paragraph_structure.py    #   dimension 8a
        ├── chapter_template.py       #   dimension 8b
        ├── semantic_chain.py         #   dimensions 3/4/5: 10 chain analyzers
        └── rewrite_planner.py        #   AnalyzerIssue → structured ModifyEntry
```

---

## 🔧 Advanced Usage

### Interactive Modification

```bash
python scripts/multi_detector.py your_text.txt --interactive
```

### Export Modification Plan

```bash
python scripts/multi_detector.py your_text.txt --plan modification_plan.json
```

### Batch Processing

```bash
# Process multiple files
for file in *.txt; do
    python scripts/multi_detector.py "$file" --output "reports/${file%.txt}_report.md"
done
```

---

## ⚠️ Important Notes

1. **Academic Integrity**: Maintain academic integrity when rewriting; do not fabricate data; all data must have authentic sources
2. **Data Verification**: For uncertain citations and data, users are advised to verify original sources
3. **Theory Adaptation**: Users are advised to select appropriate theoretical frameworks based on specific research questions
4. **Enterprise Authorization**: If involving internal enterprise data, written authorization from the enterprise or data anonymization is recommended
5. **Plagiarism Control**: Plagiarism check is recommended after rewriting to ensure rate < 15%
6. **Personalized Adjustment**: Rewritten text requires users to adjust according to specific school and advisor requirements
7. **Scope Limitation**: This tool focuses on removing AI traces and format standards, not on academic content depth review
8. **References**: Rewriting does not automatically generate references; users need to supplement complete references based on actual citations

---

## 🤝 Contributing Guidelines

Issues and Pull Requests are welcome!

### Submitting Issues

- Describe the problem clearly
- Provide example text (can be anonymized)
- Explain expected behavior

### Submitting Pull Requests

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 Changelog

### v1.4.0 (2026-07-05)

- 🧭 **`high_risk_annotations[]` per-sentence aggregation**: New top-level key on `detect_ai_patterns.generate_report` JSON output; merges regex hits and structural / chain issues by sentence; each row carries sentence-level char offsets, original sentence text, all triggered rules, per-rule phrase replacements, and real rewrite pairs
- 🔁 **TOML `phrase_replacements` field**: Phrase-level replacement mappings for 4 high-impact rules (`ai_buzzwords` / `empty_solution_verbs` / `vague_attribution` / `unsupported_quantification`); hook reserved for a v2 LLM fallback
- 📐 **`ModifyEntry.before_after_example`**: Additive field on every `modify_plan` row — None or `{before, after}` — sourced from `[[categories.examples]]`
- 🆕 **`scripts/analyzers/high_risk_annotator.py`**: New module: sentence segmentation (with char offsets) + dual-track bucketing (regex by line_number / issues by location + evidence substring) + severity sorting; decoupled from `detect_ai_patterns.py` via a lazy import
- ✅ **Backward compatible**: Existing `matches` / `modify_plan` / `summary` / `metrics` field order and types are untouched; `target_word_count_range` remains a 2-element list; all 117 tests pass

### v1.3.0 (2026-07-05)

#### Main release — `feat: rule-driven AI-trace detection with prose + semantic-chain analyzers`

- 🔬 **Externalized rules**: All AI-detection rules moved to external TOML, split across 7 categories; `scripts/rule_loader.py` provides progressive loading
- 📊 **Prose-structure analyzers**: 5 new statistical / fingerprint analyzers (dimensions 6 / 8a / 8b / 9 / 10)
- 🔗 **Semantic-chain analyzers**: 10 new cross-paragraph / cross-chapter chain analyzers (dimensions 3 / 4 / 5)
- 📋 **Structured rewrite plan**: `detect_ai_patterns.generate_report` now returns a `modify_plan` key
- 🎯 **Unified rule source**: `AIPatternDetector` / `StatisticalDetector` / `FeedbackGenerator` share the same TOML rule document
- 🛠 **New `scripts/analyzers/` package**: single home for the prose + chain analyzer code

#### v1.3.0 increments

- 📐 **SKILL.md Harris-style split**: 576 → 197 lines (-66%); identification / three-dimensional optimization / MBA checklist / chapter-specific rewrite data moved into `references/strategy_optimization.toml` / `mba_rewrite_checklist.toml` / `chapter_rewrite_rules.toml`; SKILL.md becomes a thin navigation index
- 🔁 **Cross-reference with [humanizer-academic-zh](https://github.com/cangtianhuang/humanizer-academic-zh)**: detect (us) ↔ rewrite (them) paths complement each other; patterns 21–25 wire into `references/rules/categories/*.toml` through the progressive manifest
- 📊 **Rule data upgrade**:
  - `filler_phrases` (Pattern 21): 5 → 8 regex patterns
  - `chatbot_conversation_residue` (Pattern 23): 4 → 7 regex patterns
  - New `sycophantic_praise` (Pattern 25): 9 regex patterns + 3 before/after examples, severity=medium / weight=0.5
- 🌐 **Multi-language README sync**: v1.3.0 content brought into Chinese / English / Japanese / Korean READMEs; both 致谢 / Acknowledgments and 🔗 Related Projects cross-link to `humanizer-academic-zh`

### v1.2.0 (2024-03-11)

- 📚 **Three-Dimensional Optimization Strategy**: Added 3 new strategy documents
  - strategy_ai_reduction.md: AI Detection Rate Reduction Strategy
  - strategy_plagiarism.md: Plagiarism Rate Reduction Strategy
  - strategy_polishing.md: Academic Polishing Strategy
- 🔍 **Enhanced Detection Capability**: Optimized rule matching, statistical analysis, and language feature detection
- 🎓 **Refined MBA Standards**: Further refined MBA thesis core principles
- 📝 **Improved Format Standards**: Expanded format standard documentation
- 🏗️ **Optimized Project Structure**: Added English and Korean README files

### v1.1.0 (2024-02-05)

- 📚 **Refactored Chapter Documents**: Split chapter rules into 5 independent files
  - chapter-1-introduction.md: Detailed introduction guide
  - chapter-2-theory.md: Detailed theory foundation guide
  - chapter-3-analysis.md: Detailed analysis guide
  - chapter-4-solutions.md: Detailed solutions guide
  - chapter-5-conclusion.md: Detailed conclusion guide
  - format-standards.md: Independent format standards document
- 🎓 **Refined MBA Standards**: Added MBA thesis core principles section
- 🎯 **Strengthened Practice Orientation**: Greater emphasis on data support, theoretical application, and specific cases
- 📝 **Improved Format Standards**: Independent format standards covering Chinese-English mixed typesetting, figures/tables, citations, etc.
- 🏗️ **Optimized Project Structure**: Clearer file organization and indexing

### v1.0.0 (2024-02-04)

- ✨ Initial release
- 🎯 Support for multi-dimensional AI feature detection
- 📚 Added chapter-specific rules
- 🔧 Implemented auto-fix functionality
- 🎓 Integrated Claude Skill

---

## 📄 License

This project uses [MIT License](LICENSE) - see LICENSE file for details

---

## 🙏 Acknowledgments

- Thanks to Claude Code for providing the Skill framework
- Thanks to Kimi CLI for providing the Agent parallel execution tools
- Thanks to all users who provided feedback and suggestions
- **Special thanks to the [Haimbeau1o/thesis-optimizer](https://github.com/Haimbeau1o/thesis-optimizer) project**, whose three-dimensional collaborative optimization strategy (AI detection rate reduction, plagiarism rate reduction, academic polishing enhancement) inspired this project's design
- **Rewrite strategy reference: [cangtianhuang/humanizer-academic-zh](https://github.com/cangtianhuang/humanizer-academic-zh)** — this project takes the *detect + quantify* path, while that project takes the *rewrite + polish* path; its 25-pattern taxonomy (organised into 5 categories: expression / language / style / fillers / communication residue) is cross-referenced from our SKILL.md's "supplementary reference" section, especially patterns 21-25 that we do not currently model

---

## 📮 Contact

- GitHub Issues: [https://github.com/stephenlzc/humanize-mba-text-skill/issues](https://github.com/stephenlzc/humanize-mba-text-skill/issues)
- Author: stephenlzc

---

## 🔗 Related Projects

- [thesis-optimizer](https://github.com/Haimbeau1o/thesis-optimizer) - Academic Paper Intelligent Optimization System (Computer Deep Learning Direction)
- [cangtianhuang/humanizer-academic-zh](https://github.com/cangtianhuang/humanizer-academic-zh) - Humanizer Chinese Academic Edition: a complementary *rewrite + polish* Skill to our *detect + quantify* path. Its 25-pattern taxonomy is grouped into 5 categories (expression / language / style / fillers / communication residue). v1.3.0 of this project merged patterns 21–25 into the progressive-load TOML (`references/rules/categories/*.toml`) as `filler_phrases` (boosted), `chatbot_conversation_residue` (boosted), `sycophantic_praise` (new), etc.

---

<p align="center">
  If this project helps you, please give it a ⭐ Star!
</p>
