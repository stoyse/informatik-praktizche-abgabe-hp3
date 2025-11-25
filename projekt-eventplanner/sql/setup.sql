-- SQL Schema für EventPlanner
-- Dieses Skript dient zur Dokumentation der Datenbankstruktur

-- 1. Tabelle für Events
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    event_date DATE NOT NULL,
    description TEXT,
    max_participants INTEGER DEFAULT 10,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabelle für Anmeldungen (Registrations)
CREATE TABLE registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER,
    user_name TEXT NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id)
);

-- Beispiel-Daten einfügen
INSERT INTO events (title, event_date, description, max_participants) 
VALUES ('Sommerfest 2025', '2025-07-15', 'Grillen und Chillen im Park', 50);

INSERT INTO events (title, event_date, description, max_participants) 
VALUES ('Coding Workshop', '2025-11-20', 'Lerne Python an einem Tag', 15);

-- Beispiel-Abfrage: Wie viele Leute sind angemeldet?
SELECT e.title, COUNT(r.id) as teilnehmer_anzahl
FROM events e
LEFT JOIN registrations r ON e.id = r.event_id
GROUP BY e.id;
