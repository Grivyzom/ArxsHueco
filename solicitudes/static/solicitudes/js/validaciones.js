document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form-solicitud");
  if (!form) return;

  form.addEventListener("submit", (event) => {
    const rut = form.querySelector("[name='rut']").value.trim();
    const telefono = form.querySelector("[name='telefono']").value.trim();
    const rutRegex = /^\d{7,8}-[\dkK]$/;
    const telRegex = /^(\+?56)?9\d{8}$/;

    if (!rutRegex.test(rut)) {
      alert("El RUT debe tener formato 12345678-9 (sin puntos, con guión).");
      event.preventDefault();
      return;
    }

    if (!telRegex.test(telefono)) {
      alert("El teléfono debe tener formato +56912345678 o 912345678.");
      event.preventDefault();
      return;
    }
  });
});
