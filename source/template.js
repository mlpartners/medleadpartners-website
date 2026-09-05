/* ==========================================================================
   MED LEAD PARTNERS — INTERACTIONS v2
   Shared across every page. Small, dependency-free.
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
  initMobileMenu();
  initRevealLists();
  initStageTabs();
  initPracticePills();
  initBookingFlow();
  initFooterYear();
  initHeaderShadowOnScroll();
  initBackToTop();
  initFloatingCta();
  initLogoHome();
});

/* ---------- Logo: always returns exactly to the top of the page ---------- */
function initLogoHome() {
  const logo = document.querySelector(".logo-link");
  if (!logo) return;

  logo.addEventListener("click", (e) => {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

/* ---------- Mobile menu ---------- */
function initMobileMenu() {
  const toggle = document.getElementById("menu-toggle");
  const menu = document.getElementById("mobile-menu");
  if (!toggle || !menu) return;

  toggle.addEventListener("click", () => {
    const isOpen = menu.classList.toggle("is-open");
    toggle.classList.toggle("is-open", isOpen);
    toggle.setAttribute("aria-expanded", String(isOpen));
  });

  menu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      menu.classList.remove("is-open");
      toggle.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
    });
  });
}

/* ---------- Generic reveal / accordion lists (Services, Who We Serve, FAQ) ---------- */
function initRevealLists() {
  const triggers = document.querySelectorAll(".reveal-trigger");

  triggers.forEach((trigger) => {
    const panel = trigger.nextElementSibling;

    trigger.addEventListener("click", () => {
      const isOpen = trigger.classList.contains("is-open");
      const list = trigger.closest(".reveal-list");
      const singleOpen = list && list.hasAttribute("data-single-open");

      if (singleOpen && !isOpen) {
        list.querySelectorAll(".reveal-trigger.is-open").forEach((openTrigger) => {
          if (openTrigger !== trigger) {
            openTrigger.classList.remove("is-open");
            openTrigger.setAttribute("aria-expanded", "false");
            openTrigger.nextElementSibling.style.maxHeight = "0px";
          }
        });
      }

      trigger.classList.toggle("is-open", !isOpen);
      trigger.setAttribute("aria-expanded", String(!isOpen));
      panel.style.maxHeight = isOpen ? "0px" : panel.scrollHeight + "px";
    });
  });
}

/* ---------- System stage tabs (single shared description panel) ---------- */
/* ---------- Generic tab group: N buttons, one shared text panel ----------
   Used by both the How It Works stage selector and the Who We Serve
   practice pills. Each button carries its text in data-title/data-text;
   clicking one swaps the shared panel's content and marks that button
   active. Defaults to the first button so the panel is never empty. */
function initTabGroup(tabSelector, titleId, textId) {
  const tabs = document.querySelectorAll(tabSelector);
  const titleEl = document.getElementById(titleId);
  const textEl = document.getElementById(textId);
  if (!tabs.length || !titleEl || !textEl) return;

  function activate(tab) {
    tabs.forEach((t) => t.classList.remove("is-active"));
    tab.classList.add("is-active");
    titleEl.textContent = tab.dataset.title;
    textEl.textContent = tab.dataset.text;
  }

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => activate(tab));
  });

  activate(tabs[0]);
}

function initStageTabs() {
  initTabGroup(".stage-tab", "stage-panel-title", "stage-panel-text");
}

function initPracticePills() {
  initTabGroup(".practice-pill", "practice-panel-title", "practice-panel-text");
}

/* ---------- Booking flow: lead form -> real Calendly scheduler -> confirmation ----------
   Three states, one visible at a time:
     1. #booking-step-form      the contact form (always the first thing shown)
     2. #booking-step-schedule  the REAL Calendly inline widget (opened only after the
                                 form validates — this is NOT a booking confirmation)
     3. #booking-step-confirmed shown ONLY after Calendly fires "calendly.event_scheduled"
   The Calendly URL is read from data-calendly-url on #book (set from content.py
   CALENDLY_URL in build.py) so this file has no hardcoded scheduling link. */
