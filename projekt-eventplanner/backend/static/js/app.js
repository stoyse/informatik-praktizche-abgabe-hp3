/**
 * EventPlanner Logic
 * Handles LocalStorage, Event Creation, and Registration
 */

class EventManager {
    constructor() {
        this.events = JSON.parse(localStorage.getItem('events')) || [];
    }

    // Event erstellen
    addEvent(title, date, description, maxParticipants, coverImg, bannerImg) {
        const newEvent = {
            id: Date.now().toString(), // Simple ID generation
            title,
            date,
            description,
            maxParticipants: parseInt(maxParticipants),
            currentParticipants: 0,
            attendees: [], // Could store names here
            coverImg: coverImg || '',
            bannerImg: bannerImg || ''
        };

        this.events.push(newEvent);
        this.save();
        return newEvent;
    }

    // Teilnehmer registrieren
    joinEvent(eventId, userName) {
        const event = this.events.find(e => e.id === eventId);
        
        if (!event) return { success: false, msg: "Event nicht gefunden" };
        if (event.currentParticipants >= event.maxParticipants) {
            return { success: false, msg: "Event ist voll!" };
        }

        event.currentParticipants++;
        event.attendees.push(userName || "Anonym");
        this.save();
        return { success: true, msg: "Erfolgreich angemeldet!" };
    }

    // Speichern in LocalStorage
    save() {
        localStorage.setItem('events', JSON.stringify(this.events));
    }

    // Alle Events holen
    getAllEvents() {
        // Sortieren nach Datum
        return this.events.sort((a, b) => new Date(a.date) - new Date(b.date));
    }
}

// Instanz erstellen
const manager = new EventManager();

// UI Funktionen
document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    
    // Check if we are on index.html (Dashboard)
    if (path.includes('index.html') || path.endsWith('/')) {
        renderDashboard();
    }

    // Check if we are on create.html
    if (path.includes('create.html')) {
        setupCreateForm();
    }
});

function renderDashboard() {
    const grid = document.getElementById('eventGrid');
    if (!grid) return;

    const events = manager.getAllEvents();
    grid.innerHTML = '';

    if (events.length === 0) {
        grid.innerHTML = `
            <div class="empty-state" style="grid-column: 1/-1;">
                <span class="empty-icon">📅</span>
                <h3>Keine Events geplant</h3>
                <p>Erstelle jetzt dein erstes Event!</p>
                <br>
                <a href="create.html" class="btn btn-primary">Event erstellen</a>
            </div>
        `;
        return;
    }

    events.forEach(event => {
        const percentage = Math.min(100, (event.currentParticipants / event.maxParticipants) * 100);
        const isFull = event.currentParticipants >= event.maxParticipants;

        const card = document.createElement('div');
        card.className = 'event-card';
        card.innerHTML = `
            ${event.bannerImg ? `<img src="${event.bannerImg}" alt="Banner" style="width:100%;height:80px;object-fit:cover;border-radius:8px 8px 0 0;margin-bottom:10px;">` : ''}
            <div style="display:flex;align-items:center;gap:1rem;">
                ${event.coverImg ? `<img src="${event.coverImg}" alt="Cover" style="width:60px;height:60px;object-fit:cover;border-radius:50%;box-shadow:0 2px 8px #ccc;">` : ''}
                <div>
                    <div class="event-date">${new Date(event.date).toLocaleDateString('de-DE')}</div>
                    <h3 class="event-title">${event.title}</h3>
                </div>
            </div>
            <p class="event-desc">${event.description}</p>
            <div class="capacity-info">
                <span>Teilnehmer: ${event.currentParticipants} / ${event.maxParticipants}</span>
                <span>${Math.round(percentage)}%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${percentage}%; background-color: ${isFull ? '#ff7675' : '#00b894'}"></div>
            </div>
            <button onclick="handleJoin('${event.id}')" class="btn ${isFull ? 'btn-secondary' : 'btn-primary'}" ${isFull ? 'disabled' : ''}>
                ${isFull ? 'Ausgebucht' : 'Jetzt anmelden'}
            </button>
        `;
        grid.appendChild(card);
    });
}

function setupCreateForm() {
    const form = document.getElementById('createEventForm');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = document.getElementById('title').value;
        const date = document.getElementById('date').value;
        const desc = document.getElementById('description').value;
        const max = document.getElementById('maxParticipants').value;
        const coverInput = document.getElementById('cover');
        const bannerInput = document.getElementById('banner');

        // Hilfsfunktion für File zu Base64
        function fileToBase64(file) {
            return new Promise((resolve, reject) => {
                if (!file) return resolve('');
                const reader = new FileReader();
                reader.onload = () => resolve(reader.result);
                reader.onerror = reject;
                reader.readAsDataURL(file);
            });
        }

        const coverImg = coverInput.files[0] ? await fileToBase64(coverInput.files[0]) : '';
        const bannerImg = bannerInput.files[0] ? await fileToBase64(bannerInput.files[0]) : '';

        if (title && date && max) {
            manager.addEvent(title, date, desc, max, coverImg, bannerImg);
            window.location.href = 'index.html';
        }
    });
}

// Global function for button click
window.handleJoin = function(eventId) {
    const name = prompt("Dein Name für die Anmeldung:");
    if (name) {
        const result = manager.joinEvent(eventId, name);
        alert(result.msg);
        if (result.success) {
            renderDashboard(); // Refresh UI
        }
    }
};
