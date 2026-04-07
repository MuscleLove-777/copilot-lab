"""Copilot活用ラボ - ブログ固有設定"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

BLOG_NAME = "Copilot活用ラボ"
BLOG_DESCRIPTION = (
    "GitHub Copilot・Microsoft 365 Copilotの使い方・最新機能・料金比較を毎日更新。"
    "コーディング支援からOffice活用まで、Copilotを完全に使いこなすための日本語ガイド。"
)
BLOG_URL = "https://musclelove-777.github.io/copilot-lab"
BLOG_TAGLINE = "GitHub Copilot × M365 Copilot — AI副操縦士を使いこなせ"
BLOG_LANGUAGE = "ja"

GITHUB_REPO = "MuscleLove-777/copilot-lab"
GITHUB_BRANCH = "gh-pages"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

OUTPUT_DIR = BASE_DIR / "output"
ARTICLES_DIR = OUTPUT_DIR / "articles"
SITE_DIR = OUTPUT_DIR / "site"
TOPICS_DIR = OUTPUT_DIR / "topics"

TARGET_CATEGORIES = [
    "GitHub Copilot 使い方",
    "M365 Copilot 使い方",
    "Copilot 料金・プラン",
    "Copilot vs Cursor",
    "Copilot 最新ニュース",
    "Copilot × Excel",
    "Copilot × Word・PPT",
    "Copilot 活用事例",
]

THEME = {
    "primary": "#0078d4",
    "accent": "#50e6ff",
    "gradient_start": "#0078d4",
    "gradient_end": "#005a9e",
    "dark_bg": "#0d1117",
    "dark_surface": "#161b22",
    "light_bg": "#f3f8ff",
    "light_surface": "#ffffff",
}

MAX_ARTICLE_LENGTH = 4000
ARTICLES_PER_DAY = 2
SCHEDULE_HOURS = [8, 19]

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.5-flash"

ENABLE_SEO_OPTIMIZATION = True
MIN_SEO_SCORE = 75
MIN_KEYWORD_DENSITY = 1.0
MAX_KEYWORD_DENSITY = 3.0
META_DESCRIPTION_LENGTH = 120
ENABLE_INTERNAL_LINKS = True

AFFILIATE_LINKS = {
    "開発ツール": [
        {"service": "GitHub Copilot", "url": "https://github.com/features/copilot", "description": "GitHub Copilotに登録する"},
        {"service": "VS Code", "url": "https://code.visualstudio.com", "description": "VS Codeをダウンロード"},
    ],
    "Microsoft 365": [
        {"service": "Microsoft 365", "url": "https://www.microsoft.com/microsoft-365", "description": "Microsoft 365プランを見る"},
    ],
    "オンライン講座": [
        {"service": "Udemy", "url": "https://www.udemy.com", "description": "UdemyでCopilot講座を探す"},
    ],
    "書籍": [
        {"service": "Amazon", "url": "https://www.amazon.co.jp", "description": "AmazonでAI関連書籍を探す"},
        {"service": "楽天ブックス", "url": "https://www.rakuten.co.jp", "description": "楽天でAI関連書籍を探す"},
    ],
}
AFFILIATE_TAG = "musclelove07-22"

ADSENSE_CLIENT_ID = os.environ.get("ADSENSE_CLIENT_ID", "")
ADSENSE_ENABLED = bool(ADSENSE_CLIENT_ID)

DASHBOARD_PORT = 8086

# Google Analytics (GA4)
GOOGLE_ANALYTICS_ID = "G-HJLCFVY5TF"

# Google Search Console 認証ファイル
SITE_VERIFICATION_FILES = {
    "googlea31edabcec879415.html": "google-site-verification: googlea31edabcec879415.html",
}
