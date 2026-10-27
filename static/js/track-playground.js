// Homepage hero "try it yourself" — one playground, four tracks, so the
// demo isn't just a Frontend/coding thing. Frontend/Backend/Cybersecurity
// share a code-editor pane (textarea -> sandboxed iframe, same sandboxed
// model as tutorials/article_detail.html's editor: allow-scripts only, no
// allow-same-origin, so visitor-written code can never reach the parent
// page's cookies or CSRF token). Graphic Design swaps that for a real
// drag-and-drop challenge instead of a text box — design isn't about
// typing config lines.
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

  var FLYER_LABELS = {
    headline: "the headline",
    visual: "the visual",
    cta: "a clear call-to-action",
  };

  function initCodePanel(root) {
    var tabs = root.querySelectorAll("[data-track-tab]");
    var input = root.querySelector("[data-track-input]");
    var output = root.querySelector("[data-track-output]");
    var instruction = root.querySelector("[data-track-instruction]");
    var footer = root.querySelector("[data-track-footer]");
    var runBtn = root.querySelector("[data-track-run]");
    var codePanes = root.querySelectorAll("[data-track-code-panes]");
    var flyer = root.querySelector("[data-flyer-challenge]");
    if (!tabs.length || !input || !output) return;

    var order = ["frontend", "backend", "cybersecurity", "graphic_design"];
    var current = "frontend";
    var autoRotate = !(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
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
      if (flyer) flyer.hidden = !isDesign;

      if (isDesign) {
        instruction.textContent = "Instead of code, arrange the real pieces of a flyer. Drag each card to where it belongs.";
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
      // A drag on the flyer challenge should stop rotation too, same as
      // typing/Run does for the code tabs — any real interaction counts.
      if (e.target.closest("[data-chip]")) stopAutoRotate();
    });

    selectTrack(current, false);
    footer.textContent = autoRotate
      ? "Auto-switching between tracks. Tap one, type, or drag to stop it."
      : "Auto-switching is off. Pick any track above.";
    if (autoRotate) timer = setInterval(tick, 7000);
  }

  function initFlyerChallenge(root) {
    var challenge = root.querySelector("[data-flyer-challenge]");
    if (!challenge) return;
    var feedback = challenge.querySelector("[data-flyer-feedback]");
    var slots = challenge.querySelectorAll("[data-slot]");
    var chips = challenge.querySelectorAll("[data-chip]");

    var ghost = null;
    var activeChip = null;
    var filledCount = 0;

    function setFeedback(text, kind) {
      feedback.textContent = text || "";
      feedback.classList.toggle("is-good", kind === "good");
      feedback.classList.toggle("is-nudge", kind === "nudge");
    }

    function slotUnder(x, y) {
      var el = document.elementFromPoint(x, y);
      return el ? el.closest("[data-slot]") : null;
    }

    function onPointerMove(e) {
      if (!ghost) return;
      ghost.style.left = e.clientX + "px";
      ghost.style.top = e.clientY + "px";
      slots.forEach(function (s) { s.classList.remove("is-hover"); });
      var target = slotUnder(e.clientX, e.clientY);
      if (target && !target.classList.contains("is-filled")) target.classList.add("is-hover");
    }

    function onPointerUp(e) {
      if (!ghost) return;
      var target = slotUnder(e.clientX, e.clientY);
      slots.forEach(function (s) { s.classList.remove("is-hover"); });
      document.removeEventListener("pointermove", onPointerMove);
      document.removeEventListener("pointerup", onPointerUp);
      ghost.remove();
      ghost = null;

      var chipId = activeChip.getAttribute("data-chip");
      var activeChipLabel = activeChip.textContent;
      activeChip.style.visibility = "";
      activeChip = null;

      if (!target || target.classList.contains("is-filled")) return;

      var slotId = target.getAttribute("data-slot");
      if (slotId === chipId) {
        target.textContent = "✓ " + activeChipLabel;
        target.classList.add("is-filled");
        var chipEl = challenge.querySelector('[data-chip="' + chipId + '"]');
        if (chipEl) chipEl.classList.add("is-placed");
        filledCount += 1;
        if (filledCount === slots.length) {
          setFeedback("That's a flyer. Headline + visual + one clear action — the same formula behind every piece in our design showcase.", "good");
        } else {
          setFeedback("");
        }
      } else if (chipId === "finePrint") {
        setFeedback("A wall of fine print doesn't belong on a flyer — keep it to one clear message.", "nudge");
      } else {
        setFeedback("Not quite that slot — try " + (FLYER_LABELS[chipId] || "a different one") + ".", "nudge");
      }
    }

    chips.forEach(function (chip) {
      chip.addEventListener("pointerdown", function (e) {
        if (chip.classList.contains("is-placed")) return;
        e.preventDefault();
        activeChip = chip;
        var rect = chip.getBoundingClientRect();
        ghost = document.createElement("div");
        ghost.className = "flyer-chip-ghost";
        ghost.textContent = chip.textContent;
        ghost.style.left = e.clientX + "px";
        ghost.style.top = e.clientY + "px";
        ghost.style.width = rect.width + "px";
        document.body.appendChild(ghost);
        chip.style.visibility = "hidden";
        document.addEventListener("pointermove", onPointerMove);
        document.addEventListener("pointerup", onPointerUp);
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-track-playground]").forEach(function (root) {
      initCodePanel(root);
      initFlyerChallenge(root);
    });
  });
})();
