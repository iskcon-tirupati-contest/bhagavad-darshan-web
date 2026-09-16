# bdtirupati.com

Static website for **Bhagavad Darshan**, the magazine of ISKCON Tirupati.

Before this repo existed the domain root returned a 404 from the Express API,
and the few live pages were hand-edited directly on the server.

## Layout

```
public/
  index.html                 homepage (bdtirupati.com)
  archive.html               past issues, rendered from issues.json
  issues.json                the archive data — edit this to add an issue
  download/index.html        agent app download, WhatsApp OTP gated
  legal/privacy.html         served at /privacy
  legal/delete-account.html  account deletion page required by Google Play
  404.html                   served by nginx for any unknown path
  robots.txt, sitemap.xml
nginx/bdtirupati.conf        reference config for the domain
nginx/bd-api.live.conf       snapshot of the deployed nginx site
scripts/deploy.sh            rsync deploy to the Lightsail host
```

## Adding a magazine issue

1. Put the cover scan in `public/assets/issues/` (WebP, roughly 700px wide).
2. Add an entry at the top of the `issues` array in `public/issues.json`.
3. `./scripts/deploy.sh live`

The archive renders exactly what `issues.json` lists, newest first, and shows year
filter buttons once more than one year is present.

## Pages that are not here

`/media/` serves photos and released APKs straight from `/var/www/html/bd-media`
on the host; those files are not in this repo.

## Photos

Images are referenced from paths already served by nginx (`/media/...` and
`/download/...`) rather than committed here, to keep the repo small. Those files
live in `/var/www/html/bd-media` on the host.

## Deploy

```bash
./scripts/deploy.sh preview   # https://bdtirupati.com/preview/
./scripts/deploy.sh live      # https://bdtirupati.com/
```

Override `BD_SSH_KEY` / `BD_SSH_HOST` if the key or host differs.

## Related

- API: `bhagavad-darshan-api` (Express, PM2 process `bd-api`), all routes under `/v1/*`
- Android app: [iskcon-tirupati-contest/bhagavad-darshan-app](https://github.com/iskcon-tirupati-contest/bhagavad-darshan-app)
