(() => {
    const modalDescripcion = document.getElementById('modal2');
    const descripcionCompleta = document.getElementById('descripcion-completa');
    const closeModal = document.getElementById('closeModal');

    if (!modalDescripcion || !descripcionCompleta || !closeModal) return;

    document.querySelectorAll('.btn-ver-mas').forEach(button => {
        button.addEventListener('click', () => {
            descripcionCompleta.textContent = button.dataset.descripcion;
            modalDescripcion.classList.remove('hidden');
            modalDescripcion.classList.add('flex');
        });
    });

    closeModal.addEventListener('click', () => {
        modalDescripcion.classList.add('hidden');
        modalDescripcion.classList.remove('flex');
    });

    modalDescripcion.addEventListener('click', (e) => {
        if (e.target === modalDescripcion) {
            modalDescripcion.classList.add('hidden');
            modalDescripcion.classList.remove('flex');
        }
    });
})();
