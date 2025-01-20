import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import serial
import sqlite3
from datetime import datetime
from flask import Flask, render_template
import threading

# =====================================================
# 1. AI model learning 
# =====================================================
def train_model():
    # Generate virtual data (training data)
    data = np.random.normal(loc=25, scale=5, size=(1000, 2))  # Average temperature 25°C, 5% humidity variation

    # Model Training
    model = IsolationForest(contamination=0.1)
    model.fit(data)

    # Save model
    joblib.dump(model, "anomaly_detection_model.pkl")
    print("Model trained and saved!")

# =====================================================
#2. Arduino data collection and storage functions
# =====================================================
def collect_sensor_data():
    #Arduino Serial Port Settings
    arduino_port = "COM9"  # Windows는 COM port (ex: "COM3")
    baud_rate = 9600
    ser = serial.Serial(arduino_port, baud_rate)

    # SQLite datebase connection 
    db_name = "sensor_data.db"
    conn = sqlite3.connect(db_name, check_same_thread=False)
    cursor = conn.cursor()

    # Create table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        temperature REAL,
        humidity REAL
    )
    """)
    conn.commit()

    try:
        while True:
            line = ser.readline().decode('utf-8').strip()  # Reading serial data
            print("Received:", line)

            if "TEMP" in line and "HUMIDTY" in line:
                # Parsing data
                parts = line.split(", ")
                temperature = float(parts[0].split(": ")[1])
                humidity = float(parts[1].split(": ")[1].replace("%", ""))

                # Save to database
                cursor.execute("INSERT INTO sensor_data (temperature, humidity) VALUES (?, ?)", (temperature, humidity))
                conn.commit()
                print(f"Data saved: Temperature={temperature}, Humidity={humidity}")
    except KeyboardInterrupt:
        print("End of data collection")
    finally:
        conn.close()
        ser.close()

# =====================================================
# 3. Flask Web Application
# =====================================================
app = Flask(__name__)

def get_data():
    conn = sqlite3.connect("sensor_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, temperature, humidity FROM sensor_data ORDER BY timestamp DESC LIMIT 20")
    data = cursor.fetchall()
    conn.close()
    return data

@app.route("/")
def index():
    data = get_data()
    return render_template("index.html", data=data)

# =====================================================
# 4. Integrated execution
# =====================================================
if __name__ == "__main__":
    print("1. AI model training")
    train_model()

    # Run data collection in a separate thread
    print("2. Start collecting sensor data")
    data_thread = threading.Thread(target=collect_sensor_data)
    data_thread.daemon = True
    data_thread.start()

    # 3. Running the Flask web application
    print("3. Running the Flask web application")
    app.run(debug=True)