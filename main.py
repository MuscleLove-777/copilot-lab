#!/usr/bin/env python3
"""Copilot活用ラボ - CLIエントリポイント

blog_engineのmain.pyへ処理を委譲する。

使い方:
    python main.py generate --keyword "Copilot 使い方" --category "GitHub Copilot 使い方"
    python main.py build
    python main.py deploy
    python main.py schedule
    python main.py dashboard
"""

import sys
import os
from llm import get_llm_client

# blog_engineへのパスを追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# config.pyのパスを引数に挿入
config_path = os.path.join(os.path.dirname(__file__), 'config.py')

if __name__ == "__main__":
    # --config 引数を自動挿入
    if "--config" not in sys.argv:
        sys.argv.insert(1, "--config")
        sys.argv.insert(2, config_path)

    from blog_engine.main import main
    main()
