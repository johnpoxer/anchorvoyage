# AnchorVoyage indexing investigation — 17 October 2026

## Conclusion and limits

After authenticated inspection of the **Domain property anchorvoyage.com**, the
15 October alert is confirmed to concern exactly **one URL**:
`https://www.anchorvoyage.com/`. Google last crawled it on 14 October 2026 at
03:08:47 (time displayed by Search Console), using Googlebot smartphone. Crawl
and indexing were allowed and the page fetch succeeded.

Its user-declared canonical is `https://anchorvoyage.com/`; Google's selected
canonical is **the same**. Inspecting that primary homepage returned **URL is on
Google / Page is indexed**. This is intentional duplicate exclusion, not an
indexing defect. No fix validation or indexing request was submitted for it.

All **53 URLs in the live primary sitemap** returned HTTP 200 directly, declared
their own canonical URL and exposed no meta or HTTP `noindex` directive in this
audit. These are technical fetch results, not evidence of Google's indexed state.
Google documents alternate-page exclusion as expected when the intended canonical
is indexed. Do not remove correct canonical tags to make duplicate URLs indexable.

One live defect was reproduced: an unknown path returned HTTP 200 and the homepage
canonical. A separate source/deployment mismatch would reintroduce inconsistent
canonical targets if the current repository were deployed unchanged.

## Evidence and current behavior

Repository baseline: `71d47e5c551f9291edca15013abf0f7f39ee3e7c` on `main`.
No open pull requests were returned at the start of the investigation.
The repository contained 45 indexable HTML pages and the noindex map helper.

| URL tested | Observed response | Canonical / interpretation |
| --- | --- | --- |
| `https://anchorvoyage.com/` | 200 | Self-canonical; correct |
| `https://anchorvoyage.com/index.html` | 308 to `/`, then 200 | Homepage alias; expected redirect exclusion |
| `https://anchorvoyage.com/services.html` | 308 to `/services`, then 200 | Legacy filename alias; expected redirect exclusion |
| `https://anchorvoyage.com/services` | 200 | Self-canonical; correct |
| `https://anchorvoyage.com/contact.html?service=Crew%20changes%20%26%20welfare` | 308 to `/contact?service=Crew%20changes%20%26%20welfare`, then 200 | Canonical `/contact`; the query prefills an enquiry, not a separate indexable page |
| `https://www.anchorvoyage.com/` | 200; no host redirect | Canonical apex `/`; intentional duplicate signal |
| `https://www.anchorvoyage.com/services` | 200; no host redirect | Canonical apex `/services`; intentional duplicate signal |
| `http://anchorvoyage.com/` | 301 to HTTPS, then 200 | Correct HTTPS normalization |
| `http://www.anchorvoyage.com/` | 301 to HTTPS www, then 200 | HTTPS normalization works; host remains a canonicalized duplicate |
| `https://anchorvoyage.netlify.app/` and `/index.html` | 200; no host redirect | Both canonicalize to apex `/` |
| `https://anchorvoyage.netlify.app/services` and `/services.html` | 200; no host redirect | Both canonicalize to apex `/services` |
| `https://anchorvoyage.com/robots.txt` | 200, `Allow: /` | Advertises primary-domain sitemap |
| `https://anchorvoyage.com/sitemap.xml` | 200, 53 URLs | Primary-domain extensionless URLs; all 53 checked |
| `https://anchorvoyage.com/satellite-map.html` | 308 to `/satellite-map`, then 200 | Intentionally noindex and absent from sitemap |
| `https://anchorvoyage.com/seo-audit-missing-20261017` | **200, homepage content** | **Defect: nonexistent page should return 404, not be canonicalized to the homepage** |

The sitemap and robots.txt fetched from Netlify and www matched those fetched
from the apex. The sampled Netlify content uses the newer canonical scheme too.
The Netlify mirror's cross-domain canonicalization is valid in principle, but
`anchorvoyage.netlify.app` is not in the `anchorvoyage.com` Search Console property.
The authenticated report confirms the excluded example is the **www homepage**,
not the Netlify mirror, query variants or unknown paths. Those other variants
must not be presented as affected examples from this notification.

Python urllib requests received Cloudflare 403/error 1010 responses; ordinary
curl requests succeeded. This client-dependent behavior does not prove Googlebot
is blocked. The authenticated inspection confirms Google's successful crawl of
the www homepage on 14 October. That historical success does not guarantee
current fetchability of every page; use a live URL test for any remaining
fetch concern rather than disabling security protections on this evidence.

Raw response summaries, including statuses and redirect locations, are retained
in `indexing-audit-observations-2026-10-17.json`. No email tracking links,
credentials, cookies or account-private Search Console data are included.

## Repository corrections

1. Add a top-level `404.html` with recovery links and `noindex`, without a homepage
   canonical. Cloudflare Pages documents that absence of this file enables its
   single-page-app fallback. Shipping the file with the current deployment source
   should make missing routes return a real 404. Verify the deployed status.
2. Align the existing 44 non-homepage canonical tags and their primary-domain
   structured-data URLs with the live extensionless destinations. The previous
   `.html` canonical targets redirect on the primary host.
3. Align the 45-entry repository sitemap with those same canonical URLs.
4. Replace 112 internal homepage references to `index.html` with `/`, preserving
   fragments such as `/#credits`.

No blanket redirects, robots blocking, removals or `noindex` rules were added to
valid content or mirrors. There is no evidence that those would fix this alert.
The map helper's existing noindex policy remains in place.

## Validation and deployment constraint

Local parsing verified all 45 indexable pages have exactly one expected canonical,
matching unique sitemap entries and valid JSON-LD. Every sitemap route has a
corresponding HTML source file. Both the map helper and error page are noindex and
excluded from the sitemap. Existing HTML file changes were checked against the
baseline and are limited to the intended URL substitutions. `git diff --check`
passed. No production deployment was performed, so the new 404 behavior still
requires a deployed HTTP check.

