from flask import Flask, render_template, request, Response
import requests
import json
import os  # ← adicionado

app = Flask(__name__)

# Ollama roda LOCALMENTE no mesmo servidor
OLLAMA_URL = "http://localhost:11434/api/chat"
MODELO = "llama3.2:1b"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    dados = request.get_json()
    mensagem = dados.get('mensagem', '')
    historico = dados.get('historico', [])

    mensagens = [
        {"role": "system", "content": "Você é um assistente útil que fala português do Brasil. Seja curto, claro e amigável."}
    ]
    
    for h in historico:
        mensagens.append({"role": h['tipo'], "content": h['texto']})
    
    mensagens.append({"role": "user", "content": mensagem})

    def gerar():
        try:
            r = requests.post(OLLAMA_URL, json={
                "model": MODELO,
                "messages": mensagens,
                "stream": True
            }, stream=True, timeout=300)

            for linha in r.iter_lines():
                if linha:
                    try:
                        obj = json.loads(linha.decode('utf-8'))
                        if 'message' in obj and 'content' in obj['message']:
                            pedaco = obj['message']['content']
                            yield f"data: {json.dumps({'texto': pedaco})}\n\n"
                    except:
                        pass
            yield "data: [FIM]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'erro': str(e)})}\n\n"

    return Response(gerar(), mimetype='text/event-stream')

if __name__ == '__main__':
    # 🔧 CORREÇÃO IMPORTANTE: Pega a PORTA que o Render quiser!
    PORTA = int(os.environ.get("PORT", 7860))
    print(f"✅ SITE LIGADO NA PORTA: {PORTA}", flush=True)
    app.run(host='0.0.0.0', port=PORTA, debug=False)
