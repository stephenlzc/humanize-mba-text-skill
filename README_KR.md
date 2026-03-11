# Humanize MBA Text - AI 글쓰기 흔적 감지 및 제거

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python 3.7+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/Claude-Skill-orange.svg" alt="Claude Skill">
  <img src="https://img.shields.io/badge/Version-1.2-brightgreen.svg" alt="Version: 1.2">
  <img src="https://img.shields.io/badge/Kimi-CLI-blue.svg" alt="Kimi CLI">
  <a href="README.md"><img src="https://img.shields.io/badge/中文-🇨🇳-inactive.svg" alt="中文"></a>
  <a href="README_EN.md"><img src="https://img.shields.io/badge/English-🇺🇸-inactive.svg" alt="English"></a>
  <img src="https://img.shields.io/badge/한국어-🇰🇷-red.svg" alt="한국어">
  <a href="README_JP.md"><img src="https://img.shields.io/badge/日本語-🇯🇵-inactive.svg" alt="日本語"></a>
</p>

<p align="center">
  <b>중국 MBA 졸업 논문을 위한 전문 AI 글쓰기 흔적 감지 및 제거 도구</b>
</p>

<p align="center">
  <code>#AI-Detection</code> <code>#Academic-Writing</code> <code>#MBA-Thesis</code> <code>#Claude-Skill</code> <code>#Text-Humanization</code> <code>#ChatGPT-Alternative</code> <code>#LLM-Writing</code> <code>#Research-Tools</code> <code>#Academic-Integrity</code> <code>#Chinese-NLP</code>
</p>

---

## 🎯 프로젝트 소개

이 도구는 **중국 MBA 졸업 논문**을 위해 특별히 설계된 AI 글쓰기 흔적 감지 및 제거 도구입니다. MBA 논문의 학술 규범과 실무 요구사항을 기반으로 하여, 다차원 감지 방법을 통해 텍스트의 AI 생성 특징을 식별하고 구체적인 수정 제안을 제공하여 AI 생성 텍스트를 자연스럽고 인간적인 학술 글쓰기 스타일로 변환하는 데 도움을 줍니다.

### ✨ 버전 1.1 새로운 기능

- 📚 **장 문서 재구성**: 장 규칙을 5개의 독립 파일로 분할하여 검색 및 사용이 용이
- 🎓 **MBA 규범 세분화**: MBA 논문 핵심 원칙 및 분 장별 글쓰기 가이드 신규 추가
- 📝 **형식 규범 개선**: 형식 표준 문서를 독립적으로 정리하여 중영문 혼용, 차트, 인용 등을 포괄
- 🎯 **실무 지향 강화**: 데이터 지원, 이론 적용 및 구체적 사례 분석에 더욱 중점

### 핵심 기능

- ✅ **다차원 AI 감지**: 규칙 매칭, 통계 분석, 언어 특징 세 가지 감지 방법 결합
- ✅ **장 특정 규칙**: 서론, 이론, 분석, 제안, 결론 5개 장에 대한 최적화 전략
- ✅ **MBA 논문 규범**: 중국 대학 MBA 논문의 글자 수, 구조, 형식 요구사항 준수
- ✅ **자동 수정**: 중영문 혼용 공백 등 간단한 문제 자동 처리
- ✅ **지능형 피드백**: 상세한 수정 제안 및 전후 비교 예시 생성
- ✅ **Claude Skill 통합**: Claude Code의 Skill로 직접 사용 가능

### 기술 참고

