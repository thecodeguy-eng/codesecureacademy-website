(function () {
  "use strict";

  var backdrop = document.getElementById("signup-prompt-backdrop");
  if (!backdrop) return;

  var STORAGE_KEY = "csa_signup_prompt_dismissed";
  var DELAY_MS = 15000;
  var SNOOZE_DAYS = 14;

  function dismissedRecently() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return false;
      var dismissedAt = parseInt(raw, 10);
      if (isNaN(dismissedAt)) return false;
      return Date.now() - dismissedAt < SNOOZE_DAYS * 24 * 60 * 60 * 1000;
    } catch (e) {
      return false;
    }
  }

  function markDismissed() {
    try { localStorage.setItem(STORAGE_KEY, String(Date.now())); } catch (e) { /* private mode etc — will just show again next visit */ }
  }

  function show() { backdrop.classList.add("visible"); }
  function hide() { backdrop.classList.remove("visible"); markDismissed(); }

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

  if (dismissedRecently()) return;
  setTimeout(show, DELAY_MS);
})();
