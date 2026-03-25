"""Load configuration from environment variables / .env file."""

import os
from dotenv import load_dotenv

load_dotenv()


def load_config() -> dict:
    username = os.getenv("INSTAGRAM_USERNAME", "").strip()
    password = os.getenv("INSTAGRAM_PASSWORD", "").strip()

    if not username or not password:
        raise RuntimeError(
            "INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD must be set. "
            "Copy .env.example to .env and fill in your credentials."
        )

    return {
        "username": username,
        "password": password,
        "session_file": os.getenv("SESSION_FILE", "sessions/session.json"),
        "totp_seed": os.getenv("INSTAGRAM_TOTP_SEED", ""),
    }
