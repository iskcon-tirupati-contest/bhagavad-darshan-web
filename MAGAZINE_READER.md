# Bhagavad Darshan Digital Magazine Reader

The Archive page is now an interactive public digital library and magazine reader.

## Adding an edition

Edit `public/issues.json` and add the newest issue first. Each issue supports:

- `volume`, `issue`, `month`, `title`, `summary`
- `cover`: archive-card cover image
- `pages`: ordered array of page image URLs for the reader

Example:

```json
{
  "volume": 22,
  "issue": 8,
  "month": "August 2026",
  "title": "Edition title",
  "summary": "Short archive description.",
  "cover": "/assets/issues/2026-08/cover.webp",
  "pages": [
    "/assets/issues/2026-08/001.webp",
    "/assets/issues/2026-08/002.webp"
  ]
}
```

For good reader performance, export magazine pages as optimized WebP/JPEG images rather than huge print-resolution files. Keep filenames zero-padded so ordering is obvious.

## Reader features

- Responsive archive library with year filters and search
- Full-screen distraction-free reader
- Page thumbnails on desktop
- Previous/next controls and keyboard arrow navigation
- Touch swipe navigation on mobile
- Zoom controls
- Reading progress and resume position stored locally
- Per-edition bookmark stored locally
- Native sharing with clipboard fallback
- Fullscreen mode
- Per-edition discussion interface

## Comments

The current comment interface intentionally uses browser `localStorage` as a safe preview and does **not** pretend to publish comments globally. Public multi-user comments require server-side persistence, moderation and abuse protection. The UI is isolated so it can later be connected to the site's API/Supabase/PostgreSQL without redesigning the reader.

Recommended public-comment fields: `id`, `issue_key`, `display_name`, `body`, `status`, `created_at`, `ip_hash`/rate-limit metadata. Only approved comments should be returned publicly if pre-moderation is enabled.

## Safety

Development is isolated on `feature/premium-magazine-reader`; `main` is unchanged until review/merge.
