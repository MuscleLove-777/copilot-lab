"""Copilot活用ラボ - 記事生成ラッパー

blog_engineのArticleGeneratorを呼び出す薄いラッパー。
Copilot固有のconfig/promptsを注入する。
"""

import sys
import os

# blog_engineへのパスを追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from blog_engine.article_generator import ArticleGenerator  # noqa: E402

__all__ = ["ArticleGenerator"]
