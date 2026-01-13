document.body.addEventListener('htmx:afterRequest', function (evt) {
    // evt.detail.elt es el elemento que disparó la petición
    const el = evt.detail.elt;

    if (el.closest("form[data-accion='agregar']")) {
        // Cerrar modal
        closeModal('agregar_lugar');

        // Mostrar SweetAlert
        Swal.fire({
            title: "¡Éxito!",
            text: "Lugar agregado correctamente.",
            icon: "success",
            draggable: true,
            confirmButtonColor: "#2563eb"
        });
    }
});
