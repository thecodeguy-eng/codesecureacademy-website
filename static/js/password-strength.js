// Replaces the static "your password can't be..." rules list with a live
// strength meter as the signup password field is typed into. The rules
// list itself is left in the DOM (not removed) as a no-JS fallback and
// for screen readers — this just visually supersedes it once JS runs.
(function () {
  "use strict";

  var input = document.getElementById("id_password1");
  if (!input) return;

  var helptext = document.getElementById("id_password1_helptext");

  var meter = document.createElement("div");
  meter.className = "password-strength";
  meter.innerHTML =
    '<div class="password-strength-track"><div class="password-strength-fill" data-fill></div></div>' +
    '<span class="password-strength-label" data-label></span>';
  input.insertAdjacentElement("afterend", meter);

  var fill = meter.querySelector("[data-fill]");
  var label = meter.querySelector("[data-label]");

  var LEVELS = [
    { cls: "weak", text: "Weak" },
    { cls: "fair", text: "Fair" },
    { cls: "good", text: "Good" },
    { cls: "strong", text: "Strong" },
  ];

  function score(pw) {
    if (!pw) return -1;
    var s = 0;
    if (pw.length >= 8) s++;
    if (pw.length >= 12) s++;
    if (/[a-z]/.test(pw) && /[A-Z]/.test(pw)) s++;
    if (/[0-9]/.test(pw)) s++;
    if (/[^A-Za-z0-9]/.test(pw)) s++;
    return Math.min(s, 4);
  }

  function update() {
    var pw = input.value;
    var s = score(pw);
    if (s < 0) {
      meter.classList.remove("visible");
      if (helptext) helptext.style.display = "";
      return;
    }
    meter.classList.add("visible");
    if (helptext) helptext.style.display = "none";
    var level = LEVELS[Math.max(s - 1, 0)];
    meter.className = "password-strength visible " + level.cls;
    fill.style.width = (25 * (s)) + "%";
    label.textContent = level.text;
  }

  input.addEventListener("input", update);
  update();
})();
