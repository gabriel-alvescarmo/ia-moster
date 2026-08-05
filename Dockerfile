FROM python:3.11-slim

# 🔧 CORREÇÃO: Instala curl E zstd (agora o Ollama precisa!)
RUN apt-get update && apt-get install -y curl zstd && rm -rf /var/lib/apt/lists/*

# Instala o Ollama DENTRO DO SERVIDOR
RUN curl -fsSL https://ollama.com/install.sh | sh

# Instala Python web
RUN pip install flask requests gunicorn

# Copia nossos arquivos
WORKDIR /app
COPY . .

# Permissão para o start.sh
RUN chmod +x start.sh

EXPOSE 7860

CMD ["./start.sh"]
