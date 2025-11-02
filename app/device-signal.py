#!/usr/bin/env python3
"""
Device Client mit Signal-Integration (Stable IoT Connection)
=============================================================
Python-Client für das IoT Orchestrator System mit Signal-Messaging

Dieses Script erstellt ein gerät, das:
- Als IoT Device mit txt_input und txt_output registriert wird
- Signal-Nachrichten über WebSocket empfängt (mit Auto-Reconnect)
- Signal-Nachrichten an IoT Orchestrator weiterleitet (txt_input)
- TXT Output vom IoT Orchestrator über Signal REST API versendet (txt_output)

WICHTIG: IoT-Verbindung bleibt stabil, auch wenn Signal disconnected!

Verwendung:
    1. Passe Konfiguration an (DEVICE_NAME, Signal-Nummern, etc.)
    2. Installiere Abhängigkeiten: pip install websockets httpx
    3. Stelle sicher, dass client_secret_signal-device in der DB gespeichert ist
    4. Führe aus: python3 device-signal.py
"""

import asyncio
import websockets
import json
import sys
import os
import ssl
from datetime import datetime
from typing import Optional

# HTTP-Client für Signal REST API
try:
    import httpx
except ImportError:
    print("❌ httpx nicht installiert!")
    print("   Installiere mit: pip install httpx")
    sys.exit(1)

# ======================================
# KONFIGURATION - VIA UMWELTVARIABLEN
# ======================================

# IoT Orchestrator WebSocket-Gateway
WS_HOST = os.getenv("WS_HOST", "10.0.3.17")
WS_PORT = int(os.getenv("WS_PORT", "8080"))
WS_PATH = os.getenv("WS_PATH", "/ws/external")

# Geräte-Informationen  
DEVICE_NAME = os.getenv("DEVICE_NAME", "signal-device")

# Globaler API Key
API_KEY = os.getenv("SIMPLE_API_KEY", "default-api-key-123")

# Signal-Konfiguration
SIGNAL_SERVER_URL = os.getenv("SIGNAL_SERVER_URL", "signal.local.chase295.de")
SIGNAL_RECEIVE_NUMBER = os.getenv("SIGNAL_RECEIVE_NUMBER", "+4915122215051")
SIGNAL_SEND_NUMBER = os.getenv("SIGNAL_SEND_NUMBER", "+4915122215051")
SIGNAL_RECIPIENT_NUMBER = os.getenv("SIGNAL_RECIPIENT_NUMBER", "+4917681328005")

# Protokoll-Konfiguration
SIGNAL_PROTOCOL = os.getenv("SIGNAL_PROTOCOL", "https").lower()

# SSL-Konfiguration
SIGNAL_VERIFY_SSL = os.getenv("SIGNAL_VERIFY_SSL", "False").lower() in ('true', '1', 't')

# Reconnect-Konfiguration
SIGNAL_RECONNECT_DELAY = int(os.getenv("SIGNAL_RECONNECT_DELAY", "10"))
IOT_RECONNECT_DELAY = int(os.getenv("IOT_RECONNECT_DELAY", "10"))

# Signal-URLs intelligent konstruieren
def build_signal_urls():
    """
    Baut Signal WebSocket und REST API URLs basierend auf SIGNAL_SERVER_URL und SIGNAL_PROTOCOL
    """
    url = SIGNAL_SERVER_URL.strip()
    protocol = SIGNAL_PROTOCOL
    
    if url.startswith("http://"):
        protocol = "http"
        url = url[7:]
    elif url.startswith("https://"):
        protocol = "https"
        url = url[8:]
    elif url.startswith("ws://"):
        protocol = "http"
        url = url[5:]
    elif url.startswith("wss://"):
        protocol = "https"
        url = url[6:]
    
    if protocol not in ("http", "https"):
        protocol = "https"
    
    url = url.rstrip("/")
    
    ws_protocol = "wss" if protocol == "https" else "ws"
    http_protocol = protocol
    
    ws_url = f"{ws_protocol}://{url}/v1/receive/{SIGNAL_RECEIVE_NUMBER}"
    api_url = f"{http_protocol}://{url}/v2/send"
    
    return ws_url, api_url, protocol

SIGNAL_WS_URL, SIGNAL_API_URL, SIGNAL_ACTUAL_PROTOCOL = build_signal_urls()

# ======================================
# GERÄTE-FÄHIGKEITEN (CAPABILITIES)
# ======================================
DEVICE_CAPABILITIES = [
    'txt_output',
    'txt_input',
]

# ======================================
# ENDE KONFIGURATION
# ======================================

# Vollständige IoT Orchestrator WebSocket-URL mit Authentifizierung
IOT_WS_URL = f"ws://{WS_HOST}:{WS_PORT}{WS_PATH}?clientId={DEVICE_NAME}&secret={API_KEY}"

