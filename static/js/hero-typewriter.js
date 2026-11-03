// Animates the hero headline's middle word — "Learn to [build/design/secure]
// the web, for real." — typing each one in, holding, then clearing it before
// typing the next. Respects prefers-reduced-motion by just showing the
// first word with no animation.
(function () {
  var el = document.getElementById("hero-verb");
  if (!el) return;

  var WORDS = ["build", "design", "secure"];
  var TYPE_MS = 85, DELETE_MS = 45, HOLD_MS = 1600, GAP_MS = 300;

  if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    el.textContent = WORDS[0];
    return;
  }

  var wordIndex = 0;
  var charIndex = WORDS[0].length; // starts already showing the first word in the markup
  var deleting = false;

  function tick() {
    var word = WORDS[wordIndex];
    if (!deleting) {
      charIndex++;
      el.textContent = word.slice(0, charIndex);
      if (charIndex === word.length) {
        deleting = true;
        setTimeout(tick, HOLD_MS);
        return;
      }
      setTimeout(tick, TYPE_MS);
    } else {
      charIndex--;
      el.textContent = word.slice(0, charIndex);
      if (charIndex === 0) {
        deleting = false;
        wordIndex = (wordIndex + 1) % WORDS.length;
        setTimeout(tick, GAP_MS);
        return;
      }
      setTimeout(tick, DELETE_MS);
    }
  }

  setTimeout(function () { deleting = true; tick(); }, HOLD_MS);
})();
