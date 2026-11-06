(function () {
  "use strict";

  var dialog = document.getElementById("live-session-dialog");
  if (!dialog) return;

  // Nothing to show once the session itself is over — Saturday, Nov 7
  // 2026, 9:00 PM WAT (UTC+1).
  var SESSION_ENDS = new Date("2026-11-07T21:00:00+01:00");
  if (new Date() > SESSION_ENDS) return;

  var STORAGE_KEY = "csa_live_session_dismissed_2026-11-07";

  function isDismissed() {
    try {
      return !!localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      return false;
    }
  }

  function markDismissed() {
    try { localStorage.setItem(STORAGE_KEY, "1"); } catch (e) { /* private mode etc — will just show again next visit */ }
  }

  function show() {
    if (dialog.open || typeof dialog.showModal !== "function" || isDismissed()) return;
    // Another modal already up — don't stack dialogs, just try again shortly.
    if (document.body.classList.contains("modal-open")) {
      setTimeout(show, 2000);
      return;
    }
    dialog.showModal();
    document.body.classList.add("modal-open");
  }

  dialog.addEventListener("close", function () {
    document.body.classList.remove("modal-open");
    markDismissed();
  });

  var closeBtn = document.getElementById("live-session-close");
  var laterBtn = document.getElementById("live-session-later");
  var cta = document.getElementById("live-session-cta");
  if (closeBtn) closeBtn.addEventListener("click", function () { dialog.close(); });
  if (laterBtn) laterBtn.addEventListener("click", function () { dialog.close(); });
  if (cta) cta.addEventListener("click", markDismissed);
  dialog.addEventListener("click", function (e) {
    if (e.target === dialog) dialog.close();
  });

  setTimeout(show, 1500);
})();
