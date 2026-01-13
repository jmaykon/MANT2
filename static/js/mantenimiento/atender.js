
const modal = document.getElementById('modal');
const btnAtender = document.getElementById('btnAtender');
const btnCerrar = document.getElementById('btnCerrar');
const steps = document.querySelectorAll('.step');
const stepContents = document.querySelectorAll('.step-content');
const btnNext = document.querySelector('.btn-next');

let currentStep = 1;

function showStep(step) {
    steps.forEach(s => s.classList.remove('step-active'));
    stepContents.forEach(c => c.classList.add('hidden'));

    const stepEl = document.querySelector(`.step[data-step="${step}"]`);
    stepEl.classList.add('step-active');

    document
        .querySelector(`.step-content[data-step="${step}"]`)
        .classList.remove('hidden');

    btnNext.textContent = step === 3 ? 'Finalizar' : 'Continuar';
}

btnAtender.addEventListener('click', () => {
    Swal.fire({
        title: '¿Atender ticket?',
        text: 'Confirma iniciar el proceso',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Sí, atender',
        cancelButtonText: 'Cancelar'
    }).then(result => {
        if (result.isConfirmed) {
            modal.classList.remove('hidden');
            showStep(currentStep);
        }
    });
});

btnCerrar.addEventListener('click', () => {
    modal.classList.add('hidden');
    currentStep = 1;
    showStep(currentStep);
});

btnNext.addEventListener('click', () => {

    // Si NO es el último paso
    if (currentStep < 3) {
        Swal.fire({
            title: stepInfo[currentStep].title,
            text: stepInfo[currentStep].text,
            icon: 'info',
            showCancelButton: true,
            confirmButtonText: 'Continuar',
            cancelButtonText: 'Cancelar'
        }).then(result => {
            if (result.isConfirmed) {
                currentStep++;
                showStep(currentStep);
            }
        });
    }
    // Último paso
    else {
        Swal.fire({
            title: stepInfo[3].title,
            text: stepInfo[3].text,
            icon: 'success',
            confirmButtonText: 'Finalizar'
        }).then(() => {
            modal.classList.add('hidden');
            currentStep = 1;
            showStep(currentStep);
        });
    }
});




const stepInfo = {
    1: {
        title: 'Atender Ticket pendiente',
        text: 'Ir a resolver Ticket?'
    },
    2: {
        title: 'Ticket Resuelto',
        text: 'El ticket se resolvio, ¿pasar a Completar?'
    },
    3: {
        title: 'Finalizar Ticket',
        text: 'El ticket se marcará como Completado'
    }
};

