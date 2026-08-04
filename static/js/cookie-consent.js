(function () {
  "use strict";

  var STORAGE_KEY = "csa_cookie_consent";

  function readState() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      return JSON.parse(raw);
    } catch (e) {
      return null;
    }
  }

  function writeState(state) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch (e) {
      /* localStorage unavailable (private mode etc) — consent just won't persist */
    }
    document.dispatchEvent(new CustomEvent("csa:consent-changed", { detail: state }));
  }

  var banner = document.getElementById("cookie-banner");
  var modalBackdrop = document.getElementById("cookie-modal-backdrop");
  var analyticsToggle = document.getElementById("consent-analytics");
  var marketingToggle = document.getElementById("consent-marketing");

  function hideBanner() { if (banner) banner.classList.remove("visible"); }
  function showBanner() { if (banner) banner.classList.add("visible"); }
  function openModal() {
    var state = readState() || { necessary: true, analytics: false, marketing: false };
    if (analyticsToggle) analyticsToggle.checked = !!state.analytics;
    if (marketingToggle) marketingToggle.checked = !!state.marketing;
    if (modalBackdrop) modalBackdrop.classList.add("visible");
  }
  function closeModal() { if (modalBackdrop) modalBackdrop.classList.remove("visible"); }

  document.getElementById("cookie-accept-all") && document.getElementById("cookie-accept-all").addEventListener("click", function () {
    writeState({ necessary: true, analytics: true, marketing: true, decided: true });
    hideBanner();
  });

  document.getElementById("cookie-reject-all") && document.getElementById("cookie-reject-all").addEventListener("click", function () {
    writeState({ necessary: true, analytics: false, marketing: false, decided: true });
    hideBanner();
  });

  document.getElementById("cookie-manage") && document.getElementById("cookie-manage").addEventListener("click", function () {
    openModal();
  });

  document.getElementById("cookie-modal-close") && document.getElementById("cookie-modal-close").addEventListener("click", closeModal);
  modalBackdrop && modalBackdrop.addEventListener("click", function (e) {
    if (e.target === modalBackdrop) closeModal();
  });

  document.getElementById("cookie-save-preferences") && document.getElementById("cookie-save-preferences").addEventListener("click", function () {
    writeState({
      necessary: true,
      analytics: analyticsToggle ? analyticsToggle.checked : false,
      marketing: marketingToggle ? marketingToggle.checked : false,
      decided: true,
    });
    closeModal();
    hideBanner();
  });

  // Public API — any future analytics/marketing script should check
  // window.csaConsent.hasConsent('analytics') before loading, so nothing
  // non-essential runs before the user opts in.
  window.csaConsent = {
    getState: function () {
      return readState() || { necessary: true, analytics: false, marketing: false, decided: false };
    },
    hasConsent: function (category) {
      var state = readState();
      if (category === "necessary") return true;
      return !!(state && state[category]);
    },
    openPreferences: openModal,
  };

  var existing = readState();
  if (!existing || !existing.decided) {
    showBanner();
  }
})();
