"""Copilot活用ラボ - SEO最適化ラッパー

blog_engineのSEOOptimizerを呼び出す薄いラッパー。
Copilot固有のFAQ構造化データ生成、JSON-LD、BreadcrumbListを追加。
"""

import sys
import os
import json
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from blog_engine.seo_optimizer import SEOOptimizer as BaseSEOOptimizer  # noqa: E402


class SEOOptimizer(BaseSEOOptimizer):
    """Copilot特化のSEO最適化クラス"""

    def __init__(self, config):
        super().__init__(config)
        self.blog_url = getattr(config, "BLOG_URL", "")
        self.blog_name = getattr(config, "BLOG_NAME", "")

    def generate_json_ld(self, article: dict) -> str:
        """記事用のJSON-LD構造化データを生成する"""
        schema = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": article.get("title", ""),
            "description": article.get("meta_description", ""),
            "author": {
                "@type": "Organization",
                "name": self.blog_name,
            },
            "publisher": {
                "@type": "Organization",
                "name": self.blog_name,
            },
            "datePublished": article.get("date", article.get("generated_at", "")),
            "dateModified": article.get("date", article.get("generated_at", "")),
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": f"{self.blog_url}/articles/{article.get('slug', '')}.html",
            },
            "keywords": ", ".join(article.get("tags", [])),
        }
        return f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'

    def generate_faq_schema(self, article: dict) -> str:
        """FAQ構造化データ（FAQPage）を生成する"""
        faq_items = article.get("faq", [])
        if not faq_items:
            # contentからFAQを抽出
            faq_items = self._extract_faq_from_content(article.get("content", ""))

        if not faq_items:
            return ""

        schema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": item.get("question", ""),
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": item.get("answer", ""),
                    },
                }
                for item in faq_items
            ],
        }
        return f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'

    def generate_breadcrumb_schema(self, article: dict) -> str:
        """BreadcrumbList構造化データを生成する"""
        category = article.get("category", "未分類")
        title = article.get("title", "")

        schema = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "ホーム",
                    "item": self.blog_url,
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": category,
                    "item": f"{self.blog_url}/category/{category}",
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": title,
                },
            ],
        }
        return f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'

    def _extract_faq_from_content(self, content: str) -> list:
        """Markdownコンテンツからq/aを抽出する"""
        faq_items = []
        # パターン: ### Q1: 質問 / A1: 回答
        q_pattern = re.compile(r"###\s*Q\d+[:：]\s*(.+)")
        a_pattern = re.compile(r"A\d+[:：]\s*(.+)")

        lines = content.split("\n")
        current_q = None
        for line in lines:
            q_match = q_pattern.match(line.strip())
            if q_match:
                current_q = q_match.group(1).strip()
                continue
            if current_q:
                a_match = a_pattern.match(line.strip())
                if a_match:
                    faq_items.append({
                        "question": current_q,
                        "answer": a_match.group(1).strip(),
                    })
                    current_q = None

        return faq_items


__all__ = ["SEOOptimizer"]
