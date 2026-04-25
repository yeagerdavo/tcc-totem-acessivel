# Usar imagem oficial do Python que seja leve, mas capaz de compilar e rodar pacotes
FROM python:3.10-slim

# Instalar dependências de sistema (ffmpeg é necessário para o Whisper)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho na raiz
WORKDIR /app

# Copiar a pasta de dependências e banco de dados pro container
COPY database/ /app/database/
COPY backend/ /app/backend/

# Entrar na pasta backend para instalar as dependências
WORKDIR /app/backend
RUN pip install --no-cache-dir -r requirements.txt

# O Render geralmente passa a porta via variável de ambiente PORT. 
# Caso contrário, usará a porta padrão 8000.
ENV PORT=8000

# Comando para rodar a aplicação FastAPI
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
