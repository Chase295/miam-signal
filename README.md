# IoT Orchestrator Signal Device Client

Python-Client für das IoT Orchestrator System mit Signal-Messaging-Integration. Dieser Client ermöglicht es, Signal-Nachrichten über WebSocket zu empfangen und an den IoT Orchestrator weiterzuleiten sowie TXT Output vom IoT Orchestrator über die Signal REST API zu versenden.

## 📋 Features

- ✅ **Signal-Integration**: Empfang und Versand von Signal-Nachrichten
- ✅ **IoT Orchestrator Anbindung**: Automatische Weiterleitung von Nachrichten
- ✅ **WebSocket Support**: Echtzeit-Kommunikation über WebSocket
- ✅ **Docker-ready**: Vollständig containerisiert und produktionsbereit
- ✅ **Konfigurierbar**: Alle Einstellungen über Umgebungsvariablen

## 📁 Projektstruktur

```
miam-signal/
├── app/
│   └── device-signal.py    # Haupt-Python-Skript
├── docker-compose.yml      # Docker Compose Konfiguration
├── Dockerfile              # Docker Image Definition
├── requirements.txt        # Python Abhängigkeiten
└── README.md              # Diese Datei
```

## 🚀 Schnellstart

### Voraussetzungen

- Docker und Docker Compose installiert
- Zugriff auf IoT Orchestrator WebSocket-Gateway
- Zugriff auf Signal-Server (WebSocket und REST API)

### 1. Konfiguration anpassen

Bearbeite die `docker-compose.yml` und passe die folgenden Umgebungsvariablen an:

```yaml
environment:
  # IoT Orchestrator
  WS_HOST: "10.0.3.17"              # IoT Orchestrator Host
  WS_PORT: 8080                     # WebSocket Gateway Port
  WS_PATH: "/ws/external"           # WebSocket Path
  DEVICE_NAME: "signal-device"      # Name des Gerätes
  SIMPLE_API_KEY: "DEIN-API-KEY"    # ⚠️ HIER API-KEY EINTRAGEN!

  # Signal-Konfiguration
  SIGNAL_SERVER_URL: "signal.local.chase295.de"
  SIGNAL_RECEIVE_NUMBER: "+4915122215051"   # Eigene Nummer (Empfang)
  SIGNAL_SEND_NUMBER: "+4915122215051"     # Eigene Nummer (Versand)
  SIGNAL_RECIPIENT_NUMBER: "+4917681328005" # Standard-Empfänger
  SIGNAL_VERIFY_SSL: "False"                # SSL-Verifizierung
```

### 2. Container starten

```bash
# Container bauen und starten
docker-compose up -d

# Logs anzeigen
docker-compose logs -f signal-client

# Container stoppen
docker-compose down
```

## 🔧 Konfiguration

### Umgebungsvariablen

Alle Konfigurationswerte werden über Umgebungsvariablen gesteuert:

| Variable | Beschreibung | Standard |
|----------|-------------|----------|
| `WS_HOST` | IoT Orchestrator Host-Adresse | `10.0.3.17` |
| `WS_PORT` | WebSocket Gateway Port | `8080` |
| `WS_PATH` | WebSocket Pfad | `/ws/external` |
| `DEVICE_NAME` | Name des Gerätes | `signal-device` |
| `SIMPLE_API_KEY` | API-Key für Authentifizierung | `default-api-key-123` |
| `SIGNAL_SERVER_URL` | Signal-Server URL (ohne https://) | `signal.local.chase295.de` |
| `SIGNAL_RECEIVE_NUMBER` | Eigene Signal-Nummer (Empfang) | `+4915122215051` |
| `SIGNAL_SEND_NUMBER` | Eigene Signal-Nummer (Versand) | `+4915122215051` |
| `SIGNAL_RECIPIENT_NUMBER` | Standard-Empfängernummer | `+4917681328005` |
| `SIGNAL_VERIFY_SSL` | SSL-Zertifikat-Verifizierung | `False` |

### SSL-Konfiguration

Standardmäßig ist die SSL-Verifizierung deaktiviert (`SIGNAL_VERIFY_SSL: "False"`). Für Produktionsumgebungen mit gültigen Zertifikaten sollte dies auf `"True"` gesetzt werden.

## 🐳 Docker

### Image bauen

```bash
docker-compose build
```

### Container verwalten

```bash
# Starten
docker-compose up -d

# Stoppen
docker-compose down

# Neustarten
docker-compose restart signal-client

# Logs anzeigen
docker-compose logs -f signal-client

# Status prüfen
docker-compose ps
```

## 📡 Funktionsweise

### Signal → IoT Orchestrator (txt_input)

1. Das Gerät empfängt Signal-Nachrichten über WebSocket (`wss://signal-server/v1/receive/{number}`)
2. Empfangene Nachrichten werden an den IoT Orchestrator weitergeleitet
3. Das Gerät ist als `txt_input` Device im IoT Orchestrator verfügbar

### IoT Orchestrator → Signal (txt_output)

1. Der IoT Orchestrator sendet TXT Output an das Gerät
2. Das Gerät versendet die Nachricht über die Signal REST API (`https://signal-server/v2/send`)
3. Das Gerät ist als `txt_output` Device im IoT Orchestrator verfügbar

## 🛠️ Entwicklung

### Lokal ohne Docker

```bash
# Abhängigkeiten installieren
pip install -r requirements.txt

# Umgebungsvariablen setzen (optional, falls nicht in docker-compose.yml)
export WS_HOST="10.0.3.17"
export WS_PORT="8080"
export SIMPLE_API_KEY="dein-api-key"
# ... weitere Variablen

# Script ausführen
python3 app/device-signal.py
```

### Abhängigkeiten

- `websockets` - WebSocket Client/Server Library
- `httpx` - Asynchroner HTTP Client für Signal REST API

## 📝 Troubleshooting

### Verbindungsprobleme

**Problem**: Container startet nicht oder verbindet sich nicht

**Lösung**:
- Überprüfe die Logs: `docker-compose logs -f signal-client`
- Stelle sicher, dass `SIMPLE_API_KEY` korrekt gesetzt ist
- Überprüfe Netzwerkverbindung zu `WS_HOST:WS_PORT`
- Stelle sicher, dass der Signal-Server erreichbar ist

### SSL-Fehler

**Problem**: SSL-Zertifikat-Fehler beim Verbinden zum Signal-Server

**Lösung**:
- Setze `SIGNAL_VERIFY_SSL: "False"` in `docker-compose.yml` (für selbst-signierte Zertifikate)
- Oder stelle sicher, dass gültige Zertifikate verwendet werden

### Device-Registrierung

**Problem**: Device wird nicht im IoT Orchestrator registriert

**Lösung**:
- Überprüfe ob `client_secret_{DEVICE_NAME}` in der Datenbank gespeichert ist
- Stelle sicher, dass die REST API erreichbar ist (`http://{WS_HOST}:3000/api/devices`)

## 📄 Lizenz

Dieses Projekt ist Teil des IoT Orchestrator Systems.

## 🤝 Support

Bei Fragen oder Problemen bitte ein Issue erstellen oder die Dokumentation des IoT Orchestrator Systems konsultieren.

