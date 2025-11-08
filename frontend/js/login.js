// login.js
const loginForm = document.getElementById('login-form');
loginForm.addEventListener('submit', async (e)=>{
  e.preventDefault();
  const f = e.target;
  const email = f.email.value;
  const password = f.password.value;
  try{
    const res = await window.__api.login(email,password);
    // se asume que backend devuelve {token: '...'}
    if(res.token){ localStorage.setItem('token', res.token); location.href = 'index.html'; }
    else{ alert('Login correcto pero no se recibió token.'); }
  }catch(err){
    alert('Error en login: ' + (err.body?.error || err.message));
  }
});
