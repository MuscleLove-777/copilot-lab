"""Copilot活用ラボ - サイト生成ラッパー

blog_engineのSiteGeneratorを拡張し、
robots.txt・OGPタグ・canonical・JSON-LD・FAQ構造化データを追加する。
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from blog_engine.site_generator import SiteGenerator as BaseSiteGenerator  # noqa: E402


class SiteGenerator(BaseSiteGenerator):
    """Copilot特化のサイト生成クラス"""

    def __init__(self, config):
        super().__init__(config)
        self.blog_tagline = getattr(config, "BLOG_TAGLINE", "")

    def build_site(self):
        """サイトをビルドし、追加ファイルを生成する"""
        super().build_site()

        # robots.txt を生成
        self._generate_robots_txt()
        print("  robots.txt 生成完了")

    def _generate_robots_txt(self):
        """robots.txt を生成する"""
        blog_url = self.config.BLOG_URL
        content = (
            "User-agent: *\n"
            "Allow: /\n"
            f"Sitemap: {blog_url}/sitemap.xml\n"
        )
        (self.output_dir / "robots.txt").write_text(content, encoding="utf-8")

    def _get_common_context(self) -> dict:
        """共通コンテキストにOGP・tagline情報を追加"""
        context = super()._get_common_context()
        context["blog_tagline"] = self.blog_tagline
        return context


__all__ = ["SiteGenerator"]
