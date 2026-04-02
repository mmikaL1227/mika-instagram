# mika-instagram

Automate Instagram **story** posts with Python — post photos/videos immediately or on a schedule, with AI-generated story ideas.

## Features

- Post photo and video stories
- Generate story ideas + AI image prompts by niche
- Schedule stories from a JSON queue file
- Session persistence (no repeated logins)
- 2FA (TOTP) support

## Requirements

- Python 3.11+
- An Instagram account

## Setup

### 1. Clone & create a virtual environment

```bash
git clone https://github.com/mmikal1227/mika-instagram.git
cd mika-instagram
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure credentials

```bash
cp .env.example .env
```

Edit `.env`:

```env
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

If your account uses **2FA**, also set:

```env
INSTAGRAM_TOTP_SEED=your_totp_secret_key
```

### 3. Create the uploads folder

```bash
mkdir uploads
```

---

## Usage

### Generate story ideas

```bash
python generate_ideas.py --niche "fitness" --count 7
python generate_ideas.py --niche "food" --count 5 --save ideas.json
```

Each idea includes:
- A story description
- An **AI image generation prompt** (paste into Midjourney, DALL-E, etc.)
- A suggested posting time

### Post a story immediately

```bash
# Photo story (1080x1920 recommended)
python post_story.py --image uploads/story.jpg

# Video story (MP4, max 15s)
python post_story.py --video uploads/story.mp4
```

### Scheduled story posting

1. Copy and edit the example queue:

```bash
cp stories.example.json stories.json
```

2. Edit `stories.json`:

```json
[
  { "image": "uploads/story1.jpg", "schedule": "2026-04-03 09:00" },
  { "video": "uploads/story2.mp4", "schedule": "2026-04-03 20:00" }
]
```

3. Run the scheduler:

```bash
python scheduler.py --posts stories.json
```

---

## Project Structure

```
mika-instagram/
├── bot.py                 # InstagramBot (login + story posting)
├── config.py              # Loads credentials from .env
├── generate_ideas.py      # Story idea + AI image prompt generator
├── post_story.py          # CLI for immediate story posting
├── scheduler.py           # Scheduled posting from JSON queue
├── stories.example.json   # Example story queue
├── .env.example           # Credentials template
├── requirements.txt
└── uploads/               # Put your story images/videos here
```

---

## Notes

- Story images should be **1080×1920px (9:16)** for best results.
- Video stories are capped at **15 seconds**.
- This uses [instagrapi](https://github.com/subzeroid/instagrapi), an unofficial Instagram API. Use responsibly.
- Never commit your `.env` or `sessions/` — both are in `.gitignore`.

---

## License

[MIT](LICENSE)
