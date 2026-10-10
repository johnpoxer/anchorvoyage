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
