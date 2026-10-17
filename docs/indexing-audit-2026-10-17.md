# AnchorVoyage indexing investigation — 17 October 2026

## Conclusion and limits

The 15 October Search Console notification names **Alternative page with proper
canonical tag**, but contains no URL examples or count. The authenticated report
was unavailable: Search Console opened Google's sign-in page. No affected URL has
therefore been identified from Google, and no request for indexing or fix
validation has been submitted.

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
It cannot by itself identify the URLs behind this alert. Depending on the actual
property scope, www, parameter variants and unknown paths on anchorvoyage.com are
possible examples. These remain hypotheses until the report is available.

Python urllib requests received Cloudflare 403/error 1010 responses; ordinary
curl requests succeeded. This client-dependent behavior does not prove Googlebot
is blocked. Check crawl permission and fetch success in Search Console's live
URL test rather than disabling security protections on this evidence.

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

## Search Console follow-through

1. Open the 15 October notification's indexing report in the account that owns
   anchorvoyage.com. Confirm whether this is a Domain or URL-prefix property and
   select **Alternate page with proper canonical tag**. Export its example URLs.
2. Inspect each example and compare **User-declared canonical**, **Google-selected
   canonical**, last crawl, fetch status and indexing status. Classify the exact
   reported URLs; do not substitute this audit's candidate list for Google's list.
3. Inspect these preferred URLs as priority checks:
   - `https://anchorvoyage.com/`
   - `https://anchorvoyage.com/services`
   - `https://anchorvoyage.com/contact`
   - `https://anchorvoyage.com/company`
   - `https://anchorvoyage.com/ports`
   - `https://anchorvoyage.com/insights`
   - Every other canonical destination named by an affected example, including
     any of the eight newer article URLs above.
4. If a reported URL is an intended www/query duplicate and its correct primary
   canonical is indexed, leave the exclusion in place. `.html` and `/index.html`
   aliases should resolve to their preferred route; Google may report them as
   **Page with redirect** after recrawling. Do not request indexing of aliases.
5. If a preferred URL itself is excluded in favor of an unrelated page, fails
   fetching, is blocked, or unexpectedly noindex, investigate that exact URL.
   Request indexing only for eligible preferred pages after fixing the cause.
6. After safely deploying the 404 fix, verify an unknown path returns HTTP 404
   and valid routes remain 200. Do not request indexing for the error page or
   intentionally missing URLs. An appropriate 404 exclusion is expected.
7. Confirm the submitted sitemap is `https://anchorvoyage.com/sitemap.xml` and
   still contains all intended live pages. Use **Validate fix** only for a
   genuinely unintended issue after all relevant instances are corrected; this
   notification category does not inherently need a fix or a zero count.

## Sources

- Search Console notification read through Gmail, 15 October 2026; subject:
  “New reasons prevent pages from being indexed on site anchorvoyage.com”.
- [Repository baseline](https://github.com/johnpoxer/anchorvoyage/tree/71d47e5c551f9291edca15013abf0f7f39ee3e7c)
- [Live homepage](https://anchorvoyage.com/), [services](https://anchorvoyage.com/services),
  [sitemap](https://anchorvoyage.com/sitemap.xml), [robots](https://anchorvoyage.com/robots.txt),
  [Netlify mirror](https://anchorvoyage.netlify.app/)
- [Google: Page indexing report](https://support.google.com/webmasters/answer/7440203)
- [Google: canonicalization methods and best practices](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
- [Google: property scope](https://support.google.com/webmasters/answer/34592)
- [Cloudflare Pages: route matching and not-found behavior](https://developers.cloudflare.com/pages/configuration/serving-pages/)
