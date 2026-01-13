    document.body.addEventListener("htmx:afterSwap", function (e) {
        if (e.target.id === "dynamic-content") {
            closeModal('editar_lugar');
            closeModal('agregar_lugar');
        }
    });