
const modal = document.getElementById('modal2');
const descripcionCompleta = document.getElementById('descripcion-completa');
const closeModal = document.getElementById('closeModal');

document.querySelectorAll('.btn-ver-mas').forEach(button => {
    button.addEventListener('click', () => {
        const descripcion = button.dataset.descripcion;
        descripcionCompleta.textContent = descripcion;
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    });
});

closeModal.addEventListener('click', () => {
    modal.classList.add('hidden');
    modal.classList.remove('flex');
});

// Cerrar al hacer clic fuera
modal.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
});

