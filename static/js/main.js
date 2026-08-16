(function () {
  "use strict";

  // --- Lite-mode: swap glass blur for a flat panel on slow connections
  // or data-saver mode, since backdrop-filter is GPU-expensive and a
  // meaningful share of visitors are on mid-range Android + average data.
  function shouldUseLiteMode() {
    var conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    if (!conn) return false;
    if (conn.saveData) return true;
    if (conn.effectiveType && /2g/.test(conn.effectiveType)) return true;
    return false;
  }
  if (shouldUseLiteMode()) {
    document.documentElement.classList.add("lite-mode");
  }

  // --- Theme toggle: light is the default look (see the inline pre-paint
  // script in <head> that sets data-theme before first render). Flips the
  // attribute and remembers the choice — never follows OS
  // prefers-color-scheme automatically. Where supported, wraps the switch
  // in a same-document View Transition so it expands as a circle from the
  // exact point clicked, instead of just snapping to the new theme.
  var themeToggle = document.getElementById("theme-toggle");
  if (themeToggle) {
    var themeLabel = themeToggle.querySelector(".theme-toggle-label");
    var syncThemeLabel = function () {
      if (!themeLabel) return;
      var isLight = document.documentElement.getAttribute("data-theme") === "light";
      themeLabel.textContent = isLight ? "Switch to dark mode" : "Switch to light mode";
    };
    syncThemeLabel();

    themeToggle.addEventListener("click", function (e) {
      var current = document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark";
      var next = current === "light" ? "dark" : "light";
      var applyTheme = function () {
        document.documentElement.setAttribute("data-theme", next);
        try { localStorage.setItem("csa_theme", next); } catch (err) { /* private mode etc — just won't persist */ }
        syncThemeLabel();
      };

      var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      if (!document.startViewTransition || reduceMotion) {
        applyTheme();
        return;
      }

      var x = e.clientX, y = e.clientY;
      var endRadius = Math.hypot(
        Math.max(x, window.innerWidth - x),
        Math.max(y, window.innerHeight - y)
      );
      var transition = document.startViewTransition(applyTheme);
      transition.ready.then(function () {
        document.documentElement.animate(
          { clipPath: ["circle(0px at " + x + "px " + y + "px)", "circle(" + endRadius + "px at " + x + "px " + y + "px)"] },
          { duration: 550, easing: "ease-in-out", pseudoElement: "::view-transition-new(root)" }
        );
      });
    });
  }

  // --- Top loading bar + circular-reveal origin on internal link clicks:
  // the bar gives an immediate visible response even before the new
  // document arrives (this is a multi-page app with real navigation
  // latency — matters most on the slower connections the brief flags).
  // The click position gets stashed in sessionStorage so the *arriving*
  // page can replay the same circular-reveal effect used on the theme
  // toggle, expanding from wherever the link was actually clicked — see
  // the `pagereveal` listener in the inline <head> script, which is what
  // reads this back.
  (function () {
    var bar = document.getElementById("nav-progress");
    document.addEventListener("click", function (e) {
      if (e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
      var link = e.target.closest("a[href]");
      if (!link || link.target === "_blank" || link.hasAttribute("download")) return;
      var href = link.getAttribute("href");
      if (!href || /^(#|mailto:|tel:|javascript:)/.test(href)) return;
      var url;
      try { url = new URL(href, window.location.href); } catch (err) { return; }
      if (url.origin !== window.location.origin) return;
      if (url.pathname === window.location.pathname && url.search === window.location.search) return;

      try {
        sessionStorage.setItem("csa_vt_origin", JSON.stringify({ x: e.clientX, y: e.clientY, t: Date.now() }));
      } catch (err) { /* private mode etc — the arriving page just won't find an origin and skips the reveal */ }

      if (!bar) return;
      bar.style.transition = "none";
      bar.style.width = "0%";
      bar.classList.add("active");
      // eslint-disable-next-line no-unused-expressions
      bar.offsetHeight; // force reflow so the width reset applies before animating
      bar.style.transition = "width 4s cubic-bezier(0.1, 0.7, 0.3, 1), opacity 200ms ease";
      requestAnimationFrame(function () { bar.style.width = "80%"; });
    });
    if (bar) {
      window.addEventListener("pagehide", function () {
        bar.style.transition = "width 150ms ease";
        bar.style.width = "100%";
      });
    }
  })();

  // --- Hero spotlight: soft glow that follows the cursor, the kind of
  // "feels alive" detail the brief asked for. Skipped in lite-mode/touch.
  document.querySelectorAll(".hero").forEach(function (hero) {
    if (document.documentElement.classList.contains("lite-mode")) return;
    hero.addEventListener("pointermove", function (e) {
      var rect = hero.getBoundingClientRect();
      hero.style.setProperty("--mx", ((e.clientX - rect.left) / rect.width) * 100 + "%");
      hero.style.setProperty("--my", ((e.clientY - rect.top) / rect.height) * 100 + "%");
    });
  });

  // --- Scroll-reveal text: wraps each word of a [data-scroll-reveal]
  // paragraph in a span, then brightens words progressively as the block
  // scrolls through the viewport (dim -> full color), instead of a plain
  // fade-in-once. Skipped in lite-mode — words just render fully visible.
  document.querySelectorAll("[data-scroll-reveal]").forEach(function (el) {
    if (el.dataset.revealInit) return;
    el.dataset.revealInit = "1";
    var text = el.textContent;
    el.innerHTML = text.split(/(\s+)/).map(function (chunk) {
      return /\s+/.test(chunk) ? chunk : '<span class="reveal-word">' + chunk + "</span>";
    }).join("");
  });

  // The actual scroll-linked progress is driven by animations.js via GSAP
  // ScrollTrigger when it's available — this is only the fallback path for
  // lite-mode or if the GSAP CDN failed to load, so words still reveal
  // (just via a plain scroll listener instead of a scrubbed timeline).
  var revealEls = document.querySelectorAll("[data-scroll-reveal]");
  if (revealEls.length && !window.gsap && !document.documentElement.classList.contains("lite-mode")) {
    var updateReveal = function () {
      revealEls.forEach(function (el) {
        var rect = el.getBoundingClientRect();
        var vh = window.innerHeight;
        // Progress 0 -> 1 as the block travels from just entering the
        // bottom of the viewport to reaching its middle.
        var progress = (vh - rect.top) / (vh * 0.6 + rect.height * 0.4);
        progress = Math.max(0, Math.min(1, progress));
        var words = el.querySelectorAll(".reveal-word");
        var revealCount = Math.round(progress * words.length);
        words.forEach(function (w, i) {
          w.classList.toggle("revealed", i < revealCount);
        });
      });
    };
    var ticking = false;
    window.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () { updateReveal(); ticking = false; });
    }, { passive: true });
    updateReveal();
  } else if (!window.gsap) {
    revealEls.forEach(function (el) { el.querySelectorAll(".reveal-word").forEach(function (w) { w.classList.add("revealed"); }); });
  }

  // --- Testimonial carousel: works for any [partials/testimonial_carousel.html]
  // instance on the page (homepage, per-track pages) without needing a
  // page-specific ID, since each page only ever includes one.
  document.querySelectorAll(".testimonial-nav").forEach(function (nav) {
    var panel = nav.closest(".testimonial");
    if (!panel) return;
    var slides = panel.querySelectorAll(".testimonial-slide");
    nav.querySelectorAll("button").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var target = btn.getAttribute("data-goto");
        slides.forEach(function (s) { s.style.display = s.getAttribute("data-index") === target ? "" : "none"; });
        nav.querySelectorAll("button").forEach(function (b) { b.classList.toggle("active", b === btn); });
      });
    });
  });

  // --- Mobile nav toggle: same circular-reveal treatment as the theme
  // toggle and page transitions, scoped to just the nav panel (not the
  // whole page) via its own view-transition-name, expanding from the
  // hamburger button itself. The name is only set for the moment the
  // transition runs, then cleared — so it doesn't affect page-to-page
  // navigation transitions the rest of the time.
  var toggle = document.getElementById("nav-toggle");
  var nav = document.getElementById("main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = !nav.classList.contains("open");
      var applyState = function () {
        nav.classList.toggle("open", open);
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
      };

      var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      if (!document.startViewTransition || reduceMotion) {
        applyState();
        return;
      }

      var rect = toggle.getBoundingClientRect();
      var x = rect.left + rect.width / 2, y = rect.top + rect.height / 2;
      var endRadius = Math.hypot(window.innerWidth, window.innerHeight);

      nav.style.viewTransitionName = "main-nav-panel";
      var transition = document.startViewTransition(applyState);
      transition.finished.finally(function () { nav.style.viewTransitionName = ""; });
      transition.ready.then(function () {
        var pseudo = open ? "::view-transition-new(main-nav-panel)" : "::view-transition-old(main-nav-panel)";
        var frames = open
          ? { clipPath: ["circle(0px at " + x + "px " + y + "px)", "circle(" + endRadius + "px at " + x + "px " + y + "px)"] }
          : { clipPath: ["circle(" + endRadius + "px at " + x + "px " + y + "px)", "circle(0px at " + x + "px " + y + "px)"] };
        document.documentElement.animate(frames, { duration: 420, easing: "ease-in-out", pseudoElement: pseudo });
      });
    });
  }

  // --- Nav search: collapses to an icon button, expands into an input on
  // click so it never fights the nav links for horizontal space.
  var searchWrap = document.getElementById("nav-search");
  var searchToggle = document.getElementById("search-toggle");
  var searchInput = document.getElementById("nav-search-input");
  if (searchWrap && searchToggle && searchInput) {
    searchToggle.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = !searchWrap.classList.contains("open");
      searchWrap.classList.toggle("open", open);
      searchToggle.setAttribute("aria-expanded", open ? "true" : "false");
      if (open) searchInput.focus();
    });
    document.addEventListener("click", function (e) {
      if (!searchWrap.contains(e.target)) {
        searchWrap.classList.remove("open");
        searchToggle.setAttribute("aria-expanded", "false");
      }
    });
    searchInput.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        searchWrap.classList.remove("open");
        searchToggle.setAttribute("aria-expanded", "false");
        searchToggle.focus();
      }
    });
  }

  // --- Cohort countdown timers: any element with [data-countdown="ISO-DATE"]
  function pad(n) { return String(n).padStart(2, "0"); }

  function tickCountdowns() {
    document.querySelectorAll("[data-countdown]").forEach(function (el) {
      var target = new Date(el.getAttribute("data-countdown")).getTime();
      var diff = target - Date.now();
      if (isNaN(target)) return;
      if (diff <= 0) {
        el.innerHTML = '<span class="unit"><span class="val">Started</span></span>';
        return;
      }
      var days = Math.floor(diff / 86400000);
      var hours = Math.floor((diff % 86400000) / 3600000);
      var mins = Math.floor((diff % 3600000) / 60000);
      var secs = Math.floor((diff % 60000) / 1000);
      el.innerHTML =
        '<div class="unit"><span class="val">' + days + '</span><span class="lbl">Days</span></div>' +
        '<div class="unit"><span class="val">' + pad(hours) + '</span><span class="lbl">Hrs</span></div>' +
        '<div class="unit"><span class="val">' + pad(mins) + '</span><span class="lbl">Min</span></div>' +
        '<div class="unit"><span class="val">' + pad(secs) + '</span><span class="lbl">Sec</span></div>';
    });
  }
  if (document.querySelector("[data-countdown]")) {
    tickCountdowns();
    setInterval(tickCountdowns, 1000);
  }

  // --- Seat-hold checkout countdown (shown while a Paystack payment is in flight)
  document.querySelectorAll("[data-hold-expires]").forEach(function (el) {
    var target = new Date(el.getAttribute("data-hold-expires")).getTime();
    var timer = setInterval(function () {
      var diff = target - Date.now();
      if (diff <= 0) {
        el.textContent = "Hold expiring, refresh if payment hasn't completed.";
        clearInterval(timer);
        return;
      }
      var mins = Math.floor(diff / 60000);
      var secs = Math.floor((diff % 60000) / 1000);
      el.textContent = "Seat held for " + mins + ":" + pad(secs);
    }, 1000);
  });

  // --- Password fields: a show/hide eye toggle on every password input
  // (login, signup, change/reset password all use plain <input
  // type="password"> from allauth, so this is one generic enhancement
  // rather than something wired per-template), plus live strength/match
  // feedback on signup and reset-from-key forms — one unmet rule at a
  // time, not a checklist dumped on the user all at once.
  var EYE_OPEN = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7-11-7-11-7z"/><circle cx="12" cy="12" r="3"/></svg>';
  var EYE_CLOSED = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.94 10.94 0 0 1 12 20c-7 0-11-7-11-7a20.6 20.6 0 0 1 5.06-5.94M9.9 4.24A10.6 10.6 0 0 1 12 4c7 0 11 7 11 7a20.6 20.6 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><path d="M1 1l22 22"/></svg>';

  document.querySelectorAll('input[type="password"]').forEach(function (input) {
    var wrap = document.createElement("div");
    wrap.className = "pw-field-wrap";
    input.parentNode.insertBefore(wrap, input);
    wrap.appendChild(input);

    var toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "pw-toggle";
    toggle.setAttribute("aria-label", "Show password");
    toggle.innerHTML = EYE_OPEN;
    wrap.appendChild(toggle);

    toggle.addEventListener("click", function () {
      var showing = input.type === "text";
      input.type = showing ? "password" : "text";
      toggle.innerHTML = showing ? EYE_OPEN : EYE_CLOSED;
      toggle.setAttribute("aria-label", showing ? "Show password" : "Hide password");
    });
  });

  function pwFeedbackEl(input) {
    var el = document.createElement("p");
    el.className = "pw-feedback";
    input.closest(".pw-field-wrap").insertAdjacentElement("afterend", el);
    return el;
  }

  var pw1 = document.querySelector('input[name="password1"]');
  var pw2 = document.querySelector('input[name="password2"]');

  if (pw1) {
    var fb1 = pwFeedbackEl(pw1);
    pw1.addEventListener("input", function () {
      var v = pw1.value;
      if (!v) { fb1.textContent = ""; fb1.className = "pw-feedback"; }
      else if (v.length < 8) { fb1.textContent = "Needs to be at least 8 characters."; fb1.className = "pw-feedback pw-feedback-error"; }
      else if (!/[0-9]/.test(v)) { fb1.textContent = "Add at least one number."; fb1.className = "pw-feedback pw-feedback-error"; }
      else if (!/[a-zA-Z]/.test(v)) { fb1.textContent = "Add at least one letter."; fb1.className = "pw-feedback pw-feedback-error"; }
      else { fb1.textContent = "Looks good."; fb1.className = "pw-feedback pw-feedback-ok"; }
      if (pw2 && pw2.value) pw2.dispatchEvent(new Event("input"));
    });
  }

  if (pw2) {
    var fb2 = pwFeedbackEl(pw2);
    pw2.addEventListener("input", function () {
      var v = pw2.value;
      if (!v) { fb2.textContent = ""; fb2.className = "pw-feedback"; }
      else if (pw1 && v !== pw1.value) { fb2.textContent = "Passwords don't match yet."; fb2.className = "pw-feedback pw-feedback-error"; }
      else { fb2.textContent = "Passwords match."; fb2.className = "pw-feedback pw-feedback-ok"; }
    });
  }
})();
