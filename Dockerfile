# Verwende ein schlankes Python 3 Image
FROM python:3.11-slim

# Setze Arbeitsverzeichnis
WORKDIR /app

# Kopiere requirements.txt und installiere Abhängigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere das Python-Skript
COPY app/device-signal.py .

# Führe das Skript aus
CMD ["python3", "device-signal.py"]

