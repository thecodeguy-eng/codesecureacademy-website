// "Try it yourself" editor for tutorials/article_detail.html. Renders the
// textarea's contents into a sandboxed iframe (sandbox="allow-scripts" only
// — no allow-same-origin — so visitor-written JS can execute but can never
// reach the parent page's cookies, CSRF token, or DOM).
(function () {
  "use strict";

  function debounce(fn, wait) {
    var timer;
    return function () {
      clearTimeout(timer);
      timer = setTimeout(fn, wait);
    };
  }

  function initEditor(root) {
    var input = root.querySelector("[data-code-input]");
    var output = root.querySelector("[data-code-output]");
    var runBtn = root.querySelector("[data-code-run]");
    if (!input || !output) return;

    function render() {
      output.srcdoc = input.value;
    }

    input.addEventListener("keydown", function (e) {
      if (e.key === "Tab") {
        e.preventDefault();
        var start = input.selectionStart;
        var end = input.selectionEnd;
        input.value = input.value.slice(0, start) + "  " + input.value.slice(end);
        input.selectionStart = input.selectionEnd = start + 2;
      }
    });

    input.addEventListener("input", debounce(render, 400));
    if (runBtn) runBtn.addEventListener("click", render);

    render();
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-code-editor]").forEach(initEditor);
  });
})();
