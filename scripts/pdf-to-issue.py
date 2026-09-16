#!/usr/bin/env python3
"""Turn a magazine PDF into reader page images and register it in issues.json.

    ./scripts/pdf-to-issue.py magazine.pdf \
        --month "August 2026" --volume 22 --issue 8 \
        --title "Edition title" --summary "Short archive description."

Pages are written to public/assets/issues/<slug>/ as WebP, sized for on-screen
reading rather than print, so the reader stays fast on phones.

Needs pdftoppm (apt install poppler-utils) and Pillow.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parent.parent
PUBLIC = REPO / "public"
ISSUES_JSON = PUBLIC / "issues.json"

# Long edge of a reader page. Enough to read comfortably on a laptop while
# keeping each page a few hundred KB.
MAX_EDGE = 1600
WEBP_QUALITY = 82


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def render_pages(pdf, workdir, dpi):
    if not shutil.which("pdftoppm"):
        sys.exit("pdftoppm not found. Install it with: sudo apt install -y poppler-utils")
    subprocess.run(
        ["pdftoppm", "-r", str(dpi), "-png", str(pdf), str(workdir / "page")],
        check=True,
    )
    return sorted(workdir.glob("page-*.png"))


def to_webp(src_pages, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    for existing in out_dir.glob("*.webp"):
        existing.unlink()

    written = []
    for n, src in enumerate(src_pages, start=1):
        img = Image.open(src).convert("RGB")
        if max(img.size) > MAX_EDGE:
            scale = MAX_EDGE / max(img.size)
            img = img.resize(
                (round(img.width * scale), round(img.height * scale)),
                Image.LANCZOS,
            )
        dest = out_dir / f"{n:03d}.webp"
        img.save(dest, "WEBP", quality=WEBP_QUALITY, method=6)
        written.append(dest)
        print(f"  page {n:>3}  {img.width}x{img.height}  {dest.stat().st_size // 1024} KB")
    return written


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--month", required=True, help='e.g. "August 2026"')
    ap.add_argument("--title", required=True)
    ap.add_argument("--summary", default="")
    ap.add_argument("--volume", type=int)
    ap.add_argument("--issue", type=int)
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="render pages but leave issues.json untouched",
    )
    args = ap.parse_args()

    if not args.pdf.exists():
        sys.exit(f"No such PDF: {args.pdf}")

    slug = slugify(args.month)
    out_dir = PUBLIC / "assets" / "issues" / slug

    print(f"Rendering {args.pdf.name} at {args.dpi} dpi …")
    with tempfile.TemporaryDirectory() as tmp:
        pages = render_pages(args.pdf, Path(tmp), args.dpi)
        if not pages:
            sys.exit("pdftoppm produced no pages.")
        written = to_webp(pages, out_dir)

    rel = [f"/assets/issues/{slug}/{p.name}" for p in written]
    entry = {
        "volume": args.volume,
        "issue": args.issue,
        "month": args.month,
        "title": args.title,
        "summary": args.summary,
        "cover": rel[0],
        "pages": rel,
    }
    entry = {k: v for k, v in entry.items() if v not in (None, "")}

    if args.dry_run:
        print("\n--dry-run, issues.json unchanged. Entry would be:\n")
        print(json.dumps(entry, indent=2))
        return

    data = json.loads(ISSUES_JSON.read_text())
    # Replace an existing entry for the same month rather than duplicating it.
    data["issues"] = [i for i in data["issues"] if i.get("month") != args.month]
    data["issues"].insert(0, entry)
    ISSUES_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

    print(f"\n{len(rel)} pages -> {out_dir}")
    print(f"Registered \"{args.month}\" in issues.json (newest first).")
    print("Preview locally, then publish with: ./scripts/deploy.sh live")


if __name__ == "__main__":
    main()
