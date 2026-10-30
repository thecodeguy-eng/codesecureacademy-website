(function () {
  "use strict";

  var dialog = document.getElementById("announcement-dialog");
  if (!dialog) return;

  var STORAGE_KEY = "csa_announcement_dismissed_v" + (dialog.getAttribute("data-version") || "1");
  var INITIAL_DELAY_MS = 4000;
  var REPEAT_MS = 24 * 60 * 60 * 1000; // once a day, same as the signup prompt.

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
    // Another modal (e.g. the signup prompt) is already up — don't stack
    // dialogs on top of each other, just try again shortly.
    if (document.body.classList.contains("modal-open")) {
      setTimeout(show, 2000);
      return;
    }
    dialog.showModal();
    document.body.classList.add("modal-open");
  }

  function scheduleNext() {
    var last = lastDismissedAt();
    var wait = last ? Math.max(REPEAT_MS - (Date.now() - last), 0) : INITIAL_DELAY_MS;
    setTimeout(show, wait);
  }

  dialog.addEventListener("close", function () {
    document.body.classList.remove("modal-open");
    markDismissed();
    scheduleNext();
  });

  var closeBtn = document.getElementById("announcement-close");
  var laterBtn = document.getElementById("announcement-later");
  var cta = document.getElementById("announcement-cta");
  if (closeBtn) closeBtn.addEventListener("click", function () { dialog.close(); });
  if (laterBtn) laterBtn.addEventListener("click", function () { dialog.close(); });
  if (cta) cta.addEventListener("click", markDismissed);
  dialog.addEventListener("click", function (e) {
    if (e.target === dialog) dialog.close();
  });

  scheduleNext();
})();
