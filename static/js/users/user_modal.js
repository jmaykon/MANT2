// user_modal.js

// Abrir modal
function openUserModal() {
    document.getElementById('userModal').classList.remove('hidden');
}

// Cerrar modal
function closeUserModal() {
    document.getElementById('userModal').classList.add('hidden');
    document.getElementById('userForm').reset();
    // reset de toggle y preview de firma
    document.getElementById('modalEstado').checked = false;
    toggleEstado();
    document.getElementById('modalFirmaPreview').src = '';
}

// Toggle estado activo/inactivo
function toggleEstado() {
    const checkbox = document.getElementById('modalEstado');
    const estadoLabel = document.getElementById('estadoLabel');
    const toggleBg = document.getElementById('toggleBg');
    const toggleCircle = document.getElementById('toggleCircle');

    if (checkbox.checked) {
        estadoLabel.textContent = 'Activo';
        estadoLabel.classList.remove('text-red-500');
        estadoLabel.classList.add('text-green-500');
        toggleBg.classList.remove('bg-red-500');
        toggleBg.classList.add('bg-green-500');
        toggleCircle.classList.add('translate-x-5');
    } else {
        estadoLabel.textContent = 'Inactivo';
        estadoLabel.classList.remove('text-green-500');
        estadoLabel.classList.add('text-red-500');
        toggleBg.classList.remove('bg-green-500');
        toggleBg.classList.add('bg-red-500');
        toggleCircle.classList.remove('translate-x-5');
    }
}

// Preview de la firma
document.querySelector('input[name="firma"]').addEventListener('change', function (e) {
    const preview = document.getElementById('modalFirmaPreview');
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            preview.src = e.target.result;
        }
        reader.readAsDataURL(file);
    } else {
        preview.src = '';
    }
});

