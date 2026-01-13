document.addEventListener("DOMContentLoaded", function () {

  const modal = document.getElementById("modal");
  const btnCerrar = document.getElementById("btnCerrar");
  const btnNext = document.querySelector(".btn-next");
  const steps = document.querySelectorAll(".step");
  const stepContents = document.querySelectorAll(".step-content");

  if (!modal) {
    console.error("No se encontró el modal con id='modal'");
    return;
  }

  let currentStep = 1;

  // Función para mostrar paso
  function showStep(step) {
    steps.forEach(s => s.classList.remove("border-green-500", "font-bold"));
    stepContents.forEach(c => c.classList.add("hidden"));

    const activeStep = document.querySelector(`.step[data-step="${step}"]`);
    if (activeStep) activeStep.classList.add("border-green-500", "font-bold");

    const activeContent = document.querySelector(`.step-content[data-step="${step}"]`);
    if (activeContent) activeContent.classList.remove("hidden");

    if (btnNext) btnNext.textContent = (step === 3) ? "Finalizar" : "Continuar";
  }

  // Abrir modal al hacer click en cualquier btn-atender
  document.body.addEventListener("click", function (e) {
    const btn = e.target.closest(".btn-atender");
    if (!btn) return;

    currentStep = 1;
    showStep(currentStep);

    // Opcional: rellenar textarea con descripción del ticket
    const ticketId = btn.dataset.ticketId;
    const ticketDescEl = document.querySelector(`#ticket-${ticketId} .descripcion`);
    const comentarioField = document.querySelector("textarea[name='comentario_usuario']");
    if (ticketDescEl && comentarioField) {
      comentarioField.value = ticketDescEl.innerText.trim();
    }

    modal.classList.remove("hidden");
  });

  // Cerrar modal
  btnCerrar?.addEventListener("click", () => modal.classList.add("hidden"));

  // Botón Continuar / Finalizar solo visual
  btnNext?.addEventListener("click", async function (e) {
    e.preventDefault();

    if (currentStep === 1) {
      const result = await Swal.fire({
        title: "¿Iniciar atención?",
        icon: "question",
        showCancelButton: true,
        confirmButtonText: "Sí",
        cancelButtonText: "No"
      });
      if (!result.isConfirmed) return;

      currentStep = 2;
      showStep(currentStep);
      return;
    }

    if (currentStep === 2) {
      const result = await Swal.fire({
        title: "¿Deseas finalizar?",
        text: "Este paso es solo visual",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Sí, finalizar",
        cancelButtonText: "No"
      });
      if (!result.isConfirmed) return;

      currentStep = 3;
      showStep(currentStep);

      Swal.fire({
        icon: "success",
        title: "¡Flujo completado (solo visual)!",
        showConfirmButton: false,
        timer: 1500
      });

      modal.classList.add("hidden");
    }
  });

});
