document.addEventListener("DOMContentLoaded", () => {
  const btn = document.createElement("button");
  btn.id = "back-to-top";
  btn.type = "button";
  btn.setAttribute("aria-label", "Back to top");
  btn.textContent = "↑";

  document.body.appendChild(btn);

  const toggle = () => {
    btn.style.display = window.scrollY > 400 ? "block" : "none";
  };

  btn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  window.addEventListener("scroll", toggle, { passive: true });
  toggle();
});
