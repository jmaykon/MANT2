// Obtener el modal y el botón de cerrar
var modal = document.getElementById("modal2");
var span = document.getElementsByClassName("close")[0];

// Mostrar el modal cuando se hace clic en el botón "Mostrar descripción"
document.querySelectorAll('.btn-ver-mas').forEach(function (button) {
    button.addEventListener('click', function () {
        var ticketId = button.getAttribute('data-ticket-id');
        var descripcion = document.querySelector(`#ticket-${ticketId} .descripcion`).textContent;

        // Establecer la descripción completa en el modal
        document.getElementById('descripcion-completa').textContent = descripcion;

        // Mostrar el modal
        modal.style.display = "block";
    });
});

// Cerrar el modal cuando se hace clic en el "x"
span.onclick = function () {
    modal.style.display = "none";
}

// Cerrar el modal si se hace clic fuera de él
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
