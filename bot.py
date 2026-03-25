"""
Instagram automation bot using instagrapi.
Handles login, session persistence, and posting images.
"""

import os
import json
import logging
from pathlib import Path
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, TwoFactorRequired

logger = logging.getLogger(__name__)


class InstagramBot:
    def __init__(self, username: str, password: str, session_file: str = "sessions/session.json", totp_seed: str = ""):
        self.username = username
        self.password = password
        self.session_file = Path(session_file)
        self.totp_seed = totp_seed
        self.client = Client()
        self.client.delay_range = [2, 5]  # polite delay between requests

    def login(self):
        """Login using saved session or fresh credentials."""
        if self.session_file.exists():
            try:
                self.client.load_settings(self.session_file)
                self.client.login(self.username, self.password)
                self.client.get_timeline_feed()  # verify session is valid
                logger.info("Logged in via saved session.")
                return
            except LoginRequired:
                logger.warning("Saved session expired, re-logging in.")
                self.session_file.unlink(missing_ok=True)

        try:
            self.client.login(self.username, self.password, verification_code=self.totp_seed)
        except TwoFactorRequired:
            if not self.totp_seed:
                raise RuntimeError("2FA is required. Set INSTAGRAM_TOTP_SEED in your .env file.")
            self.client.login(self.username, self.password, verification_code=self.totp_seed)

        self.session_file.parent.mkdir(parents=True, exist_ok=True)
        self.client.dump_settings(self.session_file)
        logger.info("Logged in with credentials and session saved.")

    def post_photo(self, image_path: str, caption: str = "") -> str:
        """Upload a single photo post. Returns the media ID."""
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        media = self.client.photo_upload(path, caption=caption)
        logger.info(f"Photo posted: {media.pk} — {caption[:40]!r}")
        return media.pk

    def post_video(self, video_path: str, caption: str = "") -> str:
        """Upload a video post (Reel). Returns the media ID."""
        path = Path(video_path)
        if not path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")

        media = self.client.video_upload(path, caption=caption)
        logger.info(f"Video posted: {media.pk} — {caption[:40]!r}")
        return media.pk

    def post_album(self, image_paths: list[str], caption: str = "") -> str:
        """Upload a carousel (album) post. Returns the media ID."""
        paths = [Path(p) for p in image_paths]
        for p in paths:
            if not p.exists():
                raise FileNotFoundError(f"Image not found: {p}")

        media = self.client.album_upload(paths, caption=caption)
        logger.info(f"Album posted: {media.pk} with {len(paths)} images.")
        return media.pk

    def delete_post(self, media_id: str):
        """Delete a post by its media ID."""
        self.client.media_delete(media_id)
        logger.info(f"Deleted post: {media_id}")
