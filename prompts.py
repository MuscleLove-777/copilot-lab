"""Copilot活用ラボ - プロンプト定義

GitHub Copilot / Microsoft 365 Copilot 特化ブログ用のプロンプトを一元管理する。
"""

# ペルソナ定義
PERSONA = (
    "あなたはMicrosoft Copilotの日本語エキスパートです。"
    "GitHub CopilotとMicrosoft 365 Copilotの両方を毎日使い込んでおり、"
    "最新のアップデート情報にも精通しています。"
    "エンジニアだけでなくビジネスユーザーにもわかりやすく解説できるのが強みです。"
)

# 記事フォーマット指示
ARTICLE_FORMAT = """
## この記事でわかること
- ポイント1
- ポイント2
- ポイント3

## 結論
（最も重要な結論を先に述べる）

## 本題
（メインコンテンツ。H2/H3で構造化）

## 手順・使い方
（具体的なステップバイステップ。スクリーンショットの代わりにテキストで丁寧に）

## 比較・メリット・デメリット
（競合ツールや旧バージョンとの比較表）

## よくある質問（FAQ）
### Q1: ...
A1: ...
### Q2: ...
A2: ...
### Q3: ...
A3: ...

## まとめ
（要点の振り返りと次のアクション）
"""

# カテゴリ別プロンプト追加指示
CATEGORY_PROMPTS = {
    "GitHub Copilot 使い方": (
        "VS Code・JetBrains・Neovimでの統合方法、インストール手順、初期設定を詳しく解説してください。"
        "ターゲットキーワード例: 「GitHub Copilot 使い方」「Copilot インストール」「Copilot VS Code」"
    ),
    "M365 Copilot 使い方": (
        "Word・Excel・PowerPoint・Teams・Outlookでの活用方法を具体的に解説してください。"
        "ターゲットキーワード例: 「M365 Copilot 使い方」「Copilot Teams」「Copilot Outlook」"
    ),
    "Copilot 料金・プラン": (
        "GitHub Copilot Free/Pro/Business/Enterprise、Microsoft 365 Copilotの料金体系を"
        "個人・中小企業・大企業向けに比較してください。"
        "ターゲットキーワード例: 「Copilot 料金」「Copilot 無料」「Copilot Business 料金」"
    ),
    "Copilot vs Cursor": (
        "GitHub CopilotとCursor、Windsurf、Cline等のAIコーディングツールを"
        "機能・料金・使い勝手の観点で徹底比較してください。"
        "ターゲットキーワード例: 「Copilot Cursor 比較」「Copilot Windsurf 比較」「AIコーディング 比較」"
    ),
    "Copilot 最新ニュース": (
        "Copilotに関する最新のアップデート情報やニュースを解説してください。"
        "データ学習問題、新機能リリース、Jira/Slack統合、Copilot Coworkなど。"
        "ターゲットキーワード例: 「Copilot 最新」「Copilot アップデート」「Copilot ニュース」"
    ),
    "Copilot × Excel": (
        "ExcelでのCopilot活用法を解説してください。"
        "関数生成、データ分析、ピボットテーブル、グラフ作成など具体的なユースケースを紹介。"
        "ターゲットキーワード例: 「Copilot Excel 使い方」「Excel AI 関数」「Copilot データ分析」"
    ),
    "Copilot × Word・PPT": (
        "WordやPowerPointでのCopilot活用法を解説してください。"
        "文書作成、プレゼン自動生成、校正、要約、テンプレート活用など。"
        "ターゲットキーワード例: 「Copilot Word」「Copilot PowerPoint」「Copilot プレゼン作成」"
    ),
    "Copilot 活用事例": (
        "実際のビジネスシーンでのCopilot活用事例を紹介してください。"
        "業種別、職種別、チーム規模別など多角的な視点で解説。"
        "ターゲットキーワード例: 「Copilot 活用事例」「Copilot 導入事例」「Copilot ビジネス活用」"
    ),
}

# ニュースソース
NEWS_SOURCES = [
    "GitHub Blog (https://github.blog)",
    "Microsoft AI Blog (https://blogs.microsoft.com/ai)",
    "Microsoft 365 Blog (https://www.microsoft.com/en-us/microsoft-365/blog)",
]

