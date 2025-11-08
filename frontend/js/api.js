// api.js - funciones para comunicarse con el backend
// Si no se define `window.API_BASE` en el HTML, usar como fallback el backend en localhost:5000
// (útil cuando se sirve el frontend estático en otro puerto durante desarrollo)
const API_BASE = window.API_BASE || 'http://127.0.0.1:5000';

async function request(path, opts={}){
  const headers = opts.headers || {};
  const token = localStorage.getItem('token');
  if(token){ headers['Authorization'] = 'Bearer ' + token; }
  headers['Content-Type'] = headers['Content-Type'] || 'application/json';

  const res = await fetch(API_BASE + path, {...opts, headers});
  let body = null;
  let text = null;
  try{ body = await res.json(); }catch(e){
    // respuesta no-JSON (por ejemplo un 404 HTML del servidor estático)
    try{ text = await res.text(); }catch(e2){ text = null; }
  }
  if(!res.ok){
    const errMsg = (body && (body.message || body.error)) || text || 'Error en la petición';
    const err = new Error(errMsg);
    err.status = res.status; err.body = body;
    throw err;
  }
  // devolver JSON cuando exista, o texto plano si no
  return body !== null ? body : text;
}

// Autenticación
async function login(email, password){
  return request('/auth/login', {method:'POST', body: JSON.stringify({email,password})});
}

async function registerUser(username, email, password){
  return request('/auth/register', {method:'POST', body: JSON.stringify({username,email,password})});
}

async function logout(){
  localStorage.removeItem('token');
}

// Videojuegos
async function getGames(){
  return request('/videojuegos/', {method:'GET'});
}

async function createGame(payload){
  return request('/videojuegos/', {method:'POST', body: JSON.stringify(payload)});
}

async function updateGame(id, payload){
  return request(`/videojuegos/${id}`, {method:'PUT', body: JSON.stringify(payload)});
}

async function deleteGame(id){
  return request(`/videojuegos/${id}`, {method:'DELETE'});
}

// Exponer API para uso global en scripts sin módulos
window.__api = {getGames,createGame,updateGame,deleteGame,login,registerUser,logout};