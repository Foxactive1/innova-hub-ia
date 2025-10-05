### 🧩 app.py — Backend Flask Completo

from flask import Flask, request, jsonify, render_template
import os, sqlite3, requests
from datetime import datetime
from dotenv import load_dotenv
from waitress import serve


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'innova-dev')
DB_PATH = 'innova.db'

# --- Funções auxiliares ---
def db_connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def save_history(model, user_msg, assistant_msg):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute('INSERT INTO history (model, user_message, assistant_message, created_at) VALUES (?,?,?,?)',
                (model, user_msg, assistant_msg, datetime.now().isoformat()))
    conn.commit()
    conn.close()

# --- Rotas principais ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/models')
def get_models():
    models = [
      {'name':'xAI: Grok Code Fast 1','id':'xai/grok-code-fast-1','ctx':'256K','price':'$0.20 in / $1.50 out','category':'Programming','desc':'Modelo rápido e econômico para codificação e agentes; ideal para iterações rápidas.'},
      {'name':'OpenAI: GPT-5','id':'openai/gpt-5','ctx':'400K','price':'$1.25 in / $10 out','category':'General','desc':'Modelo avançado para raciocínio complexo, análise e produção de alto nível.'},
      {'name':'Google: Gemini 2.5 Flash','id':'google/gemini-2.5-flash','ctx':'1.05M','price':'$0.30 in / $2.50 out','category':'Reasoning','desc':'Alta janela de contexto e bom em matemática/código de longa duração.'},
      {'name':'Anthropic: Claude Sonnet 4','id':'anthropic/claude-sonnet-4','ctx':'1M','price':'$3 in / $15 out','category':'Safety & Reasoning','desc':'Robusto em controle e segurança, ótimo para fluxos onde confiabilidade é crítica.'}
    ]
    return jsonify(models)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    model = data.get('model')
    messages = data.get('messages')

    headers = {
        'Authorization': f"Bearer {os.getenv('OPENROUTER_KEY')}",
        'Content-Type': 'application/json'
    }

    resp = requests.post(
        os.getenv('OPENROUTER_URL', 'https://openrouter.ai/api/v1/chat/completions'),
        headers=headers,
        json={'model': model, 'messages': messages, 'max_tokens': 512}
    )

    result = resp.json()
    assistant_message = result.get('choices', [{}])[0].get('message', {}).get('content', '(Sem resposta)')

    # salva no histórico
    save_history(model, messages[-1]['content'], assistant_message)
    return jsonify({'response': assistant_message})

@app.route('/api/history')
def history():
    conn = db_connect()
    cur = conn.cursor()
    cur.execute('SELECT * FROM history ORDER BY created_at DESC LIMIT 20')
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True)
     
    serve(app, host='0.0.0.0', port=5000)


