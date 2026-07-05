# Humanize MBA Text - AI執筆痕跡の検出と除去

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python 3.7+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/Claude-Skill-orange.svg" alt="Claude Skill">
  <img src="https://img.shields.io/badge/Version-1.3-brightgreen.svg" alt="Version: 1.3">
  <img src="https://img.shields.io/badge/Kimi-CLI-blue.svg" alt="Kimi CLI">
  <a href="README.md"><img src="https://img.shields.io/badge/中文-🇨🇳-inactive.svg" alt="中文"></a>
  <a href="README_EN.md"><img src="https://img.shields.io/badge/English-🇺🇸-inactive.svg" alt="English"></a>
  <a href="README_KR.md"><img src="https://img.shields.io/badge/한국어-🇰🇷-inactive.svg" alt="한국어"></a>
  <img src="https://img.shields.io/badge/日本語-🇯🇵-red.svg" alt="日本語">
</p>

<p align="center">
  <b>中国MBA卒業論文専用のAI執筆痕跡検出・除去ツール</b>
</p>

<p align="center">
  <code>#AI-Detection</code> <code>#Academic-Writing</code> <code>#MBA-Thesis</code> <code>#Claude-Skill</code> <code>#Text-Humanization</code> <code>#ChatGPT-Alternative</code> <code>#LLM-Writing</code> <code>#Research-Tools</code> <code>#Academic-Integrity</code> <code>#Chinese-NLP</code>
</p>

---

## 🎯 プロジェクト概要

本ツールは**中国のMBA卒業論文**専用に設計されたAI執筆痕跡検出・除去ツールです。MBA論文の学術規範と実践的な要求に基づき、多次元的な検出手法を用いてテキスト内のAI生成特徴を識別し、具体的な修正提案を提供することで、AI生成テキストを自然で人間らしい学術的執筆スタイルに書き換えることを支援します。

### ✨ バージョン1.3の新機能

- 🔬 **ルール外部化**：すべてのAI検出ルールを外部TOMLファイルに移管し、7カテゴリ（`structure / rhythm_quality / formatting / content / evidence / language / chapter-categories`）に分割。ルールはコードから独立し、拡張時にコード変更不要
- 📊 **散文構造分析器（5つ）**：文長CV / 段落長CV / 段落頭末テンプレート反復 / 段落間構造均一化 / 章節テンプレート反復。各分析器がseverity + confidence + location + evidence + suggestionを発行
- 🔗 **意味連鎖分析器（10）**：三段式 / 作者列挙 / 方法積み上げ / 要約テンプレート / 結論エコー / 曖昧問題 / 無出所数量化 / 巨大物語 / 証拠連鎖 / 問題-対策追跡 — 段落や章を横断するパターン
- 📋 **構造化書き換えプラン**：レポートに `modify_plan` キーを追加し、位置・書き換え骨格・推奨置換・目標文字数範囲を提示。severity high → medium → low でソートされ、LLMまたは人手編集に直接入力可能
- 🎯 **統一ルールソース**：`AIPatternDetector` / `StatisticalDetector` / `FeedbackGenerator` が同じTOMLルール文書を共有

### ✨ バージョン1.2の新機能

- 📚 **戦略文書の追加**：3つの最適化戦略ファイルを新規追加
  - 次元1：AI検出率の低減戦略
  - 次元2：重複率の低減戦略
  - 次元3：学術的推敲の向上戦略
- 🎓 **MBA規範の詳細化**：MBA論文の核心原則と章別執筆ガイドを拡充
- 📝 **形式規範の改善**：中国語・英語混在、図表、引用などをカバーする形式標準文書を独立整理
- 🎯 **実践重視の強化**：データ支援、理論適用、具体的な事例分析をさらに重視
- 🌐 **多言語README**：日本語版を含む4言語版を整備

### 核心機能

