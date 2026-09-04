/* ==========================================================================
   MED LEAD PARTNERS — INTERACTIONS v2
   Shared across every page. Small, dependency-free.
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
  initMobileMenu();
  initRevealLists();
  initStageTabs();
  initPracticePills();
  initFormHandler();
  initFooterYear();
  initHeaderShadowOnScroll();
  initBackToTop();
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

/* ---------- Booking form (local placeholder — no live endpoint yet) ---------- */
function initFormHandler() {
  const form = document.getElementById("lead-form");
  const success = document.getElementById("form-success");
  if (!form) return;

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    // Placeholder behavior for local/demo use.
    // In production this posts to the CRM/Zapier endpoint, then Calendly loads below.
    form.hidden = true;
    success.hidden = false;
    success.scrollIntoView({ behavior: "smooth", block: "center" });
  });
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