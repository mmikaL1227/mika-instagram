"""
Generate Instagram story ideas based on a theme/niche.

Usage:
    python generate_ideas.py --niche "fitness" --count 7
    python generate_ideas.py --niche "food blogger" --count 5 --save ideas.json
"""

import argparse
import json
import random
from datetime import datetime, timedelta

# Story idea templates organised by content type
TEMPLATES = {
    "quote": [
        'Bold text quote: "{quote}" — clean background, contrasting font',
        'Motivational quote overlay on a blurred background: "{quote}"',
        'Minimal white card with quote: "{quote}" and a small accent colour',
    ],
    "tip": [
        "Step-by-step tip card: {tip} — numbered list, icon per step",
        "Quick-tip story: '{tip}' — bold headline, 3-bullet breakdown below",
        "Did-you-know style: '{tip}' — colourful banner, white text",
    ],
    "poll": [
        "Poll story: '{question}' with options '{a}' vs '{b}'",
        "This or That: '{a}' on left half vs '{b}' on right half",
        "Engagement poll: '{question}' — emoji slider or Yes/No sticker",
    ],
    "behind_the_scenes": [
        "Behind the scenes snapshot: {scene} — raw, candid feel",
        "Day-in-the-life frame: {scene} — timestamp overlay, casual caption",
        "Process reveal: {scene} — before/after split or progress bar",
    ],
    "countdown": [
        "Countdown story: '{event}' — X days to go, bold timer graphic",
        "Hype build: 'Coming soon — {event}' — teaser silhouette image",
    ],
    "cta": [
        "Swipe-up / link-in-bio CTA: '{offer}' — arrow graphic, bright button",
        "Save this! story card: '{tip}' — bookmark icon highlighted",
        "Tag a friend who needs this: '{relatable_statement}'",
    ],
}

NICHE_EXAMPLES = {
    "fitness": {
        "quote": ["Push harder than yesterday", "Results require consistency", "Your only limit is you"],
        "tip": ["Drink water before every meal to reduce cravings", "Rest days are part of the programme", "Progressive overload = progress"],
        "poll": [("Morning workout", "Evening workout"), ("Cardio", "Weights"), ("Home gym", "Commercial gym")],
        "behind_the_scenes": ["meal prep Sunday", "pre-workout routine", "post-session recovery"],
        "countdown": ["new programme launch", "challenge start", "transformation reveal"],
        "cta": ["free workout plan", "my current stack", "30-day challenge"],
    },
    "food": {
        "quote": ["Good food is good mood", "Life is too short for bad coffee", "Cook with love, eat with joy"],
        "tip": ["Salt pasta water like the sea", "Let meat rest before cutting", "Mise en place saves time"],
        "poll": [("Sweet", "Savoury"), ("Coffee", "Tea"), ("Home cooked", "Takeaway")],
        "behind_the_scenes": ["recipe testing", "farmers market haul", "plating process"],
        "countdown": ["new recipe drop", "collab announcement", "cookbook launch"],
        "cta": ["full recipe in bio", "save this for later", "tag someone who'd love this"],
    },
    "fashion": {
        "quote": ["Style is a way to say who you are without speaking", "Dress for the life you want", "Fashion fades, style is eternal"],
        "tip": ["Invest in basics, experiment with accessories", "Fit matters more than brand", "Capsule wardrobe saves money and stress"],
        "poll": [("Streetwear", "Smart casual"), ("Colour", "Neutral"), ("Thrift", "New")],
        "behind_the_scenes": ["outfit building process", "wardrobe organisation", "photoshoot prep"],
        "countdown": ["new collection drop", "sale going live", "collab reveal"],
        "cta": ["shop the look via link in bio", "save this outfit inspo", "tag your style twin"],
    },
    "general": {
        "quote": ["Small steps every day", "Done is better than perfect", "Be the energy you want to attract"],
        "tip": ["Plan your week on Sunday evening", "Single-task instead of multitask", "Celebrate small wins"],
        "poll": [("Morning person", "Night owl"), ("Planner", "Spontaneous"), ("Introvert", "Extrovert")],
        "behind_the_scenes": ["workspace setup", "creative process", "daily routine"],
        "countdown": ["big announcement", "new project launch", "event"],
        "cta": ["link in bio for more", "save this post", "share with a friend"],
    },
}


