# bdtirupati.com

Static website for **Bhagavad Darshan**, the magazine of ISKCON Tirupati.

Before this repo existed the domain root returned a 404 from the Express API,
and the few live pages were hand-edited directly on the server.

## Layout

```
public/
  index.html                 homepage (bdtirupati.com)
  legal/privacy.html         served at /privacy
  legal/delete-account.html  account deletion page required by Google Play
nginx/bdtirupati.conf        reference config for the domain
scripts/deploy.sh            rsync deploy to the Lightsail host
```

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