function initBookingFlow() {
  const bookSection = document.getElementById("book");
  const form = document.getElementById("lead-form");
  const stepForm = document.getElementById("booking-step-form");
  const stepSchedule = document.getElementById("booking-step-schedule");
  const stepConfirmed = document.getElementById("booking-step-confirmed");
  const calendlyContainer = document.getElementById("calendly-container");
  const calendlyFallback = document.getElementById("calendly-fallback");
  if (!bookSection || !form || !stepForm || !stepSchedule || !stepConfirmed || !calendlyContainer) return;

  const calendlyUrl = bookSection.dataset.calendlyUrl;
  let widgetInitialized = false;
  let fallbackTimer = null;

  function showStep(step) {
    [stepForm, stepSchedule, stepConfirmed].forEach((el) => {
      el.hidden = el !== step;
    });
    if (step !== stepForm) {
      // Move focus/scroll to the new step so screen reader and sighted users
      // alike land on the right content instead of the page jumping silently.
      step.scrollIntoView({ behavior: "smooth", block: "start" });
      step.focus({ preventScroll: true });
    }
  }

  function showFallback() {
    if (fallbackTimer) {
      window.clearTimeout(fallbackTimer);
      fallbackTimer = null;
    }
    if (calendlyFallback) calendlyFallback.hidden = false;
  }

  function clearFallbackTimer() {
    if (fallbackTimer) {
      window.clearTimeout(fallbackTimer);
      fallbackTimer = null;
    }
    // Widget is actually rendering — no need for the fallback link anymore
    // even if it was already shown (e.g. it loaded slowly rather than failed).
    if (calendlyFallback) calendlyFallback.hidden = true;
  }

  function openScheduler(details) {
    showStep(stepSchedule);

    if (widgetInitialized || !calendlyUrl) return;
    widgetInitialized = true;

    // A hard script-load failure (blocked by an ad blocker, corporate network, etc. —
    // see the onerror handler on the widget.js <script> tag) is detectable immediately;
    // no reason to make the visitor wait out a timeout for something we already know
    // isn't going to work.
    if (
      window.__calendlyLoadFailed ||
      !(window.Calendly && typeof window.Calendly.initInlineWidget === "function")
    ) {
      showFallback();
      return;
    }

    // Script loaded, but the embed can still fail silently in the browser itself —
    // most commonly when third-party cookies are blocked (Safari's tracking
    // prevention, many ad blockers, some corporate networks), which Calendly's
    // inline widget depends on. If we haven't heard a "page_height" message back
    // (see the message listener below) within a few seconds, the calendar isn't
    // rendering, so surface the direct link rather than leaving a permanent
    // "Loading the scheduler…" box with no way forward.
    fallbackTimer = window.setTimeout(showFallback, 5000);

    window.Calendly.initInlineWidget({
      url: calendlyUrl,
      parentElement: calendlyContainer,
      prefill: {
        name: details.name,
        email: details.email,
      },
      utm: {
        utmSource: "website",
        utmMedium: "strategy_call_form",
      },
    });
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    // DEV NOTE (not shown to visitors): wire this to a real CRM/email endpoint once one
    // exists, so practice details are captured even if a visitor doesn't finish scheduling.
    const details = {
      name: (form.elements["name"].value || "").trim(),
      email: (form.elements["email"].value || "").trim(),
    };

    openScheduler(details);
  });

  // Calendly posts a window message for every step of the scheduling flow. We handle two:
  // "calendly.page_height" resizes the embed to fit its actual content (Calendly's own
  // auto-resize only covers widgets it auto-scans on page load, not ones created dynamically
  // via initInlineWidget as we do here, so we size it ourselves) and confirms the widget is
  // actually rendering, which cancels the fallback timer above. "calendly.event_scheduled"
  // is the sole signal the site treats as an actual booked meeting — opening the widget above
  // is never enough on its own.
  window.addEventListener("message", (e) => {
    if (!isCalendlyEvent(e)) return;

    if (e.data.event === "calendly.page_height") {
      clearFallbackTimer();
      const height = parseInt(e.data.payload && e.data.payload.height, 10);
      if (!isNaN(height)) {
        const iframe = calendlyContainer.querySelector("iframe");
        const target = Math.max(height, 420) + "px";
        if (iframe) iframe.style.height = target;
        calendlyContainer.style.minHeight = target;
        const note = calendlyContainer.querySelector(".calendly-loading-note");
        if (note) note.style.display = "none";
      }
      return;
    }

    if (e.data.event === "calendly.event_scheduled") {
      clearFallbackTimer();
      showStep(stepConfirmed);
    }
  });

  function isCalendlyEvent(e) {
    return (
      e.origin === "https://calendly.com" &&
      e.data &&
      typeof e.data.event === "string" &&
      e.data.event.indexOf("calendly.") === 0
    );
  }
}

