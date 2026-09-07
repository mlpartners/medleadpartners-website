"""
MEDLEAD PARTNERS. SITE CONTENT
==================================================
This file holds every piece of editable copy on the website: headlines,
nav labels, FAQ, services, industries, results, footer info, etc.

Edit THIS file when you need to change words on the site.
Edit template.css when you need to change how it looks.
Edit template.js when you need to change how it behaves.
Edit build.py only when you need to change page STRUCTURE (add/remove/reorder
a section) rather than its content.

After editing this file, regenerate the deployable site with:
    python3 build.py
That produces index.html, the single file you actually deploy or share.
"""

# --------------------------------------------------------------------------
# SITE META (SEO + browser tab + social sharing)
# --------------------------------------------------------------------------

SITE_TITLE = "MedLead Partners | Patient Acquisition"
SITE_DESCRIPTION = (
    "MedLead Partners generates new patient leads through paid advertising and runs the system "
    "that captures, qualifies, follows up with, and moves those leads toward an appointment."
)

# The browser tab / <title> element specifically. Kept separate from
# SITE_TITLE (used for og:title / twitter:title, i.e. social share
# previews) since the two serve different purposes and a person updating
# one shouldn't accidentally change the other.
PAGE_TITLE = "MedLead Partners"

# --------------------------------------------------------------------------
# PRODUCTION DOMAIN
#
# *** UPDATE THIS to the real, final domain before going live. ***
# Used to build canonical URLs, og:url, the absolute og:image URL (social
# platforms generally won't fetch a relative image path), and sitemap.xml.
# Must be the HTTPS version of whatever domain Squarespace/GitHub Pages end
# up serving (e.g. "https://www.medleadpartners.com"). No trailing slash.
# --------------------------------------------------------------------------
SITE_URL = "https://www.medleadpartners.com"

# --------------------------------------------------------------------------
# NAVIGATION
# Each tuple is (section_id, label). The section_id must match a real
# section id in build.py (id="how-it-works" etc.). These are also the
# only nav items shown, per the approved 5-item nav.
# --------------------------------------------------------------------------

NAV = [
    ("how-it-works", "How It Works"),
    ("who-we-serve", "Who We Serve"),
    ("results", "Results"),
    ("about", "About"),
    ("faq", "FAQ"),
]

PRIMARY_CTA_LABEL = "Book a Strategy Call"

# The CTA below points to the in-page booking form (#book). That form is
# Step 1 of the real booking flow: once submitted, the site opens the real
# Calendly scheduler inline (see CALENDLY_URL below) rather than claiming a
# meeting is booked outright. Every "Book a Strategy Call" button/link on
# the site reads from this one value.
BOOKING_HREF = "#book"

# --------------------------------------------------------------------------
# CALENDLY (real scheduling backend for the booking flow)
#
# This is the actual MedLead Partners scheduling page. The site never
# claims a meeting is booked until Calendly itself confirms a scheduled
# event (see render_booking() in build.py + template.js for the
# form -> inline Calendly -> confirmation flow).
# --------------------------------------------------------------------------
CALENDLY_URL = "https://calendly.com/medleadpartners"

# --------------------------------------------------------------------------
# HERO
# --------------------------------------------------------------------------

HERO_HEADLINE = "Patient Acquisition, From Click to Appointment"
HERO_SUBHEAD = "We generate the leads. We build the system that converts them."

# --------------------------------------------------------------------------
# HOW IT WORKS. The 6-stage system (interactive tabs)
# --------------------------------------------------------------------------

HOW_IT_WORKS_INTRO = (
    "One system, six stages, one accountable partner. Not a menu of disconnected tactics."
)

SYSTEM_STAGES = [
    {"num": "01", "title": "Paid Advertising", "text": "We create and manage paid campaigns designed to put your practice in front of prospective patients."},
    {"num": "02", "title": "Lead Capture", "text": "We turn campaign-driven interest into identifiable leads your practice can act on."},
    {"num": "03", "title": "Qualification", "text": "We organize and qualify incoming leads according to the criteria established with your practice."},
    {"num": "04", "title": "Follow-Up", "text": "New leads enter a structured follow-up process so opportunities do not get lost after the initial inquiry."},
    {"num": "05", "title": "Appointment Booking", "text": "We move qualified leads toward a scheduled consultation through the practice's booking process."},
    {"num": "06", "title": "Patient", "text": "Your practice takes over the patient relationship and delivers the care."},
]

