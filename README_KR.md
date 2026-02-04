# Humanize MBA Text - AI 글쓰기 흔 감지 및 제거

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python 3.7+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/Claude-Skill-orange.svg" alt="Claude Skill">
  <img src="https://img.shields.io/badge/Version-1.1-brightgreen.svg" alt="Version: 1.1">
  <a href="README.md"><img src="https://img.shields.io/badge/中文-🇨🇳-inactive.svg" alt="中文"></a>
  <a href="README_EN.md"><img src="https://img.shields.io/badge/English-🇺🇸-inactive.svg" alt="English"></a>
  <img src="https://img.shields.io/badge/한국어-🇰🇷-red.svg" alt="한국어">
</p>

<p align="center">
  <b>중국 MBA 졸업 논문을 위한 AI 글쓰기 감지 및 제거 도구</b>
</p>

<p align="center">
  <code>#AI-Detection</code> <code>#Academic-Writing</code> <code>#MBA-Thesis</code> <code>#Claude-Skill</code> <code>#Text-Humanization</code> <code>#ChatGPT-Alternative</code> <code>#LLM-Writing</code> <code>#Research-Tools</code> <code>#Academic-Integrity</code> <code>#Chinese-NLP</code>
</p>

---

## 🎯 소개

**중국 MBA 학위 논문**의 AI 글쓰기 흔을 감지하고 제거하기 위한 전문 도구입니다. MBA 논문의 학술 표준과 실무 요구사항을 기반으로 하여, 다차원 감지 방법을 사용하여 텍스트의 AI 생성 특징을 식별하고 구체적인 수정 제안을 제공하여 AI 생성 콘텐츠를 자연스럽고 인간적인 학술 글쓰기로 변환하는 데 도움을 줍니다.

### ✨ 버전 1.1 하이라이트

- 📚 **재구성된 장 문서**: 장 규칙을 5개의 독립 파일로 분할하여 접근성 향상
- 🎓 **향상된 MBA 표준**: 핵심 MBA 논문 원칙 및 장별 글쓰기 가이드 추가
- 📝 **개선된 형식 표준**: 중영 혼용 텍스트, 차트, 인용 등 형식 표준 정리
- 🎯 **강화된 실무 지향**: 데이터 지원, 이론 적용, 구체적 사례 분석 강조

---

## 🚀 빠른 시작

### 설치

```bash
# 저장소 클론
git clone https://github.com/stephenlzc/humanize-mba-text-skill.git
cd humanize-mba-text-skill

# 의존성 설치 (transformers 모델 사용 시)
pip install transformers torch
```

### 사용법

```bash
# 기본 감지
python scripts/detect_ai_patterns.py your_text.txt --format markdown --output report.md

# 다차원 감지 (권장)
python scripts/multi_detector.py your_text.txt --format markdown --output report.md

# 피드백 생성
python scripts/feedback_generator.py detection_result.json --text your_text.txt --output feedback.md

# 자동 수정
python scripts/feedback_generator.py detection_result.json --text your_text.txt --apply
```

---

## 📊 감지 차원

### 감지되는 AI 글쓰기 특징

- **AI 유행어**: 赋能, 抓手, 闭环, 痛点 등
- **모호한 귀속**: "研究表明", "专家指出" 등
- **과도한 강조**: "关键", "核心", "至关重要" 등
- **거시 서술**: "时代", "趋势", "浪潮" 등
- **표면적 분석**: "凸显了", "反映了" 등
- **공식적 결말**: "综上所述", "由此可见" 등
- **혼합 텍스트 공백**: "MBA 论文" → "MBA论文"

---

## 🎓 핵심 MBA 논문 원칙

1. **실무 지향**: 실제 관리 문제 해결 필요
2. **집중된 주제**: "작은 주제, 깊은 탐구" - 최대 2-3개 핵심 개념
3. **데이터 추적 가능성**: 모든 데이터는 출처 인용 필요
4. **이론적 지원**: 1-2개 이론을 분석 프레임워크로 사용
5. **구조적 표준**: ≥30,000자, 장당 최소 4개 섹션
6. **학술적 진실성**: <15% 표절률

---

## 📁 프로젝트 구조

```
humanize-mba-text-skill/
├── SKILL.md                          # 주요 Claude Skill 파일
├── README.md                         # 중국어 README
├── README_EN.md                      # 영어 README
├── README_KR.md                      # 한국어 README
├── LICENSE                           # MIT 라이선스
├── references/                       # 참조 문서
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

## 📝 변경 로그

### v1.1.0 (2024-02-05)

- 📚 5개의 별도 파일로 장 문서 재구성
- 🎓 MBA 논문 핵심 원칙 추가
- 🎯 실무 지향 강화
- 📝 형식 표준 개선

### v1.0.0 (2024-02-04)

- ✨ 초기 릴리스
- 🎯 다차원 AI 감지
- 📚 장별 특정 규칙
- 🔧 자동 수정 기능

---

## 📄 라이선스

[MIT 라이선스](LICENSE)

---

<p align="center">
  도움이 되었다면 ⭐ Star를 눌러주세요!
</p>
