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

import content as c

ROOT = os.path.dirname(os.path.abspath(__file__))


def data_uri(path, mime="image/png"):
    with open(os.path.join(ROOT, path), "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{b64}"


LOGO_URI = data_uri("assets/logo.png")
FAVICON_URI = data_uri("assets/favicon.png")

with open(os.path.join(ROOT, "template.css"), "r") as f:
    CSS = f.read()
with open(os.path.join(ROOT, "template.js"), "r") as f:
    JS = f.read()


# ==========================================================================
# SMALL RENDER HELPERS
# ==========================================================================

def nav_links(link_class=""):
    return "\n        ".join(
        f'<a href="#{sid}" class="{link_class}">{label}</a>' for sid, label in c.NAV
    )


def render_head():
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(c.SITE_TITLE)}</title>
<meta name="description" content="{html.escape(c.SITE_DESCRIPTION)}">

<!-- Open Graph / social link preview foundation.
     og:image is embedded as the actual brand logo (base64) so the foundation works today;
     once the site is hosted, replace it with a hosted absolute image URL. Most link-preview
     crawlers (Slack, iMessage, LinkedIn, etc.) will not fetch a base64 data URI. -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="MedLead Partners">
<meta property="og:title" content="{html.escape(c.SITE_TITLE)}">
<meta property="og:description" content="{html.escape(c.SITE_DESCRIPTION)}">
<meta property="og:image" content="{LOGO_URI}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(c.SITE_TITLE)}">
<meta name="twitter:description" content="{html.escape(c.SITE_DESCRIPTION)}">
<meta name="twitter:image" content="{LOGO_URI}">

<link rel="icon" type="image/png" href="{FAVICON_URI}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
{CSS}
</style>
</head>
<body>
"""


def render_header():
    return f"""
  <header class="site-header" id="site-header">
    <div class="container nav-inner">
      <a href="#home" class="logo-link" aria-label="MedLead Partners home">
        <img src="{LOGO_URI}" alt="MedLead Partners logo" class="logo-img">
      </a>
      <nav class="primary-nav" id="primary-nav" aria-label="Primary">
        {nav_links()}
      </nav>
      <a href="{c.BOOKING_HREF}" class="btn btn-primary nav-cta">{c.PRIMARY_CTA_LABEL}</a>
      <button class="menu-toggle" id="menu-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu">
        <span></span><span></span><span></span>
      </button>
    </div>
    <div class="mobile-menu" id="mobile-menu">
      {nav_links()}
      <a href="{c.BOOKING_HREF}" class="btn btn-primary mobile-cta">{c.PRIMARY_CTA_LABEL}</a>
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
          <a href="{c.HERO_SECONDARY_CTA_HREF}" class="btn btn-secondary">{c.HERO_SECONDARY_CTA_LABEL}</a>
        </div>
      </div>
    </section>

    <section class="core-idea">
      <div class="container">
        <p class="statement">{c.CORE_IDEA_STATEMENT}</p>
        <p class="section-intro">{c.CORE_IDEA_SUPPORT}</p>
      </div>
    </section>
"""


def render_system_flow_graphic():
    """Custom abstract 'system flow' visual: ascending node-line (traffic
    through to patient) with a subtle data-bar accent. Pure geometry in
    brand colors only; no stock imagery, no literal UI screenshots."""
    points = [(28, 132), (78, 116), (128, 98), (178, 82), (228, 62), (278, 40)]
    path = " ".join(f"{'M' if i == 0 else 'L'}{x} {y}" for i, (x, y) in enumerate(points))
    dots = "\n        ".join(
        f'<circle cx="{x}" cy="{y}" r="{5 if i < len(points)-1 else 6}" '
        f'fill="{"#6893EF" if i == len(points)-1 else "#000"}"/>'
        for i, (x, y) in enumerate(points)
    )
    return f"""<svg viewBox="0 0 320 170" class="flow-graphic" role="img" aria-label="Abstract diagram of the acquisition system trending upward from traffic to booked patient">
        <rect x="252" y="118" width="10" height="34" rx="1.5" fill="#6893EF" opacity="0.18"/>
        <rect x="268" y="98" width="10" height="54" rx="1.5" fill="#6893EF" opacity="0.28"/>
        <rect x="284" y="76" width="10" height="76" rx="1.5" fill="#6893EF" opacity="0.4"/>
        <path d="{path}" stroke="#000" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        {dots}
      </svg>"""


def render_how_it_works():
    tabs = "\n          ".join(
        f'<button class="stage-tab" data-title="{s["title"]}" data-text="{s["text"]}" role="tab">'
        f'<span class="num">{s["num"]}</span>{s["title"]}</button>'
        for s in c.SYSTEM_STAGES
    )
    first = c.SYSTEM_STAGES[0]
    process_items = "\n          ".join(
        f'<li><span class="process-num">{i+1}</span><div><h3>{step["title"]}</h3><p>{step["text"]}</p></div></li>'
        for i, step in enumerate(c.PROCESS_STEPS)
    )
    def render_badge(b):
        logo_html = f'<img src="{b["logo"]}" alt="" class="badge-logo">' if b.get("logo") else ""
        return f'<span class="badge-chip">{logo_html}{b["label"]}</span>'

    badges = "\n            ".join(render_badge(b) for b in c.CAPABILITY_BADGES)

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

        <div class="process-block">
          <h3 class="process-heading">{c.PROCESS_HEADING}</h3>
          <ol class="process-list">
            {process_items}
          </ol>
        </div>

        <div class="tech-strip">
          <div class="graphic-panel">{render_system_flow_graphic()}</div>
          <div class="tech-strip-info">
            <p class="tech-stack-label">{c.TECH_STACK_LABEL}</p>
            <div class="badge-row">
              {badges}
            </div>
          </div>
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


def render_results():
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

    return f"""
    <section class="section" id="results" data-nav-section>
      <div class="container">
        <div class="section-head">
          <h2 class="marker"><span class="plus">+</span> Results</h2>
          <p class="section-intro">{c.RESULTS_INTRO}</p>
        </div>

        <h3 class="track-heading">What we track</h3>
        <div class="track-grid">
          {track_items}
        </div>

        <div class="results-divider"></div>

        {proof_html}
      </div>
    </section>
