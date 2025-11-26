from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# ------------------- Database -------------------

def init_db():
    conn = sqlite3.connect('donnees.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS mesures
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  temperature REAL,
                  humidite REAL,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

# ------------------- Receive 6 capteurs -------------------

@app.route('/send', methods=['POST'])
def recevoir_donnees():
    capteurs = request.get_json()   # List of 6 sensors

    conn = sqlite3.connect('donnees.db')
    c = conn.cursor()

    for cap in capteurs:
        c.execute("""
            INSERT INTO mesures (temperature, humidite)
            VALUES (?, ?)
        """, (cap["temperature"], cap["humidite"]))

    conn.commit()
    conn.close()

    print("✔ Saved 6 capteurs")
    return jsonify({"status": "OK"}), 200

# ------------------- Return last 6 capteurs -------------------

@app.route('/last6', methods=['GET'])
def last6():
    conn = sqlite3.connect('donnees.db')
    c = conn.cursor()
    c.execute("SELECT temperature, humidite, timestamp FROM mesures ORDER BY id DESC LIMIT 6")
    rows = c.fetchall()
    conn.close()

    capteurs = []
    for r in rows:
        capteurs.append({
            "temperature": r[0],
            "humidite": r[1],
            "timestamp": r[2]
        })

    return jsonify(capteurs)

# ------------------- Run Server -------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
