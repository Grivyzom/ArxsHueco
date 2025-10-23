document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form-solicitud");
  if (!form) return;

  // Campo RUT: solo números, guión y K
  const rutInput = form.querySelector("[name='rut']");
  if (rutInput) {
    rutInput.addEventListener("input", (event) => {
      let value = event.target.value;
      // Permitir solo dígitos, guión (-) y letra K (mayúscula o minúscula)
      value = value.replace(/[^0-9\-kK]/g, '');
      event.target.value = value;
    });

    rutInput.addEventListener("keypress", (event) => {
      const char = event.key;
      // Permitir solo números, guión, K/k y teclas de control
      if (!/[0-9\-kK]/.test(char) && event.key !== 'Backspace' && event.key !== 'Delete' && event.key !== 'Tab' && event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') {
        event.preventDefault();
      }
    });
  }

  // Campo Teléfono: solo números y símbolo +
  const telefonoInput = form.querySelector("[name='telefono']");
  if (telefonoInput) {
    telefonoInput.addEventListener("input", (event) => {
      let value = event.target.value;
      // Permitir solo dígitos y el símbolo +
      value = value.replace(/[^0-9\+]/g, '');
      // Permitir + solo al inicio
      if (value.indexOf('+') > 0) {
        value = value.replace(/\+/g, '');
      }
      event.target.value = value;
    });

    telefonoInput.addEventListener("keypress", (event) => {
      const char = event.key;
      const currentValue = event.target.value;
      // Permitir + solo si está vacío o al inicio
      if (char === '+' && currentValue.length > 0) {
        event.preventDefault();
        return;
      }
      // Permitir solo números, + y teclas de control
      if (!/[0-9\+]/.test(char) && event.key !== 'Backspace' && event.key !== 'Delete' && event.key !== 'Tab' && event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') {
        event.preventDefault();
      }
    });
  }

  // Campo Nombres: no permitir números ni símbolos especiales
  const nombresInput = form.querySelector("[name='nombres']");
  if (nombresInput) {
    nombresInput.addEventListener("input", (event) => {
      let value = event.target.value;
      // Permitir solo letras, espacios, tildes y ñ
      value = value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]/g, '');
      event.target.value = value;
    });

    nombresInput.addEventListener("keypress", (event) => {
      const char = event.key;
      // Bloquear números y símbolos especiales
      if (/[0-9]/.test(char)) {
        event.preventDefault();
      }
    });
  }

  // Campo Apellidos: no permitir números ni símbolos especiales
  const apellidosInput = form.querySelector("[name='apellidos']");
  if (apellidosInput) {
    apellidosInput.addEventListener("input", (event) => {
      let value = event.target.value;
      // Permitir solo letras, espacios, tildes y ñ
      value = value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]/g, '');
      event.target.value = value;
    });

    apellidosInput.addEventListener("keypress", (event) => {
      const char = event.key;
      // Bloquear números y símbolos especiales
      if (/[0-9]/.test(char)) {
        event.preventDefault();
      }
    });
  }

  // Validación al enviar el formulario
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