"""


def render_about():
    pillars = "\n          ".join(
        f'<div><h3>{p["title"]}</h3><p>{p["text"]}</p></div>' for p in c.ABOUT_PILLARS
    )
    return f"""
    <section class="section section-tint" id="about" data-nav-section>
      <div class="container">
        <div class="section-head">
          <h2 class="marker"><span class="plus">+</span> About</h2>
          <p class="section-intro">{c.ABOUT_INTRO}</p>
        </div>
        <div class="three-col why-list">
          {pillars}
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
        <a href="{c.BOOKING_HREF}" class="btn btn-light">{c.PRIMARY_CTA_LABEL}</a>
      </div>
    </section>

    <section class="section section-tint" id="book">
      <div class="container container-narrow">
        <div class="section-head">
          <h2>{c.BOOKING_HEADLINE}</h2>
          <p class="section-intro">{c.BOOKING_SUBHEAD}</p>
        </div>

        <form class="lead-form" id="lead-form" novalidate>
          <div class="form-row">
            <div class="field"><label for="name">Name <span class="req">*</span></label><input type="text" id="name" name="name" required autocomplete="name"></div>
            <div class="field"><label for="business">Business <span class="req">*</span></label><input type="text" id="business" name="business" required autocomplete="organization"></div>
          </div>
          <div class="form-row">
            <div class="field"><label for="email">Email <span class="req">*</span></label><input type="email" id="email" name="email" required autocomplete="email"></div>
            <div class="field"><label for="phone">Phone <span class="req">*</span></label><input type="tel" id="phone" name="phone" required autocomplete="tel"></div>
          </div>
          <div class="form-row">
            <div class="field"><label for="website">Website</label><input type="url" id="website" name="website" placeholder="Optional" autocomplete="url"></div>
            <div class="field">
              <label for="practice-type">Practice Type <span class="req">*</span></label>
              <select id="practice-type" name="practice-type" required>
                <option value="" selected disabled>Select one</option>
                {options}
              </select>
            </div>
          </div>
          <div class="field"><label for="challenge">Biggest Growth Challenge</label><textarea id="challenge" name="challenge" rows="3" placeholder="Optional"></textarea></div>
          <button type="submit" class="btn btn-primary btn-full">Confirm &amp; Book</button>
          <!-- DEV NOTE (not shown to visitors): this form currently submits locally only.
               Wire the action above to a CRM/Zapier endpoint (and/or embed a scheduler here)
               once a real integration exists. See content.py BOOKING_HREF for the CTA target. -->
        </form>

        <div class="form-success" id="form-success" hidden>
          <h3>Thanks. You're almost done.</h3>
          <p>In the live version, a scheduler will appear here so you can pick a time immediately.</p>
        </div>
      </div>
    </section>
  </main>
"""


def render_back_to_top():
    return """
  <button id="back-to-top" class="back-to-top" aria-label="Back to top">
    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
  </button>
"""


SOCIAL_ICONS = {
    "instagram": (
        '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" aria-hidden="true">'
        '<rect x="2" y="2" width="20" height="20" rx="5.5" stroke="currentColor" stroke-width="1.8"/>'
        '<circle cx="12" cy="12" r="4.6" stroke="currentColor" stroke-width="1.8"/>'
        '<circle cx="17.3" cy="6.7" r="1.15" fill="currentColor"/>'
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


def render_footer():
    nav_row = f' <span class="footer-nav-sep" aria-hidden="true">+</span> '.join(
        f'<a href="#{sid}">{label}</a>' for sid, label in c.NAV
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
          <img src="{LOGO_URI}" alt="MedLead Partners logo" class="footer-logo-lg">
          <p class="footer-tagline">{c.FOOTER_TAGLINE}</p>
          {contact_html}
          {social_html}
        </div>
        <div class="footer-cta-block">
          <span class="footer-cta-label">Ready to talk?</span>
          <a href="{c.BOOKING_HREF}" class="btn btn-primary">{c.PRIMARY_CTA_LABEL}</a>
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

  <script>
{JS}
  </script>
</body>
</html>
"""


def build():
    parts = [
        render_head(),
        render_header(),
        render_hero(),
        render_how_it_works(),
        render_services(),
        render_who_we_serve(),
        render_results(),
        render_about(),
        render_faq(),
        render_booking(),
        render_back_to_top(),
        render_footer(),
    ]
    output = "".join(parts)
    out_path = os.path.join(ROOT, "index.html")
    with open(out_path, "w") as f:
        f.write(output)
    print(f"Built index.html ({len(output):,} bytes) from content.py + template.css + template.js")


if __name__ == "__main__":
    build()
