const form = document.getElementById("formulario");
const btnEnviar = document.getElementById("btnEnviar");

const regexCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const regexPassword = /^(?=.*\d)(?=.*[\W_]).{8,}$/;

function mostrarEstado(input, valido, mensaje) {
    const error = input.nextElementSibling;
    if (valido) {
        input.classList.add("valido");
        input.classList.remove("invalido");
        error.textContent = "";
    } else {
        input.classList.add("invalido");
        input.classList.remove("valido");
        error.textContent = mensaje;
    }
    return valido;
}

function validarFormulario() {
    const v1 = mostrarEstado(nombre, nombre.value.length >= 3, "Mínimo 3 caracteres");
    const v2 = mostrarEstado(correo, regexCorreo.test(correo.value), "Correo inválido");
    const v3 = mostrarEstado(password, regexPassword.test(password.value), "Debe tener número y símbolo");
    const v4 = mostrarEstado(confirmarPassword, confirmarPassword.value === password.value && confirmarPassword.value !== "", "No coincide");
    const v5 = mostrarEstado(edad, edad.value >= 18, "Debe ser mayor de edad");

    btnEnviar.disabled = !(v1 && v2 && v3 && v4 && v5);
}

form.addEventListener("input", validarFormulario);

form.addEventListener("submit", e => {
    e.preventDefault();
    alert("Formulario validado correctamente");
    form.reset();
    btnEnviar.disabled = true;

    form.querySelectorAll("input").forEach(input => {
        input.classList.remove("valido", "invalido");
    });
});
