FROM python:3.11-slim

# Instala dependências
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Instala o Ollama DENTRO DO SERVIDOR
RUN curl -fsSL https://ollama.com/install.sh | sh

# Instala Python web
RUN pip install flask requests gunicorn

# Copia nossos arquivos
WORKDIR /app
COPY . .

# Baixa o modelo de IA DURANTE A CONSTRUÇÃO (já fica pronto)
RUN chmod +x start.sh

EXPOSE 7860

CMD ["./start.sh"]
