// Sidebar scroll-spy for the student dashboard — highlights the nav link
// for whichever section is currently in view, like a real product sidebar.
(function () {
  const links = document.querySelectorAll("[data-dash-link]");
  if (!links.length) return;

  const sections = Array.from(links)
    .map((link) => document.querySelector(link.getAttribute("href")))
    .filter(Boolean);
  if (!sections.length) return;

  const setActive = (id) => {
    links.forEach((link) => {
      link.classList.toggle("active", link.getAttribute("href") === "#" + id);
    });
  };

  if (!("IntersectionObserver" in window)) {
    setActive(sections[0].id);
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      const visible = entries
        .filter((e) => e.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (visible) setActive(visible.target.id);
    },
    { rootMargin: "-110px 0px -60% 0px", threshold: [0, 0.25, 0.5, 1] }
  );
  sections.forEach((section) => observer.observe(section));
  setActive(sections[0].id);
})();
