FROM python:3.11-slim

# Evita gravação de arquivos .pyc e garante saída imediata nos logs do container
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependências essenciais do sistema operacional
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências Python em camada separada para otimizar o cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia a estrutura de código-fonte para a imagem
COPY src/ ./src/

# Cria os diretórios base de documentos e banco vetorial
RUN mkdir -p data documentos

EXPOSE 8000

# Inicializa o servidor FastAPI por padrão
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]