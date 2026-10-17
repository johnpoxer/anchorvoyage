# AnchorVoyage

Complete website for AnchorVoyage Shipping & Maritime Services.

- Main website: https://anchorvoyage.com/
- Netlify copy: https://anchorvoyage.netlify.app/
- Enquiries: poxer7128@gmail.com

## Contents

45 main pages, seven Nigerian port guides, 15 specialist service pages, the nine-stage port journey, maritime articles, satellite maps, photography and a port film. HTML, CSS and JavaScript are the editable website source.

The media are included as `media-photos.zip` and `media-video.zip`. GitHub's individual-file upload was unreliable, so the complete media library is packaged in these archives. `prepare-media.py` restores every asset into `assets/` and verifies its size and Git blob hash against `media-integrity.json`.

## Run locally

1. Run `python3 prepare-media.py` (or `python prepare-media.py` on Windows).
2. Run `node preview.cjs`.
3. Open http://127.0.0.1:4173/.

No third-party Python or Node dependencies are required.

## Deploy

Netlify reads `netlify.toml`: build command `python3 prepare-media.py`, publish directory `.`. For a manual upload or Cloudflare Pages, run the preparation script first and upload the website files and the extracted `assets/` folder.

The contact form prepares an email in the visitor's email app. It does not send or store submissions on a server. No phone number is displayed.

## Media

Stock images illustrate the industry and do not represent company personnel or owned assets. Source details are in assets-manifest.json, page-photography.json and individual page credits. Satellite imagery is for orientation, not navigation. Third-party media remain subject to their providers' terms; this repository does not grant a separate license to them.

## Services photography update

Every one of the 24 services-page cards has its own distinct stock photograph. Six additional service pages now have hero photographs. All 30 new images are in `media-services.zip`, extracted and verified by `prepare-media.py`. Source credits are recorded in `services-photography.json`.

## URL policy and indexing audit

Production uses `https://anchorvoyage.com/` and extensionless page URLs (for
example, `/services`). Canonical tags, structured-data page URLs and the sitemap
must use those destinations. HTML source filenames remain unchanged; Cloudflare
Pages serves the extensionless routes and redirects `.html` requests. Local
`preview.cjs` still serves the source `.html` filenames.

`404.html` is required at the publish root. Without it, Cloudflare Pages treats
unknown paths as a single-page application and can serve the homepage with status
200. Do not add a catch-all homepage rewrite. The map helper and error page are
intentionally `noindex` and are excluded from the sitemap.

See [the October 2026 indexing audit](docs/indexing-audit-2026-10-17.md) before
releasing these changes. The live site has eight additional article routes that
are absent from this repository snapshot. Reconcile the current deployment source
before deploying this branch; a full deployment of the old snapshot could remove
them. The sitemap here lists only the 45 pages present in this source tree.
