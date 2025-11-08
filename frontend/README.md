Front-end estático para la API de `ejercicioAPI`.

Contenido:
- index.html — Catálogo y CRUD (usa `/videojuegos/`)
- login.html — Formulario de inicio de sesión (usa `/auth/login`)
- register.html — Formulario de registro (usa `/auth/register`)
- js/api.js — Funciones JS que llaman a la API (login, register, juegos CRUD)
- js/index.js, js/login.js, js/register.js — Lógica por página
- css/styles.css — Estilos

Notas:
- El frontend asume que el backend expone rutas:
  - POST /auth/login -> {token: '...'}
  - POST /auth/register -> {token: '...'} o información del usuario
  - GET/POST/PUT/DELETE /videojuegos/
- Por defecto el frontend usa el mismo origen (location.origin) como `API_BASE`.
  Si tu API corre en otro puerto (ej. http://localhost:5000), ajusta `window.API_BASE` en la consola del navegador, o cambia la primera línea de `js/api.js`.

Cómo probar localmente:
1. Ejecuta tu backend Flask (por ejemplo en http://localhost:5000).
2. Abre los archivos HTML en el navegador (archivo local) o sirve la carpeta `frontend/` con un servidor estático.
   - En PowerShell: python -m http.server 8000 desde la carpeta `frontend` y visita http://localhost:8000

Limitaciones:
- El repositorio detectado tiene controladores de usuario vacíos; si las rutas /auth/* no existen deberás implementarlas en el backend o adaptar `api.js` a tus rutas reales.
