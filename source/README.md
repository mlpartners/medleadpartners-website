# MedLead Partners — Website Project

## What to open

**`index.html`** is the finished website — the main entry point. It's a
single, self-contained file: no server, no build step, no external files
required to view it. Open it directly in a browser, or upload it to any
host later. This is the file that gets deployed or shared as-is.

Everything else in this folder is *source* — it exists to make future edits
easy, and produces `index.html` when run. It is not required to view the
site, only to modify it cleanly.

## Project structure

```
index.html         <- MAIN ENTRY POINT — the deployable website (open this)
content.py          <- all editable copy: headlines, FAQ, services, industries,
                        results framework, testimonials, footer/contact info
template.css         <- ALL CSS: colors, type, spacing, layout, responsive rules
template.js           <- ALL JavaScript: nav, tabs, accordions, mobile menu, form
build.py            <- assembles content.py + template.css + template.js
                        + assets/ into index.html
assets/
  logo.png           <- real MedLead Partners logo (source PNG)
  favicon.png         <- brand mark used for the browser tab icon (source PNG)
```

`index.html` itself has three inline parts, in this order: a `<style>`
block (the exact contents of `template.css`), the HTML body, and a
`<script>` block (the exact contents of `template.js`) just before
`</body>`. The logo and favicon are embedded as base64 `data:` URIs inside
the `<img>` tags and the `<link rel="icon">` tag — there are no separate
image files to go missing. Running `build.py` regenerates `index.html`
from the four source files below it; nothing is hand-maintained inside the
generated file itself.

## Technical overview — how it works

**It's a single-page site.** There is no server-side routing and no
separate pages. Every "page" a visitor might expect (How It Works, Results,
FAQ, etc.) is a `<section>` on the one page, each with a stable `id`
(`#how-it-works`, `#who-we-serve`, `#results`, `#about`, `#faq`, plus
`#home`, `#services`, and `#book` which aren't in the top nav but are
real, linkable sections).

**Navigation** (`template.js` → `initLogoHome`, `initScrollSpy`,
`initMobileMenu`):
- Nav links and the hero's "See How It Works" button are plain `<a
  href="#section-id">` anchors. `html { scroll-behavior: smooth; }` in
  `template.css` makes all of these scroll smoothly with zero JavaScript.
- The logo and the "Back to Top" button are handled in JS instead of a
  plain `#home` anchor, calling `window.scrollTo({top: 0, behavior:
  'smooth'})` directly — this guarantees an exact `scrollY: 0`, which a
  plain anchor jump to an element just below the sticky header would not
  quite reach.
- The active nav link is highlighted by `initScrollSpy`, which on every
  scroll event finds whichever section's top has crossed a fixed
  reference line just below the header, and toggles `.is-current` (plus
  `aria-current`) on the matching nav link. This is a direct geometry
  check rather than `IntersectionObserver`, specifically because
  `IntersectionObserver`'s batched callbacks can let a stale section "win"
  during a fast scroll — see the comment above `initScrollSpy` in
  `template.js` for the full reasoning.
- The mobile hamburger (`initMobileMenu`) toggles a `.is-open` class on
  `#mobile-menu`; selecting a link inside it also closes the menu before
  the page scrolls.

**Interactive sections** (`template.js` → `initRevealLists`,
`initTabGroup`):
- FAQ uses an accordion pattern: a `.reveal-list` containing `.reveal-item`s,
  each with a `.reveal-trigger` button and a `.reveal-panel`. Clicking a
  trigger toggles `.is-open` and animates `max-height` on its panel. Adding
  `data-single-open` to a `.reveal-list` makes opening one item close any
  other open item in that same list.
- "How It Works" and "Who We Serve" both use the same generic tab pattern
  (`initTabGroup`, called once per group as `initStageTabs` and
  `initPracticePills`): a row of buttons each carrying their text in
  `data-title`/`data-text` attributes, and one shared text panel below the
  row. Clicking a button swaps the panel's content and marks that button
  `.is-active`; there's no separate show/hide per item, so it's one small
  function instead of two nearly-identical ones. Visually they're styled
  differently, underlined tabs for How It Works, rounded pills for Who We
  Serve, so the two sections still read as distinct.
