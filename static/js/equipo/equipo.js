function initEstadoDropdown(modal = document) {
    const dropdowns = modal.querySelectorAll('.estado-dropdown');

    dropdowns.forEach(wrapper => {
        const btn = wrapper.querySelector('.estado-btn');
        const menu = wrapper.querySelector('.estado-menu');
        const texto = wrapper.querySelector('.estado-texto');
        const input = wrapper.querySelector('input[type="hidden"]');

        if (!btn || !menu || !texto || !input) return;

        // Evita agregar múltiples listeners al mismo botón
        if (!btn.dataset.listenerAdded) {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                // Cerrar otros menús abiertos
                document.querySelectorAll('.estado-menu').forEach(m => {
                    if (m !== menu) m.classList.add('hidden');
                });
                menu.classList.toggle('hidden');
            });
            btn.dataset.listenerAdded = true;
        }

        // Evita agregar múltiples listeners a los botones de menú
        menu.querySelectorAll('button[data-estado]').forEach(op => {
            if (!op.dataset.listenerAdded) {
                op.addEventListener('click', () => {
                    texto.textContent = op.getAttribute('data-estado');
                    input.value = op.getAttribute('data-estado');
                    menu.classList.add('hidden');
                });
                op.dataset.listenerAdded = true;
            }
        });
    });
}

// Cerrar dropdown si se hace clic fuera (solo se agrega 1 vez)
if (!document.body.dataset.documentListenerAdded) {
    document.addEventListener('click', () => {
        document.querySelectorAll('.estado-menu').forEach(menu => menu.classList.add('hidden'));
    });
    document.body.dataset.documentListenerAdded = true;
}

// Inicializar al cargar la página
document.addEventListener('DOMContentLoaded', () => initEstadoDropdown());

// Inicializar cuando HTMX carga contenido nuevo (como un modal)
document.body.addEventListener('htmx:afterSwap', function (evt) {
    if (evt.detail.target.id === 'modal-edit-body') {
        initEstadoDropdown(evt.detail.target);
    }
});



//********************
function initUserDropdown(modal = document) {
    const dropdowns = modal.querySelectorAll('.user-dropdown');

    dropdowns.forEach(wrapper => {
        const btn = wrapper.querySelector('.user-btn');
        const menu = wrapper.querySelector('.user-menu');
        const texto = wrapper.querySelector('.user-texto');
        const input = wrapper.querySelector('input[name="id_users"]');

        if (!btn || !menu) return;

        // Mostrar / ocultar el menú
        btn.addEventListener('click', e => {
            e.stopPropagation();
            menu.classList.toggle('hidden');
        });

        // Al seleccionar un usuario
        menu.querySelectorAll('button[data-id]').forEach(op => {
            op.addEventListener('click', () => {
                const id = op.getAttribute('data-id');
                const nombre = op.getAttribute('data-nombre');

                texto.textContent = nombre;
                input.value = id;
                menu.classList.add('hidden');
            });
        });

        // Cerrar el menú si se hace clic fuera
        document.addEventListener('click', e => {
            if (!wrapper.contains(e.target)) {
                menu.classList.add('hidden');
            }
        });
    });
}

// Ejecutar al cargar la página
document.addEventListener('DOMContentLoaded', () => initUserDropdown());

// Re-inicializar si HTMX carga un modal nuevo
document.body.addEventListener('htmx:afterSwap', evt => {
    if (evt.detail.target.id === 'modal-edit-body') {
        initUserDropdown(evt.detail.target);
    }
});


























