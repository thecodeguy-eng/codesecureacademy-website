/* Premium motion pass — GSAP + ScrollTrigger. This is a progressive
   enhancement layer:
   - If the GSAP CDN failed to load (offline, blocked, etc.), this file is a
     no-op and every element is already visible via normal CSS — nothing is
     ever hidden waiting on JS that might not run.
   - Skipped entirely in lite-mode or prefers-reduced-motion, matching the
     brief's own GPU/perf constraint for mid-range Android devices. */
(function () {
  "use strict";

  if (!window.gsap || !window.ScrollTrigger) return;
  if (document.documentElement.classList.contains("lite-mode")) return;
  if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  gsap.registerPlugin(ScrollTrigger);
  var EASE = "power3.out";

  // --- The "opening of the site": header + hero stagger in on load, not
  // on scroll. This is the first thing a visitor sees, so it's what makes
  // the site feel considered rather than just present.
  // Excludes interactive controls (buttons, toggles) from the stagger — if
  // the tab is backgrounded or GSAP's ticker gets throttled mid-animation,
  // an element frozen at its from() state (y:-12, opacity:0) looks broken
  // rather than just "not yet animated in". Not worth that risk on the
  // primary CTA and the theme toggle, so only plain nav links get it.
  var headerTargets = document.querySelectorAll(".site-header .brand, .site-header .main-nav a:not(.btn)");
  if (headerTargets.length) {
    gsap.from(headerTargets, { y: -12, opacity: 0, duration: 0.5, ease: EASE, stagger: 0.05 });
  }

  var hero = document.querySelector(".hero");
  if (hero) {
    var heroTargets = hero.querySelectorAll(".track-icon-wrap, .eyebrow, h1, .lead, .hero-actions > *");
    if (heroTargets.length) {
      gsap.from(heroTargets, { y: 26, opacity: 0, duration: 0.75, ease: EASE, stagger: 0.09, delay: 0.15 });
    }
  }

  // --- Generic scroll-triggered entrance for sections/cards site-wide, so
  // motion isn't confined to one hand-built section — every page gets it
  // for free just by using the standard component classes.
  // Note: where a wrapper and its children would both match (e.g. a card
  // and the grid items inside it), only one is listed here — the other is
  // handled by the group-stagger pass below — so nothing double-animates.
  var fadeUpSelectors = [
    ".section-head",
    ".alt-text > *",
    ".product-preview",
    ".testimonial",
    ".feature-panel-header",
    ".stat",
  ];
  fadeUpSelectors.forEach(function (sel) {
    document.querySelectorAll(sel).forEach(function (el) {
      if (el.closest(".hero")) return; // hero already handled by the load-in above
      gsap.from(el, {
        y: 28, opacity: 0, duration: 0.65, ease: EASE,
        scrollTrigger: { trigger: el, start: "top 88%" },
      });
    });
  });

  // Grid children (track cards, feature cards, checklist items) stagger
  // together as a group instead of animating one at a time down the page.
  document.querySelectorAll(".grid, .feature-checklist, .pill-bar").forEach(function (group) {
    var items = group.children;
    if (!items.length || group.closest(".hero")) return;
    gsap.from(items, {
      y: 24, opacity: 0, duration: 0.6, ease: EASE, stagger: 0.07,
      scrollTrigger: { trigger: group, start: "top 90%" },
    });
  });

  // --- Manifesto word reveal, scrubbed to scroll position for a smooth,
  // continuous brighten-as-you-scroll effect (replaces the plain-JS
  // fallback in main.js, which only runs if GSAP isn't available).
  document.querySelectorAll("[data-scroll-reveal]").forEach(function (el) {
    var words = el.querySelectorAll(".reveal-word");
    if (!words.length) return;
    gsap.to(words, {
      color: "var(--text-primary)",
      stagger: 0.04,
      ease: "none",
      scrollTrigger: { trigger: el, start: "top 80%", end: "bottom 45%", scrub: 0.4 },
    });
  });

  // --- Pinned "why register" scrollytelling (per-track pages): the section
  // locks in place while the visitor scrolls, and the "why join" reasons
  // brighten in one at a time before the page releases and continues —
  // the specific "hold in place" technique behind the reference sites.
  // Skipped on narrow viewports: pin-based scrollytelling is the one
  // technique here most prone to jank on real mobile browsers (toolbar
  // show/hide, viewport-height quirks), so phones get a plain stacked
  // list instead — still fully readable, just without the pin.
  document.querySelectorAll(".why-pin-section").forEach(function (section) {
    var reasons = section.querySelectorAll(".why-reason");
    if (!reasons.length) return;

    if (window.innerWidth < 700) {
      gsap.from(reasons, {
        y: 20, opacity: 0, duration: 0.5, ease: EASE, stagger: 0.12,
        scrollTrigger: { trigger: section, start: "top 85%" },
      });
      return;
    }

    gsap.set(reasons, { opacity: 0.28, y: 14 });
    gsap.set(reasons[0], { opacity: 1, y: 0 });

    var header = section.querySelectorAll(".track-icon-wrap, .eyebrow, h2");
    if (header.length) {
      gsap.from(header, {
        y: 24, opacity: 0, duration: 0.6, ease: EASE, stagger: 0.08,
        scrollTrigger: { trigger: section, start: "top 80%" },
      });
    }

    var tl = gsap.timeline({
      scrollTrigger: {
        trigger: section,
        start: "top top+=84",
        end: "+=" + Math.max(reasons.length * 420, 600),
        pin: true,
        scrub: 0.6,
        anticipatePin: 1,
      },
    });
    for (var i = 1; i < reasons.length; i++) {
      tl.to(reasons[i - 1], { opacity: 0.28, y: -14, duration: 0.3 }, i - 1)
        .to(reasons[i], { opacity: 1, y: 0, duration: 0.3 }, i - 1);
    }
  });

  // --- Stacked story cards (FAQ page): the stacking itself is plain CSS
  // position:sticky (see .faq-story-card), no scroll-jacking involved.
  // This just adds a quick scale/fade as each card arrives at its sticky
  // position, so the stack builds with a bit of motion instead of
  // snapping in — skipped on narrow viewports, where the CSS drops the
  // sticky positioning entirely and this becomes a plain static list.
  if (window.innerWidth >= 640) {
    document.querySelectorAll(".faq-story-card").forEach(function (card) {
      gsap.from(card, {
        y: 36, scale: 0.95, opacity: 0, duration: 0.5, ease: EASE,
        scrollTrigger: { trigger: card, start: "top 92%", end: "top 65%", scrub: 0.4 },
      });
    });
  }

  // --- Countdown / stat numbers get a quick count-up instead of just
  // appearing, when they first scroll into view.
  document.querySelectorAll(".stat .num").forEach(function (el) {
    var text = el.textContent.trim();
    var match = text.match(/^([\d,]+)(\D*)$/);
    if (!match) return;
    var end = parseInt(match[1].replace(/,/g, ""), 10);
    var suffix = match[2] || "";
    var counter = { val: 0 };
    ScrollTrigger.create({
      trigger: el, start: "top 90%", once: true,
      onEnter: function () {
        gsap.to(counter, {
          val: end, duration: 1.1, ease: "power1.out",
          onUpdate: function () { el.textContent = Math.round(counter.val).toLocaleString() + suffix; },
        });
      },
    });
  });
})();