# FAQ構造化データ有効化
FAQ_SCHEMA_ENABLED = True

# キーワード選定時の追加プロンプト
KEYWORD_PROMPT_EXTRA = (
    "Microsoft CopilotはGitHub Copilot（コーディング支援）と"
    "Microsoft 365 Copilot（Office・Teams支援）の2軸があります。"
    "両方のキーワードをバランスよく選定してください。"
    "検索ボリュームの高いキーワード（「Copilot 使い方」「Copilot 料金」「Copilot 無料」等）を優先し、"
    "ロングテールキーワードも混ぜてください。"
)


def build_keyword_prompt(config):
    """キーワード選定プロンプトを構築する"""
    categories_text = "\n".join(f"- {cat}" for cat in config.TARGET_CATEGORIES)
    return (
        f"{PERSONA}\n\n"
        f"「{config.BLOG_NAME}」用のキーワードを選定してください。\n\n"
        f"{KEYWORD_PROMPT_EXTRA}\n\n"
        "以下のカテゴリから1つ選び、そのカテゴリで今注目されている"
        "Copilot関連の検索キーワードを1つ提案してください。\n\n"
        f"カテゴリ一覧:\n{categories_text}\n\n"
        "以下の形式でJSON形式のみで回答してください（説明不要）:\n"
        '{"category": "カテゴリ名", "keyword": "キーワード"}'
    )


def build_article_prompt(keyword, category, config):
    """Copilot特化の記事生成プロンプトを構築する"""
    category_extra = CATEGORY_PROMPTS.get(category, "")
    news_sources_text = "\n".join(f"- {src}" for src in NEWS_SOURCES)

    return f"""{PERSONA}

以下のキーワードに関する、SEO最適化された高品質なブログ記事を生成してください。

【基本条件】
- ブログ名: {config.BLOG_NAME}
- キーワード: {keyword}
- カテゴリ: {category}
- 言語: 日本語
- 文字数: {config.MAX_ARTICLE_LENGTH}文字程度

【カテゴリ固有の指示】
{category_extra}

【記事フォーマット（必ず以下の構成で書くこと）】
{ARTICLE_FORMAT}

【SEO要件】
1. タイトルにキーワード「{keyword}」を必ず含めること
2. タイトルは32文字以内で魅力的に（数字を入れると効果的）
3. H2、H3の見出し構造を適切に使用すること
4. キーワード密度は{config.MIN_KEYWORD_DENSITY}%〜{config.MAX_KEYWORD_DENSITY}%を目安に
5. メタディスクリプションは{config.META_DESCRIPTION_LENGTH}文字以内
6. 内部リンクのプレースホルダーを2〜3箇所に配置（{{{{internal_link:関連トピック}}}}の形式）

【FAQ構造化データ】
- 必ず3つ以上のFAQを含めること（JSON-LD FAQPage対応のため）
- FAQの各質問はユーザーが実際に検索しそうな自然な文にすること

【参考ニュースソース】
{news_sources_text}

【出力形式】
以下のJSON形式で出力してください。JSONブロック以外のテキストは出力しないでください。

```json
{{
  "title": "SEO最適化されたタイトル",
  "content": "# タイトル\\n\\n本文（Markdown形式）...",
  "meta_description": "120文字以内のメタディスクリプション",
  "tags": ["タグ1", "タグ2", "タグ3", "タグ4", "タグ5"],
  "slug": "url-friendly-slug",
  "faq": [
    {{"question": "質問1", "answer": "回答1"}},
    {{"question": "質問2", "answer": "回答2"}},
    {{"question": "質問3", "answer": "回答3"}}
  ]
}}
```

【注意事項】
- content内のMarkdownは適切にエスケープしてJSON文字列として有効にすること
- tagsは5個ちょうど生成すること
- slugは半角英数字とハイフンのみ使用すること
- faqは必ず3つ以上含めること
- 読者にとって実用的で具体的な内容を心がけること
- 最新情報（2025年〜2026年）を意識した内容にすること"""
