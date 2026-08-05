from flask import Flask, render_template, request, jsonify
import requests
import json
import os

app = Flask(__name__)
OLLAMA_URL = "http://localhost:11434/api/chat"
MODELO = "qwen2:0.5b"  # ✅ 352MB

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    dados = request.get_json()
    mensagem = dados.get('mensagem', '')
    historico = dados.get('historico', [])

    mensagens = [
        {"role": "system", "content": "Você é um assistente útil que fala português do Brasil. Responda sempre em português, de forma curta e clara."}
    ]
    for h in historico:
        mensagens.append({"role": h['tipo'], "content": h['texto']})
    mensagens.append({"role": "user", "content": mensagem})

    try:
        r = requests.post(OLLAMA_URL, json={
            "model": MODELO,
            "messages": mensagens,
            "stream": False  # ✅ Resposta toda de uma vez (mais rápido no Render)
        }, timeout=120)
        
        obj = r.json()
        return jsonify({"resposta": obj['message']['content']})
        
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    PORTA = int(os.environ.get("PORT", 7860))
    print(f"✅ Rodando na porta {PORTA}", flush=True)
    app.run(host='0.0.0.0', port=PORTA, debug=False)