- The "What We Run" section is not interactive by design: it's a static
  vertical list of `<li class="service-pill">` elements beside a custom
  graphic. They're informational, not accordions or buttons, so there's
  no click handler, no cursor change, and no hover state at all, only a
  thin divider between rows. Only sections that are actually interactive
  (the How It Works tabs, the Who We Serve pills, the FAQ accordion)
  should visually suggest they respond to a click.
- The booking form (`initFormHandler`) intercepts `submit`, runs native
  HTML5 validation, and swaps the form for a static "thanks" message. It
  does not send data anywhere yet, see "What needs production wiring"
  below.

**Custom graphics.** All three illustrations (in How It Works, Services,
and Who We Serve) are hand-written inline SVG returned by small
Python functions in `build.py` (`render_system_flow_graphic`,
`render_acquisition_path_graphic`, `render_segmentation_graphic`).
They're plain shapes (circles, lines, rects) in
the brand's two colors, no image files, nothing that can 404.

**External dependencies.** There is exactly one: a `<link>` to
`fonts.googleapis.com`/`fonts.gstatic.com` to load Montserrat. This
requires the visitor to have internet access; if that's ever a concern,
the font-family fallback stack (`-apple-system, BlinkMacSystemFont,
sans-serif`) is already in place in `template.css` and the site remains
fully usable without Google Fonts loading, just in a different typeface.
Nothing else — no analytics, no tracking pixels, no third-party scripts —
is present anywhere in the code.

## How to make a change

**Changing words on the site** (FAQ answer, a service description, the hero
headline, footer contact info, etc.) → edit `content.py`, then run:

```
python3 build.py
```

That regenerates `index.html`. Nothing else needs to change.

**Changing how something looks** (color, spacing, type size) → edit
`template.css`, then rebuild the same way.

**Changing how something behaves** (what happens on click, tab switching,
the mobile menu) → edit `template.js`, then rebuild.

**Adding/removing/reordering a whole section** → edit the section functions in
`build.py` (each section — Hero, How It Works, Services, etc. — is one
function that reads its content from `content.py`).

If Python isn't available wherever you're editing, `index.html` can also be
hand-edited directly — it's plain HTML/CSS/JS with no build tooling required
to run it, only to regenerate it cleanly from source.

## Testimonials and case studies

`content.py` has two lists, `TESTIMONIALS` and `CASE_STUDIES`, that are
intentionally **empty** right now, because no real, verified client results
or testimonials exist yet. Nothing fabricated is shown in their place.

Each list has a documented schema in `content.py` (right above the empty
list). Add a real entry as a dict matching that schema, rebuild, and it
renders as a real proof card in the Results section, alongside (or in
place of) the sample testimonial. No redesign needed.

`content.py` → `RESULTS_FRAMEWORK` is the separate "What we track" grid
shown near the top of Results, always visible regardless of whether
`CASE_STUDIES` has entries. It's real, permanent content describing what
MedLead Partners actually measures (Lead Volume, Lead Quality, etc.), not
a placeholder, and it never shows numbers since none are verified yet.
It's deliberately kept lightweight (no border, no card) so it doesn't
compete visually with actual proof below it.

(The Results section also shows one fictional sample testimonial. See
"The one placeholder that IS visible" near the bottom of this file.)

## Technology badges

`content.py` → `CAPABILITY_BADGES` is a small list of internal capabilities
(Paid Advertising, CRM & Lead Management, etc.) rendered as a compact badge
row inside the How It Works section, alongside a small custom abstract
graphic. These are labeled as capabilities, not certifications or
partnerships — don't repurpose this list for third-party logos without
being certain no implied affiliation exists.

Each badge is a dict with a `label` and a `logo` field. `logo` is `None`
for all of them right now, which renders as a plain text badge (current
behavior). To add a real platform logo later, set `logo` to an image path
or data URI on that badge's entry — it will render inline automatically,
no redesign needed. Never add a logo in a way that implies a certification,
partnership, or endorsement that hasn't actually been established.

## Custom brand graphics

