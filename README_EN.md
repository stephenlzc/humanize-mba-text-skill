# Humanize MBA Text - Remove AI Writing Traces

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python 3.7+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/Claude-Skill-orange.svg" alt="Claude Skill">
  <img src="https://img.shields.io/badge/Version-1.2-brightgreen.svg" alt="Version: 1.2">
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

### ✨ Version 1.2 New Features

- 📚 **Three-Dimensional Optimization Strategy**: Added three new strategy documents for AI detection rate reduction, plagiarism rate reduction, and academic polishing
- 🔍 **Enhanced Detection Capability**: Optimized rule matching, statistical analysis, and language feature detection
- 🎓 **Refined MBA Standards**: Further refined MBA thesis core principles and chapter-specific writing guidelines
- 📝 **Improved Format Standards**: Expanded format standard documentation covering more edge cases
- 🎯 **Strengthened Practice Orientation**: Greater emphasis on data support, theoretical application, and specific case analysis

### Core Features

- ✅ **Multi-dimensional AI Detection**: Combines rule matching, statistical analysis, and linguistic feature detection
- ✅ **Chapter-specific Rules**: Optimization strategies for 5 chapters: Introduction, Theory, Analysis, Solutions, and Conclusion
- ✅ **MBA Thesis Standards**: Complies with Chinese university MBA thesis word count, structure, and format requirements
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
├── README_EN.md                      # English README
├── README_KR.md                      # Korean README
├── LICENSE                           # MIT License
│
├── references/                       # Reference documents
│   ├── ai-writing-patterns.md        # AI writing characteristics guide
│   ├── chapter-1-introduction.md     # Chapter 1: Introduction guide
│   ├── chapter-2-theory.md           # Chapter 2: Theory foundation guide
│   ├── chapter-3-analysis.md         # Chapter 3: Analysis guide
│   ├── chapter-4-solutions.md        # Chapter 4: Solutions guide
│   ├── chapter-5-conclusion.md       # Chapter 5: Conclusion guide
│   ├── format-standards.md           # Format standards
│   ├── strategy_ai_reduction.md      # AI Detection Rate Reduction Strategy ⭐NEW
│   ├── strategy_plagiarism.md        # Plagiarism Rate Reduction Strategy ⭐NEW
│   └── strategy_polishing.md         # Academic Polishing Strategy ⭐NEW
│
└── scripts/                          # Detection scripts
    ├── detect_ai_patterns.py         # Basic rule detection
    ├── multi_detector.py             # Multi-scheme fusion detector
    └── feedback_generator.py         # Feedback generator
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

---

## 📮 Contact

- GitHub Issues: [https://github.com/stephenlzc/humanize-mba-text-skill/issues](https://github.com/stephenlzc/humanize-mba-text-skill/issues)
- Author: stephenlzc

---

## 🔗 Related Projects

- [thesis-optimizer](https://github.com/Haimbeau1o/thesis-optimizer) - Academic Paper Intelligent Optimization System (Computer Deep Learning Direction)

---

<p align="center">
  If this project helps you, please give it a ⭐ Star!
</p>
