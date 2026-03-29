#!/usr/bin/env python3
"""Copilot活用ラボ - GitHub Actions用一括実行スクリプト

キーワード選定 → 記事生成 → SEO最適化 → アフィリエイト挿入 → サイトビルド
を一括で実行する。topics.jsonのトピックを優先的に使用する。
"""

import sys
import os
import json
import logging
from datetime import datetime
from pathlib import Path

# blog_engineへのパスを追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def run(config, prompts=None):
    """メイン処理: トピック選定 → 記事生成 → サイトビルド"""
    logger.info("=== %s 自動生成開始 ===", config.BLOG_NAME)
    start_time = datetime.now()

    # ステップ1: トピック/キーワード選定
    logger.info("ステップ1: トピック/キーワード選定")
    category = None
    keyword = None

    # まずtopics.jsonから未記事化トピックを探す
    try:
        from topic_collector import TopicCollector
        collector = TopicCollector(config)
        category, keyword = collector.select_next_topic()

        if category and keyword:
            logger.info("topics.jsonから選定 - カテゴリ: %s, キーワード: %s", category, keyword)
        else:
            logger.info("topics.jsonに未記事化トピックなし。AIで選定します。")
    except Exception as e:
        logger.warning("TopicCollector失敗: %s。AIで選定します。", e)

    # topics.jsonに該当がなければAIで選定
    if not category or not keyword:
        try:
            from google import genai

            if not config.GEMINI_API_KEY:
                logger.error("GEMINI_API_KEY が設定されていません")
                sys.exit(1)

            client = genai.Client(api_key=config.GEMINI_API_KEY)

            if prompts and hasattr(prompts, "build_keyword_prompt"):
                prompt = prompts.build_keyword_prompt(config)
            else:
                categories_text = "\n".join(f"- {cat}" for cat in config.TARGET_CATEGORIES)
                prompt = (
                    f"{config.BLOG_NAME}用のキーワードを選定してください。\n\n"
                    "以下のカテゴリから1つ選び、そのカテゴリで今注目されている"
                    "トピック・キーワードを1つ提案してください。\n\n"
                    f"カテゴリ一覧:\n{categories_text}\n\n"
                    "検索ボリュームの高いキーワードを意識してください。\n\n"
                    "以下の形式でJSON形式のみで回答してください（説明不要）:\n"
                    '{"category": "カテゴリ名", "keyword": "キーワード"}'
                )

            response = client.models.generate_content(
                model=config.GEMINI_MODEL, contents=prompt
            )
            response_text = response.text.strip()

            if "```" in response_text:
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()

            data = json.loads(response_text)
            category = data["category"]
            keyword = data["keyword"]
            logger.info("AI選定結果 - カテゴリ: %s, キーワード: %s", category, keyword)

        except Exception as e:
            logger.error("キーワード選定に失敗: %s", e)
            sys.exit(1)

    # ステップ2: 記事生成
    logger.info("ステップ2: 記事生成")
    try:
        from blog_engine.article_generator import ArticleGenerator

        generator = ArticleGenerator(config)
        article = generator.generate_article(
            keyword=keyword, category=category, prompts=prompts
        )
        logger.info("記事生成完了: %s", article.get("title", "不明"))

    except Exception as e:
        logger.error("記事生成に失敗: %s", e)
        sys.exit(1)

    # ステップ2.5: SEO最適化チェック
    logger.info("ステップ2.5: SEO最適化チェック")
    try:
        from seo_optimizer import SEOOptimizer
        optimizer = SEOOptimizer(config)
        seo_result = optimizer.check_seo_score(article)
        logger.info("SEOスコア: %d/100", seo_result.get("total_score", 0))

        # JSON-LD・FAQ構造化データを記事に付与
        article["json_ld"] = optimizer.generate_json_ld(article)
        article["faq_schema"] = optimizer.generate_faq_schema(article)
        article["breadcrumb_schema"] = optimizer.generate_breadcrumb_schema(article)
        logger.info("構造化データ（JSON-LD, FAQ, Breadcrumb）を生成")

    except Exception as e:
        logger.warning("SEO最適化をスキップ: %s", e)
        # フォールバック: blog_engineのSEOOptimizer
        try:
            from blog_engine.seo_optimizer import SEOOptimizer as FallbackSEO
            seo_result = FallbackSEO(config).check_seo_score(article)
            logger.info("SEOスコア（フォールバック）: %d/100", seo_result.get("total_score", 0))
        except Exception:
            pass

    # ステップ3: アフィリエイトリンク挿入
    logger.info("ステップ3: アフィリエイトリンク挿入")
    try:
        from blog_engine.affiliate import AffiliateManager
        affiliate_mgr = AffiliateManager(config)
        article = affiliate_mgr.insert_affiliate_links(article)
        logger.info("アフィリエイトリンク: %d件挿入", article.get("affiliate_count", 0))
    except Exception as aff_err:
        logger.warning("アフィリエイトリンク挿入をスキップ: %s", aff_err)

    # ステップ4: 記事JSONを更新保存
    try:
        file_path = article.get("file_path")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(article, f, ensure_ascii=False, indent=2)
            logger.info("記事JSONを更新保存: %s", file_path)
    except Exception as e:
        logger.warning("記事JSON更新に失敗: %s", e)

    # ステップ5: サイトビルド
    logger.info("ステップ5: サイトビルド")
    try:
        from site_generator import SiteGenerator
        site_gen = SiteGenerator(config)
        site_gen.build_site()
        logger.info("サイトビルド完了")
    except Exception as e:
        logger.warning("拡張SiteGenerator失敗、フォールバック: %s", e)
        try:
            from blog_engine.site_generator import SiteGenerator as FallbackSiteGen
            site_gen = FallbackSiteGen(config)
            site_gen.build_site()
            logger.info("サイトビルド完了（フォールバック）")
        except Exception as e2:
            logger.error("サイトビルドに失敗: %s", e2)
            sys.exit(1)

    # 完了
    duration = (datetime.now() - start_time).total_seconds()
    logger.info("=== 自動生成完了（%.1f秒） ===", duration)
    logger.info("  カテゴリ: %s", category)
    logger.info("  キーワード: %s", keyword)
    logger.info("  タイトル: %s", article.get("title", "不明"))
    seo_score = seo_result.get("total_score", 0) if "seo_result" in dir() else 0
    logger.info("  SEOスコア: %d/100", seo_score)


if __name__ == "__main__":
    import config
    import prompts
    run(config, prompts)
