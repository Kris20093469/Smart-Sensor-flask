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
            
@app.route('/')
def home():
    return render_template('home.html')



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
        print("Arduino sent:", data)
        print("Database latest:", dict(latest) if latest else None)
    
        if latest is None or(
             data["doorState"] != latest["doorState"] or data["motion"] != latest["motion"]
        ):
            print("STATE CHANGED - INSERTING")
            conn.execute("""INSERT INTO sensor_logs (doorState, motion) 
                         VALUES (?, ?)
                       
                         """, (data["doorState"], data["motion"]))
            print("NEW ROW ID:", conn.execute(
    "SELECT last_insert_rowid()"
).fetchone()[0])
        else:
            print("NO CHANGE - NOT INSERTING")    

    
    return jsonify({
        "status": "ok"
    })

@app.get('/api/sensor')
def get_sensor():
     with sqlite3.connect("sensor.db") as conn:
          conn.row_factory = sqlite3.Row
          rows = conn.execute(""" 
            SELECT id, timestamp, doorState, motion
                            FROM sensor_logs
                            ORDER BY id DESC 

        """)
          logs = [dict(row) for row in rows]
          return jsonify(logs)
          
    

@app.route('/index/')
def index():
    
    return render_template('index.html',
        sensor=latest_sensor_data  )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
