#!/bin/bash
set -e

echo "🔧 Ligando Ollama..."
ollama serve &
OLLAMA_PID=$!
sleep 8

# ✅ MODELO DE 352MB - CABE NO RENDER GRÁTIS!
if ! ollama list | grep -q "qwen2:0.5b"; then
    echo "⬇️ Baixando qwen2:0.5b (352MB)..."
    ollama pull qwen2:0.5b
else
    echo "✅ Modelo já existe"
fi

echo "🚀 Iniciando site..."
cd /app
exec python app.py
