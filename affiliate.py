"""Copilot活用ラボ - アフィリエイトリンクラッパー

blog_engineのAffiliateManagerを呼び出す薄いラッパー。
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from blog_engine.affiliate import AffiliateManager  # noqa: E402

__all__ = ["AffiliateManager"]
