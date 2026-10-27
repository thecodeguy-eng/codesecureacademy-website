// Homepage hero "try it yourself" — one playground, four tracks, so the
// demo isn't just a Frontend/coding thing. Frontend/Backend/Cybersecurity
// share a code-editor pane (textarea -> sandboxed iframe, same sandboxed
// model as tutorials/article_detail.html's editor: allow-scripts only, no
// allow-same-origin, so visitor-written code can never reach the parent
// page's cookies or CSRF token). Graphic Design swaps that for a live
// poster you edit directly (tap the text, pick colors/font/size) —
// design isn't something you do by typing config lines or code.
(function () {
  "use strict";

  var WEAK_PASSWORDS = [
    "123456", "password", "123456789", "12345678", "12345", "qwerty", "abc123",
    "111111", "iloveyou", "admin", "letmein", "welcome", "monkey", "dragon",
    "000000", "1234567", "football", "121212", "qwerty123", "1234", "passw0rd",
  ];

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function wrapIframeDoc(bodyHtml) {
    return (
      "<!doctype html><html><head><meta charset=\"utf-8\"><style>" +
      "body{font-family:system-ui,-apple-system,sans-serif;margin:0;padding:1.5rem;color:#0d1224;}" +
      ".result-title{font-weight:700;font-size:1.05rem;margin:0 0 0.4rem;}" +
      ".result-body{margin:0;line-height:1.5;}" +
      "code{background:#eef1f7;padding:0.1rem 0.35rem;border-radius:4px;font-family:ui-monospace,monospace;}" +
      "pre{background:#0d1224;color:#dfe7ff;padding:1rem;border-radius:8px;overflow:auto;font-family:ui-monospace,monospace;font-size:0.85rem;}" +
      "</style></head><body>" + bodyHtml + "</body></html>"
    );
  }

  function passwordVerdict(raw) {
    var trimmed = (raw || "").trim();
    if (!trimmed) {
      return { ok: false, title: "No password set.", body: "Add a value after <code>password = </code> and hit Run." };
    }
    var lower = trimmed.toLowerCase();
    if (WEAK_PASSWORDS.indexOf(lower) !== -1) {
      return {
        ok: false, title: "Cracked instantly.",
        body: "&quot;" + escapeHtml(trimmed) + "&quot; is on every hacker's first list. Try something long and unusual.",
      };
    }
    var hasLower = /[a-z]/.test(trimmed), hasUpper = /[A-Z]/.test(trimmed),
      hasDigit = /[0-9]/.test(trimmed), hasSymbol = /[^a-zA-Z0-9]/.test(trimmed);
    var variety = [hasLower, hasUpper, hasDigit, hasSymbol].filter(Boolean).length;

    if (trimmed.length < 8) {
      return { ok: false, title: "Cracked in under a minute.", body: "Short passwords don't survive automated guessing. Try 12+ characters." };
    }
    if (variety <= 1) {
      return { ok: false, title: "Cracked in a few hours.", body: "One character type isn't enough. Mix in uppercase, numbers, and symbols." };
    }
    if (trimmed.length >= 12 && variety >= 3) {
      return { ok: true, title: "This would take centuries to crack.", body: "Long, mixed, and unpredictable — exactly what a real password should look like." };
    }
    return { ok: true, title: "Decent, but not bulletproof.", body: "This would hold up for a while. Longer and more varied is always better." };
  }

  var TRACKS = {
    frontend: {
      label: "Frontend",
      instruction: "Edit the HTML, then hit Run.",
      starter:
        "<!-- edit this, then hit Run -->\n<h1>You can play around with this code</h1>\n" +
        "<p>This preview is live. Try changing it.</p>\n<style>\n" +
        "  body { font-family: sans-serif; color: #2f7dff; text-align: center; padding: 2rem; }\n</style>",
      run: function (code) { return code; },
    },
    backend: {
      label: "Backend",
      instruction: "This is a tiny server. Change the details it sends back, then press Run.",
      starter:
        "// A server's job is to send back data.\n// Change the values below and hit Run.\n\n" +
        "function getStudent() {\n  return {\n    name: \"Ada\",\n    track: \"Backend\",\n    cohort: 3\n  };\n}",
      run: function (code) {
        var script =
          "try {\n" + code + "\n" +
          "var __r = getStudent();\n" +
          "var __j = JSON.stringify(__r, null, 2).replace(/</g, '&lt;');\n" +
          "document.write('<p class=\"result-title\" style=\"color:#0a7a3d;\">200 OK</p>" +
          "<p class=\"result-body\">The server replied with:</p><pre>' + __j + '</pre>');\n" +
          "} catch (e) {\n" +
          "document.write('<p class=\"result-title\" style=\"color:#c0392b;\">500 Error</p>" +
          "<p class=\"result-body\">' + String(e.message).replace(/</g, '&lt;') + '</p>');\n" +
          "}";
        return wrapIframeDoc("<script>" + script + "<\/script>");
      },
    },
    cybersecurity: {
      label: "Cybersecurity",
      instruction: "Hackers guess passwords first. Change the password and see how long they'd need.",
      starter: "// A hacker's computer is guessing your password.\n// Change it below, then hit Run.\n\npassword = \"123456\"",
      run: function (code) {
        var match = code.match(/password\s*=\s*["'](.*?)["']/);
        var verdict = passwordVerdict(match ? match[1] : "");
        var color = verdict.ok ? "#0a7a3d" : "#c0392b";
        return wrapIframeDoc(
          '<p class="result-title" style="color:' + color + ';">' + escapeHtml(verdict.title) + "</p>" +
          '<p class="result-body">' + verdict.body + "</p>"
        );
      },
    },
  };

  var PALETTES = [
    { bg: "#0d1224", text: "#ffffff", tagline: "rgba(255,255,255,.72)", blob: "#2f7dff" },
    { bg: "#06231a", text: "#ffffff", tagline: "rgba(255,255,255,.72)", blob: "#1fae6e" },
    { bg: "#241206", text: "#ffffff", tagline: "rgba(255,255,255,.72)", blob: "#ff8a3d" },
    { bg: "#240a0a", text: "#ffd84d", tagline: "rgba(255,255,255,.78)", blob: "#e23b3b" },
    { bg: "#140a24", text: "#ffffff", tagline: "rgba(255,255,255,.72)", blob: "#8f7dff" },
    { bg: "#240a1c", text: "#ffffff", tagline: "rgba(255,255,255,.72)", blob: "#ff5fa8" },
  ];
  var FONT_STACKS = {
    serif: "Georgia, 'Times New Roman', serif",
    sans: "var(--font-sans)",
    mono: "var(--font-mono)",
    bold: "var(--font-sans)",
  };

  function initCodePanel(root) {
    var tabs = root.querySelectorAll("[data-track-tab]");
    var input = root.querySelector("[data-track-input]");
    var output = root.querySelector("[data-track-output]");
    var instruction = root.querySelector("[data-track-instruction]");
    var footer = root.querySelector("[data-track-footer]");
    var runBtn = root.querySelector("[data-track-run]");
    var codePanes = root.querySelectorAll("[data-track-code-panes]");
    var poster = root.querySelector("[data-poster-editor]");
    if (!tabs.length || !input || !output) return;

    var order = ["frontend", "backend", "cybersecurity", "graphic_design"];
    var requestedTab = root.getAttribute("data-initial-tab");
    var current = order.indexOf(requestedTab) !== -1 ? requestedTab : "frontend";
    // A dedicated per-track page (data-initial-tab set) is a focused tool
    // for that one track — it shouldn't auto-rotate away to a different
    // one. Only the homepage hero's showcase carousel does that.
    var autoRotate = !requestedTab && !(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
    var paused = false;
    var timer = null;

    function render() {
      var track = TRACKS[current];
      if (track) output.srcdoc = track.run(input.value);
    }

    function stopAutoRotate() {
      if (!autoRotate) return;
      autoRotate = false;
      if (timer) clearInterval(timer);
      footer.textContent = "Auto-switching is off. Pick any track above.";
    }

    function selectTrack(id, userInitiated) {
      current = id;
      var isDesign = id === "graphic_design";

      tabs.forEach(function (t) {
        var active = t.getAttribute("data-track-tab") === id;
        t.classList.toggle("active", active);
        t.setAttribute("aria-selected", active ? "true" : "false");
      });

      codePanes.forEach(function (el) { el.hidden = isDesign; });
      if (poster) poster.hidden = !isDesign;

      if (isDesign) {
        instruction.textContent = "Tap the words on the poster to type. Pick colors, a font, and a size.";
      } else {
        var track = TRACKS[id];
        instruction.textContent = track.instruction;
        input.value = track.starter;
        render();
      }

      if (userInitiated) stopAutoRotate();
    }

    function tick() {
      if (!autoRotate || paused) return;
      var idx = order.indexOf(current);
      selectTrack(order[(idx + 1) % order.length], false);
    }

    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        selectTrack(tab.getAttribute("data-track-tab"), true);
      });
    });

    input.addEventListener("input", function () { stopAutoRotate(); });
    input.addEventListener("focus", stopAutoRotate);
    if (runBtn) runBtn.addEventListener("click", function () { render(); stopAutoRotate(); });

    root.addEventListener("mouseenter", function () { paused = true; });
    root.addEventListener("mouseleave", function () { paused = false; });
    root.addEventListener("pointerdown", function (e) {
      // Touching the poster editor should stop rotation too, same as
      // typing/Run does for the code tabs — any real interaction counts.
      if (e.target.closest("[data-poster-editor]")) stopAutoRotate();
    });
    root.addEventListener("input", function (e) {
      if (e.target.closest("[data-poster-editor]")) stopAutoRotate();
    });

    selectTrack(current, false);
    footer.textContent = autoRotate
      ? "Auto-switching between tracks. Tap one, type, or edit to stop it."
      : "Auto-switching is off. Pick any track above.";
    if (autoRotate) timer = setInterval(tick, 7000);
  }

  function initPosterEditor(root) {
    var editor = root.querySelector("[data-poster-editor]");
    if (!editor) return;
    var canvas = editor.querySelector("[data-poster-canvas]");
    var blob = editor.querySelector("[data-poster-blob]");
    var headline = editor.querySelector("[data-poster-headline]");
    var tagline = editor.querySelector("[data-poster-tagline]");
    var swatches = editor.querySelectorAll("[data-palette]");
    var fontBtns = editor.querySelectorAll("[data-font]");
    var alignBtns = editor.querySelectorAll("[data-align]");
    var sizeInput = editor.querySelector("[data-poster-size]");
    var surpriseBtn = editor.querySelector("[data-poster-surprise]");
    if (!canvas || !headline || !tagline) return;

    var state = { palette: 0, font: "sans", align: "left", size: 32 };

    function applyPalette() {
      var p = PALETTES[state.palette];
      canvas.style.background = p.bg;
      headline.style.color = p.text;
      tagline.style.color = p.tagline;
      if (blob) blob.style.background = p.blob;
      swatches.forEach(function (sw, i) { sw.classList.toggle("active", i === state.palette); });
    }
    function applyFont() {
      var stack = FONT_STACKS[state.font];
      headline.style.fontFamily = stack;
      headline.style.fontWeight = state.font === "bold" ? "900" : "700";
      headline.style.textTransform = state.font === "bold" ? "uppercase" : "none";
      fontBtns.forEach(function (b) { b.classList.toggle("active", b.getAttribute("data-font") === state.font); });
    }
    function applyAlign() {
      canvas.classList.toggle("is-centered", state.align === "center");
      alignBtns.forEach(function (b) { b.classList.toggle("active", b.getAttribute("data-align") === state.align); });
    }
    function applySize() {
      headline.style.fontSize = state.size + "px";
    }

    swatches.forEach(function (sw, i) {
      sw.addEventListener("click", function () { state.palette = i; applyPalette(); });
    });
    fontBtns.forEach(function (b) {
      b.addEventListener("click", function () { state.font = b.getAttribute("data-font"); applyFont(); });
    });
    alignBtns.forEach(function (b) {
      b.addEventListener("click", function () { state.align = b.getAttribute("data-align"); applyAlign(); });
    });
    if (sizeInput) {
      sizeInput.addEventListener("input", function () {
        state.size = parseInt(sizeInput.value, 10) || 32;
        applySize();
      });
    }
    if (surpriseBtn) {
      surpriseBtn.addEventListener("click", function () {
        state.palette = Math.floor(Math.random() * PALETTES.length);
        var fonts = Object.keys(FONT_STACKS);
        state.font = fonts[Math.floor(Math.random() * fonts.length)];
        applyPalette();
        applyFont();
      });
    }

    [headline, tagline].forEach(function (el) {
      el.addEventListener("paste", function (e) {
        e.preventDefault();
        var text = (e.clipboardData || window.clipboardData).getData("text/plain");
        document.execCommand("insertText", false, text);
      });
      el.addEventListener("keydown", function (e) {
        if (e.key === "Enter") e.preventDefault();
      });
    });

    applyPalette();
    applyFont();
    applyAlign();
    applySize();
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-track-playground]").forEach(function (root) {
      initCodePanel(root);
      initPosterEditor(root);
    });
  });
})();
