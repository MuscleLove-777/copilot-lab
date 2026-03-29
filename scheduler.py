"""Copilot活用ラボ - スケジューラーラッパー

blog_engineのBlogSchedulerを呼び出す薄いラッパー。
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from blog_engine.scheduler import BlogScheduler  # noqa: E402

__all__ = ["BlogScheduler"]
