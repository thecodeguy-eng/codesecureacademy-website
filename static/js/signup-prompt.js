(function () {
  "use strict";

  var backdrop = document.getElementById("signup-prompt-backdrop");
  if (!backdrop) return;

  var STORAGE_KEY = "csa_signup_prompt_dismissed";
  var INITIAL_DELAY_MS = 15000;
  var REPEAT_MS = 60000;

  function lastDismissedAt() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      var t = parseInt(raw, 10);
      return isNaN(t) ? null : t;
    } catch (e) {
      return null;
    }
  }

  function markDismissed() {
    try { localStorage.setItem(STORAGE_KEY, String(Date.now())); } catch (e) { /* private mode etc — will just show again next visit */ }
  }

  function show() { backdrop.classList.add("visible"); }

  // Every dismissal (X, "Maybe later", clicking outside, Escape, or the CTA
  // itself) reschedules the next appearance a minute out — keeps nagging
  // once a minute, on this page or the next one they navigate to, until
  // they actually register or log in (at which point this whole partial
  // stops rendering server-side, so this script never even loads).
  function hide() {
    backdrop.classList.remove("visible");
    markDismissed();
    scheduleNext();
  }

  function scheduleNext() {
    var last = lastDismissedAt();
    var wait = last ? Math.max(REPEAT_MS - (Date.now() - last), 0) : INITIAL_DELAY_MS;
    setTimeout(show, wait);
  }

  var closeBtn = document.getElementById("signup-prompt-close");
  var laterBtn = document.getElementById("signup-prompt-later");
  var cta = document.getElementById("signup-prompt-cta");
  if (closeBtn) closeBtn.addEventListener("click", hide);
  if (laterBtn) laterBtn.addEventListener("click", hide);
  if (cta) cta.addEventListener("click", markDismissed);
  backdrop.addEventListener("click", function (e) {
    if (e.target === backdrop) hide();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && backdrop.classList.contains("visible")) hide();
  });

  scheduleNext();
})();
