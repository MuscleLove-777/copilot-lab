"""Copilot活用ラボ - ダッシュボードラッパー

blog_engineのdashboard.create_appを呼び出す薄いラッパー。
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from blog_engine.dashboard import create_app  # noqa: E402

__all__ = ["create_app"]
