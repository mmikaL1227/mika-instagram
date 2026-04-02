"""
Post a story to Instagram immediately.

Usage:
    python post_story.py --image uploads/story.jpg
    python post_story.py --video uploads/story.mp4
"""

import argparse
import logging
from bot import InstagramBot
from config import load_config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def main():
    parser = argparse.ArgumentParser(description="Post an Instagram story.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--image", help="Path to a story image (JPG/PNG, ideally 1080x1920)")
    group.add_argument("--video", help="Path to a story video (MP4, max 15s)")
    args = parser.parse_args()

    cfg = load_config()
    bot = InstagramBot(
        username=cfg["username"],
        password=cfg["password"],
        session_file=cfg["session_file"],
        totp_seed=cfg.get("totp_seed", ""),
    )
    bot.login()

    if args.image:
        media_id = bot.post_story_photo(args.image)
        print(f"Story posted! Media ID: {media_id}")
    elif args.video:
        media_id = bot.post_story_video(args.video)
        print(f"Story posted! Media ID: {media_id}")


if __name__ == "__main__":
    main()
