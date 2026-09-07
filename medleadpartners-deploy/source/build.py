"""
MEDLEAD PARTNERS. BUILD SCRIPT
==================================================
Assembles the single deployable index.html from:
  content.py     -> what the site says (edit this for copy changes)
  template.css   -> how the site looks (edit this for visual changes)
  template.js     -> how the site behaves (edit this for interaction changes)
  assets/logo.png, assets/favicon.png -> the real brand image files

Run:
    python3 build.py

Output:
    index.html, a single, self-contained file with no external
    dependencies except the Google Fonts stylesheet link. This is the
    file you deploy or share; everything else in this folder is source.
"""

import base64
import html
import os
import sys
import shutil

import content as c

ROOT = os.path.dirname(os.path.abspath(__file__))


def data_uri(path, mime="image/png"):
    with open(os.path.join(ROOT, path), "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{b64}"


with open(os.path.join(ROOT, "template.css"), "r") as f:
    CSS = f.read()
with open(os.path.join(ROOT, "template.js"), "r") as f:
    JS = f.read()

# ==========================================================================
# BUILD MODE
#
# "inline" (default, `python3 build.py`): produces a single self-contained
#   index.html in THIS folder — CSS/JS inlined, logo/favicon as base64.
#   This is the file to open directly or hand-edit; see README.
#
# "deploy" (`python3 build.py --deploy <dir>`): produces a plain static
#   deployment bundle in <dir> — styles.css / script.js as real linked
#   files, assets/logo.png + assets/favicon.png as real image files.
#   Both modes are generated from the exact same content.py / build.py /
#   template.css / template.js, so they can never drift out of sync.
# ==========================================================================
DEPLOY = "--deploy" in sys.argv
if DEPLOY:
    idx = sys.argv.index("--deploy")
    OUT_DIR = os.path.abspath(sys.argv[idx + 1]) if len(sys.argv) > idx + 1 else os.path.join(ROOT, "..", "deploy")
else:
    OUT_DIR = ROOT

if DEPLOY:
    LOGO_SRC = "assets/logo.png"
    FAVICON_SRC = "assets/favicon.png"
    APPLE_ICON_SRC = "assets/apple-touch-icon.png"
else:
    LOGO_SRC = data_uri("assets/logo.png")
    FAVICON_SRC = data_uri("assets/favicon.png")
    APPLE_ICON_SRC = data_uri("assets/apple-touch-icon.png")

# Backwards-compatible aliases used throughout the render_* functions below.
LOGO_URI = LOGO_SRC
FAVICON_URI = FAVICON_SRC
APPLE_ICON_URI = APPLE_ICON_SRC


# ==========================================================================
# SMALL RENDER HELPERS
# ==========================================================================

def nav_links(link_class="", home=""):
    # `home` is the relative path back to index.html: "" when this link is
    # rendered on the homepage itself (so plain "#section" anchors work),
    # or "index.html" when rendered on a different page (privacy.html etc.),
    # so the link becomes "index.html#section" instead of a dead "#section"
    # that would just scroll a page with no matching id.
    return "\n        ".join(
        f'<a href="{home}#{sid}" class="{link_class}">{label}</a>' for sid, label in c.NAV
    )


def render_head(page_title=None, page_description=None, canonical_path="", noindex=False, og_type="website", include_calendly=True, og_title=None):
    """Shared <head> for every page. canonical_path is the page's own path
    relative to the site root ("" for the homepage, "privacy.html" for the
    privacy page, etc.) — used to build the canonical link and og:url from
    content.py's SITE_URL. Update SITE_URL there once the real domain is live.
    include_calendly should be False for any page that doesn't render the
    booking widget (privacy/terms/404) — no reason to load Calendly's
    stylesheet on a page that will never use it.
    page_title is the literal <title> element (the browser tab). og_title is
    what's shown in social-share previews (og:title/twitter:title) — kept as
    a separate parameter so the homepage can have a bare "MedLead Partners"
    tab title while social previews stay descriptive. Defaults to page_title
    when not given, so every other page's behavior is unchanged."""
    page_title = page_title or c.PAGE_TITLE
    og_title = og_title or page_title
    page_description = page_description or c.SITE_DESCRIPTION
    canonical_url = f"{c.SITE_URL}/{canonical_path}" if canonical_path else f"{c.SITE_URL}/"

    # og:image needs an absolute URL — social platforms generally won't
    # resolve a relative path or fetch a base64 data URI. In deploy mode
    # this becomes a real hosted URL once SITE_URL is the live domain; in
    # inline/self-contained mode we fall back to the embedded logo so the
    # tag is still valid for local viewing.
    og_image = f"{c.SITE_URL}/assets/logo.png" if DEPLOY else LOGO_URI

    css_block = (
        '<link rel="stylesheet" href="styles.css">'
        if DEPLOY
        else f"<style>\n{CSS}\n</style>"
    )
    robots_tag = (
        '<meta name="robots" content="noindex, nofollow">'
        if noindex
        else '<meta name="robots" content="index, follow">'
    )
    calendly_css = (
        '<!-- Calendly\'s stylesheet for the real, inline scheduling widget used in the\n'
        '     booking flow (see #book section). This is the one additional external\n'
        '     dependency the real Calendly integration requires. -->\n'
        '<link href="https://assets.calendly.com/assets/external/widget.css" rel="stylesheet">\n'
        if include_calendly else ""
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{html.escape(page_title)}</title>
<meta name="description" content="{html.escape(page_description)}">
{robots_tag}
<link rel="canonical" href="{canonical_url}">

<!-- Open Graph / social link preview. -->
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="MedLead Partners">
<meta property="og:url" content="{canonical_url}">
<meta property="og:title" content="{html.escape(og_title)}">
<meta property="og:description" content="{html.escape(page_description)}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(og_title)}">
<meta name="twitter:description" content="{html.escape(page_description)}">
<meta name="twitter:image" content="{og_image}">

<link rel="icon" type="image/png" href="{FAVICON_URI}">
<link rel="apple-touch-icon" href="{APPLE_ICON_URI}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">
{calendly_css}{css_block}
</head>
<body>
"""


def render_header(home=""):
    return f"""
  <header class="site-header" id="site-header">
    <div class="container nav-inner">
      <a href="{home}#home" class="logo-link" aria-label="MedLead Partners home">
        <img src="{LOGO_URI}" alt="MedLead Partners logo" class="logo-img" width="112" height="32">
      </a>
      <nav class="primary-nav" id="primary-nav" aria-label="Primary">
        {nav_links(home=home)}
      </nav>
      <a href="{home}{c.BOOKING_HREF}" class="btn btn-primary nav-cta">{c.PRIMARY_CTA_LABEL}</a>
      <button class="menu-toggle" id="menu-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu">
        <span></span><span></span><span></span>
      </button>
    </div>
    <div class="mobile-menu" id="mobile-menu">
      {nav_links(home=home)}
      <a href="{home}{c.BOOKING_HREF}" class="btn btn-primary mobile-cta">{c.PRIMARY_CTA_LABEL}</a>
    </div>
  </header>
"""


def render_hero():
    return f"""
  <main>
    <section class="hero" id="home" data-nav-section>
      <div class="hero-watermark" aria-hidden="true">+</div>
      <div class="container hero-inner">
        <h1>{c.HERO_HEADLINE}</h1>
        <p class="hero-sub">{c.HERO_SUBHEAD}</p>
        <div class="hero-actions">
          <!-- CTA target comes from content.py's BOOKING_HREF. It currently points to the
               in-page booking form at #book, which is live and functional now. Update
               BOOKING_HREF in content.py once a real Calendly/booking URL exists. -->
          <a href="{c.BOOKING_HREF}" class="btn btn-primary">{c.PRIMARY_CTA_LABEL}</a>
        </div>
      </div>
    </section>
"""


def render_how_it_works():
    tabs = "\n          ".join(
        f'<button class="stage-tab" data-title="{s["title"]}" data-text="{s["text"]}" role="tab">'
        f'<span class="num">{s["num"]}</span>{s["title"]}</button>'
        for s in c.SYSTEM_STAGES
    )
    first = c.SYSTEM_STAGES[0]

    return f"""
    <section class="section section-tint" id="how-it-works" data-nav-section>
      <div class="container">
        <div class="section-head">
          <h2 class="marker"><span class="plus">+</span> How It Works</h2>
          <p class="section-intro">{c.HOW_IT_WORKS_INTRO}</p>
        </div>

        <div class="stage-tabs" role="tablist" aria-label="Patient acquisition system stages">
          {tabs}
        </div>

        <div class="stage-panel">
          <div class="stage-panel-title" id="stage-panel-title">{first["title"]}</div>
          <p class="stage-panel-text" id="stage-panel-text">{first["text"]}</p>
        </div>
      </div>
    </section>
"""


def render_acquisition_path_graphic():
    """Custom abstract visual for What We Run: a vertical process rail
    naming the five stages MedLead Partners actually operates, ending in
    a highlighted appointment node. Deliberately vertical (not the
    ascending growth-line or funnel used elsewhere) so it mirrors the
    stacked service pills beside it and reads as one composition."""
    stages = ["Traffic", "Lead Capture", "Qualification", "Follow-Up", "Appointment"]
    ys = [26, 88, 150, 212, 274]
    cx = 28

    line = f'<line x1="{cx}" y1="{ys[0]}" x2="{cx}" y2="{ys[-1]}" stroke="#E4E7EE" stroke-width="2"/>'
    progress_line = f'<line x1="{cx}" y1="{ys[0]}" x2="{cx}" y2="{ys[-1]}" stroke="#6893EF" stroke-width="2" opacity="0.35"/>'

    nodes = []
    for i, (y, label) in enumerate(zip(ys, stages)):
        is_last = i == len(ys) - 1
        r = 9 if is_last else 6
        fill = "#6893EF" if is_last else "#000"
        opacity = "1" if is_last else "0.65"
        weight = "700" if is_last else "600"
        text_fill = "#000" if is_last else "#52566B"
        nodes.append(
            f'<circle cx="{cx}" cy="{y}" r="{r}" fill="{fill}" opacity="{opacity}"/>'
            f'<text x="{cx + 24}" y="{y + 5}" font-size="14" font-weight="{weight}" fill="{text_fill}">{label}</text>'
        )

    return f"""<svg viewBox="0 0 220 300" role="img" aria-label="The five stages MedLead Partners runs: traffic, lead capture, qualification, follow-up, and appointment">
        {line}
        {progress_line}
        {"".join(nodes)}
      </svg>"""


def render_services():
    pills = "\n          ".join(
        f'<li class="service-pill"><span class="service-pill-dot" aria-hidden="true"></span>{item}</li>'
        for item in c.WHAT_WE_RUN_ITEMS
    )

    return f"""
    <section class="section" id="services">
      <div class="container">
        <div class="section-head">
          <h2 class="marker"><span class="plus">+</span> What We Run</h2>
          <p class="section-intro">{c.SERVICES_INTRO}</p>
        </div>
        <div class="services-system">
          <div class="graphic-panel services-system-visual">{render_acquisition_path_graphic()}</div>
          <ul class="service-pills">
            {pills}
          </ul>
        </div>
      </div>
    </section>
"""


def render_segmentation_graphic():
    """Custom abstract visual for Who We Serve: a loose cluster of
    practice 'types' with one segment highlighted, suggesting matching
    the system to the right kind of practice. Distinct composition from
    the growth-line and interface-panel graphics used elsewhere."""
    positions = [
        (40, 40), (78, 30), (112, 48), (58, 78), (96, 90),
        (140, 34), (150, 76), (34, 108), (120, 116),
    ]
    highlighted = {0, 3, 7}
    dots = "\n        ".join(
        f'<circle cx="{x}" cy="{y}" r="7" fill="{"#6893EF" if i in highlighted else "#000"}" '
        f'opacity="{1 if i in highlighted else 0.22}"/>'
        for i, (x, y) in enumerate(positions)
    )
    return f"""<svg viewBox="0 0 180 150" role="img" aria-label="Abstract diagram of practice types, with a matched segment highlighted">
        <circle cx="58" cy="72" r="46" fill="none" stroke="#6893EF" stroke-width="1.5" stroke-dasharray="4 5" opacity="0.5"/>
        {dots}
      </svg>"""


def render_who_we_serve():
    pills = "\n          ".join(
        f'<button class="practice-pill" data-title="{ind["label"]}" data-text="{ind["text"]}">{ind["label"]}</button>'
        for ind in c.INDUSTRIES
    )
    first = c.INDUSTRIES[0]

    return f"""
    <section class="section section-tint" id="who-we-serve" data-nav-section>
      <div class="container">
        <div class="head-split">
          <div>
            <h2 class="marker"><span class="plus">+</span> Who We Serve</h2>
            <p class="section-intro">{c.WHO_WE_SERVE_INTRO}</p>
          </div>
          <div class="graphic-panel head-split-visual">{render_segmentation_graphic()}</div>
        </div>

        <div class="practice-pills" role="tablist" aria-label="Practice types MedLead Partners serves">
          {pills}
        </div>

        <div class="practice-panel">
          <div class="practice-panel-title" id="practice-panel-title">{first["label"]}</div>
          <p class="practice-panel-text" id="practice-panel-text">{first["text"]}</p>
        </div>
      </div>
    </section>
"""


def render_case_study_card(cs):
    """Render one real, verified case study."""
    metric_html = f'<div class="case-metric">{cs["metric"]}</div>' if cs.get("metric") else ""
    return f"""<article class="case-card case-card-real">
          <span class="case-tag">{html.escape(cs.get("practice", ""))}</span>
          <h3>{html.escape(cs.get("title", ""))}</h3>
          <dl class="case-fields">
            <dt>Challenge</dt><dd>{html.escape(cs.get("challenge", ""))}</dd>
            <dt>Strategy</dt><dd>{html.escape(cs.get("strategy", ""))}</dd>
            <dt>Results</dt><dd>{html.escape(cs.get("results", ""))}</dd>
          </dl>
          {metric_html}
        </article>"""


def render_testimonial_card(t):
    photo_html = f'<img src="{t["photo"]}" alt="" class="testimonial-photo">' if t.get("photo") else '<div class="testimonial-photo testimonial-photo-placeholder" aria-hidden="true"></div>'
    logo_html = f'<img src="{t["logo"]}" alt="{html.escape(t.get("practice",""))} logo" class="testimonial-logo">' if t.get("logo") else ""
    return f"""<figure class="testimonial-card">
          <blockquote>&ldquo;{html.escape(t["quote"])}&rdquo;</blockquote>
          <figcaption>
            {photo_html}
            <div>
              <div class="testimonial-name">{html.escape(t["name"])}</div>
              <div class="testimonial-role">{html.escape(t.get("title",""))}{", " if t.get("title") and t.get("practice") else ""}{html.escape(t.get("practice",""))}</div>
            </div>
            {logo_html}
          </figcaption>
        </figure>"""


def render_sample_testimonial_card():
    t = c.SAMPLE_TESTIMONIAL
    return f"""<figure class="testimonial-card sample-testimonial">
          <span class="case-tag">Sample client feedback: illustrative, not a verified review</span>
          <blockquote>&ldquo;{html.escape(t["quote"])}&rdquo;</blockquote>
          <figcaption>
            <div>
              <div class="testimonial-name">{html.escape(t["name"])}</div>
              <div class="testimonial-role">{html.escape(t["title"])}</div>
              <div class="testimonial-disclaimer">{t["disclaimer"]}</div>
            </div>
          </figcaption>
        </figure>"""


def render_results_and_about():
    track_items = "\n          ".join(
        f'<div class="track-item"><div class="track-label">{item["label"]}</div>'
        f'<p class="track-text">{item["text"]}</p></div>'
        for item in c.RESULTS_FRAMEWORK
    )

    proof_cards = []
    if c.CASE_STUDIES:
        proof_cards.extend(render_case_study_card(cs) for cs in c.CASE_STUDIES)
    if c.TESTIMONIALS:
        proof_cards.extend(render_testimonial_card(t) for t in c.TESTIMONIALS)
    elif c.SAMPLE_TESTIMONIAL:
        # Temporary/fictional. See the SAMPLE_TESTIMONIAL comment in content.py.
        proof_cards.append(render_sample_testimonial_card())

    if c.CASE_STUDIES or c.TESTIMONIALS:
        proof_html = f'<div class="proof-grid">{"".join(proof_cards)}</div>'
    else:
        # No verified case study exists yet. Say so in plain text (no
        # bordered box) rather than a second placeholder card next to
        # the sample testimonial.
        proof_html = f"""<p class="proof-note">Verified case studies will appear here as client results come in.</p>
        <div class="proof-single">{"".join(proof_cards)}</div>"""

    # Results and About share one section wrapper (one set of top/bottom
    # padding instead of two) since both are now short, adjacent ideas —
    # trust/credibility and why the system matters. Each keeps its own
    # id so nav anchors (#results, #about) still work independently.
    return f"""
    <section class="section">
      <div class="container">
        <div id="results" class="section-head" data-nav-section>
          <h2 class="marker"><span class="plus">+</span> Results</h2>
          <p class="section-intro">{c.RESULTS_INTRO}</p>
        </div>

        <h3 class="track-heading">What we track</h3>
        <div class="track-grid">
          {track_items}
        </div>

        {proof_html}

        <div class="results-divider"></div>

        <div id="about" class="section-head" data-nav-section>
          <h2 class="marker"><span class="plus">+</span> About</h2>
          <p class="section-intro">{c.ABOUT_INTRO}</p>
        </div>
      </div>
    </section>
"""


def render_faq():
    items = "\n          ".join(
        f"""<div class="reveal-item">
            <button class="reveal-trigger" aria-expanded="false"><span class="reveal-label">{q}</span><span class="reveal-icon" aria-hidden="true"></span></button>
            <div class="reveal-panel"><div class="reveal-panel-inner"><p>{a}</p></div></div>
          </div>"""
        for q, a in c.FAQ_ITEMS
    )
    return f"""
    <section class="section" id="faq" data-nav-section>
      <div class="container container-narrow">
        <div class="section-head">
          <h2 class="marker"><span class="plus">+</span> FAQ</h2>
        </div>
        <div class="reveal-list no-nums" data-single-open>
          {items}
        </div>
      </div>
    </section>
"""


def render_booking():
    options = "\n                ".join(
        f'<option value="{val}">{label}</option>' for val, label in c.PRACTICE_TYPE_OPTIONS
    )
    return f"""
    <section class="final-cta">
      <div class="container">
        <h2>{c.FINAL_CTA_HEADLINE}</h2>
      </div>
    </section>

    <!-- Booking flow: three mutually-exclusive steps, one visible at a time.
         Only #booking-step-form is ever a claim-free contact form. Step 2
         opens the REAL Calendly scheduler (content.py CALENDLY_URL) inline;
         opening it is not a booking confirmation. Step 3 (the only step
         that says a call is scheduled) renders only after Calendly itself
         fires "calendly.event_scheduled" — see initBookingFlow() in
         template.js. data-calendly-url is the single source of truth the
         JS reads from, so the URL only has to change in content.py. -->
    <section class="section section-tint" id="book" data-calendly-url="{c.CALENDLY_URL}">
      <div class="container container-narrow">

        <div class="booking-step" id="booking-step-form">
          <div class="section-head">
            <h2>{c.BOOKING_HEADLINE}</h2>
            <p class="section-intro">{c.BOOKING_SUBHEAD}</p>
          </div>

          <form class="lead-form" id="lead-form" novalidate>
            <!-- Honeypot spam-protection field: invisible to real visitors (CSS + tabindex="-1"),
                 but a plain, generic-looking form field to automated bots that fill in every
                 input they find. If it comes back non-empty, initBookingFlow() in template.js
                 silently blocks the submission rather than opening the scheduler. -->
            <div class="hp-field" aria-hidden="true">
              <label for="hp-website">Leave this field blank</label>
              <input type="text" id="hp-website" name="hp-website" tabindex="-1" autocomplete="off">
            </div>
            <div class="form-row">
              <div class="field"><label for="name">Name <span class="req">*</span></label><input type="text" id="name" name="name" required autocomplete="name" maxlength="100"></div>
              <div class="field"><label for="business">Business <span class="req">*</span></label><input type="text" id="business" name="business" required autocomplete="organization" maxlength="120"></div>
            </div>
            <div class="form-row">
              <div class="field"><label for="email">Email <span class="req">*</span></label><input type="email" id="email" name="email" required autocomplete="email" maxlength="200"></div>
              <div class="field"><label for="phone">Phone <span class="req">*</span></label><input type="tel" id="phone" name="phone" required autocomplete="tel" inputmode="tel" pattern="[0-9\\s\\-\\+\\(\\)]{{7,20}}" maxlength="20"></div>
            </div>
            <div class="form-row">
              <div class="field"><label for="website">Website</label><input type="url" id="website" name="website" placeholder="Optional" autocomplete="url" maxlength="200"></div>
              <div class="field">
                <label for="practice-type">Practice Type <span class="req">*</span></label>
                <select id="practice-type" name="practice-type" required>
                  <option value="" selected disabled>Select one</option>
                  {options}
                </select>
              </div>
            </div>
            <div class="field"><label for="challenge">Biggest Growth Challenge</label><textarea id="challenge" name="challenge" rows="3" placeholder="Optional" maxlength="1000"></textarea></div>
            <button type="submit" class="btn btn-primary btn-full">{c.CONFIRM_BUTTON_LABEL}</button>
            <!-- DEV NOTE (not shown to visitors): this form's details currently stay in the
                 browser only (used to prefill Calendly in Step 2). Wire the submit handler in
                 template.js (initBookingFlow) to a real CRM/email endpoint once one exists, so
                 practice details are captured even if a visitor doesn't finish scheduling. -->
          </form>
        </div>

        <div class="booking-step" id="booking-step-schedule" hidden tabindex="-1">
          <div class="section-head">
            <h2>{c.SCHEDULING_HEADLINE}</h2>
            <p class="section-intro">{c.SCHEDULING_SUBHEAD}</p>
          </div>
          <div class="calendly-container calendly-inline-widget" id="calendly-container">
            <p class="calendly-loading-note">Loading the scheduler&hellip;</p>
          </div>
          <div class="calendly-fallback" id="calendly-fallback" hidden>
            <p class="calendly-fallback-text">Having trouble loading the scheduler above?</p>
            <a href="{c.CALENDLY_URL}" target="_blank" rel="noopener noreferrer" class="btn btn-secondary calendly-fallback-btn">Open Scheduler in a New Tab</a>
          </div>
        </div>

        <div class="form-success booking-step" id="booking-step-confirmed" hidden tabindex="-1">
          <h3>{c.CONFIRMATION_HEADLINE}</h3>
          <p>{c.CONFIRMATION_TEXT}</p>
        </div>

      </div>
    </section>
  </main>

<!-- Calendly's widget script powers the real inline scheduler in Step 2 above (initBookingFlow
     in template.js calls window.Calendly.initInlineWidget once the lead form validates).
     onerror sets a flag so initBookingFlow can show the fallback link immediately if the
     script itself is blocked (ad blocker, corporate network) rather than waiting out the
     full timeout meant for "script loaded but the embed still didn't render" cases. -->
<script src="https://assets.calendly.com/assets/external/widget.js" onerror="window.__calendlyLoadFailed = true;"></script>
"""


def render_back_to_top():
    return """
  <button id="back-to-top" class="back-to-top" aria-label="Back to top">
    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
  </button>
"""


def render_floating_cta():
    # Small floating pill, fixed to the viewport. JS (initFloatingCta in
    # template.js) toggles .is-visible: hidden until the visitor scrolls
    # past the hero, and hidden again once the final-CTA/booking area
    # scrolls into view, so it never competes with the "Book a Strategy
    # Call" buttons already there. Positioned above #back-to-top so the
    # two never overlap.
    return f"""
  <a href="{c.BOOKING_HREF}" class="floating-cta" id="floating-cta">
    <span>{c.PRIMARY_CTA_LABEL}</span>
  </a>
"""


SOCIAL_ICONS = {
    "instagram": (
        '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" aria-hidden="true">'
        '<rect x="2" y="2" width="20" height="20" rx="5.5" stroke="currentColor" stroke-width="1.8"/>'
        '<circle cx="12" cy="12" r="4.6" stroke="currentColor" stroke-width="1.8"/>'
        '<circle cx="17.3" cy="6.7" r="1.15" fill="currentColor"/>'
        '</svg>'
    ),
    "facebook": (
        '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" aria-hidden="true">'
        '<rect x="2" y="2" width="20" height="20" rx="5.5" stroke="currentColor" stroke-width="1.8"/>'
        '<path d="M13.8 18.2V12.4H15.75L16.05 10.05H13.8V8.55C13.8 7.89 13.98 7.44 14.93 7.44H16.13V5.34C15.93 5.31 15.24 5.25 14.44 5.25C12.77 5.25 11.62 6.27 11.62 8.14V10.05H9.75V12.4H11.62V18.2H13.8Z" fill="currentColor"/>'
        '</svg>'
    ),
}


def render_social_link(s):
    icon = SOCIAL_ICONS.get(s.get("icon"))
    aria_label = s.get("aria_label", s["label"])
    inner = icon if icon else s["label"]
    css_class = "footer-social-icon" if icon else ""
    return (
        f'<a href="{s["url"]}" class="{css_class}" target="_blank" rel="noopener noreferrer" '
        f'aria-label="{aria_label}">{inner}</a>'
    )


def render_footer(home=""):
    nav_row = f' <span class="footer-nav-sep" aria-hidden="true">+</span> '.join(
        f'<a href="{home}#{sid}">{label}</a>' for sid, label in c.NAV
    )

    contact_bits = []
    if c.CONTACT_EMAIL:
        contact_bits.append(f'<a href="mailto:{c.CONTACT_EMAIL}">{c.CONTACT_EMAIL}</a>')
    if c.CONTACT_PHONE:
        contact_bits.append(f'<a href="tel:{c.CONTACT_PHONE}">{c.CONTACT_PHONE}</a>')
    contact_html = ""
    if contact_bits:
        contact_html = f'<div class="footer-contact-line">{" &middot; ".join(contact_bits)}</div>'

    social_html = ""
    if c.SOCIAL_LINKS:
        links = " ".join(render_social_link(s) for s in c.SOCIAL_LINKS)
        social_html = f'<div class="footer-social">{links}</div>'

    legal_html = ""
    if c.LEGAL_LINKS:
        links = "\n          ".join(f'<a href="{l["url"]}">{l["label"]}</a>' for l in c.LEGAL_LINKS)
        legal_html = f'<div class="footer-legal">\n          {links}\n        </div>'

    return f"""
  <footer class="site-footer">
    <div class="container">
      <div class="footer-top">
        <div class="footer-brand-block">
          <img src="{LOGO_URI}" alt="MedLead Partners logo" class="footer-logo-lg" width="112" height="32">
          <p class="footer-tagline">{c.FOOTER_TAGLINE}</p>
          {contact_html}
          {social_html}
        </div>
        <div class="footer-cta-block">
          <span class="footer-cta-label">Ready to talk?</span>
          <a href="{home}{c.BOOKING_HREF}" class="btn btn-primary">{c.PRIMARY_CTA_LABEL}</a>
        </div>
      </div>

      <nav class="footer-nav-row">
        {nav_row}
      </nav>

      <div class="footer-divider"></div>

      <div class="footer-bottom-row">
        <p>&copy; <span id="year"></span> {c.COPYRIGHT_HOLDER}. All rights reserved.</p>
        {legal_html}
      </div>
    </div>
  </footer>

{'<script src="script.js"></script>' if DEPLOY else f'<script>{chr(10)}{JS}{chr(10)}</script>'}
</body>
</html>
"""


def render_legal_page(page_title, page_description, canonical_path, heading, sections):
    """Shared renderer for Privacy Policy and Terms & Conditions — same
    header/footer as the homepage (with home="index.html" so nav/logo/CTA
    links point back correctly), a simple heading + "last updated" line,
    and a stack of (heading, body_html) sections using the site's existing
    typographic styles. No new visual language introduced."""
    body = "\n        ".join(
        f'<div class="legal-section"><h2>{h}</h2><p>{text}</p></div>'
        for h, text in sections
    )
    return f"""{render_head(page_title, page_description, canonical_path, include_calendly=False)}{render_header(home="index.html")}
  <main>
    <section class="section legal-page" id="top">
      <div class="container container-narrow">
        <div class="section-head">
          <h1>{heading}</h1>
          <p class="section-intro">Last updated: {c.LAST_UPDATED}</p>
        </div>
        {body}
      </div>
    </section>
  </main>
{render_footer(home="index.html")}"""


def render_404_page():
    """A real, working page — GitHub Pages automatically serves this for any
    unmatched path when a file named 404.html sits at the site root, no
    extra configuration needed. noindex since it's not a real destination."""
    return f"""{render_head(c.NOT_FOUND_TITLE, c.NOT_FOUND_TEXT, "404.html", noindex=True, include_calendly=False)}{render_header(home="index.html")}
  <main>
    <section class="section not-found">
      <div class="container container-narrow" style="text-align:center;">
        <p class="not-found-code" aria-hidden="true">404</p>
        <h1>{c.NOT_FOUND_HEADLINE}</h1>
        <p class="section-intro" style="margin-left:auto;margin-right:auto;">{c.NOT_FOUND_TEXT}</p>
        <div class="not-found-actions">
          <a href="index.html" class="btn btn-primary">Back to Homepage</a>
          <a href="index.html{c.BOOKING_HREF}" class="btn btn-secondary">{c.PRIMARY_CTA_LABEL}</a>
        </div>
      </div>
    </section>
  </main>
{render_footer(home="index.html")}"""


def render_sitemap():
    pages = ["", "privacy.html", "terms.html"]  # 404.html is deliberately excluded — not a real destination
    urls = "\n".join(
        f"""  <url>
    <loc>{c.SITE_URL}/{p}</loc>
    <changefreq>monthly</changefreq>
    <priority>{"1.0" if p == "" else "0.5"}</priority>
  </url>"""
        for p in pages
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
"""


def render_robots():
    return f"""User-agent: *
Allow: /

Sitemap: {c.SITE_URL}/sitemap.xml
"""


def build():
    parts = [
        render_head(og_title=c.SITE_TITLE),
        render_header(),
        render_hero(),
        render_how_it_works(),
        render_services(),
        render_who_we_serve(),
        render_results_and_about(),
        render_faq(),
        render_booking(),
        render_back_to_top(),
        render_floating_cta(),
        render_footer(),
    ]
    output = "".join(parts)

    privacy_html = render_legal_page(
        c.PRIVACY_TITLE, c.PRIVACY_DESCRIPTION, "privacy.html", "Privacy Policy", c.PRIVACY_SECTIONS
    )
    terms_html = render_legal_page(
        c.TERMS_TITLE, c.TERMS_DESCRIPTION, "terms.html", "Terms & Conditions", c.TERMS_SECTIONS
    )
    not_found_html = render_404_page()
    sitemap_xml = render_sitemap()
    robots_txt = render_robots()

    if DEPLOY:
        os.makedirs(OUT_DIR, exist_ok=True)
        os.makedirs(os.path.join(OUT_DIR, "assets"), exist_ok=True)
        with open(os.path.join(OUT_DIR, "index.html"), "w") as f:
            f.write(output)
        with open(os.path.join(OUT_DIR, "privacy.html"), "w") as f:
            f.write(privacy_html)
        with open(os.path.join(OUT_DIR, "terms.html"), "w") as f:
            f.write(terms_html)
        with open(os.path.join(OUT_DIR, "404.html"), "w") as f:
            f.write(not_found_html)
        with open(os.path.join(OUT_DIR, "sitemap.xml"), "w") as f:
            f.write(sitemap_xml)
        with open(os.path.join(OUT_DIR, "robots.txt"), "w") as f:
            f.write(robots_txt)
        with open(os.path.join(OUT_DIR, "styles.css"), "w") as f:
            f.write(CSS)
        with open(os.path.join(OUT_DIR, "script.js"), "w") as f:
            f.write(JS)
        shutil.copyfile(os.path.join(ROOT, "assets/logo.png"), os.path.join(OUT_DIR, "assets/logo.png"))
        shutil.copyfile(os.path.join(ROOT, "assets/favicon.png"), os.path.join(OUT_DIR, "assets/favicon.png"))
        shutil.copyfile(os.path.join(ROOT, "assets/apple-touch-icon.png"), os.path.join(OUT_DIR, "assets/apple-touch-icon.png"))
        print(f"Built deploy bundle in {OUT_DIR}")
        print("  index.html, privacy.html, terms.html, 404.html, sitemap.xml, robots.txt, styles.css, script.js, assets/")
    else:
        for name, content_ in [
            ("index.html", output),
            ("privacy.html", privacy_html),
            ("terms.html", terms_html),
            ("404.html", not_found_html),
            ("sitemap.xml", sitemap_xml),
            ("robots.txt", robots_txt),
        ]:
            with open(os.path.join(ROOT, name), "w") as f:
                f.write(content_)
        print(f"Built index.html ({len(output):,} bytes) + privacy.html + terms.html + 404.html + sitemap.xml + robots.txt")


if __name__ == "__main__":
    build()