The site uses small, custom-made abstract SVG graphics instead of stock
photography — no external images to manage, nothing to break. There are
four, each a distinct composition so none of them repeat, all built from
the same visual language (black + brand blue, thin strokes, no gradients,
no icons/illustrations):

| Graphic | Function | Where |
|---|---|---|
| `render_system_flow_graphic()` | Ascending node-line + data bars, growth and progression | How It Works |
| `render_acquisition_path_graphic()` | Vertical process rail naming the five acquisition stages | Services |
| `render_segmentation_graphic()` | Clustered dots with a highlighted segment | Who We Serve |

All four live in `build.py` as small functions returning inline SVG, and
share one CSS frame (`template.css` → `.graphic-panel`) so they read as one
consistent family. To add another in the same style elsewhere, write a new
`render_..._graphic()` function following the same pattern (plain shapes,
brand colors only) and drop it into a `.graphic-panel` wrapper.

## The booking CTA

No real booking URL (Calendly or otherwise) has been provided yet. Every
"Book a Strategy Call" button on the site currently points to the in-page
booking form (`content.py` → `BOOKING_HREF = "#book"`), which is live and
functional right now. Once a real booking URL exists, change that one value
in `content.py` and rebuild — every button on the site updates from that
single source.

## What's intentionally not included yet — full checklist

Nothing below is broken; each item is a deliberate placeholder-free gap
(the site never shows fake data or a bracketed placeholder in its place).

| Item | Where in `content.py` | Current state |
|---|---|---|
| Real booking URL (Calendly, etc.) | `BOOKING_HREF` | Points to the in-page form at `#book`, which works right now |
| Booking form → CRM/backend | `render_booking()` in `build.py`, see the `DEV NOTE` comment in that function | Submits locally only; shows a static success message |
| Contact email | `CONTACT_EMAIL` | `None` — omitted from footer until set |
| Contact phone | `CONTACT_PHONE` | `None` — omitted from footer until set |
| Social links | `SOCIAL_LINKS` | Instagram is live and opens in a new tab. Add more entries the same way to add more platforms |
| Privacy Policy / Terms links | `LEGAL_LINKS` | Empty — the site never links to a page that doesn't exist |
| Real case studies | `CASE_STUDIES` | Empty — `RESULTS_FRAMEWORK` (real, permanent content) shows instead |
| Real client testimonials | `TESTIMONIALS` | Empty — one clearly-labeled fictional `SAMPLE_TESTIMONIAL` shows instead (see below) |
| Real technology/platform logos | `CAPABILITY_BADGES` (`logo` field on each entry) | All `None` — badges render as text only |
| Hosted Open Graph image | `render_head()` in `build.py` (see comment above the `og:image` tag) | Uses the embedded logo directly; most link-preview crawlers need a real hosted URL, not a data URI, once this is live somewhere |

### The one placeholder that IS visible: `SAMPLE_TESTIMONIAL`

The Results section shows one fictional, explicitly-labeled testimonial
(`content.py` → `SAMPLE_TESTIMONIAL`) so the testimonial component can be
seen with realistic content before real client feedback exists. It's
tagged "Sample client feedback: illustrative, not a verified review"
above the quote and "Illustrative Client. Sample Only." below the
attribution, and given a dashed border, so it can't be mistaken for a
real review. When real feedback exists: set `SAMPLE_TESTIMONIAL = None`
and add the real one to `TESTIMONIALS` instead.

## Social links

`content.py` → `SOCIAL_LINKS` is a list of dicts, each needing `label`,
`url`, `aria_label`, and optionally `icon`. If `icon` matches a key in
`build.py`'s `SOCIAL_ICONS` dict, it renders as a small circular icon link
(current behavior for Instagram); otherwise it falls back to a plain text
link. Every social link opens in a new tab (`target="_blank"` with
`rel="noopener noreferrer"`) and carries its own `aria-label` for
accessibility. To add another platform, add an SVG string to
`SOCIAL_ICONS` under a new key, then reference that key from a new entry
in `SOCIAL_LINKS`.

## Deployment

This project makes no assumptions about hosting. `index.html` is a static
file with everything (styles, scripts, logo, favicon) embedded inline — it
will work correctly wherever it's ultimately placed. No platform-specific
configuration has been added, since that decision hasn't been made yet.
