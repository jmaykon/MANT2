// 1. Manejo de Errores de validación (400)
document.body.addEventListener('htmx:responseError', function (evt) {
    if (evt.detail.xhr.status === 400) {
        Swal.fire({
            icon: 'warning',
            title: 'Selección requerida',
            text: evt.detail.xhr.responseText,
            confirmButtonColor: '#3085d6',
            confirmButtonText: 'Entendido'
        });
    }
});

// Manejo de éxito
document.body.addEventListener("eventoTicketCreado", function (evt) {
    Swal.fire({
        title: '¡Solicitud Registrada!',
        html: `Se ha generado con éxito el <b>Ticket #${evt.detail.numero}</b>`,
        icon: 'success',
        confirmButtonText: 'Ok',
        confirmButtonColor: '#2563eb',
        allowOutsideClick: false
    }).then((result) => {
        if (result.isConfirmed) {
            // Buscamos cuál contenedor existe en el DOM actual
            let selectorTarget = '#dynamic-content';

            if (!document.querySelector(selectorTarget)) {
                selectorTarget = '#dynamic-content'; // Tu segunda opción en admin.html
            }
            htmx.ajax('GET', '/mantenimiento/solicitar/', {
                target: selectorTarget,
                swap: 'innerHTML'
            });
        }
    });
});