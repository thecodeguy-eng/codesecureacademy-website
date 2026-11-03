(function () {
  var stage = document.getElementById("bug-hunt-stage");
  if (!stage) return;
  var tracksUrl = stage.dataset.tracksUrl || "/tracks/";

  var ROUNDS = [
    {
      lang: "python",
      lines: [
        "def find_user(email):",
        "    query = \"SELECT * FROM users WHERE email = '\" + email + \"'\"",
        "    return db.execute(query)",
      ],
      bug: 1,
      good: "Building SQL by gluing a string together lets someone type <code>' OR '1'='1</code> as their \"email\" and read every row in the table.",
      bad: "Not this one. Look at how the SQL string itself gets built, not how the function is called.",
      fix: "Fix: use a parameterized query (<code>WHERE email = %s</code>, params) and let the database driver handle escaping.",
    },
    {
      lang: "python",
      lines: [
        "def save_user(email, password):",
        "    user = User(email=email, password=password)",
        "    user.save()",
      ],
      bug: 1,
      good: "That password is going into the database exactly as the user typed it — no hashing, no salt. One database leak and every password is exposed in plain text.",
      bad: "Not this one. Look at what actually happens to the password value.",
      fix: "Fix: hash the password (e.g. bcrypt/argon2) before it ever gets saved, and never store or log the raw value.",
    },
    {
      lang: "javascript",
      lines: [
        "function showComment(text) {",
        "  document.getElementById(\"comments\").innerHTML = text;",
        "}",
      ],
      bug: 1,
      good: "If \"text\" comes from another user's comment, they can submit a &lt;script&gt; tag and it'll execute in everyone else's browser. Classic stored XSS.",
      bad: "Not this one. Think about what innerHTML does with a string that contains HTML tags.",
      fix: "Fix: use <code>textContent</code>, or sanitize/escape the string before it touches the DOM.",
    },
    {
      lang: "javascript",
      lines: [
        "const STRIPE_KEY = \"PASTE_YOUR_REAL_SECRET_KEY_HERE\"; // looks just like this in real code",
        "fetch(\"https://api.stripe.com/v1/charges\", {",
        "  headers: { Authorization: STRIPE_KEY }",
        "});",
      ],
      bug: 0,
      good: "That's a live secret key, hardcoded, shipped straight to anyone who opens dev tools. They can now charge cards on your account.",
      bad: "Not this one — the fetch call itself is fine. The problem is further up.",
      fix: "Fix: secret keys live in environment variables on the server, never in client-side code.",
    },
    {
      lang: "python",
      lines: [
        "@app.route(\"/admin/delete-user/<id>\")",
        "def delete_user(id):",
        "    User.objects.get(id=id).delete()",
        "    return \"deleted\"",
      ],
      bug: 0,
      good: "The whole route is the bug — there's no check anywhere that the requester is actually an admin. Anyone who guesses this URL can delete any user.",
      bad: "Keep looking — the delete itself works fine technically. The question is who's allowed to call it.",
      fix: "Fix: verify the logged-in user's permissions on the server before a destructive action — never rely on a hidden link or a missing button in the UI.",
    },
    {
      lang: "python",
      lines: [
        "@app.route(\"/invoice/<id>\")",
        "def get_invoice(id):",
        "    return Invoice.objects.get(id=id).to_json()",
      ],
      bug: 2,
      good: "This fetches ANY invoice by id with no check that it belongs to the person asking. Change the number in the URL, see someone else's invoice. This is called IDOR.",
      bad: "Not this one. The lookup itself works — it's missing a second check.",
      fix: "Fix: confirm <code>invoice.owner == request.user</code> before returning it, not just that the id exists.",
    },
    {
      lang: "python",
      lines: [
        "def is_valid_password(pw):",
        "    return len(pw) >= 4",
      ],
      bug: 1,
      good: "4 characters is crackable almost instantly — that's not a real minimum.",
      bad: "Look again at the actual number being checked.",
      fix: "Fix: require real length (12+ characters matters far more than forcing symbols), and check against known-breached password lists.",
    },
    {
      lang: "html",
      lines: [
        "<input type=\"hidden\" name=\"price\" value=\"5000\">",
        "<!-- server trusts this value directly at checkout -->",
      ],
      bug: 0,
      good: "A hidden field is still just a form field — anyone can open dev tools and change \"5000\" to \"5\" before submitting. If the server trusts it blindly, that's a free product.",
      bad: "Not this one — the comment is just a comment. The real problem is the value the browser is allowed to send.",
      fix: "Fix: never trust a client-submitted price (or role, or permission). Recompute or re-verify anything that controls money or access, server-side.",
    },
  ];

  var state = { round: 0, score: 0, startedAt: 0, attempted: false };

  function el(html) {
    var t = document.createElement("template");
    t.innerHTML = html.trim();
    return t.content.firstElementChild;
  }

  function renderIntro() {
    stage.innerHTML =
      '<div class="bug-result">' +
      '<p class="bug-hunt-prompt">8 rounds. Real code, real mistakes — the kind that show up in production, not puzzle-box trick questions. Click the line that’s the actual vulnerability.</p>' +
      '<button class="btn btn-primary" id="bh-start">Start →</button>' +
      "</div>";
    stage.querySelector("#bh-start").addEventListener("click", function () {
      state.startedAt = Date.now();
      renderRound();
    });
  }

  function renderRound() {
    var r = ROUNDS[state.round];
    state.attempted = false;
    var linesHtml = r.lines
      .map(function (line, i) {
        return (
          '<button type="button" class="bug-line" data-i="' + i + '">' +
          '<span class="ln">' + (i + 1) + "</span><span>" + escapeHtml(line) + "</span>" +
          "</button>"
        );
      })
      .join("");

    stage.innerHTML =
      '<div class="bug-hunt-top">' +
      '<span class="bug-hunt-progress">Round ' + (state.round + 1) + " of " + ROUNDS.length + "</span>" +
      '<span class="bug-hunt-score" id="bh-score">Score: ' + state.score + "/" + ROUNDS.length + "</span>" +
      "</div>" +
      '<p class="bug-hunt-prompt">Which line is the <strong>security bug</strong>?</p>' +
      '<div class="bug-code">' + linesHtml + "</div>" +
      '<div id="bh-feedback"></div>' +
      '<div class="bug-hunt-actions" id="bh-actions"></div>';

    Array.prototype.forEach.call(stage.querySelectorAll(".bug-line"), function (btn) {
      btn.addEventListener("click", function () { onPick(parseInt(btn.dataset.i, 10)); });
    });
  }

  function onPick(i) {
    var r = ROUNDS[state.round];
    var lineButtons = stage.querySelectorAll(".bug-line");
    var correct = i === r.bug;

    if (correct || state.attempted) {
      Array.prototype.forEach.call(lineButtons, function (btn) { btn.disabled = true; });
      lineButtons[i].classList.add(correct ? "is-correct" : "is-wrong");
      if (!correct) lineButtons[r.bug].classList.add("is-correct");

      if (correct && !state.attempted) {
        state.score++;
        var scoreEl = stage.querySelector("#bh-score");
        if (scoreEl) scoreEl.textContent = "Score: " + state.score + "/" + ROUNDS.length;
      }

      var feedback = stage.querySelector("#bh-feedback");
      feedback.innerHTML =
        '<div class="bug-feedback ' + (correct ? "good" : "bad") + '">' +
        '<span class="title">' + (correct ? "Found it." : "Here's the one.") + "</span>" +
        r.good +
        '<div style="margin-top:0.5rem;color:var(--text-muted);font-size:0.86rem;">' + r.fix + "</div>" +
        "</div>";

      var isLast = state.round === ROUNDS.length - 1;
      var actions = stage.querySelector("#bh-actions");
      actions.innerHTML = '<button class="btn btn-primary" id="bh-next">' + (isLast ? "See your score →" : "Next round →") + "</button>";
      actions.querySelector("#bh-next").addEventListener("click", function () {
        if (isLast) { renderResult(); }
        else { state.round++; renderRound(); }
      });
    } else {
      state.attempted = true;
      lineButtons[i].classList.add("is-wrong");
      lineButtons[i].disabled = true;
      var fb = stage.querySelector("#bh-feedback");
      fb.innerHTML = '<div class="bug-feedback bad"><span class="title">Not quite.</span>' + r.bad + "</div>";
    }
  }

  function renderResult() {
    var elapsed = Math.round((Date.now() - state.startedAt) / 1000);
    var mins = Math.floor(elapsed / 60), secs = elapsed % 60;
    var timeStr = mins > 0 ? mins + "m " + secs + "s" : secs + "s";
    var verdict;
    if (state.score === ROUNDS.length) verdict = "Perfect run. That instinct — reading code and asking “what could go wrong here” — is exactly what the Cybersecurity track builds on, on purpose.";
    else if (state.score >= ROUNDS.length * 0.6) verdict = "Solid. You caught most of them on sight — the rest is pattern recognition you build with practice.";
    else verdict = "These are the exact mistakes that ship to production constantly. Spotting them is a trainable skill — that's the whole Cybersecurity track.";

    stage.innerHTML =
      '<div class="bug-result">' +
      '<div class="bug-hunt-progress">Finished in ' + timeStr + "</div>" +
      '<div class="score-big">' + state.score + "/" + ROUNDS.length + "</div>" +
      '<div class="score-label">vulnerabilities spotted</div>' +
      '<p class="verdict">' + verdict + "</p>" +
      '<div class="result-actions">' +
      '<a href="' + tracksUrl + '" class="btn btn-primary">Explore the Cybersecurity track</a>' +
      '<button class="btn btn-outline" id="bh-replay">Play again</button>' +
      "</div></div>";

    stage.querySelector("#bh-replay").addEventListener("click", function () {
      state = { round: 0, score: 0, startedAt: Date.now(), attempted: false };
      renderRound();
    });
  }

  function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  renderIntro();
})();