- ✅ **多層AI検出**：正規表現ルール → 散文統計（5次元） → 意味連鎖（10次元）の3層構成
- ✅ **章別特定ルール**：緒論、理論、分析、提言、結論の5つの章に対応した最適化戦略
- ✅ **MBA論文規範**：中国の大学MBA論文の字数、構造、形式要件に準拠
- ✅ **構造化書き換えプラン**：各issueに位置・骨格・推奨置換・目標文字数を付与
- ✅ **自動修正**：中国語・英語混在のスペースなどの簡単な問題を自動処理
- ✅ **インテリジェントフィードバック**：詳細な修正提案と前後比較例を生成
- ✅ **Claude Skill統合**：Claude CodeのSkillとして直接使用可能

### 技術参考

本プロジェクトの最適化戦略設計は、[thesis-optimizer](https://github.com/Haimbeau1o/thesis-optimizer)プロジェクトの三次元協同最適化理念を参考にしています：

- 🔍 **次元1：AI検出率の低減**
  - 文構造の多様化
  - 学術トーンの自然化
  - 論理連鎖の人間化
  
- 📉 **次元2：重複率の低減**
  - 深層意味の書き換え
  - 引用の標準化
  - 専門用語の処理
  
- ✨ **次元3：学術的推敲の向上**
  - 表現の精緻化
  - 学術規範化
  - 可読性の最適化

---

## 🎓 MBA論文の核心原則

本ツールは中国のMBA論文学術規範に基づいて設計され、以下の核心原則に従います：

### 1. 実践志向
- 企業経営の実際に由来し、具体的な経営問題を解決すること
- 純粋な理論の空論を避けること

### 2. 小題大做（小さなテーマを深く掘り下げる）
- テーマは明確に焦点を絞り、「小題深做」
- 核心概念は2-3個以内に抑える
- テーマが大きすぎたり、範囲が広すぎたりすることを避ける

### 3. データの溯源
- すべてのデータには出典を明記すること
- 正確性と信頼性を確保すること
- 「関連データが示す」などの曖昧な表現を削除すること

### 4. 理論支援
- 分析フレームワークとして1-2の関連理論を用いること
- 事実だけを述べることを避ける

### 5. 構造規範
- 本文の字数：3万字以上
- 各章は少なくとも4節（章末まとめを含む）
- 各節の内容は充実させ、1ページ未満の節を避ける

### 6. 学術倫理
- 複製率：15%未満
- データの捏造をせず、すべての引用は確認可能であること

---

## 🚀 クイックスタート

### インストール

```bash
# リポジトリをクローン
git clone https://github.com/stephenlzc/humanize-mba-text-skill.git
cd humanize-mba-text-skill

# 依存関係をインストール（transformersモデルを使用する場合）
pip install transformers torch
```

### 基本的な使用方法

#### 1. 基礎検出

```bash
# 基礎ルールを使用した検出
python scripts/detect_ai_patterns.py your_text.txt --format markdown --output report.md
```

#### 2. 多次元融合検出（推奨）

```bash
# 多次元検出を使用
python scripts/multi_detector.py your_text.txt --format markdown --output report.md --plan plan.json
```

#### 3. 修正提案の生成

```bash
# 検出結果に基づいてフィードバックを生成
python scripts/feedback_generator.py detection_result.json --text your_text.txt --output feedback.md
```

#### 4. 自動修正の適用

```bash
# スペースなどの簡単な問題を自動修正
python scripts/feedback_generator.py detection_result.json --text your_text.txt --apply
```

### Claude Skillとして使用

1. 本リポジトリをClaude Codeのskillsディレクトリにクローン：

```bash
cd ~/.config/opencode/skills
git clone https://github.com/stephenlzc/humanize-mba-text-skill.git
```

2. Claude CodeでSkillをトリガー：

```
AI痕跡を除去：[テキストを貼り付け]
```

または

```
この文章のAI執筆痕跡を除去してください
```

---

## 📊 検出次元

### 1. ルールマッチング検出

以下のAI執筆特徴を識別：

- **AI用語**：赋能、抓手、闭环、痛点、赛道など
- **曖昧な帰属**：「有研究指出」「专家认为」など
- **過度な強調**：「关键」「核心」「至关重要」など
- **マクロナラティブ**：「时代」「趋势」「浪潮」など
- **表面的分析**：「凸显了」「反映了」など-ingで終わる分析
- **決まり文句の結び**：「综上所述」「由此可见」など
- **過多な接続詞**：「首先...其次...最后」など
- **中国語・英語混在のスペース**：「MBA 论文」→「MBA论文」

### 2. 統計分析検出

- **文の長さの均一性**：AIテキストは通常、文の長さがより均一
- **語彙の多様性**：AIテキストは語彙多様性が低い
- **句読点の分布**：句読点の使用パターンを分析
- **段落構造**：段落長の分布を検出

### 3. 言語特徴検出

- **接続詞密度**：論理接続詞の使用頻度を統計
- **正式表現パターン**：過度に形式的な学術表現を識別
- **文型の複雑さ**：複雑な文型の使用状況を分析

### 4. 散文構造分析器（v1.3）

各分析器が `AnalyzerIssue`（analyzer_id / severity / confidence / location / evidence / suggestion）と統計指標を発行：

| 次元 | analyzer_id | トリガー |
| --- | --- | --- |
| 6 | `uniform_sentence_length` | 文長分散・CVが閾値超過（段落+全文） |
| 9 | `uniform_paragraph_length` | 段落間CJK長CV < 0.25 |
| 10 | `paragraph_edge_template_repeat` | 3+ 連続段落が同一頭末指紋を共有 |
| 8a | `paragraph_structure_uniformity` | 3+ 連続段落が同一4要素構造指紋を共有 |
| 8b | `chapter_template_repeat` | 単一章で3+節が同一章節テンプレートを再利用 |

### 5. 意味連鎖分析器（v1.3）

段落や章を横断するAIパターン：

| 次元 | analyzer_id | トリガー |
| --- | --- | --- |
| 3 | `chain_three_part_rule` | 3+ 連続段落が「一是…二是…三是」または「まず…次に…最後に」を使用 |
| 3 | `chain_author_listing` | 単一章で4+「作者(年) 指出/认为」を列挙 |
| 3 | `chain_method_name` | 単一段落で2+ 方法/モデル/理論名を個別説明なしで積層 |
| 3 | `chain_abstract_template` | 単一段落が3+ 要約テンプレート語句にヒット |
| 3 | `chain_conclusion_echo` | 結論章冒頭と緒論冒頭の文字Jaccard ≥ 0.30 |
| 4 | `chain_vague_problem_statement` | 2+ 曖昧問題表現で30字内に数値根拠なし |
| 4 | `chain_unsupported_quantification` | 2+ 百分率/順位主張で80字内に「根据/来源/问卷/N=」不在 |
| 4 | `chain_macro_narrative` | 1000字ウィンドウ内で3+ マクロ物語表現 |
| 5 | `evidence_chain_completeness` | content+evidence横断：2+ 定量化/調査主張が方法根拠不在 |
| 5 | `cross_section_problem_trace` | 第3章の問題 ↔ 第5章の対策キーワード重複率 < 30% |

### 6. 構造化書き換えプラン（v1.3）

`detect_ai_patterns.AIPatternDetector.generate_report()` と `multi_detector.FusionEngine.detect()` が `modify_plan` キーを公開：

```json
{
  "analyzer_id": "chain_unsupported_quantification",
  "severity": "high",
  "location": "global",
  "evidence": "百分率/順位主張が7件、そのうち5件が80字内に根拠不在",
  "suggestion": "各定量主張に根拠を付与",
  "rewrite_template": "サンプル・時間窓・統計スコープを各主張に付与する。",
  "recommended_replacements": [
    "「2023年12月顧客アンケート（N=120）によると…」",
    "サンプル説明：「5段階リカート尺度」",
    "検証不能時：「本指標は別途検証が必要」",
  ],
  "target_word_count_range": [60, 140]
}
```

---

## 🎓 章別執筆ガイド

本ツールはMBA論文の5つの核心章に対する詳細な執筆ガイドを提供します：

### 第1章 緒論

**よくある問題**：
- ❌ 壮大なナラティブで始まる：「随着经济的发展...」
- ❌ 研究意義が空疎：「具有重要理论意义和实践价值」
- ❌ 文献レビューが単なる列挙：A说、B说、C说
- ❌ 研究方法が単純な列挙

**改善戦略**：
- ✅ オープニングは率直に：研究対象企業、具体的な問題を直接明示
- ✅ 意義を具体的に：どの問題を解決し、どのような価値をもたらすかを説明
- ✅ レビューをテーマ別に：テーマ別に構成し、批判的な分析を含める
- ✅ 方法を具体的に：データ出典、サンプル、分析ツールを説明

📄 **詳細ガイド**：[chapter-1-introduction.md](references/chapter-1-introduction.md)

### 第2章 理論基礎

**よくある問題**：
- ❌ 教科書的な定義の羅列
- ❌ 理論の列挙：5-6個の理論を紹介
- ❌ 理論と実践の乖離

**改善戦略**：
- ✅ 簡潔な定義：2-3個の核心概念
- ✅ 理論を厳選：1-2個の核心理論を選び、選択理由を説明
- ✅ 適用志向：理論が後続の分析にフレームワークを提供する

📄 **詳細ガイド**：[chapter-2-theory.md](references/chapter-2-theory.md)

### 第3章 現状と問題分析

**よくある問題**：
- ❌ 企業概況の資料が研究との関連度が低い
- ❌ 現状記述が定性的でデータに欠ける
- ❌ 問題認識が漠然：「管理不善」「效率低下」
- ❌ 原因分析が表面的：現象記述に留まる

**改善戦略**：
- ✅ 関連性に焦点：研究に関連する背景のみ提供
- ✅ データで語る：具体的指標と時系列データを使用
- ✅ 問題を具体化：各問題に測定指標と調査データを持たせる
- ✅ 深く掘り下げる：理論フレームワークで根本原因を分析

📄 **詳細ガイド**：[chapter-3-analysis.md](references/chapter-3-analysis.md)

### 第4章 対策提言

**よくある問題**：
- ❌ 提言が空疎：「加强管理」「优化流程」
- ❌ 実現可能性に欠ける
- ❌ 制約条件を無視
- ❌ テンプレートの流用：SWOTが形骸化

**改善戦略**：
- ✅ 具体的で実現可能：何をするか、どうやるか、誰がやるかを明確に
- ✅ 段階的実施：短期、中期、長期を区別
- ✅ 制約を考慮：リソース、能力、文化の制限を分析
- ✅ 効果を定量化：期待効果は可能な限り定量化

📄 **詳細ガイド**：[chapter-4-solutions.md](references/chapter-4-solutions.md)

### 第5章 結論

**よくある問題**：
- ❌ 要旨の内容を繰り返す
- ❌ 単純に各章の内容を列挙
- ❌ 独創性が空疎：「首次研究」「填补空白」
- ❌ 研究限界を回避

**改善戦略**：
- ✅ 研究発見：核心発見を強調し、要旨と重複させない
- ✅ 独創性を具体化：理論、方法、応用の革新を客観的に説明
- ✅ 誠実な限界：限界と影響を具体的に分析
- ✅ 今後の展望：具体的で実現可能な研究方向を提案

📄 **詳細ガイド**：[chapter-5-conclusion.md](references/chapter-5-conclusion.md)

---

## 📝 形式規範

独立した形式規範文書が以下をカバー：

- 中国語・英語・数字混在の規範
- 図表の番号付けと組版規範
- 引用と参考文献の規範
- 数字と単位の規範
- 句読点の規範
- 段落と階層の規範

📄 **詳細規範**：[format-standards.md](references/format-standards.md)

---

## 📈 検出結果の解釈

検出レポートには以下の次元が含まれます：

- **AI生成確率**：0-100%、スコアが高いほどAI痕跡が明らか
- **リスクレベル**：🔴 高リスク / 🟡 中リスク / 🟢 低リスク
- **検出器の一致度**：3つの検出手法の結果の一致性
- **優先修正項目**：深刻度でソートされた修正提案
- **章別特定提案**：検出された章タイプに基づく対象的な提案

### 修正戦略

AI確率スコアに応じて異なる戦略を採用：

**🔴 高リスク（>70%）**：深い書き換え
- 段落構造を全面的に再構築
- すべてのAI特徴語彙を削除
- 具体的なデータと事例を補充
- 想定時間：2-3時間

**🟡 中リスク（40-70%）**：対象的な最適化
- 高優先度のAI特徴を修正
- 決まり文句とテンプレート表現を調整
- 关键なデータ支援を補充
- 想定時間：1-2時間

**🟢 低リスク（<40%）**：詳細な推敲
- 少量のAI痕跡を修正
- 言語表現を最適化
- 最終校正
- 想定時間：30分-1時間

---

## 💡 使用例

### 例1：AI用語の除去

**原文**：
```
数字化转型已成为推动企业高质量发展的关键抓手，
通过赋能业务创新，为企业创造显著价值。
```

**書き換え後**：
```
本研究はデジタル変革が企業パフォーマンスに与える影響を検討する。
XX社2018-2023年の財務データを分析した結果、
デジタル投資と営業収入増加には正の相関関係があることが判明した。
```

### 例2：曖昧な帰属の除去

**原文**：
```
有研究指出，企业文化对组织绩效具有重要影响。
```

**書き換え後**：
```
Schein(2010)の研究は、強い企業文化と組織パフォーマンスに
正の相関関係があることを示している（r=0.42, p<0.05）。
```

### 例3：MBA論文の小題大做

**原文**：
```
企业数字化转型研究
```

**書き換え後**：
```
XX公司生产部门数字化转型中的流程优化研究
```

### 例4：データの溯源

**原文**：
```
企业营收增长20%，员工满意度为85%。
```

**書き換え後**：
```
XX社2023年年次報告書によると、企業の営業収入は前年比20%増加した。
2023年12月に実施したアンケート調査（N=120）によると、従業員満足度は85%であった。
```

### 例5：中国語・英語混在スペースの修正

**原文**：
```
MBA 论文写作需要关注 AI 痕迹问题。
2023 年的研究表明，15 % 的企业存在此类问题。
```

**書き換え後**：
```
MBA论文写作需要关注AI痕迹问题。
2023年的研究表明，15%的企业存在此类问题。
```

---

## 📁 プロジェクト構造

```
humanize-mba-text-skill/
├── SKILL.md                          # Claude Skillメインファイル
├── README.md                         # 中国語版
├── README_EN.md                      # 英語版
├── README_JP.md                      # 日本語版（このファイル）
├── README_KR.md                      # 韓国語版
├── LICENSE                           # MITライセンス
│
├── references/                       # 参考文書 + AI検出ルール
│   ├── ai-writing-patterns.md        # AI執筆特徴詳細ガイド
│   ├── chapter-1-introduction.md     # 第1章：緒論執筆ガイド
│   ├── chapter-2-theory.md           # 第2章：理論基礎執筆ガイド
│   ├── chapter-3-analysis.md         # 第3章：現状と問題分析執筆ガイド
│   ├── chapter-4-solutions.md        # 第4章：対策提言執筆ガイド
│   ├── chapter-5-conclusion.md       # 第5章：結論執筆ガイド
│   ├── format-standards.md           # 形式規範
│   ├── strategy_ai_reduction.md      # AI検出率低減戦略
│   ├── strategy_plagiarism.md        # 重複率低減戦略
│   ├── strategy_polishing.md         # 学術的推敲向上戦略
│   ├── chinese-paper-humanization-rules.toml   # ルール単一入口（フォールバック）
│   └── rules/                        # ⭐v1.3：漸進読み込み対応AIルール
│       ├── index.toml                #   軽量マニフェスト
│       ├── categories/
│       │   ├── structure.toml        #   構造カテゴリ
│       │   ├── rhythm_quality.toml  #   リズムカテゴリ
│       │   ├── formatting.toml       #   形式カテゴリ
│       │   ├── content.toml          #   内容（マクロ物語/曖昧問題/無出所数量化を含む）
│       │   ├── evidence.toml         #   証拠（方法未記載/因果飛躍を含む）
│       │   └── language.toml         #   言語カテゴリ
│       ├── chapter-categories.toml  #   章節タイプ分類
│       └── metrics.toml              #   共通度量語彙
│
└── scripts/                          # 検出スクリプト
    ├── rule_loader.py                # ⭐v1.3：TOMLルール漸進読み込みローダー
    ├── detect_ai_patterns.py         # AIPatternDetectorエントリ（modify_plan付き）
    ├── multi_detector.py             # FusionEngineエントリ
    ├── feedback_generator.py         # フィードバック生成器
    └── analyzers/                    # ⭐v1.3：分析器パッケージ
        ├── __init__.py               #   run_prose_analyzers / run_semantic_chain_analyzers / build_modify_plan を公開
        ├── _types.py                 #   AnalyzerIssue / AnalyzerReport データ契約
        ├── _segments.py              #   共通セグメンテーションヘルパー
        ├── _regex_categories.py      #   hitレベルラッパー（連鎖層用）
        ├── sentence_length.py        #   次元 6
        ├── paragraph_length.py       #   次元 9
        ├── paragraph_edges.py        #   次元 10
        ├── paragraph_structure.py    #   次元 8a
        ├── chapter_template.py       #   次元 8b
        ├── semantic_chain.py         #   次元 3/4/5：10連鎖分析器
        └── rewrite_planner.py        #   AnalyzerIssue → 構造化ModifyEntry
```

---

## 🔧 高度な使用方法

### インタラクティブ修正

```bash
python scripts/multi_detector.py your_text.txt --interactive
```

### 修正計画のエクスポート

```bash
python scripts/multi_detector.py your_text.txt --plan modification_plan.json
```

### バッチ処理

```bash
# 複数ファイルを処理
for file in *.txt; do
    python scripts/multi_detector.py "$file" --output "reports/${file%.txt}_report.md"
done
```

---

## ⚠️ 注意事項

1. **学術倫理**：書き換え時は学術倫理を守り、データを捏造しないこと；すべてのデータは真実の出典を持つこと
2. **データ検証**：不確実な引用やデータについては、ユーザーに元資料の検証を推奨すること
3. **理論の適合**：具体的な研究問題に応じて適切な理論フレームワークを選択することをユーザーに推奨すること
4. **企業承認**：企業内部データを扱う場合は、企業の書面による承認を得るか、匿名化処理を行うことを推奨すること
5. **重複チェック**：書き換え後は重複チェックを行い、複製率が15%未満であることを確認すること
6. **個別調整**：書き換え後のテキストは、ユーザーが具体的な大学と指導教員の要件に応じて調整すること
7. **範囲制限**：本ツールはAI痕跡の除去と形式規範に焦点を当てており、学術的内容の深度審査は行わない
8. **参考文献**：書き換えでは参考文献は自動生成されないため、ユーザーは実際の引用に基づいて補完する必要がある

---

## 🤝 貢献ガイド

IssueとPull Requestの提出を歓迎します！

### Issueの提出

- 遭遇した問題を明確に説明すること
- 例テキストを提供すること（匿名化可能）
- 期待される動作を説明すること

### Pull Requestの提出

1. 本リポジトリをForkすること
2. 特性ブランチを作成すること（`git checkout -b feature/AmazingFeature`）
3. 修正をコミットすること（`git commit -m 'Add some AmazingFeature'`）
4. ブランチにプッシュすること（`git push origin feature/AmazingFeature`）
5. Pull Requestを開くこと

---

## 📝 更新履歴

### v1.3.0 (2026-07-05)

- 🔬 **ルール外部化**：全AI検出ルールを外部TOMLへ移管し、7カテゴリに分割。`scripts/rule_loader.py`が漸進読み込みを提供
- 📊 **散文構造分析器**：5つの統計/指紋分析器を追加（次元 6 / 8a / 8b / 9 / 10）
- 🔗 **意味連鎖分析器**：10の段落/章節横断連鎖分析器を追加（次元 3 / 4 / 5）
- 📋 **構造化書き換えプラン**：`detect_ai_patterns.generate_report` が `modify_plan` キーを返すように
- 🎯 **統一ルールソース**：`AIPatternDetector` / `StatisticalDetector` / `FeedbackGenerator` が同じTOMLルール文書を共有
- 🛠 **新規 `scripts/analyzers/` パッケージ**：散文+連鎖分析器の統合ディレクトリ

### v1.2.0 (2026-03-11)

- 📚 **戦略文書の追加**：3つの最適化戦略ファイルを新規追加
  - strategy_ai_reduction.md：AI検出率低減の詳細戦略
    - 文構造の多様化
    - 学術トーンの自然化
    - 論理連鎖の人間化
  - strategy_plagiarism.md：重複率低減の詳細戦略
    - 深層意味の書き換え
    - 引用の標準化
    - 専門用語の処理
  - strategy_polishing.md：学術的推敲向上の詳細戦略
    - 表現の精緻化
    - 学術規範化
    - 可読性の最適化
- 🌍 **多言語サポート**：日本語版READMEを追加
- 🎯 **戦略の詳細化**：三次元協同最適化戦略をより詳細に文書化

### v1.1.0 (2024-02-05)

- 📚 **章文書の再構築**：章ルールを5つの独立ファイルに分割
  - chapter-1-introduction.md：緒論の詳細ガイド
  - chapter-2-theory.md：理論基礎の詳細ガイド
  - chapter-3-analysis.md：現状と問題分析の詳細ガイド
  - chapter-4-solutions.md：対策提言の詳細ガイド
  - chapter-5-conclusion.md：結論の詳細ガイド
  - format-standards.md：形式規範の独立文書
- 🎓 **MBA規範の詳細化**：MBA論文の核心原則の新規章を追加
- 🎯 **実践重視の強化**：データ支援、理論適用、具体的事例をさらに重視
- 📝 **形式規範の改善**：形式標準を独立して整理し、中国語・英語混在、図表、引用などをカバー
- 🏗️ **プロジェクト構造の最適化**：より明確なファイル構成と索引

### v1.0.0 (2024-02-04)

- ✨ 初期バージョンリリース
- 🎯 多次元的AI特徴検出をサポート
- 📚 章別特定ルールを追加
- 🔧 自動修正機能を実装
- 🎓 Claude Skillを統合

---

## 📄 ライセンス

本プロジェクトは[MITライセンス](LICENSE)を採用しています - 詳細はLICENSEファイルをご参照ください

---

## 🙏 謝辞

- Claude Codeが提供するSkillフレームワークに感謝
- Kimi CLIが提供するAgent並列実行ツールに感謝
- フィードバックと提案を提供してくださったすべてのユーザーに感謝
- **特別に[Haimbeau1o/thesis-optimizer](https://github.com/Haimbeau1o/thesis-optimizer)プロジェクトに感謝**。本プロジェクトの三次元協同最適化戦略（AI検出率低減、重複率低減、学術的推敲向上）は、同プロジェクトの優れた設計を参考にしています
- **書き換え戦略参考：[cangtianhuang/humanizer-academic-zh](https://github.com/cangtianhuang/humanizer-academic-zh)**。本プロジェクトは「検出+定量位置特定」の経路を取り、当該プロジェクトは「書き換え+推敲」の経路を取る。同プロジェクトの25類セマンティックパターン（表現/言語/スタイル/フィラー/コミュニケーション残滓の5大類に分類）のうち「パターン21-25」を本プロジェクトSKILL.mdの補足参考節で相互参照

---

## 📮 連絡先

- GitHub Issues: [https://github.com/stephenlzc/humanize-mba-text-skill/issues](https://github.com/stephenlzc/humanize-mba-text-skill/issues)
- 作者：stephenlzc

---

## 🔗 関連プロジェクト

- [thesis-optimizer](https://github.com/Haimbeau1o/thesis-optimizer) - 学術論文インテリジェント最適化システム（コンピュータ深層学習方向）
- [cangtianhuang/humanizer-academic-zh](https://github.com/cangtianhuang/humanizer-academic-zh) - Humanizer 中文学術版：本プロジェクトの「検出＋定量位置特定」経路を補完する「書き換え＋推敲」Skill。25類セマンティックパターンは表現/言語/スタイル/フィラー/コミュニケーション残滓の5大類に分類。本プロジェクトv1.3.0でパターン21〜25を漸進ロードTOML（`references/rules/categories/*.toml`）に統合（`filler_phrases`強化、`chatbot_conversation_residue`強化、`sycophantic_praise`新規追加など）。

---

<p align="center">
  このプロジェクトが役に立ったら、⭐ Starをお願いします！
</p>
