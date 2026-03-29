"""Copilot活用ラボ - デプロイヤーラッパー

blog_engineのGitHubPagesDeployerを呼び出す薄いラッパー。
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from blog_engine.deployer import GitHubPagesDeployer  # noqa: E402

__all__ = ["GitHubPagesDeployer"]