**Do not deploy this older source tree over the current site before reconciling
the deployment source.** The live sitemap has 53 pages; this repository has 45.
These eight live articles are absent from the repository:

- `/insight-appointing-a-shipping-agent-nigeria`
- `/insight-bunker-fresh-water-enquiry-checklist`
- `/insight-choosing-a-nigerian-port`
- `/insight-container-release-inland-delivery-nigeria`
- `/insight-crew-change-planning-nigerian-ports`
- `/insight-project-cargo-readiness-nigeria`
- `/insight-ship-spares-repair-attendance-guide`
- `/insight-ship-waste-reception-planning`

All eight currently return 200 with matching self-canonicals. Other deployed
content may also be newer. Preserve the full current source and the 53-entry
live sitemap when integrating these corrections; do not copy the smaller sitemap
over it. The draft pull request provides a reviewable patch, not a release.

## Authenticated Search Console findings and follow-through

The overview showed 38 indexed URLs and 51 not indexed: 33 redirects, one
canonical alternate, 12 discovered/not indexed and five crawled/not indexed.
These counts cover all known URLs, including aliases, not just the 53 sitemap
destinations. The report displayed "Last update: 12/10/2026" while the alternate
example displayed a 14 October crawl; these dates are recorded as shown, not
treated as a synchronized real-time snapshot.

The submitted `https://anchorvoyage.com/sitemap.xml` is **Success**, submitted
10 October, last read **16 October 2026**, with **53 discovered pages**.
The www URL inspection's "Temporary processing error" under Sitemaps is not
evidence that the submitted sitemap failed; the dedicated sitemap report succeeds.

### Follow-up URL list

These are separate from the October 15 canonical alert. All 17 were included in
the HTTP audit and returned 200 with matching self-canonicals and no observed
noindex directives. Their report status alone does not establish a code defect.

**Discovered – currently not indexed (12; last crawl shown as N/A):**

- `https://anchorvoyage.com/company`
- `https://anchorvoyage.com/journey-unloading-cargo`
- `https://anchorvoyage.com/port-apapa`
- `https://anchorvoyage.com/port-calabar`
- `https://anchorvoyage.com/port-delta`
- `https://anchorvoyage.com/port-lekki`
- `https://anchorvoyage.com/port-onne`
- `https://anchorvoyage.com/port-rivers`
- `https://anchorvoyage.com/port-tin-can-island`
- `https://anchorvoyage.com/service-chartering-support`
- `https://anchorvoyage.com/service-crew-change`
- `https://anchorvoyage.com/service-project-cargo`

**Crawled - currently not indexed (5; last crawled 13 October 2026):**

- `https://anchorvoyage.com/service-shipping-agency-husbandry`
- `https://anchorvoyage.com/service-port-operations`
- `https://anchorvoyage.com/port-harcourt`
- `https://anchorvoyage.com/service-ship-management`
- `https://anchorvoyage.com/service-cargo-inland-logistics`

Prioritize individual URL Inspection/live tests for `/company`,
`/service-shipping-agency-husbandry`, `/service-port-operations`,
`/service-ship-management` and `/service-cargo-inland-logistics`, then the port
guides and remaining pages. Confirm Google's current fetchability, declared and
selected canonicals, rendered content and internal discovery before deciding on
changes. Review distinct service/port content and useful internal links for the
crawled group; crawling alone does not guarantee indexing. No bulk reindexing or
speculative content rewrites were performed.

### Validation decisions

- **No action for the www exclusion:** preserve its apex canonical. The preferred
  homepage is already indexed; do not request indexing of the duplicate or click
  Validate fix for this intentional condition.
- **No sitemap resubmission needed:** the existing sitemap is successfully read
  and contains all 53 live pages.
- **Monitor/inspect the 17 URLs above:** request indexing only where justified by
  eligibility and meaningful corrections. Do not treat a validation button as
  proof that a source-code error exists.
- **After safely deploying the separate 404 correction:** verify
  `https://anchorvoyage.com/seo-audit-missing-20261017` returns HTTP 404 and valid
  routes remain 200. Do not request indexing for nonexistent URLs.
- **Keep the draft PR undeployed until source reconciliation:** preserve the
  eight newer articles and full live sitemap before releasing the patch.

## Sources

- Search Console notification read through Gmail, 15 October 2026; subject:
  “New reasons prevent pages from being indexed on site anchorvoyage.com”.
- [Authenticated alternate-page report](https://search.google.com/search-console/index/drilldown?resource_id=sc-domain%3Aanchorvoyage.com&item_key=CAMYGCAC), inspected 17 October 2026.
- [Submitted sitemap report](https://search.google.com/search-console/sitemaps?resource_id=sc-domain%3Aanchorvoyage.com), inspected 17 October 2026. Access requires the property account.
- [Repository baseline](https://github.com/johnpoxer/anchorvoyage/tree/71d47e5c551f9291edca15013abf0f7f39ee3e7c)
- [Live homepage](https://anchorvoyage.com/), [services](https://anchorvoyage.com/services),
  [sitemap](https://anchorvoyage.com/sitemap.xml), [robots](https://anchorvoyage.com/robots.txt),
  [Netlify mirror](https://anchorvoyage.netlify.app/)
- [Google: Page indexing report](https://support.google.com/webmasters/answer/7440203)
- [Google: canonicalization methods and best practices](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
- [Google: property scope](https://support.google.com/webmasters/answer/34592)
- [Cloudflare Pages: route matching and not-found behavior](https://developers.cloudflare.com/pages/configuration/serving-pages/)
