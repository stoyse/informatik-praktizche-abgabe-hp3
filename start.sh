#!/bin/bash

# Pfad zum Projektordner
PROJECT_DIR="projekt-eventplanner"

# Prüfen, ob der Projektordner existiert
if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ Fehler: Ordner '$PROJECT_DIR' nicht gefunden."
    echo "Bitte stelle sicher, dass du das Skript im Hauptverzeichnis ausführst."
    exit 1
fi

echo "🚀 Starte StickerVerse App..."

# Funktion zum Öffnen des Browsers (OS-unabhängig)
open_browser() {
    local url="$1"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "$url"
    elif command -v xdg-open &> /dev/null; then
        xdg-open "$url"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]]; then
        start "$url"
    else
        echo "Bitte öffne $url manuell."
    fi
}

# Versuche, einen lokalen Server mit Python zu starten (empfohlen)
if command -v python3 &> /dev/null; then
    echo "🌐 Starte lokalen Webserver..."
    echo "👉 Die App läuft unter: http://localhost:8000"
    echo "Drücke STRG+C um den Server zu stoppen."
    
    # Browser öffnen (im Hintergrund, damit der Server starten kann)
    (sleep 1 && open_browser "http://localhost:8000") &
    
    # Server starten
    cd "$PROJECT_DIR" && python3 -m http.server
else
    # Fallback: Datei direkt öffnen (file:// Protokoll)
    echo "⚠️ Python3 nicht gefunden. Öffne index.html direkt..."
    open_browser "$PROJECT_DIR/index.html"
fi
