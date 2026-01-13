document.addEventListener("DOMContentLoaded", () => {

  // --- Abrir modales al click ---
  const modales = {
    openEditar: "modalEditar",
    openPassword: "modalPassword",
    openCerrarSesion: "modalCerrarSesion",
  };

  Object.entries(modales).forEach(([btnId, modalId]) => {
    const btn = document.getElementById(btnId);
    const modal = document.getElementById(modalId);
    if (btn && modal) {
      btn.addEventListener("click", () => modal.classList.remove("hidden"));
    }
  });

  // --- Abrir perfil con hover ---
  const btnPerfil = document.getElementById("openPerfil");
  const modalPerfil = document.getElementById("modalPerfil");

  if (btnPerfil && modalPerfil) {
    btnPerfil.addEventListener("mouseenter", () => {
      modalPerfil.classList.remove("hidden");
    });

    // Se cierra cuando el mouse sale del modal o del botón
    modalPerfil.addEventListener("mouseleave", () => {
      modalPerfil.classList.add("hidden");
    });
    btnPerfil.addEventListener("mouseleave", (e) => {
      // Si el mouse no entra al modal, cerramos
      setTimeout(() => {
        if (!modalPerfil.matches(":hover") && !btnPerfil.matches(":hover")) {
          modalPerfil.classList.add("hidden");
        }
      }, 200);
    });
  }

  // --- Cerrar modales secundarios ---
  document.querySelectorAll(".closeModal, #closePerfil").forEach(btn => {
    btn.addEventListener("click", () => {
      btn.closest(".fixed").classList.add("hidden");
    });
  });

  // --- Cerrar al hacer clic fuera del contenido ---
  window.addEventListener("click", (e) => {
    if (e.target.classList.contains("fixed")) e.target.classList.add("hidden");
  });
});