본 프로젝트는 최적화 전략 설계에 [thesis-optimizer](https://github.com/Haimbeau1o/thesis-optimizer) 프로젝트의 3차원 협동 최적화 개념을 참고하였습니다:

- 🔍 **AI 감지율 감소**: 문장 구조 다양화, 어조 자연화, 논리 인간화
- 📉 **표절률 감소**: 심층 의미 재작성, 인용 표준화, 전문 용어 처리
- ✨ **학술 윤문**: 표현 정밀화, 학술 규범화, 가독성 최적화

---

## 🎓 MBA 논문 핵심 원칙

본 도구는 중국 MBA 논문의 학술 규범을 기반으로 설계되었으며, 다음 핵심 원칙을 따릅니다:

### 1. 실무 지향
- 기업 관리 실제에서 출발하여 구체적인 관리 문제 해결 필요
- 순수 이론적 공론 지양

### 2. 작은 주제 심층 연구
- 주제 선정이 명확하고 집중되어야 하며, "작은 주제 심층 탐구" 필요
- 핵심 개념은 2-3개를 초과하지 않음
- 주제가 너무 크거나 광범위한 것 지양

### 3. 데이터 추적 가능성
- 모든 데이터는 출처를 명시해야 함
- 정확성과 신뢰성 확보
- "관련 데이터에 따륩니" 등 모호한 표현 삭제

### 4. 이론적 지원
- 1-2개 관련 이론을 분석 프레임워크로 활용
- 일반적 사실 나열 지양

### 5. 구조 규범
- 본문 글자 수 ≥ 3만 자
- 장당 최소 4개 절(장 요약 포함)
- 각 절 내용이 충실하여 한 페이지 미만인 절 지양

### 6. 학술적 진실성
- 복사율 < 15%
- 데이터 조작 금지, 모든 인용은 확인 가능해야 함

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

### 기본 사용법

#### 1. 기본 감지

```bash
# 기본 규칙 감지 사용
python scripts/detect_ai_patterns.py your_text.txt --format markdown --output report.md
```

#### 2. 다차원 융합 감지 (권장)

```bash
# 다차원 감지 사용
python scripts/multi_detector.py your_text.txt --format markdown --output report.md --plan plan.json
```

#### 3. 수정 제안 생성

```bash
# 감지 결과를 기반으로 피드백 생성
python scripts/feedback_generator.py detection_result.json --text your_text.txt --output feedback.md
```

#### 4. 자동 수정 적용

```bash
# 공백 등 간단한 문제 자동 수정
python scripts/feedback_generator.py detection_result.json --text your_text.txt --apply
```

### Claude Skill로 사용

1. 본 저장소를 Claude Code의 skills 디렉토리에 클론:

```bash
cd ~/.config/opencode/skills
git clone https://github.com/stephenlzc/humanize-mba-text-skill.git
```

2. Claude Code에서 Skill 트리거:

```
AI 흔적 제거: [텍스트 붙여넣기]
```

또는

```
이 텍스트의 AI 글쓰기 흔적을 제거해 주세요
```

---

## 📊 감지 차원

### 1. 규칙 매칭 감지

다음 AI 글쓰기 특징을 식별:

- **AI 용어**: 赋能(임파워먼트), 抓手(핵심수단), 闭环(폐쇄형루프), 痛点(고충점), 赛道(분야) 등
- **모호한 귀속**: "연구에 따르면", "전문가는 지적한다" 등
- **과도한 강조**: "핵심", "핵심", "지대한" 등
- **거시 서술**: "시대", "추세", "물결" 등
- **표면적 분석**: "부각되었다", "반영되었다" 등 -ing로 끝나는 분석
- **형식적 결말**: "종합하면", "이로 보건대" 등
- **과도한 접속사**: "첫째...둘째...마지막으로" 등
- **중영문 혼용 공백**: "MBA 논문" → "MBA논문"

### 2. 통계 분석 감지

- **문장 길이 균일성**: AI 텍스트는 보통 문장 길이가 더 균일함
- **어휘 다양성**: AI 텍스트는 어휘 다양성이 낮음
- **구두점 분포**: 구두점 사용 패턴 분석
- **단락 구조**: 단락 길이 분포 감지

### 3. 언어 특징 감지

- **접속사 밀도**: 논리적 접속사 사용 빈도 통계
- **형식적 표현 패턴**: 과도하게 형식적인 학술 표현 식별
- **문장 구조 복잡성**: 복잡한 문장 구조 사용 분석

---

## 🎓 분 장별 글쓰기 가이드

본 도구는 MBA 논문 5개 핵심 장에 대한 상세한 글쓰기 가이드를 제공합니다:

### 제1장 서론

**일반적인 문제**:
- ❌ 거시 서술식 도입: "경제 발전에 따라..."
- ❌ 연구 의의가 공허함: "중요한 이론적 의의와 실무적 가치가 있음"
- ❌ 문헌 고찰 나열: A의견, B의견, C의견
- ❌ 연구 방법 단순 나열

**개선 전략**:
- ✅ 바로 핵심: 연구 기업, 구체적인 문제를 직접 언급
- ✅ 의의 구체화: 어떤 문제를 해결하고 어떤 가치를 가져오는지 설명
- ✅ 문헌 주제 중심: 주제별로 구성하고 비판적 분석 포함
- ✅ 방법 구체화: 데이터 출처, 샘플, 분석 도구 설명

📄 **상세 가이드**: [chapter-1-introduction.md](references/chapter-1-introduction.md)

### 제2장 이론적 기초

**일반적인 문제**:
- ❌ 교과서식 정의 나열
- ❌ 이론 나열: 5-6개 이론 소개
- ❌ 이론과 실무 괴리

**개선 전략**:
- ✅ 간결한 정의: 2-3개 핵심 개념
- ✅ 이론 엄선: 1-2개 핵심 이론, 선택 이유 설명
- ✅ 적용 지향: 후속 분석을 위한 프레임워크 제공

📄 **상세 가이드**: [chapter-2-theory.md](references/chapter-2-theory.md)

### 제3장 현황 및 문제 분석

**일반적인 문제**:
- ❌ 기업 개황 자료 나열, 연구와의 연관성 낮음
- ❌ 현황 서술이 정성적 위주이며 데이터 부족
- ❌ 문제 식별이 모호함: "관리 미흡", "효율 저하"
- ❌ 원인 분석이 표면적임: 현상 서술에 머무름

**개선 전략**:
- ✅ 관련성 집중: 연구와 관련된 배경 정보만 제공
- ✅ 데이터 중심: 구체적 지표와 시계열 데이터 사용
- ✅ 문제 구체화: 각 문제에 측정 지표와 조사 데이터
- ✅ 심층 분석: 이론 프레임워크로 근본 원인 분석

📄 **상세 가이드**: [chapter-3-analysis.md](references/chapter-3-analysis.md)

### 제4장 대안 제안

**일반적인 문제**:
- ❌ 제안이 공허함: "관리 강화", "프로세스 최적화"
- ❌ 실행 가능성 부족
- ❌ 제약 조건 무시
- ❌ 템플릿 적용: SWOT 형식적 사용

**개선 전략**:
- ✅ 구체적이고 실행 가능: 무엇을, 어떻게, 누가 할지 명확히
- ✅ 단계별 실행: 단기, 중기, 장기 구분
- ✅ 제약 고려: 자원, 역량, 문화적 제한 분석
- ✅ 효과 정량화: 예상 효과는 가능한 한 정량화

📄 **상세 가이드**: [chapter-4-solutions.md](references/chapter-4-solutions.md)

### 제5장 결론

**일반적인 문제**:
- ❌ 초록 내용 반복
- ❌ 각 장 내용 단순 나열
- ❌ 혁신점이 공허함: "최초 연구", "공백 메우기"
- ❌ 연구 한계 회피

**개선 전략**:
- ✅ 연구 발견: 핵심 발견 강조, 초록과 중복 금지
- ✅ 혁신 구체화: 이론, 방법, 응용 혁신을 객관적으로 설명
- ✅ 한계 정직: 구체적인 한계와 영향 분석
- ✅ 향후 전망: 구체적이고 실행 가능한 연구 방향 제시

📄 **상세 가이드**: [chapter-5-conclusion.md](references/chapter-5-conclusion.md)

---

## 📝 형식 규범

독립적인 형식 규범 문서가 다음을 포괄:

- 중영문/숫자 혼용 규범
- 차트 번호 및 조판 규범
- 인용 및 참고문헌 규범
- 숫자 및 단위 규범
- 구두점 규범
- 단락 및 계층 규범

📄 **상세 규범**: [format-standards.md](references/format-standards.md)

---

## 📈 감지 결과 해석

감지 보고서는 다음 차원을 포함:

- **AI 생성 확률**: 0-100%, 점수가 높을수록 AI 흔적이 뚜렷함
- **위험 등급**: 🔴 고위험 / 🟡 중위험 / 🟢 저위험
- **감지기 일관성**: 세 가지 감지 방법의 결과 일치성
- **우선 수정 항목**: 심각도순으로 정렬된 수정 제안
- **장 특정 제안**: 감지된 장 유형에 따른 대응 제안

### 수정 전략

AI 확률 점수에 따라 다른 전략 적용:

**🔴 고위험 (>70%)**: 심층 재작성
- 단락 구조 전면 재구성
- 모든 AI 특징 어휘 삭제
- 구체적 데이터와 사례 보충
- 예상 시간: 2-3시간

**🟡 중위험 (40-70%)**: 대응 최적화
- 고우선순위 AI 특징 수정
- 형식적 표현과 템플릿화된 표현 조정
- 핵심 데이터 지원 보충
- 예상 시간: 1-2시간

**🟢 저위험 (<40%)**: 세부 윤문
- 소량의 AI 흔적 수정
- 언어 표현 최적화
- 최종 교정
- 예상 시간: 30분-1시간

---

## 💡 사용 예시

### 예시 1: AI 용어 제거

**원문**:
```
디지털 전환은 기업의 고품질 발전을 촉진하는 핵심 수단이 되었으며,
비즈니스 혁신에 임파워먼트를 제공하여 기업에 상당한 가치를 창출합니다.
```

**수정 후**:
```
본 연구는 디지털 전환이 기업 성과에 미치는 영향을 탐구합니다.
XX사의 2018-2023년 재무 데이터를 분석한 결과,
디지털 투자와 영업 수익 성장 간에 정의 상관관계가 있음을 발견했습니다.
```

### 예시 2: 모호한 귀속 제거

**원문**:
```
연구에 따르면 기업 문화가 조직 성과에 중요한 영향을 미칩니다.
```

**수정 후**:
```
Schein(2010)의 연구에 따르면, 강력한 기업 문화와 조직 성과 간에
정의 상관관계가 존재합니다(r=0.42, p<0.05).
```

### 예시 3: MBA 논문 작은 주제 심층 연구

**원문**:
```
기업 디지털 전환 연구
```

**수정 후**:
```
XX사 생산 부문 디지털 전환의 프로세스 최적화 연구
```

### 예시 4: 데이터 추적 가능성

**원문**:
```
기업 매출 성장 20%, 직원 만족도 85%.
```

**수정 후**:
```
XX사 2023년 연례 보고서에 따르면, 기업 매출은 전년 대비 20% 성장했습니다.
2023년 12월에 실시된 설문조사(N=120)에 따르면, 직원 만족도는 85%입니다.
```

### 예시 5: 중영문 혼용 공백 수정

**원문**:
```
MBA 논문 작성에서 AI 흔적 문제에 주목해야 합니다.
2023 년의 연구에 따르면, 15 %의 기업이 이러한 문제를 겪고 있습니다.
```

**수정 후**:
```
MBA논문 작성에서 AI흔적 문제에 주목해야 합니다.
2023년의 연구에 따르면, 15%의 기업이 이러한 문제를 겪고 있습니다.
```

---

## 📁 프로젝트 구조

```
humanize-mba-text-skill/
├── SKILL.md                          # 주요 Claude Skill 파일
├── README.md                         # 본 파일
├── LICENSE                           # MIT 라이선스
│
├── references/                       # 참조 문서
│   ├── ai-writing-patterns.md        # AI 글쓰기 특징 상세 가이드
│   ├── chapter-1-introduction.md     # 제1장: 서론 글쓰기 가이드
│   ├── chapter-2-theory.md           # 제2장: 이론적 기초 글쓰기 가이드
│   ├── chapter-3-analysis.md         # 제3장: 현황 및 문제 분석 글쓰기 가이드
│   ├── chapter-4-solutions.md        # 제4장: 대안 제안 글쓰기 가이드
│   ├── chapter-5-conclusion.md       # 제5장: 결론 글쓰기 가이드
│   ├── format-standards.md           # 형식 규범
│   ├── strategy_ai_reduction.md      # AI 감지율 감소 전략 ⭐신규
│   ├── strategy_plagiarism.md        # 표절률 감소 전략 ⭐신규
│   └── strategy_polishing.md         # 학술 윤문 전략 ⭐신규
│
└── scripts/                          # 감지 스크립트
    ├── detect_ai_patterns.py         # 기본 규칙 감지
    ├── multi_detector.py             # 다방안 융합 감지기
    └── feedback_generator.py         # 피드백 생성기
```

---

## 🔧 고급 사용법

### 대화형 수정

```bash
python scripts/multi_detector.py your_text.txt --interactive
```

### 수정 계획 내보내기

```bash
python scripts/multi_detector.py your_text.txt --plan modification_plan.json
```

### 일괄 처리

```bash
# 여러 파일 처리
for file in *.txt; do
    python scripts/multi_detector.py "$file" --output "reports/${file%.txt}_report.md"
done
```

---

## ⚠️ 주의사항

1. **학술적 진실성**: 재작성 시 학술적 진실성을 유지하고 데이터를 조작하지 않음; 모든 데이터는 실제 출처가 있어야 함
2. **데이터 검증**: 불확실한 인용과 데이터는 사용자가 원시 자료를 검증할 것을 권장
3. **이론 적합성**: 사용자가 구체적인 연구 문제에 적합한 이론 프레임워크를 선택할 것을 권장
4. **기업 승인**: 기업 내부 데이터가 포함된 경우 기업의 서면 승인을 받거나 비식별화 처리 권장
5. **표절 통제**: 재작성 후 표절 검사를 받아 복사율이 15% 미만인지 확인 권장
6. **개인화 조정**: 재작성된 텍스트는 사용자가 구체적인 학교와 지도 교수의 요구사항에 따라 조정해야 함
7. **범위 제한**: 본 도구는 AI 흔적 제거와 형식 규범에 집중하며, 학술적 내용의 심층 검토는 포함하지 않음
8. **참고문헌**: 재작성은 참고문헌을 자동 생성하지 않으며, 사용자가 실제 인용에 따라 완전히 보충해야 함

---

## 🤝 기여 가이드

Issue와 Pull Request를 환영합니다!

### Issue 제출

- 문제점을 명확히 설명
- 예시 텍스트 제공(비식별화 가능)
- 기대하는 동작 설명

### Pull Request 제출

1. 본 저장소를 Fork
2. 특성 브랜치 생성 (`git checkout -b feature/AmazingFeature`)
3. 수정사항 커밋 (`git commit -m 'Add some AmazingFeature'`)
4. 브랜치에 푸시 (`git push origin feature/AmazingFeature`)
5. Pull Request 열기

---

## 📝 변경 로그

### v1.2.0 (2024-02-10)

- 📊 **3차원 협동 최적화 전략 문서화**: AI 감지율 감소, 표절률 감소, 학술 윤문 향상을 위한 전략 문서 추가
  - strategy_ai_reduction.md: AI 감지율 감소 전략
  - strategy_plagiarism.md: 표절률 감소 전략
  - strategy_polishing.md: 학술 윤문 전략
- 🌐 **다국어 지원 개선**: 한국어 README 완전 번역
- 🎓 **전략 가이드 세분화**: 각 최적화 차원에 대한 상세한 실행 가이드 제공

### v1.1.0 (2024-02-05)

- 📚 **장 문서 재구성**: 장 규칙을 5개의 독립 파일로 분할
  - chapter-1-introduction.md: 서론 상세 가이드
  - chapter-2-theory.md: 이론적 기초 상세 가이드
  - chapter-3-analysis.md: 현황 및 문제 분석 상세 가이드
  - chapter-4-solutions.md: 대안 제안 상세 가이드
  - chapter-5-conclusion.md: 결론 상세 가이드
  - format-standards.md: 형식 규범 독립 문서
- 🎓 **MBA 규범 세분화**: MBA 논문 핵심 원칙 장 신규 추가
- 🎯 **실무 지향 강화**: 데이터 지원, 이론 적용 및 구체적 사례에 더욱 중점
- 📝 **형식 규범 개선**: 중영문 혼용, 차트, 인용 등 형식 표준 독립 정리
- 🏗️ **프로젝트 구조 최적화**: 더 명확한 파일 구성 및 인덱스

### v1.0.0 (2024-02-04)

- ✨ 초기 버전 출시
- 🎯 다차원 AI 특징 감지 지원
- 📚 장 특정 규칙 추가
- 🔧 자동 수정 기능 구현
- 🎓 Claude Skill 통합

---

## 📄 라이선스

본 프로젝트는 [MIT 라이선스](LICENSE)를 채택합니다 - 자세한 내용은 LICENSE 파일 참조

---

## 🙏 감사의 글

- Claude Code의 Skill 프레임워크 제공에 감사드립니다
- 피드백과 제안을 제공한 모든 사용자에게 감사드립니다
- **특히 [Haimbeau1o/thesis-optimizer](https://github.com/Haimbeau1o/thesis-optimizer) 프로젝트에 감사드립니다**. 본 프로젝트의 3차원 협동 최적화 전략(AI 감지율 감소, 표절률 감소, 학술 윤문 향상)은 해당 프로젝트의 우수한 설계를 참고하였습니다
- Kimi CLI의 서브 에이전트 개발 지원에 감사드립니다

---

## 📮 연락처

- GitHub Issues: [https://github.com/stephenlzc/humanize-mba-text-skill/issues](https://github.com/stephenlzc/humanize-mba-text-skill/issues)
- 작성자: stephenlzc

---

## 🔗 관련 프로젝트

- [thesis-optimizer](https://github.com/Haimbeau1o/thesis-optimizer) - 학술 논문 지능형 최적화 시스템(컴퓨터 딥러닝 방향)

---

<p align="center">
  이 프로젝트가 도움이 되었다면 ⭐ Star를 눌러주세요!
</p>
