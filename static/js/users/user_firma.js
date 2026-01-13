// Modal de Firma
function openFirmaModal(url) {
    const modal = document.getElementById('firmaModal');
    const img = document.getElementById('firmaModalImg');
    img.src = url;
    modal.classList.remove('hidden');
}

function closeFirmaModal() {
    const modal = document.getElementById('firmaModal');
    const img = document.getElementById('firmaModalImg');
    img.src = '';
    modal.classList.add('hidden');
}

// Cerrar modal al hacer click fuera de la imagen
document.getElementById('firmaModal').addEventListener('click', function (e) {
    if (e.target.id === 'firmaModal') closeFirmaModal();
});