# IoT Orchestrator Signal Device Client

Python-Client für das IoT Orchestrator System mit Signal-Messaging-Integration. Dieser Client ermöglicht es, Signal-Nachrichten über WebSocket zu empfangen und an den IoT Orchestrator weiterzuleiten sowie TXT Output vom IoT Orchestrator über die Signal REST API zu versenden.

**🐳 Docker Image verfügbar auf Docker Hub:** [chase295/miam-signal](https://hub.docker.com/r/chase295/miam-signal)

## 📋 Features

- ✅ **Signal-Integration**: Empfang und Versand von Signal-Nachrichten
- ✅ **IoT Orchestrator Anbindung**: Automatische Weiterleitung von Nachrichten
- ✅ **WebSocket Support**: Echtzeit-Kommunikation über WebSocket
- ✅ **Docker-ready**: Vollständig containerisiert und produktionsbereit
- ✅ **Multi-Architecture**: Unterstützt `linux/amd64` und `linux/arm64`
- ✅ **Konfigurierbar**: Alle Einstellungen über Umgebungsvariablen
- ✅ **Einfache Installation**: Einfach `docker-compose up` - kein Build nötig!
- ✅ **Automatische Reconnection**: Automatische Wiederverbindung bei Verbindungsabbrüchen
- ✅ **Streaming Support**: Unterstützt gestreamte TXT Outputs vom IoT Orchestrator

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

## 🚀 Schnellstart (Installation in 2 Minuten)

### Voraussetzungen

- **Docker** und **Docker Compose** installiert ([Installationsanleitung](https://docs.docker.com/get-docker/))
- Zugriff auf IoT Orchestrator WebSocket-Gateway
- Zugriff auf Signal-Server (WebSocket und REST API)

### Installation

#### Schritt 1: Repository klonen oder docker-compose.yml herunterladen

```bash
# Option 1: Repository klonen
git clone https://github.com/Chase295/miam-signal.git
cd miam-signal

# Option 2: Nur docker-compose.yml herunterladen
wget https://raw.githubusercontent.com/Chase295/miam-signal/main/docker-compose.yml
```

#### Schritt 2: Konfiguration anpassen

Öffne `docker-compose.yml` und passe die Umgebungsvariablen an:

```yaml
environment:
  # IoT Orchestrator (BITTE ANPASSEN!)
  WS_HOST: "10.0.3.17"                        # IoT Orchestrator Host
  WS_PORT: 8080                                 # WebSocket Gateway Port
  WS_PATH: "/ws/external"                     # WebSocket Path
  DEVICE_NAME: "signal-device"                # Name des Gerätes
  SIMPLE_API_KEY: "BITTE-DEIN-API-KEY-EINFUEGEN" # ⚠️ WICHTIG: API-KEY eintragen!

  # Signal-Konfiguration (BITTE ANPASSEN!)
  SIGNAL_SERVER_URL: "signal.local.chase295.de"  # Signal-Server URL
  SIGNAL_RECEIVE_NUMBER: "+4915122215051"         # Eigene Signal-Nummer (Empfang)
  SIGNAL_SEND_NUMBER: "+4915122215051"           # Eigene Signal-Nummer (Versand)
  SIGNAL_RECIPIENT_NUMBER: "+4917681328005"      # Standard-Empfänger
  SIGNAL_VERIFY_SSL: "False"                      # SSL-Verifizierung (True/False)
```

**⚠️ Wichtig:** Passe mindestens die folgenden Werte an:
- `SIMPLE_API_KEY` - Dein IoT Orchestrator API-Key
- `WS_HOST` - Die IP-Adresse oder Domain deines IoT Orchestrators
- `SIGNAL_SERVER_URL` - Die URL deines Signal-Servers
- `SIGNAL_RECEIVE_NUMBER`, `SIGNAL_SEND_NUMBER`, `SIGNAL_RECIPIENT_NUMBER` - Deine Signal-Nummern

#### Schritt 3: Container starten

```bash
# Container starten (lädt automatisch das Image von Docker Hub)
docker-compose up -d

# Logs anzeigen (um zu sehen, ob alles funktioniert)
docker-compose logs -f signal-client

# Container stoppen
docker-compose down
```

**🎉 Fertig!** Das Image wird automatisch von Docker Hub geladen - kein Build erforderlich!

### Verfügbare Docker Images

- **Latest Version**: `chase295/miam-signal:latest`
- **Stabile Version**: `chase295/miam-signal:v1.0.0`

Das Image ist öffentlich auf [Docker Hub](https://hub.docker.com/r/chase295/miam-signal) verfügbar.

### Multi-Architecture Support

Das Docker Image unterstützt mehrere Plattformen:
- **linux/amd64** - Für Intel/AMD Server und Desktop
- **linux/arm64** - Für ARM64 Server (z.B. AWS Graviton, Apple Silicon)

Docker wählt automatisch das passende Image für deine Plattform beim Pull.

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

### Image direkt von Docker Hub verwenden (Empfohlen)

Die `docker-compose.yml` ist so konfiguriert, dass das Image automatisch von Docker Hub geladen wird. **Kein Build nötig!**

```bash
# Starten (lädt Image automatisch von Docker Hub)
docker-compose up -d

# Image manuell pullen
docker pull chase295/miam-signal:latest
```

### Eigenes Image bauen (Optional)

Falls du das Image selbst bauen möchtest (z.B. für Entwicklung):

```bash
docker-compose build
```

Oder manuell:

```bash
docker build -t chase295/miam-signal:latest .
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
- Teste die Verbindung manuell: `ping {WS_HOST}` oder `curl http://{WS_HOST}:8080`

**Problem**: "no matching manifest for linux/amd64"

**Lösung**:
- Das Image wurde mit Multi-Architecture Support aktualisiert
- Führe `docker-compose pull` aus, um das neueste Multi-Arch Image zu laden
- Oder verwende explizit: `docker pull chase295/miam-signal:latest`

### SSL-Fehler

**Problem**: SSL-Zertifikat-Fehler beim Verbinden zum Signal-Server

**Lösung**:
- Setze `SIGNAL_VERIFY_SSL: "False"` in `docker-compose.yml` (für selbst-signierte Zertifikate)
- Oder stelle sicher, dass gültige Zertifikate verwendet werden
- Für Produktionsumgebungen: Verwende ein gültiges SSL-Zertifikat und setze `SIGNAL_VERIFY_SSL: "True"`

### Device-Registrierung

**Problem**: Device wird nicht im IoT Orchestrator registriert

**Lösung**:
- Überprüfe ob `client_secret_{DEVICE_NAME}` in der Datenbank gespeichert ist
- Stelle sicher, dass die REST API erreichbar ist (`http://{WS_HOST}:3000/api/devices`)
- Überprüfe die Logs auf Registrierungsfehler
- Stelle sicher, dass `DEVICE_NAME` und `SIMPLE_API_KEY` korrekt gesetzt sind

### Container beendet sich sofort (Exit Code 137)

**Problem**: Container wird nach kurzer Zeit beendet

**Lösung**:
- Überprüfe die Logs auf Fehlermeldungen: `docker-compose logs signal-client`
- Stelle sicher, dass alle Umgebungsvariablen korrekt gesetzt sind
- Überprüfe die Docker-Ressourcen (Speicher, CPU)
- Exit Code 137 deutet oft auf OOM (Out of Memory) hin

### Keine Signal-Nachrichten werden empfangen

**Problem**: Signal-Nachrichten kommen nicht an

**Lösung**:
- Überprüfe, ob die Signal-Nummer korrekt registriert ist
- Stelle sicher, dass `SIGNAL_RECEIVE_NUMBER` korrekt formatiert ist (z.B. `+4915122215051`)
- Überprüfe die Signal WebSocket-URL in den Logs
- Teste die Signal-Server-Erreichbarkeit

## 🔗 Links

- **GitHub Repository**: https://github.com/Chase295/miam-signal
- **Docker Hub**: https://hub.docker.com/r/chase295/miam-signal
- **Docker Image**: `chase295/miam-signal:latest`
- **Releases**: https://github.com/Chase295/miam-signal/releases

## 🔄 Updates und Versionierung

### Image aktualisieren

```bash
# Neueste Version pullen
docker-compose pull

# Container neu starten mit neuer Version
docker-compose up -d
```

### Versionierte Tags verwenden

Für produktive Umgebungen empfehlen wir, spezifische Versionen zu verwenden:

```yaml
services:
  signal-client:
    image: chase295/miam-signal:v1.0.0  # Stabile Version
    # statt: image: chase295/miam-signal:latest
```

### Verfügbare Versionen

- `latest` - Neueste Entwicklungsversion
- `v1.0.0` - Stabile Release-Version

## 📊 Monitoring und Health Checks

### Container-Status prüfen

```bash
# Status anzeigen
docker-compose ps

# Logs in Echtzeit verfolgen
docker-compose logs -f signal-client

# Ressourcenverbrauch überwachen
docker stats miam-signal-signal-client-1
```

### Log-Analyse

```bash
# Letzte 100 Zeilen
docker-compose logs --tail=100 signal-client

# Fehler filtern
docker-compose logs signal-client | grep -i error

# Zeitstempel anzeigen
docker-compose logs -t signal-client
```

## 🔒 Sicherheitshinweise

### Best Practices

1. **API-Keys schützen**: Speichere `SIMPLE_API_KEY` niemals in Version-Control
2. **Umgebungsvariablen**: Verwende `.env` Dateien für sensible Daten (nicht in git)
3. **SSL-Verifizierung**: In Produktion `SIGNAL_VERIFY_SSL: "True"` verwenden
4. **Netzwerk-Isolation**: Nutze Docker-Netzwerke für Container-Isolation
5. **Regelmäßige Updates**: Halte das Image aktuell mit `docker-compose pull`

### .env Datei verwenden

Erstelle eine `.env` Datei für sensible Daten:

```bash
# .env Datei (nicht committen!)
SIMPLE_API_KEY=dein-geheimer-api-key
WS_HOST=10.0.3.17
```

Und verwende sie in `docker-compose.yml`:

```yaml
environment:
  SIMPLE_API_KEY: ${SIMPLE_API_KEY}
  WS_HOST: ${WS_HOST}
```

## 💡 Use Cases und Beispiele

### Beispiel 1: Einfache Nachrichtenweiterleitung

Einrichtung eines Geräts, das alle eingehenden Signal-Nachrichten an den IoT Orchestrator weiterleitet:

```yaml
environment:
  DEVICE_NAME: "signal-bridge"
  SIGNAL_RECEIVE_NUMBER: "+4915122215051"
```

### Beispiel 2: Mehrere Geräte mit verschiedenen Nummern

Mehrere Container mit verschiedenen Signal-Nummern:

```yaml
services:
  signal-client-1:
    image: chase295/miam-signal:latest
    environment:
      DEVICE_NAME: "signal-device-1"
      SIGNAL_RECEIVE_NUMBER: "+4915122215051"
      # ...
  
  signal-client-2:
    image: chase295/miam-signal:latest
    environment:
      DEVICE_NAME: "signal-device-2"
      SIGNAL_RECEIVE_NUMBER: "+4915122215052"
      # ...
```

### Beispiel 3: Produktions-Setup mit spezifischer Version

```yaml
services:
  signal-client:
    image: chase295/miam-signal:v1.0.0  # Stabile Version
    restart: always  # Automatischer Neustart
    environment:
      # ... Konfiguration
```

## ❓ Häufig gestellte Fragen (FAQ)

### Q: Kann ich das Image selbst bauen?

**A:** Ja! Verwende `docker-compose build` oder `docker build -t chase295/miam-signal .`

### Q: Unterstützt das Image ARM64 Server?

**A:** Ja! Das Image wurde mit Multi-Architecture Support gebaut und unterstützt sowohl `linux/amd64` als auch `linux/arm64`.

### Q: Wie starte ich das Gerät automatisch beim Boot?

**A:** Verwende `restart: always` oder `restart: unless-stopped` in der `docker-compose.yml`. Oder richte einen systemd Service ein.

### Q: Kann ich mehrere Signal-Nummern mit einem Container verwenden?

**A:** Nein, jeder Container verwendet eine Signal-Nummer. Für mehrere Nummern starte mehrere Container mit verschiedenen `DEVICE_NAME` und `SIGNAL_RECEIVE_NUMBER`.

### Q: Wie teste ich die Verbindung?

**A:** Überprüfe die Logs: `docker-compose logs -f signal-client`. Du solltest sehen:
- ✓ IoT Orchestrator Verbindung hergestellt
- ✓ Signal WebSocket verbunden

### Q: Was bedeutet Exit Code 137?

**A:** Exit Code 137 bedeutet, dass der Container vom System beendet wurde (SIGKILL), oft wegen Speichermangels oder manueller Beendigung.

### Q: Wie aktualisiere ich auf eine neue Version?

**A:** 
```bash
docker-compose pull
docker-compose up -d
```

## 🏗️ Architektur

### System-Übersicht

```
┌─────────────────┐         ┌──────────────┐         ┌─────────────────┐
│  Signal Server │◄────────┤ Signal Device│────────►│ IoT Orchestrator│
│  (WebSocket)   │         │   (Client)   │         │  (WebSocket)    │
└─────────────────┘         └──────────────┘         └─────────────────┘
                                      │
                                      │
                            ┌─────────▼──────────┐
                            │  Signal REST API   │
                            │   (Nachrichten     │
                            │    versenden)      │
                            └────────────────────┘
```

### Datenfluss

1. **Signal → IoT Orchestrator (txt_input)**
   - Signal-Nachricht wird über WebSocket empfangen
   - Wird an IoT Orchestrator als txt_input weitergeleitet
   - Metadata enthält Absender-Informationen

2. **IoT Orchestrator → Signal (txt_output)**
   - IoT Orchestrator sendet TXT Output
   - Client sendet über Signal REST API
   - Unterstützt Streaming von langen Nachrichten

## 📚 Weitere Ressourcen

### Dokumentation

- [Docker Compose Dokumentation](https://docs.docker.com/compose/)
- [WebSocket Protocol](https://datatracker.ietf.org/doc/html/rfc6455)
- [Signal REST API](https://github.com/AsamK/signal-cli/wiki/REST-API)

### Ähnliche Projekte

- [IoT Orchestrator](https://github.com/Chase295) - Hauptprojekt
- Weitere Signal-Integrationen

## 📄 Lizenz

Dieses Projekt ist Teil des IoT Orchestrator Systems.

## 🤝 Support

Bei Fragen oder Problemen bitte ein Issue erstellen oder die Dokumentation des IoT Orchestrator Systems konsultieren.

### Community

- **GitHub Issues**: Für Bug-Reports und Feature-Requests
- **Pull Requests**: Beiträge sind willkommen!

### Changelog

#### v1.0.0 (2025-10-31)

- ✨ Initial Release
- ✅ Multi-Architecture Support (linux/amd64, linux/arm64)
- ✅ Signal WebSocket Integration
- ✅ IoT Orchestrator WebSocket Integration
- ✅ TXT Input/Output Support
- ✅ Streaming Support für lange Nachrichten
- ✅ Docker Image auf Docker Hub verfügbar

