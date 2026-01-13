(() => {
    // =======================
    // Variables
    // =======================
    const ticketsContainer = document.getElementById('tickets-container');
    const URL_ATENDER_TICKET = ticketsContainer.dataset.urlAtender;

    const modal = document.getElementById('modal');
    const btnCerrar = document.getElementById('btnCerrar');
    const steps = document.querySelectorAll('.step');
    const stepContents = document.querySelectorAll('.step-content');
    const btnNext = document.querySelector('.btn-next');

    let currentStep = 1;
    let currentTicketId = null;

    const btnAtenderList = document.querySelectorAll('#btnAtender');

    function getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') return decodeURIComponent(value);
        }
        return '';
    }

    function showStep(step) {
        steps.forEach(s => s.classList.remove('step-active'));
        stepContents.forEach(c => c.classList.add('hidden'));

        const stepEl = document.querySelector(`.step[data-step="${step}"]`);
        if (stepEl) stepEl.classList.add('step-active');

        const contentEl = document.querySelector(`.step-content[data-step="${step}"]`);
        if (contentEl) contentEl.classList.remove('hidden');

        btnNext.textContent = step === 3 ? 'Finalizar' : 'Continuar';
    }

    function showStepByEstado(estado) {
        if (estado === 'pendiente') currentStep = 1;
        else if (estado === 'en_proceso') currentStep = 2;
        else if (estado === 'completado') currentStep = 3;
        showStep(currentStep);
    }

    // =======================
    // Guardar en cada paso
    // =======================
    // =======================
    // Guardar en cada paso
    // =======================
    async function guardarPaso(step) {
        const formEl = document.querySelector('.step-content[data-step="3"] form');
        const formData = new FormData();

        formData.append('id_ticket', currentTicketId);
        formData.append('step', step);

        if (step === 3 || step === 'finalizar') {
            const diagnosticoEl = formEl.querySelector('.diagnostico');
            const solucionEl = formEl.querySelector('.solucion');
            const observacionesEl = formEl.querySelector('.observaciones');
            const comentarioEl = formEl.querySelector('.comentario');

            formData.append('diagnostico', diagnosticoEl ? diagnosticoEl.value.trim() : '');
            formData.append('solucion_aplicada', solucionEl ? solucionEl.value.trim() : '');
            formData.append('observaciones_tecnicas', observacionesEl ? observacionesEl.value.trim() : '');
            formData.append('comentario_usuario', comentarioEl ? comentarioEl.value.trim() : '');
        }

        const response = await fetch(URL_ATENDER_TICKET, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCSRFToken() },
            body: formData
        });

        if (!response.ok) throw new Error('Error al guardar el ticket');
        return await response.json();
    }

    function actualizarVistaTicket(estado) {
        const ticketEl = document.getElementById(`ticket-${currentTicketId}`);
        if (!ticketEl) return;

        const statusSpan = ticketEl.querySelector('.status span');
        const btn = ticketEl.querySelector('#btnAtender');

        if (statusSpan && btn) {
            if (estado === 'en_proceso') {
                statusSpan.textContent = 'En Proceso';
                statusSpan.className = 'en_proceso';
            } else if (estado === 'completado') {
                statusSpan.textContent = 'Completado';
                statusSpan.className = 'completado';
                btn.textContent = 'Completado';
                btn.disabled = true;
                btn.classList.add('bg-gray-400', 'cursor-not-allowed', 'hover:bg-gray-400');
            }
        }
    }

    // =======================
    // Click en btnAtender
    // =======================
    btnAtenderList.forEach(btn => {
        const ticketId = btn.dataset.ticketId;
        const ticketEl = document.getElementById(`ticket-${ticketId}`);
        const statusSpan = ticketEl.querySelector('.status span');

        if (statusSpan && statusSpan.textContent.toLowerCase() === 'completado') {
            btn.textContent = 'Completado';
            btn.disabled = true;
            btn.classList.add('bg-gray-400', 'cursor-not-allowed', 'hover:bg-gray-400');
        }

        btn.addEventListener('click', async () => {
            currentTicketId = ticketId;
            let estadoActual = statusSpan ? statusSpan.textContent.toLowerCase() : 'pendiente';

            if (estadoActual === 'pendiente') {
                const result = await Swal.fire({
                    title: '¿Atender ticket?',
                    text: 'Confirma iniciar el proceso',
                    icon: 'question',
                    showCancelButton: true,
                    confirmButtonText: 'Sí, atender',
                    cancelButtonText: 'Cancelar'
                });

                if (!result.isConfirmed) return;

                // Guardar paso 1 automáticamente
                try {
                    const data = await guardarPaso('1');
                    if (data.estado) actualizarVistaTicket(data.estado);
                    estadoActual = data.estado;
                } catch (err) {
                    console.error(err);
                    Swal.fire('Error', 'No se pudo iniciar la atención', 'error');
                    return;
                }
            }

            // Abrir modal en paso correspondiente
            modal.classList.remove('hidden');
            showStepByEstado(estadoActual);
        });
    });

    // =======================
    // Botón siguiente paso
    // =======================
    const stepInfo = {
        1: { title: 'Atender Ticket pendiente', text: 'Ir a resolver Ticket?' },
        2: { title: 'Ticket en Proceso', text: 'El ticket se está atendiendo, continuar?' },
        3: { title: 'Finalizar Ticket', text: 'El ticket se marcará como Completado' }
    };

    btnNext.addEventListener('click', async () => {
        const nextStep = currentStep < 3 ? currentStep + 1 : 'finalizar';

        try {
            const result = await Swal.fire({
                title: stepInfo[currentStep].title,
                text: stepInfo[currentStep].text,
                icon: 'info',
                showCancelButton: true,
                confirmButtonText: 'Guardar',
                cancelButtonText: 'Cancelar'
            });

            if (!result.isConfirmed) return;

            const data = await guardarPaso(nextStep);
            if (data.estado) actualizarVistaTicket(data.estado);

            if (nextStep !== 'finalizar') {
                currentStep++;
                showStep(currentStep);
            } else {
                Swal.fire('Éxito', 'Ticket completado', 'success');
                modal.classList.add('hidden');
                currentStep = 1;
                showStep(currentStep);
            }
        } catch (err) {
            console.error(err);
            Swal.fire('Error', 'No se pudo guardar el ticket', 'error');
        }
    });

    btnCerrar.addEventListener('click', () => {
        modal.classList.add('hidden');
        currentStep = 1;
        showStep(currentStep);
    });

})();
