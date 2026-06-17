FROM python:3.14-slim

# Evita archivos .pyc y fuerza salida inmediata de logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Actualiza pip
RUN pip install --upgrade pip

# Copia primero requirements para aprovechar la cache
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del proyecto
COPY . .

# Crear usuario no root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]