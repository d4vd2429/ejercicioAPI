// register.js
const regForm = document.getElementById('register-form');
regForm.addEventListener('submit', async (e)=>{
  e.preventDefault();
  const f = e.target;
  const username = f.username.value;
  const email = f.email.value;
  const password = f.password.value;
  try{
    const res = await window.__api.registerUser(username,email,password);
    // esperar respuesta: puede devolver token o usuario
    if(res.token){ localStorage.setItem('token', res.token); location.href='index.html'; }
    else{ alert('Registro completado. Puedes iniciar sesión.'); location.href='login.html'; }
  }catch(err){ alert('Error al registrar: ' + (err.body?.error || err.message)); }
});
