const productos = [
    {
        nombre: "Laptop",
        precio: 800,
        descripcion: "Equipo portátil para estudio y trabajo"
    },
    {
        nombre: "Mouse",
        precio: 15,
        descripcion: "Mouse inalámbrico"
    },
    {
        nombre: "Teclado",
        precio: 25,
        descripcion: "Teclado mecánico básico"
    }
];

const lista = document.getElementById("lista-productos");
const boton = document.getElementById("btn-agregar");

function renderizarProductos() {
    lista.innerHTML = "";

    productos.forEach(producto => {
        const li = document.createElement("li");

        li.innerHTML = `
            <strong>${producto.nombre}</strong><br>
            <span class="precio">$${producto.precio}</span><br>
            ${producto.descripcion}
        `;

        lista.appendChild(li);
    });
}

boton.addEventListener("click", () => {
    const nombre = prompt("Ingrese el nombre del producto:");
    const precio = prompt("Ingrese el precio del producto:");
    const descripcion = prompt("Ingrese una descripción breve:");

    if (nombre && precio && descripcion) {
        productos.push({
            nombre: nombre,
            precio: precio,
            descripcion: descripcion
        });

        renderizarProductos();
    } else {
        alert("Debe completar todos los campos.");
    }
});

renderizarProductos();
