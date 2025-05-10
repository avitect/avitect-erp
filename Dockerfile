# 1. Basis-Image
FROM python:3.11-slim

# 2. Arbeitsverzeichnis
WORKDIR /app

# 3. System-Abhängigkeiten (falls benötigt)
RUN apt-get update && apt-get install -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Requirements kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Restlichen Code kopieren
COPY . .

# 6. Port freigeben
EXPOSE 8000

# 7. Standard-Startbefehl (hier FastAPI mit Uvicorn)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