# --------------------------------------------------------------------------
# SERVICES ("What We Run"). Acquisition-system graphic + service pills
# --------------------------------------------------------------------------

SERVICES_INTRO = "The patient-acquisition system behind the growth."

# Flat list of what MedLead Partners runs, rendered as a stacked column of
# pills beside the acquisition-system graphic. Deliberately not phrased as
# "CRM & Lead Management" or anything implying the practice manages leads
# after we generate them; this is the system we operate, end to end.
WHAT_WE_RUN_ITEMS = [
    "Paid Advertising",
    "Lead Generation",
    "Lead Capture",
    "Lead Qualification",
    "Follow-Up Automation",
    "Appointment Scheduling",
    "Performance Analytics",
]

# --------------------------------------------------------------------------
# WHO WE SERVE. Interactive accordion
# --------------------------------------------------------------------------

WHO_WE_SERVE_INTRO = "Built around the way your practice grows."

INDUSTRIES = [
    {"label": "Medical Practices", "text": "A structured system for generating and following up on new patient inquiries."},
    {"label": "Med Spas", "text": "High frequency visits where fast follow up fills the calendar."},
    {"label": "Plastic Surgery", "text": "Longer decision windows call for structured, ongoing follow up."},
    {"label": "Dental Practices", "text": "A more organized system for new patient inquiries."},
    {"label": "Aesthetic &amp; Elective Care", "text": "Any practice where a booked patient has real, defined value."},
]

# --------------------------------------------------------------------------
# RESULTS / PROOF
#
# CASE_STUDIES is intentionally empty. No verified client results exist yet.
# When a real one is ready, append a dict here with the fields below and it
# will render automatically in place of the results framework below.
# Never fill this with invented names, numbers, or outcomes.
#
# Schema per case study:
#   title        - short case study title
#   practice     - client/practice name (only if they've agreed to be named)
#   challenge    - what problem they came in with
#   strategy     - what MedLead Partners did
#   implementation - how it was rolled out (optional)
#   results      - what changed (only verified, real outcomes)
#   metric       - one optional standout verified metric
#   image        - optional image path/data URI
# --------------------------------------------------------------------------

RESULTS_INTRO = "We monitor the acquisition process end to end. Verified case studies will appear here as client results come in."

CASE_STUDIES = []  # populate with real, verified case studies only. See schema above.

# --------------------------------------------------------------------------
# RESULTS FRAMEWORK
#
# Shown in place of a case study while CASE_STUDIES (above) is empty. This
# is not a placeholder to delete later. It's real, permanent content
# describing what MedLead Partners actually measures. No numbers are
# attached to it because none are verified yet. Once CASE_STUDIES has a
# real entry, that renders instead (see render_results() in build.py).
# --------------------------------------------------------------------------

RESULTS_FRAMEWORK = [
    {"label": "Lead Volume", "text": "How much demand campaigns generate."},
    {"label": "Lead Quality", "text": "Whether inquiries meet the practice's criteria."},
    {"label": "Follow-Up", "text": "How consistently opportunities move through the follow-up process."},
    {"label": "Appointments", "text": "How many qualified opportunities book."},
    {"label": "Funnel Performance", "text": "Where opportunities move forward and where they drop off."},
]

# --------------------------------------------------------------------------
# TESTIMONIALS
#
# Intentionally empty. No real client testimonials exist yet. Nothing
# testimonial-related renders on the site while this list is empty; that's
# deliberate, so the site never shows fabricated quotes. When a real one
# exists, append a dict here with the fields below.
#
# Schema per testimonial:
#   quote     - the testimonial text, verbatim, from the client
#   name      - client's real name
#   title     - client's role/title
#   practice  - practice/company name
#   photo     - optional image path/data URI
#   logo      - optional practice logo path/data URI
# --------------------------------------------------------------------------

TESTIMONIALS = []  # populate with real, attributed testimonials only. See schema above.

