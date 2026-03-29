"""Copilot活用ラボ - トピック収集モジュール

topics.jsonからトピックを読み込み、優先度に基づいて次のトピックを選定する。
既に記事化済みのトピックはスキップする。
"""

import json
import logging
import random
from pathlib import Path

logger = logging.getLogger(__name__)


class TopicCollector:
    """トピックの収集と管理を行うクラス"""

    def __init__(self, config):
        self.config = config
        self.base_dir = Path(config.BASE_DIR)
        self.topics_file = self.base_dir / "topics.json"
        self.articles_dir = self.base_dir / "output" / "articles"

    def load_topics(self) -> dict:
        """topics.jsonからトピック一覧を読み込む"""
        if not self.topics_file.exists():
            logger.warning("topics.json が見つかりません: %s", self.topics_file)
            return {}

        with open(self.topics_file, "r", encoding="utf-8") as f:
            topics = json.load(f)

        logger.info("トピックを読み込みました: %d カテゴリ", len(topics))
        return topics

    def get_published_keywords(self) -> set:
        """既に記事化済みのキーワード一覧を取得する"""
        published = set()
        if not self.articles_dir.exists():
            return published

        for filepath in self.articles_dir.glob("*.json"):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    article = json.load(f)
                keyword = article.get("keyword", "")
                if keyword:
                    published.add(keyword)
            except (json.JSONDecodeError, IOError):
                continue

        logger.info("記事化済みキーワード: %d件", len(published))
        return published

    def select_next_topic(self) -> tuple:
        """次に記事化すべきトピックを選定する

        Returns:
            tuple: (category, keyword) のタプル。トピックがない場合は (None, None)
        """
        topics = self.load_topics()
        if not topics:
            return None, None

        published = self.get_published_keywords()

        # 優先度順にソートして未記事化のトピックを探す
        candidates_high = []
        candidates_medium = []
        candidates_low = []

        for category, topic_list in topics.items():
            for topic in topic_list:
                keyword = topic.get("keyword", "")
                if keyword and keyword not in published:
                    priority = topic.get("priority", "medium")
                    entry = (category, keyword)
                    if priority == "high":
                        candidates_high.append(entry)
                    elif priority == "medium":
                        candidates_medium.append(entry)
                    else:
                        candidates_low.append(entry)

        # 優先度の高いものからランダムに選択
        for candidates in [candidates_high, candidates_medium, candidates_low]:
            if candidates:
                selected = random.choice(candidates)
                logger.info(
                    "次のトピックを選定: カテゴリ=%s, キーワード=%s",
                    selected[0], selected[1],
                )
                return selected

        logger.info("未記事化のトピックがありません。AIでキーワードを生成します。")
        return None, None

    def get_topic_stats(self) -> dict:
        """トピックの統計情報を取得する"""
        topics = self.load_topics()
        published = self.get_published_keywords()

        total = 0
        done = 0
        by_category = {}

        for category, topic_list in topics.items():
            cat_total = len(topic_list)
            cat_done = sum(
                1 for t in topic_list
                if t.get("keyword", "") in published
            )
            total += cat_total
            done += cat_done
            by_category[category] = {
                "total": cat_total,
                "done": cat_done,
                "remaining": cat_total - cat_done,
            }

        return {
            "total_topics": total,
            "published": done,
            "remaining": total - done,
            "completion_rate": round(done / total * 100, 1) if total > 0 else 0,
            "by_category": by_category,
        }
