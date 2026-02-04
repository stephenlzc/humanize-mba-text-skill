# Humanize MBA Text - AI Writing Detection & Removal

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python 3.7+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/Claude-Skill-orange.svg" alt="Claude Skill">
  <img src="https://img.shields.io/badge/Version-1.1-brightgreen.svg" alt="Version: 1.1">
  <img src="https://img.shields.io/badge/中文-🇨🇳-red.svg" alt="中文">
  <a href="README_EN.md"><img src="https://img.shields.io/badge/English-🇺🇸-inactive.svg" alt="English"></a>
  <a href="README_KR.md"><img src="https://img.shields.io/badge/한국어-🇰🇷-inactive.svg" alt="한국어"></a>
</p>

<p align="center">
  <b>AI Writing Detection & Removal Tool for Chinese MBA Theses</b>
</p>

<p align="center">
  <code>#AI-Detection</code> <code>#Academic-Writing</code> <code>#MBA-Thesis</code> <code>#Claude-Skill</code> <code>#Text-Humanization</code> <code>#ChatGPT-Alternative</code> <code>#LLM-Writing</code> <code>#Research-Tools</code> <code>#Academic-Integrity</code> <code>#Chinese-NLP</code>
</p>

---

## 🎯 Introduction

A specialized tool for detecting and removing AI writing traces in **Chinese MBA dissertations**. Based on academic standards and practical requirements of MBA theses, this tool uses multi-dimensional detection methods to identify AI-generated features in text and provides specific revision suggestions to help transform AI-generated content into natural, human-like academic writing.

### ✨ Version 1.1 Highlights

- 📚 **Restructured Chapter Documents**: Split chapter rules into 5 independent files for easier access
- 🎓 **Enhanced MBA Standards**: Added core MBA thesis principles and chapter-specific writing guides
- 📝 **Improved Format Standards**: Organized formatting standards covering Chinese-English mixed text, charts, citations, etc.
- 🎯 **Strengthened Practical Orientation**: Greater emphasis on data support, theoretical application, and specific case analysis

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/stephenlzc/humanize-mba-text-skill.git
cd humanize-mba-text-skill

# Install dependencies (if using transformers models)
pip install transformers torch
```

### Usage

```bash
# Basic detection
python scripts/detect_ai_patterns.py your_text.txt --format markdown --output report.md

# Multi-dimensional detection (recommended)
python scripts/multi_detector.py your_text.txt --format markdown --output report.md

# Generate feedback
python scripts/feedback_generator.py detection_result.json --text your_text.txt --output feedback.md

# Auto-fix
python scripts/feedback_generator.py detection_result.json --text your_text.txt --apply
```

---

## 📊 Detection Dimensions

### AI Writing Features Detected

- **AI Buzzwords**: 赋能, 抓手, 闭环, 痛点, etc.
- **Vague Attribution**: "研究表明", "专家指出", etc.
- **Over-emphasis**: "关键", "核心", "至关重要", etc.
- **Macro Narratives**: "时代", "趋势", "浪潮", etc.
- **Surface Analysis**: "凸显了", "反映了", etc.
- **Formulaic Endings**: "综上所述", "由此可见", etc.
- **Mixed-text Spaces**: "MBA 论文" → "MBA论文"

---

## 🎓 Core MBA Thesis Principles

1. **Practice-oriented**: Must solve practical management problems
2. **Focused Topics**: "Small topic, deep dive" - max 2-3 core concepts
3. **Data Traceability**: All data must cite sources
4. **Theoretical Support**: Use 1-2 theories as analytical frameworks
5. **Structural Standards**: ≥30,000 words, min 4 sections per chapter
6. **Academic Integrity**: <15% plagiarism rate

---

## 📁 Project Structure

```
humanize-mba-text-skill/
├── SKILL.md                          # Main Claude Skill file
├── README.md                         # Chinese README
├── README_EN.md                      # English README
├── README_KR.md                      # Korean README
├── LICENSE                           # MIT License
├── references/                       # Reference documents
│   ├── ai-writing-patterns.md
│   ├── chapter-1-introduction.md
│   ├── chapter-2-theory.md
│   ├── chapter-3-analysis.md
│   ├── chapter-4-solutions.md
│   ├── chapter-5-conclusion.md
│   └── format-standards.md
└── scripts/
    ├── detect_ai_patterns.py
    ├── multi_detector.py
    └── feedback_generator.py
```

---

## 📝 Changelog

### v1.1.0 (2024-02-05)

- 📚 Restructured chapter documents into 5 separate files
- 🎓 Added MBA thesis core principles
- 🎯 Enhanced practical orientation
- 📝 Improved format standards

### v1.0.0 (2024-02-04)

- ✨ Initial release
- 🎯 Multi-dimensional AI detection
- 📚 Chapter-specific rules
- 🔧 Auto-fix functionality

---

## 📄 License

[MIT License](LICENSE)

---

<p align="center">
  ⭐ Star this project if it helps you!
</p>
