(function () {
  "use strict";

  var dialog = document.getElementById("signup-prompt-dialog");
  if (!dialog) return;

  var STORAGE_KEY = "csa_signup_prompt_dismissed";
  var INITIAL_DELAY_MS = 15000;
  var REPEAT_MS = 24 * 60 * 60 * 1000; // once a day — a dismissal should actually stick, not nag every minute.

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

  function show() {
    if (dialog.open || typeof dialog.showModal !== "function") return;
    dialog.showModal();
    document.body.classList.add("modal-open");
  }

  function scheduleNext() {
    var last = lastDismissedAt();
    var wait = last ? Math.max(REPEAT_MS - (Date.now() - last), 0) : INITIAL_DELAY_MS;
    setTimeout(show, wait);
  }

  // Fires on every way the dialog closes — the X button, "Maybe later",
  // clicking the backdrop, or pressing Escape (native `cancel` -> `close`)
  // — so this is the one place dismissal bookkeeping needs to live.
  dialog.addEventListener("close", function () {
    document.body.classList.remove("modal-open");
    markDismissed();
    scheduleNext();
  });

  var closeBtn = document.getElementById("signup-prompt-close");
  var laterBtn = document.getElementById("signup-prompt-later");
  var cta = document.getElementById("signup-prompt-cta");
  if (closeBtn) closeBtn.addEventListener("click", function () { dialog.close(); });
  if (laterBtn) laterBtn.addEventListener("click", function () { dialog.close(); });
  if (cta) cta.addEventListener("click", markDismissed);
  dialog.addEventListener("click", function (e) {
    if (e.target === dialog) dialog.close();
  });

  scheduleNext();
})();
