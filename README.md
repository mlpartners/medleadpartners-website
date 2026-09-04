# MedLead Partners Website — Deployment Package

This folder is the complete, self-contained website, ready to upload to any
static host (GitHub Pages, Netlify, Vercel, S3, cPanel, etc.). It is not
tied to Claude in any way: no data URIs pointing at a Claude environment,
no temporary preview links, no external service calls other than the
Google Fonts stylesheet and the real Calendly scheduling widget, both
described below.

## 1. Homepage entry point

**`index.html`** is the homepage and the site's only page. There are no
other HTML files, this is a single-page site; every section (How It Works,
Who We Serve, Results, About, FAQ, the booking form) lives on this one
page, reached by scrolling or by clicking the navigation.

## 2. Framework

**None.** This is plain HTML, CSS, and JavaScript, no React, no Vite, no
Tailwind, no build step, no `package.json`, no `node_modules`. Nothing
needs to be installed or compiled before it runs. That also means it's
compatible with essentially any static host, since there's nothing for
the host to build.

## 3. Running it locally

Just open `index.html` in a browser. Double-click the file, or drag it
into a browser window. Every style and script loads from the relative
files sitting next to it in this folder, so no local server is required.

If you'd prefer to preview it the way a real web server would serve it
(recommended before deploying, though not required), from inside this
folder run:
```
python3 -m http.server 8000
```
then open `http://localhost:8000` in a browser.

## 4. Where the code lives

```
index.html      <- all page content and structure
styles.css       <- all visual styling (colors, type, spacing, layout, responsive rules)
script.js         <- all interactivity (nav, mobile menu, tabs, pills, accordions, back to top, form)
assets/
  logo.png         <- the MedLead Partners logo (used in the header and footer)
  favicon.png        <- the browser tab icon
```
That's the entire project. Four files and one small assets folder.

## 5. Where images and assets are

`assets/logo.png` and `assets/favicon.png` are the only local images the
site uses. Both are referenced with relative paths (`assets/logo.png`,
`assets/favicon.png`) in `index.html`, so as long as the `assets` folder
stays in the same place relative to `index.html`, they'll keep working
no matter where this project is hosted or what URL it's hosted at.

Every custom graphic on the page (the process diagrams in How It Works,
Services, and Who We Serve) is inline SVG written directly into
`index.html`, not separate image files, so there's nothing else to track
down or that can go missing.

## 6. Making text/content edits

You can hand-edit `index.html` directly and it will work fine, it's
plain HTML. Search for the text you want to change and edit it in place.

If you expect to make ongoing content edits, ask whoever built this site
for the companion **source project** (`content.py` / `build.py` /
`template.css` / `template.js`), which separates every piece of copy
into one plain-language file so changes don't require touching HTML
directly. That source project regenerates a file identical in structure
to this one. This deployment folder is a snapshot of that system's
output; either can be edited going forward, but the source project is
easier for repeated changes.

## 7. The booking flow (real Calendly integration)

Every "Book a Strategy Call" button points to `#book`, a section with a
real three-step flow (`script.js` → `initBookingFlow`):

1. The visitor fills out the contact form. Submitting it never claims a
   meeting is booked — it only validates and reveals step 2.
2. The real MedLead Partners Calendly page
   (`https://calendly.com/medleadpartners`) opens inline, embedded via
   Calendly's own widget script and prefilled with the name/email just
   entered. `#book`'s `data-calendly-url` attribute is the one place that
   URL lives — change it there to point at a different Calendly page.
3. Only once Calendly itself fires a `calendly.event_scheduled` message
   does the site show the "Strategy Call Scheduled" confirmation. Opening
   the scheduler in step 2 is never treated as a booking on its own.

This requires two external files loaded from `assets.calendly.com`
(`widget.css` and `widget.js`) — already linked in `index.html`'s
`<head>` and just before `</body>`, so no extra setup is needed.

## 8. Other external links

- **Instagram**: the footer's Instagram icon links to
  `https://www.instagram.com/medleadpartners/` and opens in a new tab.
  No action needed unless the URL changes.
- **Contact email**: `info@medleadpartners.com` is live in the footer as
  a `mailto:` link.
- **Other social links, Privacy Policy/Terms**: not included in this
  build because none were provided, nothing fake was added in their
  place. Search `index.html` for `footer-cta-block` and
  `footer-bottom-row` to find where these would go if added later.

## 9. Deploying to a standard web host

Upload all five items (`index.html`, `styles.css`, `script.js`, and the
`assets` folder with both images inside it) to your host, preserving
their relative positions exactly as they are in this folder. Most hosts
just need the contents of this folder placed at the site's root (or
whatever folder they serve as the site root, sometimes called `public/`
or `www/`, check your host's instructions for the exact folder name).
There is no build command to run first.

## 10. GitHub Pages compatibility

Yes. To deploy with GitHub Pages:
1. Create a GitHub repository (or use an existing one).
2. Upload the contents of this folder (`index.html`, `styles.css`,
   `script.js`, `assets/`) to the repository root, or to a `/docs`
   folder if you prefer that convention.
3. In the repository's Settings → Pages, set the source to the branch
   and folder you uploaded to.
4. GitHub gives you a URL (typically `https://[username].github.io/[repo]/`)
   once it finishes publishing, usually within a minute or two.

No configuration file is required for GitHub Pages to serve this project;
it's plain static files, which is exactly what Pages expects.

## 11. Making sure it behaves exactly like the current version

It already does, this isn't a rebuild. This export was produced by taking
the exact, already-tested current site and splitting its inlined CSS and
JavaScript into `styles.css` and `script.js`, and pointing the logo and
favicon at real image files instead of embedded data. No copy, layout,
color, font, or behavior was changed in that process.

Before this was handed to you, it was verified by:
- Serving these exact files over a local HTTP server (simulating GitHub
  Pages) and confirming zero console errors and zero failed asset
  requests.
- Opening `index.html` directly via `file://` with no server at all, and
  confirming the same: zero errors, zero failed requests, identical
  visual result.
- Clicking through: logo returning to the exact top of the page, all 5
  navigation links, the How It Works stage tabs, the Who We Serve
  practice-type pills (all 5, single-selection behavior confirmed), the
  FAQ accordion, the Instagram footer icon (correct URL, opens in a new
  tab), Back to Top, and the mobile hamburger menu (opens, closes,
  navigates, closes again).

If anything about this page's behavior differs from what you saw in
Claude, that would indicate something about the specific hosting
environment (server configuration, a browser extension, etc.) rather
than a difference in these files, since these are the identical files
that were just tested.

## What's in this folder vs. the `source/` subfolder

The five items at the top level (`index.html`, `styles.css`, `script.js`,
`assets/`) are the ready-to-deploy website, upload exactly these to your
host. The `source/` subfolder is a separate, optional system for making
future content edits more easily (plain-language content file, no HTML
editing required); it is not needed to deploy or run the site and your
host does not need it. See `source/README.md` for how it works.

## What's still a placeholder

Nothing was invented to fill these in. They're intentionally absent
rather than faked:
- Contact phone number
- Any social link besides Instagram
- Privacy Policy / Terms of Service pages
- Real client case studies or testimonials (one clearly-labeled
  fictional sample testimonial exists for design purposes only, marked
  "Sample client feedback" and "Illustrative Client. Sample Only.")