def resolve_niche(niche: str) -> dict:
    key = niche.lower()
    for k in NICHE_EXAMPLES:
        if k in key:
            return NICHE_EXAMPLES[k]
    return NICHE_EXAMPLES["general"]


def generate_idea(niche_data: dict, content_type: str, niche_label: str) -> dict:
    template = random.choice(TEMPLATES[content_type])
    nd = niche_data

    if content_type == "quote":
        desc = template.format(quote=random.choice(nd["quote"]))
    elif content_type == "tip":
        desc = template.format(tip=random.choice(nd["tip"]))
    elif content_type == "poll":
        pair = random.choice(nd["poll"])
        q = f"{pair[0]} or {pair[1]}?"
        desc = template.format(question=q, a=pair[0], b=pair[1])
    elif content_type == "behind_the_scenes":
        desc = template.format(scene=random.choice(nd["behind_the_scenes"]))
    elif content_type == "countdown":
        desc = template.format(event=random.choice(nd["countdown"]))
    elif content_type == "cta":
        cta_keys = ["offer", "tip", "relatable_statement"]
        vals = {
            "offer": random.choice(nd["cta"]),
            "tip": random.choice(nd["tip"]),
            "relatable_statement": f"every {niche_label} lover",
        }
        try:
            desc = template.format(**vals)
        except KeyError:
            desc = template.format(offer=vals["offer"], tip=vals["tip"], relatable_statement=vals["relatable_statement"])

    return {
        "type": content_type,
        "description": desc,
        "image_prompt": build_image_prompt(content_type, desc, niche_label),
        "best_time": suggest_time(),
    }


def build_image_prompt(content_type: str, description: str, niche: str) -> str:
    """Build an AI image generation prompt based on the story idea."""
    style_map = {
        "quote": f"Minimalist Instagram story graphic, 1080x1920px, clean typography, {niche} aesthetic. {description}",
        "tip": f"Bold, modern infographic-style Instagram story, 1080x1920px, {niche} theme. {description}",
        "poll": f"Fun, vibrant Instagram story poll graphic, 1080x1920px, {niche} style. {description}",
        "behind_the_scenes": f"Authentic, warm-toned lifestyle photo, vertical 9:16, {niche} theme. {description}",
        "countdown": f"High-energy countdown graphic, 1080x1920px, bold fonts, {niche} branding. {description}",
        "cta": f"Eye-catching Instagram story CTA graphic, 1080x1920px, {niche} colours, clear call-to-action. {description}",
    }
    return style_map.get(content_type, description)


def suggest_time() -> str:
    """Suggest a good posting time (stories: morning or evening)."""
    windows = ["07:00", "08:00", "12:00", "17:00", "19:00", "20:00", "21:00"]
    base = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    offset_days = random.randint(0, 6)
    t = base + timedelta(days=offset_days)
    h, m = random.choice(windows).split(":")
    t = t.replace(hour=int(h), minute=int(m))
    return t.strftime("%Y-%m-%d %H:%M")


def generate_ideas(niche: str, count: int) -> list[dict]:
    niche_data = resolve_niche(niche)
    types = list(TEMPLATES.keys())
    ideas = []
    for i in range(count):
        content_type = types[i % len(types)]
        ideas.append(generate_idea(niche_data, content_type, niche))
    return ideas


def main():
    parser = argparse.ArgumentParser(description="Generate Instagram story ideas.")
    parser.add_argument("--niche", default="general", help="Your account niche (e.g. fitness, food, fashion)")
    parser.add_argument("--count", type=int, default=7, help="Number of ideas to generate")
    parser.add_argument("--save", default="", help="Optional: save ideas to a JSON file")
    args = parser.parse_args()

    ideas = generate_ideas(args.niche, args.count)

    print(f"\n{'='*60}")
    print(f"  {args.count} Story Ideas for niche: {args.niche.upper()}")
    print(f"{'='*60}\n")

    for i, idea in enumerate(ideas, 1):
        print(f"[{i}] Type: {idea['type'].upper().replace('_', ' ')}")
        print(f"    Story:  {idea['description']}")
        print(f"    Prompt: {idea['image_prompt']}")
        print(f"    Post at: {idea['best_time']}")
        print()

    if args.save:
        with open(args.save, "w") as f:
            json.dump(ideas, f, indent=2)
        print(f"Saved to {args.save}")


if __name__ == "__main__":
    main()