# Sample client feedback. Temporary and fictional, for design purposes only.
#
# This is NOT a real client and NOT a verified testimonial. It exists only
# so the testimonial component can be visualized with real-looking content
# before any actual client feedback exists. It renders inside the Results
# section, next to the results framework card, with a visible
# "Sample client feedback" tag and a dashed border (the same visual
# language the site uses elsewhere for not-yet-real content) so it can
# never be mistaken for a verified review.
#
# When real client feedback exists:
#   1. Set SAMPLE_TESTIMONIAL to None below.
#   2. Add the real testimonial to the TESTIMONIALS list above instead
#      (see its schema above it). It will render as a real, unlabeled
#      testimonial card with no "sample" tag.

SAMPLE_TESTIMONIAL = None

# --------------------------------------------------------------------------
# ABOUT
# --------------------------------------------------------------------------

ABOUT_INTRO = (
    "MedLead Partners was built around a simple observation: generating an inquiry is only "
    "the beginning. We connect paid advertising, lead capture, qualification, follow-up, "
    "appointment booking, and reporting into one system, so opportunities never get lost "
    "between the steps."
)

# --------------------------------------------------------------------------
# FAQ
# --------------------------------------------------------------------------

FAQ_ITEMS = [
    (
        "What does MedLead Partners actually do?",
        "We generate new patient leads through paid advertising and run the acquisition system "
        "around those leads: lead capture, structural qualification, follow-up, appointment "
        "booking, and performance reporting. We are not simply managing leads your practice "
        "has already generated.",
    ),
    (
        "How do you qualify leads?",
        "Structurally only. We check location, insurance status, and availability against your "
        "practice's own rules. We never apply medical judgment.",
    ),
    (
        "Do you replace our medical or front-office team?",
        "No. Your practice remains responsible for the patient relationship and healthcare "
        "delivery. We focus on generating and moving new patient opportunities through the "
        "acquisition process.",
    ),
    (
        "Do you guarantee a certain number of patients?",
        "No. We do not promise a specific number of patients or revenue. We focus on building "
        "and optimizing the acquisition system and measuring what happens throughout the funnel.",
    ),
    (
        "Who is MedLead Partners designed for?",
        "Medical practices, med spas, plastic surgery, dental practices, and aesthetic or "
        "elective care businesses. Practices where a booked patient has clear, defined value.",
    ),
]

# --------------------------------------------------------------------------
# FOOTER / CONTACT
#
# Set these to real values whenever they're available. They'll render
# automatically. Leave as None to omit them cleanly (no bracketed
# placeholders are ever shown on the live site).
# --------------------------------------------------------------------------

FOOTER_TAGLINE = "Patient acquisition, run as one system."

CONTACT_EMAIL = "info@medleadpartners.com"
CONTACT_PHONE = None   # e.g. "+1 (555) 123-4567"

SOCIAL_LINKS = [
    {"label": "Instagram", "url": "https://www.instagram.com/medleadpartners/", "aria_label": "MedLead Partners on Instagram", "icon": "instagram"},
    {"label": "Facebook", "url": "https://www.facebook.com/MedLeadPartners/", "aria_label": "MedLead Partners on Facebook", "icon": "facebook"},
]  # each entry needs a matching icon renderer in build.py's SOCIAL_ICONS, or it falls back to a plain text link

# Only add an entry here once a real destination page exists for it.
LEGAL_LINKS = [
    {"label": "Privacy Policy", "url": "privacy.html"},
    {"label": "Terms &amp; Conditions", "url": "terms.html"},
]

COPYRIGHT_HOLDER = "MedLead Partners"

# --------------------------------------------------------------------------
# FINAL CTA (the blue band right before the booking form)
# --------------------------------------------------------------------------

FINAL_CTA_HEADLINE = "See what a full-funnel system looks like for your practice."

# --------------------------------------------------------------------------
# BOOKING FORM
#
# The booking flow has three states, shown one at a time in the #book
# section (see render_booking() in build.py and initBookingFlow() in
# template.js):
#   1. FORM      — lead-form below (BOOKING_HEADLINE / BOOKING_SUBHEAD)
#   2. SCHEDULE  — the real Calendly inline widget, opened only after the
#                  form validates (SCHEDULING_HEADLINE / SCHEDULING_SUBHEAD)
#   3. CONFIRMED — shown only after Calendly fires calendly.event_scheduled,
#                  never just from opening the scheduler
#                  (CONFIRMATION_HEADLINE / CONFIRMATION_TEXT)
# --------------------------------------------------------------------------

