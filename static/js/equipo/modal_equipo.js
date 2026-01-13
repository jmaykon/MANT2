function openModal(modalEquipo) {
    const modal = document.getElementById(modalEquipo);
    modal.classList.remove('hidden');
    modal.classList.add('flex');
}

function closeModal(modalEquipo) {
    const modal = document.getElementById(modalEquipo);
    modal.classList.add('hidden');
    modal.classList.remove('flex');
}
