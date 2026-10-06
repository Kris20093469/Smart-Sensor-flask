from flask import Flask
import sqlite3;
from flask import request
from flask import url_for, render_template, jsonify, g

# 1. Initialize the Flask application
app = Flask(__name__)
latest_sensor_data = {
    "doorState": "unknown",
    "motion": "unknown"
}


# 2. Define a route (URL path) and a function to handle it
@app.route('/')
def home():
    return render_template('home.html')

@app.post('/api/sensor')
def recieve_sensor():
    global latest_sensor_data
    data = request.get_json()
    doorstate = data["doorState"]
    motion = data["motion"]
    latest_sensor_data = data
    
    return jsonify({
        "status": "ok"
    })

@app.get('/api/sensor')
def get_sensor():
    return jsonify(latest_sensor_data)

@app.route('/index/')
def index():
    print("sending to web:", latest_sensor_data)
    return render_template('index.html',
        sensor=latest_sensor_data  )


# 3. Start the local development server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
