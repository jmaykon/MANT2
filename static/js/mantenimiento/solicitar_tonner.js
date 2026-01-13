document.getElementById('tipo_soporte').addEventListener('change', function () {
    const tonnerDiv = document.getElementById('tonner');
    const coloresDiv = document.getElementById('colores_tinta'); // Referencia al otro para ocultarlo

    // Verifica ambos valores por si acaso (Mayúscula/Minúscula)
    if (this.value === 'Tonner' || this.value === 'tonner') {
        tonnerDiv.classList.remove('hidden');
        // Ocultamos el bloque del otro script
        if (coloresDiv) {
            coloresDiv.classList.add('hidden');
            coloresDiv.querySelectorAll('input[type="checkbox"]').forEach(chk => chk.checked = false);
        }
    } else {
        tonnerDiv.classList.add('hidden');
    }
});