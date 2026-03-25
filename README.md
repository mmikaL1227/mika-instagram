# mika-instagram

Automate Instagram posts with Python — post photos, videos, and carousels immediately or on a schedule.

## Features

- Post photos, videos (Reels), and carousel albums
- Schedule posts from a JSON queue file
- Session persistence (no repeated logins)
- 2FA (TOTP) support
- Polite request delays to avoid rate limits

## Requirements

- Python 3.11+
- An Instagram account

## Setup

### 1. Clone & install dependencies

```bash
git clone https://github.com/mmikal1227/mika-instagram.git
cd mika-instagram
pip install -r requirements.txt
```

### 2. Configure credentials

```bash
cp .env.example .env
```

Edit `.env` with your Instagram username and password:

```env
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

If your account uses **2FA (authenticator app)**, also set:

```env
INSTAGRAM_TOTP_SEED=your_totp_secret_key
```

### 3. Create the uploads folder

```bash
mkdir uploads
```

Add your images or videos to the `uploads/` folder.

---

## Usage

### Post immediately

```bash
# Single photo
python post_now.py --image uploads/photo.jpg --caption "Hello world! #python"

# Video / Reel
python post_now.py --video uploads/clip.mp4 --caption "Watch this!"

# Carousel (multiple images)
python post_now.py --album uploads/1.jpg uploads/2.jpg --caption "Swipe through!"
```

### Scheduled posting

1. Copy the example queue file and edit it:

```bash
cp posts.example.json posts.json
```

2. Edit `posts.json` to set your images, captions, and schedule times:

```json
[
  {
    "image": "uploads/photo1.jpg",
    "caption": "Good morning! #morning #vibes",
    "schedule": "2026-03-26 09:00"
  }
]
```

3. Run the scheduler:

```bash
python scheduler.py --posts posts.json
```

The scheduler will run continuously and post at the specified times. Press `Ctrl+C` to stop.

---

## Project Structure

```
mika-instagram/
├── bot.py            # InstagramBot class (login, post, delete)
├── config.py         # Loads credentials from .env
├── post_now.py       # CLI for immediate posting
├── scheduler.py      # Scheduled posting from JSON queue
├── posts.example.json
├── .env.example
├── requirements.txt
└── uploads/          # Put your media files here (git-ignored)
```

---

## Notes & Limitations

- This project uses [instagrapi](https://github.com/subzeroid/instagrapi), an unofficial Instagram private API client.
- Using unofficial APIs may violate Instagram's Terms of Service. Use responsibly and at your own risk.
- Do **not** commit your `.env` file or `sessions/` folder — they are in `.gitignore`.
- Session files are saved to `sessions/session.json` to avoid logging in on every run.

---

## License

[MIT](LICENSE)
