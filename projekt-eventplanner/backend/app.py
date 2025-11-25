from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for, abort
from flask_cors import CORS
import sqlite3
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
DB_PATH = os.path.join(os.path.dirname(__file__), 'events.db')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# SQLite Setup
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    date TEXT NOT NULL,
    description TEXT,
    max_participants INTEGER,
    cover_path TEXT,
    banner_path TEXT,
    time TEXT,
    dresscode TEXT,
    address TEXT,
    price TEXT,
    discount_info TEXT,
    current_participants INTEGER DEFAULT 0,
    min_age INTEGER DEFAULT 0
)''')

c.execute('''CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    participants_count INTEGER NOT NULL,
    FOREIGN KEY(event_id) REFERENCES events(id)
)''')

# Migration: Add new columns if they don't exist (for existing databases)
try:
    c.execute('ALTER TABLE events ADD COLUMN time TEXT')
except sqlite3.OperationalError:
    pass
try:
    c.execute('ALTER TABLE events ADD COLUMN dresscode TEXT')
except sqlite3.OperationalError:
    pass
try:
    c.execute('ALTER TABLE events ADD COLUMN address TEXT')
except sqlite3.OperationalError:
    pass
try:
    c.execute('ALTER TABLE events ADD COLUMN price TEXT')
except sqlite3.OperationalError:
    pass
try:
    c.execute('ALTER TABLE events ADD COLUMN discount_info TEXT')
except sqlite3.OperationalError:
    pass
try:
    c.execute('ALTER TABLE events ADD COLUMN current_participants INTEGER DEFAULT 0')
except sqlite3.OperationalError:
    pass
try:
    c.execute('ALTER TABLE events ADD COLUMN min_age INTEGER DEFAULT 0')
except sqlite3.OperationalError:
    pass

conn.commit()
conn.close()

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/impressum')
def impressum():
    return render_template('impressum.html')

@app.route('/events')
def events():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM events')
    rows = c.fetchall()
    conn.close()
    events = []
    for row in rows:
        events.append({
            'id': row[0],
            'title': row[1],
            'date': row[2],
            'description': row[3],
            'max_participants': row[4],
            'cover_url': url_for('uploaded_file', filename=os.path.basename(row[5])) if row[5] else '',
            'banner_url': url_for('uploaded_file', filename=os.path.basename(row[6])) if row[6] else ''
        })
    return render_template('events.html', events=events)

@app.route('/create', methods=['GET', 'POST'])
def create_event_page():
    if request.method == 'POST':
        title = request.form.get('title')
        date = request.form.get('date')
        description = request.form.get('description')
        max_participants = request.form.get('maxParticipants')
        
        # New fields
        time = request.form.get('time')
        dresscode = request.form.get('dresscode')
        address = request.form.get('address')
        price = request.form.get('price')
        discount_info = request.form.get('discount_info')
        min_age = request.form.get('min_age', 0)

        cover = request.files.get('cover')
        banner = request.files.get('banner')
        cover_path = ''
        banner_path = ''
        if cover:
            filename = secure_filename(cover.filename)
            cover.save(os.path.join(UPLOAD_FOLDER, filename))
            cover_path = os.path.join(UPLOAD_FOLDER, filename)
        if banner:
            filename = secure_filename(banner.filename)
            banner.save(os.path.join(UPLOAD_FOLDER, filename))
            banner_path = os.path.join(UPLOAD_FOLDER, filename)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''INSERT INTO events (title, date, description, max_participants, cover_path, banner_path, time, dresscode, address, price, discount_info, min_age) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (title, date, description, max_participants, cover_path, banner_path, time, dresscode, address, price, discount_info, min_age))
        conn.commit()
        conn.close()
        return redirect(url_for('events'))
    return render_template('create.html')

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM events WHERE id = ?', (event_id,))
    row = c.fetchone()
    
    if not row:
        conn.close()
        abort(404)
    
    # Fetch reservations
    c.execute('SELECT name, participants_count FROM reservations WHERE event_id = ?', (event_id,))
    reservations = [{'name': r[0], 'count': r[1]} for r in c.fetchall()]
    
    conn.close()
    
    # row indices: 0=id, 1=title, 2=date, 3=desc, 4=max, 5=cover, 6=banner, 
    # 7=time, 8=dresscode, 9=address, 10=price, 11=discount_info
    
    event = {
        'id': row[0],
        'title': row[1],
        'date': row[2],
        'description': row[3],
        'max_participants': row[4],
        'cover_url': url_for('uploaded_file', filename=os.path.basename(row[5])) if row[5] else '',
        'banner_url': url_for('uploaded_file', filename=os.path.basename(row[6])) if row[6] else '',
        'time': row[7] if len(row) > 7 else '',
        'dresscode': row[8] if len(row) > 8 else '',
        'address': row[9] if len(row) > 9 else '',
        'price': row[10] if len(row) > 10 else '',
        'discount_info': json.loads(row[11]) if (len(row) > 11 and row[11]) else [],
        'current_participants': row[12] if len(row) > 12 else 0,
        'min_age': row[13] if len(row) > 13 else 0,
        'reservations': reservations
    }
    return render_template('event_detail.html', event=event)

@app.route('/event/<int:event_id>/reserve', methods=['POST'])
def reserve_event(event_id):
    participants = int(request.form.get('participants', 0))
    name = request.form.get('name')
    birthdate_str = request.form.get('birthdate')
    
    if not name:
        return jsonify({'error': "Name ist erforderlich!"}), 400
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Check availability and age
    c.execute('SELECT max_participants, current_participants, min_age FROM events WHERE id = ?', (event_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return jsonify({'error': "Event nicht gefunden"}), 404
        
    max_p = row[0]
    current_p = row[1] if row[1] else 0
    min_age = row[2] if row[2] else 0
    
    # Age Check
    if min_age > 0:
        if not birthdate_str:
            conn.close()
            return jsonify({'error': "Geburtsdatum ist erforderlich für die Altersprüfung!"}), 400
        try:
            birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d')
            today = datetime.today()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            if age < min_age:
                conn.close()
                return jsonify({'error': f"Du bist leider zu jung für dieses Event. Mindestalter: {min_age} Jahre."}), 400
        except ValueError:
            conn.close()
            return jsonify({'error': "Ungültiges Geburtsdatum!"}), 400

    if current_p + participants > max_p:
        conn.close()
        return jsonify({'error': "Nicht genügend Plätze verfügbar!"}), 400
        
    # Update participants
    new_total = current_p + participants
    c.execute('UPDATE events SET current_participants = ? WHERE id = ?', (new_total, event_id))
    
    # Add reservation
    c.execute('INSERT INTO reservations (event_id, name, participants_count) VALUES (?, ?, ?)', (event_id, name, participants))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/events', methods=['GET'])
def get_events():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM events')
    rows = c.fetchall()
    conn.close()
    events = []
    for row in rows:
        events.append({
            'id': row[0],
            'title': row[1],
            'date': row[2],
            'description': row[3],
            'max_participants': row[4],
            'cover_url': f'/uploads/{os.path.basename(row[5])}' if row[5] else '',
            'banner_url': f'/uploads/{os.path.basename(row[6])}' if row[6] else ''
        })
    return jsonify(events)

@app.route('/api/events', methods=['POST'])
def create_event():
    title = request.form.get('title')
    date = request.form.get('date')
    description = request.form.get('description')
    max_participants = request.form.get('maxParticipants')
    cover = request.files.get('cover')
    banner = request.files.get('banner')
    cover_path = ''
    banner_path = ''
    if cover:
        filename = secure_filename(cover.filename)
        cover.save(os.path.join(UPLOAD_FOLDER, filename))
        cover_path = os.path.join(UPLOAD_FOLDER, filename)
    if banner:
        filename = secure_filename(banner.filename)
        banner.save(os.path.join(UPLOAD_FOLDER, filename))
        banner_path = os.path.join(UPLOAD_FOLDER, filename)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO events (title, date, description, max_participants, cover_path, banner_path) VALUES (?, ?, ?, ?, ?, ?)''',
              (title, date, description, max_participants, cover_path, banner_path))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
