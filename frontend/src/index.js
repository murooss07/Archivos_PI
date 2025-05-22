// Obtener el token almacenado en localStorage si existe
let token = localStorage.getItem('token');
// Variable para guardar el nombre de usuario tras login
let username = '';

// Actualiza la interfaz según si el usuario está autenticado
function updateUI() {
  const authDiv = document.getElementById('auth');
  const appDiv = document.getElementById('app');

  if (token) {
    // Comprobar si el token sigue siendo válido llamando al backend
    fetch('/api/ping', {
      headers: {
        'Authorization': 'Bearer ' + token
      }
    })
      .then(res => {
        if (!res.ok) throw new Error('Token inválido');
        return res.json();
      })
      .then(data => {
        // Extraer el nombre de usuario del mensaje recibido
        const user = data.message.replace("pong, ", "");
        username = user;
        document.getElementById('user-name').textContent = user;

        // Mostrar interfaz principal y ocultar login
        authDiv.style.display = 'none';
        appDiv.style.display = 'block';
      })
      .catch(() => {
        // Si hay error, eliminar token y mostrar login
        localStorage.removeItem('token');
        token = null;
        authDiv.style.display = 'block';
        appDiv.style.display = 'none';
      });
  } else {
    // Si no hay token, mostrar login
    authDiv.style.display = 'block';
    appDiv.style.display = 'none';
  }
}

// Función para hacer login con usuario y contraseña
function login() {
  const nombre_usuario = document.getElementById('login-username').value;
  const contrasena = document.getElementById('login-password').value;

  fetch('/api/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    // Enviar credenciales al backend
    body: JSON.stringify({ nombre_usuario, contrasena })
  })
    .then(res => {
      if (!res.ok) throw new Error('Credenciales incorrectas');
      return res.json();
    })
    .then(data => {
      // Guardar token y actualizar interfaz
      token = data.access_token;
      localStorage.setItem('token', token);
      updateUI();
    })
    .catch(err => {
      // Mostrar error si las credenciales son incorrectas
      alert(err.message);
    });
}

// Función para cerrar sesión
function logout() {
  localStorage.removeItem('token');
  token = null;
  updateUI();
}

// Encender o apagar un enchufe
function togglePlug(name, on) {
  const action = on ? 'on' : 'off';
  const statusDiv = document.getElementById('status-message');
  statusDiv.textContent = 'Procesando...';
  statusDiv.className = 'status-message'; // resetear clases

  fetch(`/api/device/${name}/${action}`, {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + token
    }
  })
    .then(res => {
      if (!res.ok) throw new Error('Error al cambiar estado');
      return res.json();
    })
    .then(data => {
      // Cambiar estilo visual del enchufe según su estado
      const box = document.getElementById(`plug-${name}`);
      if (on) {
        box.classList.add('on');
      } else {
        box.classList.remove('on');
      }

      // Mostrar mensaje de estado al usuario
      const plugName = name === 'tele' ? 'Televisión' : 'Luz';
      statusDiv.textContent = `${plugName} ${on ? 'encendida' : 'apagada'} correctamente.`;
      statusDiv.className = 'status-message';
      statusDiv.classList.add(on ? 'status-success' : 'status-error');
    })
    .catch(err => {
      // Mostrar mensaje de error si algo falla
      console.error('Error:', err.message);
      statusDiv.textContent = 'No se pudo cambiar el estado del enchufe.';
      statusDiv.classList.add('status-error');
    });
}

// Probar si el backend está accesible y responde correctamente
function pingBackend() {
  fetch('/api/ping', {
    headers: { 'Authorization': 'Bearer ' + token }
  })
    .then(res => {
      if (!res.ok) throw new Error('Fallo en la conexión');
      return res.json();
    })
    .then(data => {
      document.getElementById('response').textContent = '✅ La conexión es correcta.';
    })
    .catch(() => {
      document.getElementById('response').textContent = '❌ La conexión no es correcta.';
    });
}

// Ejecutar cuando el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', () => {
  const passwordInput = document.getElementById('login-password');
  const togglePassword = document.getElementById('toggle-password');

  // Alternar visibilidad de la contraseña al hacer clic en el icono
  togglePassword.addEventListener('click', () => {
    const isVisible = passwordInput.type === 'text';
    passwordInput.type = isVisible ? 'password' : 'text';
    togglePassword.textContent = isVisible ? '👁️‍🗨️' : '👁️';
  });

  // Permitir iniciar sesión con la tecla Enter
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      const authVisible = document.getElementById('auth').style.display !== 'none';
      if (authVisible) login();
    }
  });

  // Inicializar la interfaz al cargar la página
  updateUI();
});
