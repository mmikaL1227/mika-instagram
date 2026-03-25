"""
Scheduled posting from a JSON queue file.

Usage:
    python scheduler.py --posts posts.json
"""

import json
import logging
import time
import argparse
from datetime import datetime
from pathlib import Path

import schedule

from bot import InstagramBot
from config import load_config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/scheduler.log"),
    ],
)
logger = logging.getLogger(__name__)


def load_posts(posts_file: str) -> list[dict]:
    path = Path(posts_file)
    if not path.exists():
        raise FileNotFoundError(f"Posts file not found: {posts_file}")
    with open(path) as f:
        return json.load(f)


def schedule_posts(bot: InstagramBot, posts: list[dict]):
    now = datetime.now()

    for post in posts:
        scheduled_at = datetime.strptime(post["schedule"], "%Y-%m-%d %H:%M")
        if scheduled_at <= now:
            logger.warning(f"Skipping past-due post scheduled for {scheduled_at}: {post.get('image')}")
            continue

        delay_seconds = (scheduled_at - now).total_seconds()

        def make_job(p, delay):
            def job():
                time.sleep(delay)
                try:
                    image = p.get("image")
                    caption = p.get("caption", "")
                    if image:
                        bot.post_photo(image, caption)
                    else:
                        logger.error(f"Post has no image path: {p}")
                except Exception as e:
                    logger.error(f"Failed to post {p.get('image')}: {e}")

            return job

        schedule.every().second.do(make_job(post, delay_seconds)).tag("once")
        logger.info(f"Scheduled post at {scheduled_at}: {post.get('image')}")


def run_scheduler(posts_file: str):
    cfg = load_config()
    bot = InstagramBot(
        username=cfg["username"],
        password=cfg["password"],
        session_file=cfg["session_file"],
        totp_seed=cfg.get("totp_seed", ""),
    )
    bot.login()

    posts = load_posts(posts_file)
    schedule_posts(bot, posts)

    logger.info("Scheduler running. Press Ctrl+C to stop.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Scheduler stopped.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Schedule Instagram posts from a JSON file.")
    parser.add_argument("--posts", default="posts.json", help="Path to the posts JSON file")
    args = parser.parse_args()

    Path("logs").mkdir(exist_ok=True)
    run_scheduler(args.posts)
