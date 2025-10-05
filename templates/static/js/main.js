let selected = null;
const list = document.getElementById('modelList');
const chatBtn = document.getElementById('chatBtn');


async function loadModels() {
const res = await fetch('/api/models');
const data = await res.json();
list.innerHTML = '';
data.forEach(m => {
const el = document.createElement('div');
el.className = 'model-card';
el.textContent = `${m.name} (${m.ctx})`;
el.onclick = () => selectModel(m);
list.appendChild(el);
});
}


function selectModel(m) {
selected = m;
document.getElementById('modelName').textContent = m.name;
document.getElementById('modelDesc').textContent = m.desc;
chatBtn.disabled = false;
}


chatBtn.addEventListener('click', async () => {
if (!selected) return;
const msg = prompt('Pergunta:');
if (!msg) return;
const res = await fetch('/api/chat', {
method: 'POST',
headers: {'Content-Type': 'application/json'},
body: JSON.stringify({
model: selected.id,
messages: [
{role:'system', content:'Você é um assistente da InNovaIdeia.'},
{role:'user', content: msg}
]
})
});
const data = await res.json();
document.getElementById('chatOutput').textContent = data.response;
});


document.getElementById('year').textContent = new Date().getFullYear();
loadModels();