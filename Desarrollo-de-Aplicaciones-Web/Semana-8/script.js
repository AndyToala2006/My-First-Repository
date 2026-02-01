// Esperar a que cargue el DOM
document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("contactForm");
    const alertBtn = document.getElementById("alertBtn");

    const nombre = document.getElementById("nombre");
    const correo = document.getElementById("correo");
    const mensaje = document.getElementById("mensaje");

    // Botón de alerta
    alertBtn.addEventListener("click", () => {
        mostrarAlerta("Gracias por visitar TechStore 🚀", "success");
    });

    // Validación en tiempo real
    [nombre, correo, mensaje].forEach(input => {
        input.addEventListener("input", () => validarCampo(input));
    });

    // Envío del formulario
    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const valido =
            validarCampo(nombre) &
            validarCampo(correo) &
            validarCampo(mensaje);

        if (valido) {
            simularEnvio();
        }
    });

    // Funciones
    function validarCampo(campo) {
        const error = document.getElementById("error" + capitalizar(campo.id));

        if (campo.value.trim() === "") {
            error.textContent = "Este campo es obligatorio";
            campo.classList.add("is-invalid");
            return false;
        }

        error.textContent = "";
        campo.classList.remove("is-invalid");
        campo.classList.add("is-valid");
        return true;
    }

    function simularEnvio() {
        mostrarAlerta("Enviando formulario...", "info");

        setTimeout(() => {
            mostrarAlerta("Formulario enviado correctamente ✔️", "success");
            form.reset();
            limpiarClases();
        }, 1500);
    }

    function mostrarAlerta(mensaje, tipo) {
        const alerta = document.createElement("div");
        alerta.className = `alert alert-${tipo} mt-3`;
        alerta.textContent = mensaje;

        form.appendChild(alerta);

        setTimeout(() => alerta.remove(), 3000);
    }

    function limpiarClases() {
        [nombre, correo, mensaje].forEach(campo => {
            campo.classList.remove("is-valid", "is-invalid");
        });
    }

    function capitalizar(texto) {
        return texto.charAt(0).toUpperCase() + texto.slice(1);
    }

});
