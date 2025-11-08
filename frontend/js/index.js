// index.js - carga y muestra videojuegos, permite crear

async function renderGames(){
  const list = document.getElementById('games-list');
  list.innerHTML = '<p class="small">Cargando...</p>';
  try{
    const games = await window.__api.getGames();
    if(!games || games.length===0){ list.innerHTML = '<p class="small">No hay juegos aún.</p>'; return; }
    list.innerHTML = '';
    games.forEach(g => {
      const card = document.createElement('div');
      card.className = 'game-card';
      card.innerHTML = `<h3>${escapeHtml(g.titulo || g.title)}</h3>
        <p>Precio: $${(g.precio||g.price||0)}</p>
        <p class="small">Consola: ${g.consola_id||g.console_id||'-'}</p>
        <div style="margin-top:8px">
          <button data-id="${g.id}" class="btn-edit">Editar</button>
          <button data-id="${g.id}" class="btn-delete">Eliminar</button>
        </div>`;
      list.appendChild(card);
    });
  }catch(err){
    list.innerHTML = `<p class="small">Error al cargar juegos: ${err.message}</p>`;
  }
}

function escapeHtml(s){ if(!s) return ''; return String(s).replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#39;"})[c]); }

document.getElementById('add-game-form').addEventListener('submit', async (e)=>{
  e.preventDefault();
  const f = e.target;
  const data = {titulo: f.titulo.value, precio: parseFloat(f.precio.value), consola_id: f.consola_id.value};
  try{
    await window.__api.createGame(data);
    f.reset();
    await renderGames();
  }catch(err){ alert('Error creando: ' + (err.body?.error || err.message)); }
});

// Delegación para editar/eliminar
document.getElementById('games-list').addEventListener('click', async (e)=>{
  const id = e.target.getAttribute('data-id');
  if(!id) return;
  if(e.target.classList.contains('btn-delete')){
    if(!confirm('¿Eliminar este videojuego?')) return;
    try{ await window.__api.deleteGame(id); await renderGames(); }catch(err){ alert('Error al eliminar: '+err.message); }
  }
  if(e.target.classList.contains('btn-edit')){
    const newTitle = prompt('Nuevo título');
    if(newTitle==null) return;
    try{ await window.__api.updateGame(id,{titulo:newTitle}); await renderGames(); }catch(err){ alert('Error al editar: '+err.message); }
  }
});

// Inicializar
renderGames();
