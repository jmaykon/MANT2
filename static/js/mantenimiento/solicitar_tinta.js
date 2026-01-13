function initSoporte() {
    const tipoSelect = document.getElementById('tipo_soporte');
    const coloresDiv = document.getElementById('colores_tinta');
    const tonnerDiv = document.getElementById('tonner');

    if (!tipoSelect || !coloresDiv) return;

    // evitar listeners duplicados
    if (tipoSelect.dataset.ready) return;
    tipoSelect.dataset.ready = "true";

    tipoSelect.addEventListener('change', function () {
        coloresDiv.classList.toggle('hidden', this.value !== 'recarga_tinta');
        tonnerDiv?.classList.toggle('hidden', this.value !== 'tonner');
    });

    const checks = coloresDiv.querySelectorAll('input[type="checkbox"]');
    const checkTodos = coloresDiv.querySelector('input[value="todos"]');

    checks.forEach(chk => {
        chk.addEventListener('change', function () {
            if (this.value === 'todos' && this.checked) {
                checks.forEach(c => c.value !== 'todos' && (c.checked = false));
            } else if (this.checked && checkTodos) {
                checkTodos.checked = false;
            }
        });
    });
}

// HTMX (cuando entra por swap)
document.body.addEventListener('htmx:afterSwap', initSoporte);

// Carga normal
document.addEventListener('DOMContentLoaded', initSoporte);
