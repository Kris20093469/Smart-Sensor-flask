from flask import Flask
import sqlite3;
from flask import request
from flask import url_for, render_template, jsonify


app = Flask(__name__)
latest_sensor_data = {
    "doorState": "unknown",
    "motion": "unknown"
}

with sqlite3.connect("sensor.db") as conn:
            conn.execute("""
        CREATE TABLE IF NOT EXISTS sensor_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        doorState TEXT,
        motion TEXT
        )
        """)
            


@app.post('/api/sensor')
def recieve_sensor():
    
    
    data = request.get_json()

    with sqlite3.connect("sensor.db") as conn:
        conn.row_factory = sqlite3.Row

        latest = conn.execute(""" 
            SELECT doorState, motion, timestamp
                              FROM sensor_logs
                              ORDER BY id DESC
                              LIMIT 1
                              
        """).fetchone()
        if latest is None or(
             data["doorState"] != latest["doorState"] or data["motion"] != latest["motion"]
        ):
            conn.execute("""INSERT INTO sensor_logs (doorState, motion) 
                         VALUES (?, ?)
                       
                         """, (data["doorState"], data["motion"])) 

    
    return jsonify({
        "status": "ok"
    })

@app.get('/api/sensor')
def get_sensor():
    page = request.args.get("page", 1, type=int)
    per_page = 15
    offset = (page - 1) * per_page

    with sqlite3.connect("sensor.db") as conn:
        conn.row_factory = sqlite3.Row

        rows = conn.execute("""
            SELECT id, timestamp, doorState, motion
            FROM sensor_logs
            ORDER BY id DESC
            LIMIT ? OFFSET ?
        """, (per_page, offset)).fetchall()

        logs = [dict(row) for row in rows]

        total = conn.execute(
            "SELECT COUNT(*) FROM sensor_logs"
        ).fetchone()[0]

    return jsonify({
        "logs": logs,
        "page": page,
        "totalPages": (total + per_page - 1) // per_page
    })
          
    

@app.route('/')
def index():
    
    return render_template('index.html',
        sensor=latest_sensor_data  )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