BOOKING_HEADLINE = "Book a Strategy Call"
BOOKING_SUBHEAD = "Tell us a bit about your practice. We'll come to the call ready to talk specifics."
CONFIRM_BUTTON_LABEL = "Confirm &amp; Book"

SCHEDULING_HEADLINE = "Choose a Time"
SCHEDULING_SUBHEAD = "Thanks — your details are saved. Pick a time below to confirm your strategy call."

CONFIRMATION_HEADLINE = "Strategy Call Scheduled"
CONFIRMATION_TEXT = "Your strategy call with MedLead Partners has been scheduled. We'll see you then."

PRACTICE_TYPE_OPTIONS = [
    ("medical", "Medical Practice"),
    ("med-spa", "Med Spa"),
    ("plastic-surgery", "Plastic Surgery"),
    ("dental", "Dental Practice"),
    ("aesthetic-elective", "Aesthetic &amp; Elective Care"),
    ("other", "Other"),
]

# --------------------------------------------------------------------------
# LEGAL PAGES
#
# *** TEMPLATE LEGAL CONTENT — NOT LEGAL ADVICE. ***
# This is a standard, reasonable starting point for a small B2B marketing
# services site, not a substitute for review by a licensed attorney familiar
# with your jurisdiction, industry (working with medical/healthcare-adjacent
# clients), and how you actually handle data. Have a lawyer review both
# pages before relying on them, and update LAST_UPDATED whenever the text
# changes.
# --------------------------------------------------------------------------

LAST_UPDATED = "September 7, 2026"

PRIVACY_TITLE = "Privacy Policy - MedLead Partners"
PRIVACY_DESCRIPTION = "How MedLead Partners collects, uses, and protects information submitted through this website."

PRIVACY_SECTIONS = [
    (
        "Overview",
        "This Privacy Policy explains what information MedLead Partners (\u201cwe,\u201d \u201cus,\u201d \u201cour\u201d) "
        "collects through this website, how we use it, and the choices available to you. It applies to "
        "this website only, not to any practice or business that partners with MedLead Partners, nor to "
        "any patient of theirs.",
    ),
    (
        "Information We Collect",
        "When you submit the \u201cBook a Strategy Call\u201d form, we collect the information you provide: "
        "your name, business name, email address, phone number, website (optional), practice type, and "
        "anything you enter under \u201cBiggest Growth Challenge.\u201d We do not currently use analytics or "
        "tracking cookies of our own on this site.",
    ),
    (
        "How We Use Information",
        "We use the information you submit to respond to your inquiry, prepare for a scheduled strategy "
        "call, and evaluate whether MedLead Partners is a good fit for your practice. We do not sell your "
        "information, and we do not use it for purposes unrelated to responding to your inquiry.",
    ),
    (
        "Scheduling Through Calendly",
        "After you submit the form, this site opens a scheduling widget provided by Calendly, Inc. so you "
        "can pick a time for your strategy call. Calendly operates independently of this site: it may set "
        "its own cookies and process information (such as your name, email, and time zone) according to "
        "its own privacy policy, available at "
        "<a href=\"https://calendly.com/privacy\" target=\"_blank\" rel=\"noopener noreferrer\">calendly.com/privacy</a>.",
    ),
    (
        "Other Third-Party Services",
        "This site loads the Montserrat typeface from Google Fonts. Loading a font can result in your "
        "browser making a request to Google's servers; see Google's privacy policy for how they handle "
        "that. We do not currently run analytics, advertising pixels, or other tracking scripts on this "
        "site.",
    ),
    (
        "Cookies",
        "This site does not set its own cookies. The Calendly scheduling widget described above may set "
        "cookies belonging to Calendly (and its own sub-processors, such as reCAPTCHA) once you open it; "
        "those are governed by Calendly's privacy policy, not this one.",
    ),
    (
        "Data Retention",
        "We retain information submitted through the strategy-call form for as long as reasonably "
        "necessary to respond to your inquiry and, if you become a partner, to provide our services. You "
        "can request deletion at any time using the contact information below.",
    ),
    (
        "Your Choices",
        "You can ask us what information we have about you, request a correction, or request deletion, by "
        "emailing us at the address below. If you'd rather not submit the form, you can still reach us "
        "directly by email.",
    ),
    (
        "Children's Privacy",
        "This website is intended for business use by adults evaluating patient-acquisition services for "
        "their practice. It is not directed at children, and we do not knowingly collect information from "
        "anyone under 18.",
    ),
    (
        "Changes to This Policy",
        "We may update this policy from time to time. The date at the top of this page reflects the most "
        "recent revision.",
    ),
    (
        "Contact",
        "Questions about this policy or your information can be sent to "
        f"<a href=\"mailto:{CONTACT_EMAIL}\">{CONTACT_EMAIL}</a>." if CONTACT_EMAIL else
        "Questions about this policy or your information can be sent using the contact details on this site.",
    ),
]

