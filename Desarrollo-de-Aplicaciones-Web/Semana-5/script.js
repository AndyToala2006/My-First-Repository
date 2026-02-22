const imageUrlInput = document.getElementById("imageUrl");
const addImageBtn = document.getElementById("addImage");
const deleteImageBtn = document.getElementById("deleteImage");
const gallery = document.getElementById("gallery");

let selectedCard = null;

// Agregar imagen
addImageBtn.addEventListener("click", () => {
  const url = imageUrlInput.value.trim();
  if (!url) return;

  const card = document.createElement("div");
  card.classList.add("image-card");

  const img = document.createElement("img");
  img.src = url;
  img.alt = "Imagen de la galería";

  card.appendChild(img);
  gallery.appendChild(card);

  // Evento de selección
  card.addEventListener("click", () => {
    if (selectedCard) {
      selectedCard.classList.remove("selected");
    }
    card.classList.add("selected");
    selectedCard = card;
  });

  imageUrlInput.value = "";
});

// Eliminar imagen seleccionada
deleteImageBtn.addEventListener("click", () => {
  if (selectedCard) {
    selectedCard.remove();
    selectedCard = null;
  }
});
