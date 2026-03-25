"""
Post immediately from the command line.

Usage:
    python post_now.py --image uploads/photo.jpg --caption "Hello world! #python"
    python post_now.py --video uploads/clip.mp4 --caption "Watch this!"
    python post_now.py --album uploads/1.jpg uploads/2.jpg --caption "Check these out!"
"""

import argparse
import logging
from pathlib import Path

from bot import InstagramBot
from config import load_config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def main():
    parser = argparse.ArgumentParser(description="Post to Instagram immediately.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--image", help="Path to a single image to post")
    group.add_argument("--video", help="Path to a video/reel to post")
    group.add_argument("--album", nargs="+", help="Paths to images for a carousel post")
    parser.add_argument("--caption", default="", help="Post caption")
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
        media_id = bot.post_photo(args.image, args.caption)
        print(f"Posted photo. Media ID: {media_id}")
    elif args.video:
        media_id = bot.post_video(args.video, args.caption)
        print(f"Posted video. Media ID: {media_id}")
    elif args.album:
        media_id = bot.post_album(args.album, args.caption)
        print(f"Posted album. Media ID: {media_id}")


if __name__ == "__main__":
    main()
