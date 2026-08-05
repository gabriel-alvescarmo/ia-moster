#!/bin/bash

# Inicia o Ollama em background
ollama serve &
OLLAMA_PID=$!

# Espera ligar
sleep 5

# BAIXA O MODELO DE IA (só baixa se não tiver ainda)
echo "=== VERIFICANDO MODELO ==="
ollama pull llama3.2:1b

# Inicia o site (FORMA SIMPLES QUE SEMPRE FUNCIONA)
echo "=== INICIANDO SITE ==="
cd /app
python app.py

# Mata o Ollama ao sair
kill $OLLAMA_PID
