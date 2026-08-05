#!/bin/bash

# Inicia o Ollama em background
ollama serve &
OLLAMA_PID=$!

# Espera ligar
sleep 5

# BAIXA O MODELO DE IA AQUI (escolha um)
# llama3.2 = ~2GB (bom e rápido)
# phi3 = ~2.3GB
# tinyllama = ~600MB (muito leve)
echo "=== BAIXANDO MODELO DE IA ==="
ollama pull llama3.2:1b

# Inicia o site
echo "=== INICIANDO SITE ==="
gunicorn --bind 0.0.0.0:7860 --workers 1 --timeout 300 app:app

# Mata o Ollama ao sair
kill $OLLAMA_PID