TERMS_TITLE = "Terms & Conditions - MedLead Partners"
TERMS_DESCRIPTION = "The terms that govern use of the MedLead Partners website and strategy-call booking process."

TERMS_SECTIONS = [
    (
        "Agreement to Terms",
        "By using this website, you agree to these Terms &amp; Conditions. If you do not agree, please do "
        "not use the site. These terms govern use of the website itself; a separate written agreement "
        "governs the actual patient-acquisition services provided to any practice that becomes a partner.",
    ),
    (
        "Who This Site Is For",
        "This website is intended for medical practices, med spas, plastic surgery practices, dental "
        "practices, and aesthetic/elective-care businesses evaluating patient-acquisition services. It is "
        "not intended for patients seeking medical care or advice.",
    ),
    (
        "No Medical Advice",
        "Nothing on this website is medical advice, and MedLead Partners does not provide healthcare "
        "services, make clinical decisions, or practice medicine in any capacity. Any lead qualification "
        "described on this site is structural only (location, insurance status, availability) and never "
        "medical.",
    ),
    (
        "No Guaranteed Results",
        "We do not guarantee a specific number of leads, appointments, patients, or any particular revenue "
        "outcome. Results depend on many factors outside our control, including a practice's own follow-up, "
        "market conditions, and advertising performance.",
    ),
    (
        "The Booking Process",
        "Submitting the strategy-call form does not itself book a meeting. A meeting is only scheduled once "
        "you complete that step in the Calendly scheduler and Calendly confirms it. Calendly's own terms of "
        "service govern your use of that scheduling tool.",
    ),
    (
        "Acceptable Use",
        "You agree not to use this website to submit false or fraudulent information, attempt to interfere "
        "with its normal operation, or attempt to gain unauthorized access to it.",
    ),
    (
        "Intellectual Property",
        "The MedLead Partners name, logo, and the content of this website are the property of MedLead "
        "Partners and may not be copied or used without permission.",
    ),
    (
        "Third-Party Links and Services",
        "This site links to or embeds third-party services, including Calendly, Instagram, and Facebook. "
        "We are not responsible for the content, policies, or practices of those third parties.",
    ),
    (
        "Limitation of Liability",
        "To the fullest extent permitted by law, MedLead Partners is not liable for any indirect, "
        "incidental, or consequential damages arising from your use of this website.",
    ),
    (
        "Changes to These Terms",
        "We may update these terms from time to time. The date at the top of this page reflects the most "
        "recent revision. Continued use of the site after a change means you accept the updated terms.",
    ),
    (
        "Contact",
        "Questions about these terms can be sent to "
        f"<a href=\"mailto:{CONTACT_EMAIL}\">{CONTACT_EMAIL}</a>." if CONTACT_EMAIL else
        "Questions about these terms can be sent using the contact details on this site.",
    ),
]

# --------------------------------------------------------------------------
# 404 PAGE
# --------------------------------------------------------------------------

NOT_FOUND_TITLE = "Page Not Found - MedLead Partners"
NOT_FOUND_HEADLINE = "Page Not Found"
NOT_FOUND_TEXT = "The page you're looking for doesn't exist or may have moved."
