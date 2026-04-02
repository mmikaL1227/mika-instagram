"""
Scheduled story posting from a JSON queue file.

Usage:
    python scheduler.py --posts stories.json

Queue file format:
    [
      { "image": "uploads/story1.jpg", "schedule": "2026-04-03 09:00" },
      { "video": "uploads/story2.mp4", "schedule": "2026-04-03 20:00" }
    ]
"""

import json
import logging
import time
import argparse
from datetime import datetime
from pathlib import Path

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
        raise FileNotFoundError(f"Queue file not found: {posts_file}")
    with open(path) as f:
        return json.load(f)


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
    now = datetime.now()
    queue = []

    for post in posts:
        scheduled_at = datetime.strptime(post["schedule"], "%Y-%m-%d %H:%M")
        if scheduled_at <= now:
            logger.warning(f"Skipping past-due story scheduled for {scheduled_at}")
            continue
        queue.append((scheduled_at, post))

    queue.sort(key=lambda x: x[0])
    logger.info(f"{len(queue)} stories queued. Press Ctrl+C to stop.")

    try:
        while queue:
            scheduled_at, post = queue[0]
            wait = (scheduled_at - datetime.now()).total_seconds()
            if wait > 0:
                logger.info(f"Next story at {scheduled_at} (in {int(wait)}s)")
                time.sleep(min(wait, 30))  # wake up every 30s to re-check
                continue

            queue.pop(0)
            try:
                if "image" in post:
                    media_id = bot.post_story_photo(post["image"])
                    logger.info(f"Story posted (photo): {media_id}")
                elif "video" in post:
                    media_id = bot.post_story_video(post["video"])
                    logger.info(f"Story posted (video): {media_id}")
                else:
                    logger.error(f"Post entry has no 'image' or 'video' key: {post}")
            except Exception as e:
                logger.error(f"Failed to post story: {e}")

        logger.info("All stories posted. Scheduler done.")
    except KeyboardInterrupt:
        logger.info("Scheduler stopped.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Schedule Instagram stories from a JSON queue file.")
    parser.add_argument("--posts", default="stories.json", help="Path to the stories JSON file")
    args = parser.parse_args()

    Path("logs").mkdir(exist_ok=True)
    run_scheduler(args.posts)
