
/* AGREGADO */
document.body.addEventListener("lugarAgregado", function (e) {
    Swal.fire({
        icon: "success",
        title: "Lugar agregado",
        text: `Se agregó: ${e.detail.value}`,
        timer: 2000,
        showConfirmButton: false
    });
});

/* EDITADO */
document.body.addEventListener("lugarEditado", function (e) {
    Swal.fire({
        icon: "success",
        title: "Lugar editado",
        text: `Se editó: ${e.detail.value}`,
        timer: 2000,
        showConfirmButton: false
    });
});

/* ELIMINADO */
document.body.addEventListener("lugarEliminado", function (e) {
    Swal.fire({
        icon: "success",
        title: "Lugar eliminado",
        text: `Se eliminó: ${e.detail.value}`,
        timer: 2000,
        showConfirmButton: false
    });
});

