#!/usr/bin/env python3
"""Build a multi-page sample magazine PDF so the reader can be tested end to end."""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

W, H = 1240, 1754  # A4 at 150 dpi
CREAM = (255, 248, 236)
PAPER = (255, 253, 249)
INK = (58, 31, 18)
INK_SOFT = (122, 97, 85)
MAROON = (122, 31, 61)
MARIGOLD = (230, 81, 0)
GOLD = (217, 160, 60)
LINE = (234, 220, 196)


TELUGU_FONT = "/usr/share/fonts/truetype/fonts-telu-extra/Pothana2000.ttf"
DEVANAGARI_FONT = "/usr/share/fonts/truetype/Gargi/Gargi.ttf"


def script_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return font(size, True)


def font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def cover():
    img = Image.new("RGB", (W, H), MAROON)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(
            int(122 + (78 - 122) * t),
            int(31 + (19 - 31) * t),
            int(61 + (39 - 61) * t),
        ))
    d.ellipse([W - 420, -220, W + 180, 380], fill=(140, 42, 74))
    d.text((W // 2, 150), "ॐ", font=script_font(DEVANAGARI_FONT, 120), fill=(230, 184, 92), anchor="mm")

    d.text((W // 2, 330), "BHAGAVAD DARSHAN", font=font(64, True), fill=(255, 255, 255), anchor="mm")
    d.line([(220, 385), (W - 220, 385)], fill=GOLD, width=3)
    d.text((W // 2, 430), "ISKCON TIRUPATI  ·  SAMPLE EDITION", font=font(26), fill=(245, 207, 131), anchor="mm")

    d.rounded_rectangle([160, 520, W - 160, 1180], 24, fill=(255, 248, 236))
    d.text((W // 2, 640), "Jagannath", font=font(78, True), fill=MAROON, anchor="mm")
    d.text((W // 2, 730), "Rathayatra", font=font(78, True), fill=MAROON, anchor="mm")
    d.text((W // 2, 820), "Mahotsavam", font=font(78, True), fill=MARIGOLD, anchor="mm")
    d.line([(400, 890), (W - 400, 890)], fill=GOLD, width=2)
    d.text((W // 2, 950), "A festival edition on the Lord's", font=font(32), fill=INK_SOFT, anchor="mm")
    d.text((W // 2, 1000), "grand chariot procession", font=font(32), fill=INK_SOFT, anchor="mm")
    d.text((W // 2, 1100), "Volume 22  ·  Issue 7  ·  July 2026", font=font(28, True), fill=MAROON, anchor="mm")

    d.text((W // 2, 1290), "This is a demonstration file used to test the", font=font(26), fill=(240, 220, 200), anchor="mm")
    d.text((W // 2, 1335), "digital reader. It is not a real magazine issue.", font=font(26), fill=(240, 220, 200), anchor="mm")
    d.text((W // 2, H - 90), "bdtirupati.com", font=font(30, True), fill=(245, 207, 131), anchor="mm")
    return img


def article(n, heading, paras, telugu=False):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, W, 14], fill=MAROON)
    d.text((90, 70), "BHAGAVAD DARSHAN", font=font(22, True), fill=MARIGOLD)
    d.text((W - 90, 70), "SAMPLE EDITION", font=font(22), fill=INK_SOFT, anchor="ra")
    d.line([(90, 110), (W - 90, 110)], fill=LINE, width=2)

    y = 190
    for line in wrap(d, heading, font(58, True), W - 180):
        d.text((90, y), line, font=font(58, True), fill=MAROON)
        y += 74
    y += 10
    d.line([(90, y), (330, y)], fill=GOLD, width=4)
    y += 60

    body = font(30)
    for para in paras:
        for line in wrap(d, para, body, W - 180):
            d.text((90, y), line, font=body, fill=INK)
            y += 48
        y += 34

    if telugu:
        d.rounded_rectangle([90, y, W - 90, y + 190], 18, fill=CREAM, outline=LINE, width=2)
        d.text((W // 2, y + 70), "భగవద్దర్శన్", font=script_font(TELUGU_FONT, 52), fill=MAROON, anchor="mm")
        d.text((W // 2, y + 135), "ISKCON Tirupati", font=font(28), fill=INK_SOFT, anchor="mm")

    d.line([(90, H - 130), (W - 90, H - 130)], fill=LINE, width=2)
    d.text((90, H - 100), "July 2026", font=font(24), fill=INK_SOFT)
    d.text((W // 2, H - 100), f"— {n} —", font=font(26, True), fill=MAROON, anchor="ma")
    d.text((W - 90, H - 100), "bdtirupati.com", font=font(24), fill=INK_SOFT, anchor="ra")
    return img


PAGES = [
    ("From the Editor", [
        "Hare Krishna. It is with great joy that we place this edition in your hands. Each month "
        "Bhagavad Darshan carries the timeless teachings of Srila Prabhupada to devotees across "
        "Tirupati and far beyond it.",
        "This sample edition exists so that the new digital reader on our website can be tested "
        "properly before real magazine scans are published. Every page you can turn here is a "
        "placeholder, generated to confirm that page navigation, zoom, thumbnails and reading "
        "progress all behave as they should.",
        "When the actual issue is scanned, these pages will simply be replaced, and the reader "
        "will work exactly as it does now.",
    ], True),
    ("The Chariot Festival", [
        "The Rathayatra of Lord Jagannath is among the most beloved festivals in the Vaishnava "
        "calendar. Devotees pull the great chariot through the streets while chanting the holy "
        "names, and the Lord comes out to greet everyone without distinction.",
        "Srila Prabhupada brought this festival to cities around the world, so that anyone who "
        "simply watched the procession would receive spiritual benefit. What was once confined to "
        "Puri is now celebrated on every continent.",
        "In Tirupati, the festival brings together families, students and pilgrims. Preparations "
        "begin weeks in advance, with the construction of the chariot, the making of garlands, "
        "and the cooking of prasadam offered to thousands.",
    ], False),
    ("Teachings for Daily Life", [
        "Bhakti is not a practice reserved for the temple alone. Srila Prabhupada repeatedly "
        "emphasised that devotional service can be woven into ordinary work, study and family "
        "responsibility.",
        "Chanting the holy name, honouring prasadam, reading a few verses each morning, and "
        "serving the devotees — these simple daily acts gradually transform consciousness without "
        "requiring anyone to abandon their duties.",
        "Readers often write to ask how to begin. The answer given in our tradition is refreshingly "
        "practical: begin where you are, with whatever time you can honestly offer, and remain "
        "steady.",
    ], False),
    ("Temple News & Subscriptions", [
        "Bhagavad Darshan is published monthly in Telugu and English by ISKCON Tirupati. Annual "
        "and multi-year subscriptions are available, and the magazine is delivered to your home "
        "address by post.",
        "Subscriptions can now be managed entirely from our Android app — subscribe, renew, pay by "
        "UPI, and update your delivery address without visiting the temple office. The app can be "
        "downloaded from bdtirupati.com/download.",
        "For assistance with a subscription, please reach the book department on WhatsApp at "
        "+91 94938 05059, or write to iskcon.tirupati.books@gmail.com.",
    ], True),
]


def main():
    pages = [cover()]
    for n, (heading, paras, telugu) in enumerate(PAGES, start=2):
        pages.append(article(n, heading, paras, telugu))

    out = Path("/tmp/bhagavad-darshan-sample-july-2026.pdf")
    pages[0].save(out, "PDF", save_all=True, append_images=pages[1:], resolution=150.0)
    print(f"{out}  ({len(pages)} pages, {out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
