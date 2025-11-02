# Verwende ein schlankes Python 3 Image
FROM python:3.11-slim

# Setze Arbeitsverzeichnis
WORKDIR /app

# Kopiere requirements.txt und installiere Abhängigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere das Python-Skript
COPY app/device-signal.py .

# Führe das Skript aus (mit -u für unbuffered output)
CMD ["python3", "-u", "device-signal.py"]