def print_header():
    """Zeigt den Header mit Konfiguration an"""
    print("\n" + "="*70)
    print("  IoT Orchestrator Signal Device Client (Stable Mode)")
    print("="*70 + "\n")
    print(f"📱 Gerät: {DEVICE_NAME}")
    print(f"🔗 IoT Orchestrator: {IOT_WS_URL}")
    print(f"📲 Signal-Empfang: {SIGNAL_WS_URL}")
    print(f"📤 Signal-Senden: {SIGNAL_API_URL}")
    print(f"🔐 Signal-Protokoll: {SIGNAL_ACTUAL_PROTOCOL.upper()}")
    print(f"📞 Signal-Nummer (Empfang): {SIGNAL_RECEIVE_NUMBER}")
    print(f"📞 Signal-Nummer (Senden): {SIGNAL_SEND_NUMBER}")
    print(f"👤 Standard-Empfänger: {SIGNAL_RECIPIENT_NUMBER}")
    print(f"🔄 Signal Reconnect: {SIGNAL_RECONNECT_DELAY}s")
    print(f"🔄 IoT Reconnect: {IOT_RECONNECT_DELAY}s\n")

async def send_signal_message(message: str, recipient: Optional[str] = None):
    """
    Sendet eine Nachricht über die Signal REST API
    """
    try:
        recipient_number = recipient or SIGNAL_RECIPIENT_NUMBER
        
        if not isinstance(message, str):
            message = str(message)
        
        payload = {
            "message": message,
            "number": SIGNAL_SEND_NUMBER,
            "recipients": [recipient_number]
        }
        
        verify_ssl = SIGNAL_VERIFY_SSL if SIGNAL_ACTUAL_PROTOCOL == "https" else False
        
        async with httpx.AsyncClient(timeout=10.0, verify=verify_ssl) as client:
            response = await client.post(
                SIGNAL_API_URL,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            print(f"✅ [Signal] Nachricht gesendet an {recipient_number}")
            print(f"   → Nachricht: {message[:100]}")
            return True
    except Exception as e:
        print(f"❌ [Signal] Fehler beim Senden: {e}")
        return False

async def safe_send_to_iot(iot_websocket, header, message):
    """
    Sendet Nachricht an IoT mit Error-Handling
    """
    try:
        await iot_websocket.send(json.dumps(header))
        await iot_websocket.send(message)
        return True
    except websockets.exceptions.ConnectionClosed:
        print("⚠️  [Signal] IoT-Verbindung geschlossen, Nachricht verworfen")
        return False
    except Exception as e:
        print(f"⚠️  [Signal] Fehler beim Senden an IoT: {e}")
        return False

async def receive_signal_messages(iot_websocket, stop_event):
    """
    Empfängt Signal-Nachrichten über WebSocket mit Auto-Reconnect
    IoT-Verbindung bleibt stabil, auch wenn Signal disconnected!
    """
    reconnect_delay = SIGNAL_RECONNECT_DELAY
    
    while not stop_event.is_set():
        signal_websocket = None
        try:
            print("⏳ [Signal] Verbinde zu Signal WebSocket...")
            
            ssl_context = None
            if SIGNAL_ACTUAL_PROTOCOL == "https" and not SIGNAL_VERIFY_SSL:
                ssl_context = ssl.SSLContext()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
            
            async with websockets.connect(
                SIGNAL_WS_URL,
                ping_interval=None,
                close_timeout=10,
                ssl=ssl_context
            ) as signal_websocket:
                print("✅ [Signal] WebSocket verbunden!\n")
                
                # Reset reconnect delay bei erfolgreicher Verbindung
                reconnect_delay = SIGNAL_RECONNECT_DELAY
                
                async for message in signal_websocket:
                    if stop_event.is_set():
                        break
                        
                    try:
                        data = json.loads(message)
                        
                        envelope = data.get('envelope', {})
                        if 'typingMessage' in envelope:
                            continue
                        
                        if 'dataMessage' in envelope:
                            signal_message = envelope['dataMessage'].get('message', '')
                            source_number = envelope.get('sourceNumber', 'unknown')
                            source_name = envelope.get('sourceName', 'unknown')
                            
                            if signal_message:
                                print(f"📩 [Signal] Nachricht empfangen")
                                print(f"   → Von: {source_name} ({source_number})")
                                print(f"   → Nachricht: {signal_message}")
                                
                                session_id = f"signal_{DEVICE_NAME}_{int(datetime.now().timestamp() * 1000)}"
                                header = {
                                    "id": session_id,
                                    "type": "text",
                                    "sourceId": DEVICE_NAME,
                                    "timestamp": int(datetime.now().timestamp() * 1000),
                                    "final": True,
                                    "metadata": {
                                        "signalSource": source_number,
                                        "signalSourceName": source_name,
                                        "signalAccount": SIGNAL_RECEIVE_NUMBER
                                    }
                                }
                                
                                # Sende an IoT mit Error-Handling
                                if await safe_send_to_iot(iot_websocket, header, signal_message):
                                    print("✅ [Signal] An IoT Orchestrator weitergeleitet\n")
                        
                    except json.JSONDecodeError:
                        pass
                    except Exception as e:
                        print(f"❌ [Signal] Fehler beim Verarbeiten: {e}")
                        import traceback
                        traceback.print_exc()
                        
        except websockets.exceptions.WebSocketException as e:
            print(f"❌ [Signal] WebSocket-Fehler: {e}")
        except Exception as e:
            print(f"❌ [Signal] Verbindungsfehler: {e}")
        
        # Reconnect nur wenn nicht gestoppt
        if not stop_event.is_set():
            print(f"🔌 [Signal] Reconnect in {reconnect_delay} Sekunden...")
            await asyncio.sleep(reconnect_delay)
            # Exponentielles Backoff (max 60s)
            reconnect_delay = min(reconnect_delay * 1.5, 60)
        else:
            break
    
    print("👋 [Signal] Signal-Listener beendet")

async def receive_iot_messages(iot_websocket):
    """
    Empfängt TXT Output-Nachrichten vom IoT Orchestrator und sendet sie über Signal
    """
    last_uso_header = None
    session_buffer = {}
    
    try:
        async for message in iot_websocket:
            if isinstance(message, (bytes, bytearray)):
                if last_uso_header and last_uso_header.get('type') == 'text':
                    payload = message.decode('utf-8')
                    is_final = last_uso_header.get('final', True)
                    session_id = last_uso_header.get('id', 'unknown')
                    
                    if not is_final:
                        if session_id not in session_buffer:
                            session_buffer[session_id] = {'chunks': [], 'chunk_count': 0}
                            print("\n📝 [IoT] TXT Output gestartet")
                        
                        session = session_buffer[session_id]
                        session['chunks'].append(payload)
                        session['chunk_count'] += 1
                    else:
                        if session_id in session_buffer:
                            session = session_buffer[session_id]
                            full_text = ''.join(session['chunks']) + payload
                            
                            print(f"\n✅ [IoT] TXT Output abgeschlossen!")
                            print(f"   • Chunks: {session['chunk_count']}")
                            print(f"   • Länge: {len(full_text)} Zeichen")
                            
                            await send_signal_message(full_text)
                            del session_buffer[session_id]
                        else:
                            print(f"\n📝 [IoT] TXT Output: {payload}")
                            await send_signal_message(payload)
                    
                    if is_final:
                        last_uso_header = None
                        
            elif isinstance(message, str):
                try:
                    data = json.loads(message)
                    
                    if data.get('type') == 'welcome' or 'connectionId' in data:
                        pass
                    elif 'id' in data and 'type' in data:
                        last_uso_header = data
                        
                except json.JSONDecodeError:
                    if last_uso_header and last_uso_header.get('type') == 'text':
                        payload = message
                        is_final = last_uso_header.get('final', True)
                        session_id = last_uso_header.get('id', 'unknown')
                        
                        if not is_final:
                            if session_id not in session_buffer:
                                session_buffer[session_id] = {'chunks': [], 'chunk_count': 0}
                                print("\n📝 [IoT] TXT Output gestartet")
                            
                            session = session_buffer[session_id]
                            session['chunks'].append(payload)
                            session['chunk_count'] += 1
                        else:
                            if session_id in session_buffer:
                                session = session_buffer[session_id]
                                full_text = ''.join(session['chunks']) + payload
                                
                                print(f"\n✅ [IoT] TXT Output abgeschlossen!")
                                print(f"   • Chunks: {session['chunk_count']}")
                                print(f"   • Länge: {len(full_text)} Zeichen")
                                
                                await send_signal_message(full_text)
                                del session_buffer[session_id]
                            else:
                                print(f"\n📝 [IoT] TXT Output: {payload}")
                                await send_signal_message(payload)
                        
                        if is_final:
                            last_uso_header = None
                        
    except websockets.exceptions.ConnectionClosed:
        print("❌ [IoT] WebSocket-Verbindung geschlossen")
        raise  # Propagiere den Fehler, damit IoT reconnected
    except Exception as e:
        print(f"❌ [IoT] Fehler beim Empfangen: {e}")
        raise

def register_device_sync():
    """
    Registriert das Device über die REST API (synchron)
    """
    import urllib.request
    import urllib.error
    
    try:
        url = f'http://{WS_HOST}:3000/api/devices'
        data = json.dumps({
            'clientId': DEVICE_NAME,
            'name': DEVICE_NAME,
            'capabilities': DEVICE_CAPABILITIES,
            'metadata': {
                'type': 'signal-client',
                'platform': sys.platform,
                'signalReceiveNumber': SIGNAL_RECEIVE_NUMBER,
                'signalSendNumber': SIGNAL_SEND_NUMBER,
                'stableMode': True
            }
        }).encode('utf-8')
        
        req = urllib.request.Request(
            url,
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status in (200, 201):
                print("✅ [IoT] Device registriert")
            return True
    except Exception:
        return True

async def register_device():
    """
    Wrapper für synchrone Registrierung
    """
    import concurrent.futures
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        await loop.run_in_executor(executor, register_device_sync)

async def signal_device_client():
    """
    Hauptfunktion: Verbindet Signal und IoT Orchestrator
    Signal hat eigenen Reconnect-Loop, IoT bleibt stabil
    """
    print_header()
    await register_device()

    reconnect_delay = IOT_RECONNECT_DELAY
    
    # UNENDLICHE IoT RECONNECT-SCHLEIFE
    while True:
        signal_task = None
        stop_event = asyncio.Event()
        
        try:
            print("⏳ [IoT] Verbinde zu IoT Orchestrator...")
            
            async with websockets.connect(
                IOT_WS_URL,
                ping_interval=None,
                close_timeout=10
            ) as iot_websocket:
                print("✅ [IoT] Verbindung hergestellt!\n")
                
                # Warte auf Willkommensnachricht
                try:
                    welcome_msg = await asyncio.wait_for(iot_websocket.recv(), timeout=5)
                    if isinstance(welcome_msg, str):
                        welcome_data = json.loads(welcome_msg)
                        connection_id = welcome_data.get('connectionId', 'unknown')
                        print(f"✅ [IoT] Connection ID: {connection_id}")
                except asyncio.TimeoutError:
                    print("⚠️  [IoT] Keine Willkommensnachricht")

                print("\n" + "="*70)
                print("✅ Device verbunden und bereit")
                print(f"💡 Device '{DEVICE_NAME}' verfügbar in TXT Input/Output Nodes")
                print(f"🔄 Signal läuft unabhängig mit Auto-Reconnect")
                print("="*70 + "\n")

                # Reset reconnect delay bei erfolgreicher Verbindung
                reconnect_delay = IOT_RECONNECT_DELAY

                # Starte beide Tasks - Signal mit eigenem Reconnect
                signal_task = asyncio.create_task(
                    receive_signal_messages(iot_websocket, stop_event)
                )
                iot_task = asyncio.create_task(receive_iot_messages(iot_websocket))

                # Warte NUR auf IoT-Task - Signal läuft unabhängig
                try:
                    await iot_task
                except Exception as e:
                    print(f"❌ [IoT] IoT-Task Fehler: {e}")
                
                print("❌ [IoT] IoT-Verbindung verloren")

        except websockets.exceptions.InvalidStatusCode as e:
            print(f"❌ [IoT] Verbindung fehlgeschlagen! Status: {e.status_code}")
            print("💡 Überprüfe API-Key und Backend-Status")
            
        except ConnectionRefusedError:
            print("❌ [IoT] Verbindung abgelehnt! Server läuft nicht?")
            
        except KeyboardInterrupt:
            print("\n👋 Beende Signal Device-Client...")
            stop_event.set()
            if signal_task:
                signal_task.cancel()
                try:
                    await signal_task
                except asyncio.CancelledError:
                    pass
            break
            
        except Exception as e:
            print(f"❌ [IoT] Fehler: {e}")

        finally:
            # Stoppe Signal-Task wenn noch aktiv
            stop_event.set()
            if signal_task and not signal_task.done():
                signal_task.cancel()
                try:
                    await signal_task
                except asyncio.CancelledError:
                    pass

        # AUTOMATISCHER IoT RECONNECT
        print(f"🔌 [IoT] Reconnect in {reconnect_delay} Sekunden...\n")
        await asyncio.sleep(reconnect_delay)
        # Exponentielles Backoff (max 60s)
        reconnect_delay = min(reconnect_delay * 1.5, 60)

    print("\n✅ Signal Device-Client beendet.\n")

def main():
    """Entry Point"""
    try:
        if sys.version_info < (3, 7):
            print("❌ Python 3.7 oder höher erforderlich!")
            sys.exit(1)

        asyncio.run(signal_device_client())

    except KeyboardInterrupt:
        print("\n⚠️  Abgebrochen.\n")

if __name__ == "__main__":
    main()