document.addEventListener("DOMContentLoaded", () => {
  const btn = document.createElement("button");
  btn.id = "back-to-top";
  btn.type = "button";
  btn.setAttribute("aria-label", "Back to top");

  // icon + label (label can be hidden on very small screens via CSS)
  btn.innerHTML = '<span class="btt-icon" aria-hidden="true">↑</span><span class="btt-label">Top</span>';

  document.body.appendChild(btn);

  const SHOW_AT = 250; // was 400 (appears earlier now)

  const toggle = () => {
    btn.style.display = window.scrollY > SHOW_AT ? "inline-flex" : "none";
  };

  btn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  window.addEventListener("scroll", toggle, { passive: true });
  toggle();
});
