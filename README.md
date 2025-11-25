# EventPlanner App (Python/Flask Version)

Eine voll funktionsfähige Web-Applikation zur Verwaltung und Buchung von Events, basierend auf Python (Flask) und SQLite.

## 🚀 Features

### Für Veranstalter
*   **Events erstellen:** Detaillierte Erfassung von Titel, Datum, Beschreibung, Bild-URL.
*   **Kapazitätsmanagement:** Festlegen einer maximalen Teilnehmerzahl.
*   **Altersbeschränkung:** Setzen eines Mindestalters für Events.
*   **Preisgestaltung:** Basispreis pro Ticket und Definition von Mengenrabatten (z.B. ab 5 Tickets 10% Rabatt).

### Für Teilnehmer
*   **Event-Übersicht:** Liste aller verfügbaren Veranstaltungen.
*   **Detailansicht:** Genaue Informationen zu jedem Event, inkl. aktueller Auslastung.
*   **Reservierungssystem:**
    *   Eingabe von Name und Geburtsdatum.
    *   **Automatische Altersprüfung:** Das System berechnet das Alter und blockiert die Buchung, wenn das Mindestalter nicht erreicht ist.
    *   **Live-Preisberechnung:** Der Gesamtpreis wird in Echtzeit aktualisiert, inklusive Rabattanzeige.
    *   **Feedback:** Sofortige Rückmeldung bei Erfolg oder Fehlern (z.B. "Event voll", "Zu jung") via Browser-Popup (AJAX), ohne die Seite neu zu laden.

### Weitere Seiten
*   **Über uns:** Informationen zum Team.
*   **Kontakt:** Kontaktmöglichkeiten.
*   **Impressum:** Rechtliche Hinweise.

## 🛠 Technologien

*   **Backend:** Python 3, Flask (Web Framework)
*   **Datenbank:** SQLite (lokale Datei `events.db`)
*   **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
*   **Kommunikation:** AJAX (Fetch API) für asynchrone Datenübertragung (JSON).

## 📦 Installation & Start

Voraussetzung: Python 3 ist installiert.

1.  **Terminal öffnen** und in den Projektordner navigieren:
    ```bash
    cd projekt-eventplanner
    ```

2.  **Abhängigkeiten installieren** (falls noch nicht geschehen):
    ```bash
    pip install flask
    ```

3.  **App starten:**
    ```bash
    python backend/app.py
    ```

4.  **Im Browser öffnen:**
    Gehe zu: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 📂 Projektstruktur

*   `backend/app.py`: Hauptdatei des Servers (Routen, Logik, Datenbank-Zugriff).
*   `backend/templates/`: HTML-Dateien (Jinja2 Templates).
*   `backend/static/`: Statische Dateien (CSS, JS, Bilder).
    *   `js/reservation.js`: Frontend-Logik für Preisberechnung und Reservierung.
*   `backend/events.db`: SQLite Datenbank (wird automatisch erstellt).
