(() => {
    // ==========================
    // ELEMENTOS PRINCIPALES
    // ==========================
    const ticketsContainer = document.getElementById('tickets-container');
    const URL_ATENDER_TICKET = ticketsContainer.dataset.urlAtender;

    const modal = document.getElementById('modal');
    const btnCerrar = modal.querySelector('#btnCerrar');
    const btnCancel = modal.querySelector('.btn-cancel');
    const btnNext = modal.querySelector('.btn-next');

    const steps = modal.querySelectorAll('.step');
    const stepContents = modal.querySelectorAll('.step-content');

    let currentStep = 1;
    let currentTicketId = null;

    const btnAtenderList = document.querySelectorAll('.btn-atender');

    // ==========================
    // CSRF
    // ==========================
    function getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') return decodeURIComponent(value);
        }
        return '';
    }

    // ==========================
    // MOSTRAR PASO
    // ==========================
    function showStep(step) {
        steps.forEach(s => s.classList.remove('step-active', 'step-completed'));
        stepContents.forEach(c => c.classList.add('hidden'));

        steps.forEach(s => {
            const num = parseInt(s.dataset.step);
            if (num < step) s.classList.add('step-completed');
            else if (num === step) s.classList.add('step-active');
        });

        const content = modal.querySelector(`.step-content[data-step="${step}"]`);
        if (content) content.classList.remove('hidden');

        btnNext.textContent = step === 3 ? 'Finalizar y Guardar' : 'Continuar y Guardar';
    }

    // ==========================
    // PRECARGAR DATOS
    // ==========================
    function precargarDatos(ticketData) {
        if (!ticketData) return;

        currentStep = ticketData.paso_actual || 1;
        showStep(currentStep);

        const form = modal.querySelector('form');
        if (!form) return;

        form.querySelector('.diagnostico').value = ticketData.diagnostico || '';
        form.querySelector('.solucion').value = ticketData.solucion || '';
        form.querySelector('.observaciones').value = ticketData.observaciones || '';
        form.querySelector('.comentario').value = ticketData.comentario || '';
    }

    // ==========================
    // OBTENER DATOS DEL TICKET
    // ==========================
    async function fetchTicketData(ticketId) {
        try {
            const response = await fetch(`/mantenimiento/get_ticket_data/${ticketId}/`);
            if (!response.ok) throw new Error('Error al obtener datos del ticket');

            const data = await response.json();

            // Guardamos el ticket actual
            currentTicketId = ticketId;

            // Precargamos modal
            precargarDatos(data);
            modal.classList.remove('hidden');

        } catch (error) {
            console.error('Error al obtener el ticket:', error);
            Swal.fire('Error', 'No se pudo cargar el ticket', 'error');
        }
    }

    // ==========================
    // GUARDAR ESTADO
    // ==========================
    async function guardarEstado(step) {
        const form = modal.querySelector('form');
        const formData = new FormData();

        formData.append('id_ticket', currentTicketId);
        formData.append('step', step);

        if (step >= 3 && form) {
            formData.append('diagnostico', form.querySelector('.diagnostico').value.trim());
            formData.append('solucion_aplicada', form.querySelector('.solucion').value.trim());
            formData.append('observaciones_tecnicas', form.querySelector('.observaciones').value.trim());
            formData.append('comentario_usuario', form.querySelector('.comentario').value.trim());
        }

        const res = await fetch(URL_ATENDER_TICKET, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCSRFToken() },
            body: formData
        });

        if (!res.ok) throw new Error('Error al guardar estado');
        return await res.json();
    }

    // ==========================
    // ACTUALIZAR VISTA DEL TICKET
    // ==========================
    function actualizarVistaTicket(data) {
        const ticketEl = document.getElementById(`ticket-${currentTicketId}`);
        if (!ticketEl) return;

        const statusSpan = ticketEl.querySelector('.status span');
        const btn = ticketEl.querySelector('.btn-atender');

        const estados = {
            pendiente: { text: 'Pendiente', class: 'pendiente' },
            en_proceso: { text: 'En Proceso', class: 'en_proceso' },
            documentando: { text: 'Documentando', class: 'documentando' },
            completado: { text: 'Completado', class: 'completado' }
        };

        const estado = estados[data.estado];
        if (!estado) return;

        statusSpan.textContent = estado.text;
        statusSpan.className = estado.class;

        ticketEl.dataset.ultimoPaso = data.ultimo_paso;

        if (data.estado === 'completado') {
            btn.textContent = 'Completado';
            btn.disabled = true;
            btn.classList.add('bg-gray-400', 'cursor-not-allowed', 'hover:bg-gray-400');
        }
    }

    // ==========================
    // CLICK ATENDER
    // ==========================
    btnAtenderList.forEach(btn => {
        btn.addEventListener('click', () => {
            const ticketId = btn.dataset.ticketId;
            fetchTicketData(ticketId);
        });
    });

    // ==========================
    // CONTINUAR / FINALIZAR
    // ==========================
    btnNext.addEventListener('click', async () => {
        const stepToSave = currentStep + 1;

        try {
            const result = await Swal.fire({
                title: 'Guardar Ticket',
                text: '¿Deseas guardar los cambios?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Guardar',
                cancelButtonText: 'Cancelar'
            });

            if (!result.isConfirmed) return;

            const data = await guardarEstado(stepToSave);
            actualizarVistaTicket(data);

            if (currentStep < 3) {
                currentStep++;
                showStep(currentStep);
            } else {
                Swal.fire('Éxito', 'Ticket completado', 'success');
                modal.classList.add('hidden');
            }

        } catch (err) {
            console.error(err);
            Swal.fire('Error', 'No se pudo guardar el estado', 'error');
        }
    });

    // ==========================
    // CERRAR MODAL
    // ==========================
    btnCancel.addEventListener('click', () => modal.classList.add('hidden'));
    btnCerrar.addEventListener('click', () => modal.classList.add('hidden'));
})();
