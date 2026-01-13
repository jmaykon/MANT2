(() => {
  // Obtener elementos
  const sidebar = document.getElementById("sidebar");
  const overlay = document.getElementById("overlay");
  const collapseBtn = document.getElementById("collapse-btn");
  const menuToggle = document.getElementById("menu-toggle");
  const agendaToggles = document.querySelectorAll(".agenda-toggle");

  // Toggle sidebar en móvil
  menuToggle?.addEventListener("click", () => {
    sidebar?.classList.toggle("-translate-x-full");
    overlay?.classList.toggle("hidden");
  });

  // Cerrar sidebar al hacer clic en overlay
  overlay?.addEventListener("click", () => {
    sidebar?.classList.add("-translate-x-full");
    overlay?.classList.add("hidden");
  });

  // Submenús (agenda)
  agendaToggles.forEach(btn => {
    btn.addEventListener("click", () => {
      const submenu = btn.nextElementSibling;
      submenu?.classList.toggle("hidden");
      // Rotar icono
      const icon = btn.querySelector("svg");
      icon?.classList.toggle("rotate-180");
    });
  });

  // Colapsar/expandir sidebar (desktop)
  collapseBtn?.addEventListener("click", () => {
    sidebar?.classList.toggle("w-64");
    sidebar?.classList.toggle("w-20");
    document.querySelectorAll("#sidebar nav li a span, #profile-section").forEach(el => {
      el.classList.toggle("hidden");
    });
  });
})();