/* ---------- Footer year ---------- */
function initFooterYear() {
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();
}

/* ---------- Header: becomes slightly more solid + subtle shadow once scrolled ---------- */
function initHeaderShadowOnScroll() {
  const header = document.querySelector(".site-header");
  if (!header) return;

  const setState = () => {
    header.classList.toggle("is-scrolled", window.scrollY > 4);
  };

  setState();
  window.addEventListener("scroll", setState, { passive: true });
}

/* ---------- Back to top ---------- */
function initBackToTop() {
  const btn = document.getElementById("back-to-top");
  if (!btn) return;

  const setVisibility = () => {
    btn.classList.toggle("is-visible", window.scrollY > 700);
  };

  setVisibility();
  window.addEventListener("scroll", setVisibility, { passive: true });

  btn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

/* ---------- Floating "Book a Strategy Call" pill ----------
   Visible once the visitor scrolls past the hero; hidden again once the
   final-CTA/booking area scrolls into view so it never sits alongside the
   "Book a Strategy Call" buttons already there (nav CTA excluded — that
   one lives in the fixed header, not the scrolling page). Uses
   IntersectionObserver rather than scroll-position math so it stays
   correct regardless of how content above it changes length. */
function initFloatingCta() {
  const cta = document.getElementById("floating-cta");
  const hero = document.getElementById("home");
  const bookingArea = document.querySelector(".final-cta");
  if (!cta || !hero || !bookingArea) return;

  let pastHero = false;
  let inOrPastBookingArea = false;

  const update = () => {
    cta.classList.toggle("is-visible", pastHero && !inOrPastBookingArea);
  };

  const heroObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        pastHero = !entry.isIntersecting;
        update();
      });
    },
    { threshold: 0 }
  );
  heroObserver.observe(hero);

  // Once the visitor reaches the final-CTA band, keep the pill hidden for the rest of
  // the page (through the booking form and the footer), not just while that one band
  // happens to be on screen — a plain intersection check would let it reappear once the
  // band scrolls out of view above (e.g. down at the footer), sitting on top of footer
  // content.
  let ticking = false;
  const checkBookingArea = () => {
    ticking = false;
    const bandTop = bookingArea.getBoundingClientRect().top + window.scrollY;
    inOrPastBookingArea = window.scrollY + window.innerHeight > bandTop;
    update();
  };
  const onScroll = () => {
    if (!ticking) {
      ticking = true;
      requestAnimationFrame(checkBookingArea);
    }
  };

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", checkBookingArea);
  checkBookingArea();
}

/* ---------- Scroll-spy: highlight the current section's nav link ----------
   Uses direct geometry rather than raw IntersectionObserver batching, so that
   when multiple sections briefly overlap the trigger band, the one that is
   actually most visible (closest to just below the header) always wins —
   IntersectionObserver's per-entry callbacks can otherwise let a stale
   section "win" on a fast/instant scroll. */
function initScrollSpy() {
  const sections = Array.from(document.querySelectorAll("main [data-nav-section]"));
  const navLinks = document.querySelectorAll(".primary-nav a, .mobile-menu a");
  if (!sections.length || !navLinks.length) return;

  const setActive = (id) => {
    navLinks.forEach((link) => {
      const isMatch = link.getAttribute("href") === `#${id}`;
      link.classList.toggle("is-current", isMatch);
      if (isMatch) {
        link.setAttribute("aria-current", "true");
      } else {
        link.removeAttribute("aria-current");
      }
    });
  };

  const referenceLine = () => Math.min(window.innerHeight * 0.35, 220);

  let ticking = false;
  const update = () => {
    ticking = false;
    const line = referenceLine();
    let current = null;
    for (const section of sections) {
      const rect = section.getBoundingClientRect();
      if (rect.top <= line) {
        current = section;
      }
    }
    if (current) setActive(current.id);
  };

  window.addEventListener(
    "scroll",
    () => {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(update);
      }
    },
    { passive: true }
  );

  update();
}

document.addEventListener("DOMContentLoaded", initScrollSpy);
