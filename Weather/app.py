from flask import Flask, jsonify, render_template
import requests
import psycopg2
from datetime import datetime
import threading
import serial
import time
from psycopg2 import pool
import logging
import os
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

app = Flask(__name__, 
    template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'),
    static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'))

# OpenWeatherMap API Information
API_KEY = "f761d06ee6470da39cb6d1070febf362"
CITY = "Vientiane"
WEATHER_URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# connection pool set up
db_pool = psycopg2.pool.SimpleConnectionPool(
    1, 20,
    dbname="postgres",
    user="postgres",
    password="1212",
    host="localhost",
    port="5432"
)

def get_connection():
    try:
        conn = db_pool.getconn()
        return conn
    except Exception as e:
        print(f"Error getting connection from pool: {e}")
        return None

def release_connection(conn):
    try:
        db_pool.putconn(conn)
    except Exception as e:
        print(f"Error releasing connection back to pool: {e}")

# serial port setting
SERIAL_PORT = "COM9"  # mac 포트 예시
BAUD_RATE = 9600

# Glabal variable
serial_conn = None
latest_weather = None

# PostgreSQL Create table function
def create_table_if_not_exists():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS weather_data (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP NOT NULL,
        temperature NUMERIC NOT NULL,
        humidity NUMERIC NOT NULL
    );
    """
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(create_table_query)
            conn.commit()
            cur.close()
            logging.info("The table was created successfully or already exists.")
        except Exception as e:
            logging.error(f"Table creation error: {e}")
        finally:
            release_connection(conn)
    else:
        logging.error("Failed to get database connection.")

# PostgreSQL Data storage function
def save_to_db(temp, humidity):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO weather_data (timestamp, temperature, humidity) VALUES (%s, %s, %s)",
                (datetime.now(), temp, humidity)
            )
            conn.commit()
            cur.close()
            logging.info(f"Data saved to DB: Temperature={temp}, Humidity={humidity}")
        except Exception as e:
            logging.error(f"Database Error: {e}")
        finally:
            release_connection(conn)

# OpenWeatherMap Get weather data from API
def fetch_weather_data():
    global latest_weather
    try:
        response = requests.get(WEATHER_URL)
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            latest_weather = {'temp': temp, 'humidity': humidity}
            save_to_db(temp, humidity)
            print(f"Fetched weather data: {latest_weather}")
            return latest_weather
        else:
            print(f"Error fetching weather data: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception fetching weather data: {e}")
        return None

# Retrieving historical data from PostgreSQL
def get_historical_data():
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT timestamp, temperature, humidity FROM weather_data ORDER BY timestamp DESC LIMIT 50")
            rows = cur.fetchall()
            cur.close()
            logging.info(f"Fetched {len(rows)} rows from DB.")
            return rows
        except Exception as e:
            logging.error(f"Error fetching historical data: {e}")
            return []
        finally:
            release_connection(conn)
    return []
def send_weather_to_arduino():
    global serial_conn, latest_weather
    while True:
        if serial_conn and latest_weather:
            try:
                data = f"{latest_weather['temp']},{latest_weather['humidity']}\n"
                serial_conn.write(data.encode('utf-8'))
                print(f"Sent to Arduino: {data}")
            except Exception as e:
                print(f"Error in serial communication: {e}")
        else:
            if not serial_conn:
                print("Serial connection is not established.")
            if not latest_weather:
                print("No latest_weather data available.")
        time.sleep(10)  # Set to an appropriate cycle

# Flask Route: Returning the latest weather data
@app.route('/weather', methods=['GET'])
def get_weather():
    global latest_weather
    if latest_weather:
        #Returns current weather and recent records together
        recent_data = get_recent_weather_data()
        return jsonify({
            'current': latest_weather,
            'recent': recent_data
        })
    else:
        return jsonify({'error': 'No weather data available'})

def get_recent_weather_data():
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT timestamp, temperature, humidity 
                FROM weather_data 
                ORDER BY timestamp DESC 
                LIMIT 5
            """)
            rows = cur.fetchall()
            cur.close()
            return [
                {
                    'timestamp': row[0].strftime('%Y-%m-%d %H:%M:%S'),
                    'temp': row[1],
                    'humidity': row[2]
                } for row in rows
            ]
        except Exception as e:
            print(f"Error fetching recent weather data: {e}")
            return []
        finally:
            release_connection(conn)
    return []

# Flask Routes: Rendering a Web Dashboard
@app.route('/')
@app.route('/dashboard')
def dashboard():
    global latest_weather
    if not latest_weather:
        latest_weather = fetch_weather_data()
    recent_data = get_recent_weather_data()
    return render_template('index.html', latest=latest_weather, recent_data=recent_data)

if __name__ == '__main__':
    # Create table
    create_table_if_not_exists()
    
    # Serial port connection
    try:
        serial_conn = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Waiting for serial initialization
        print("Serial connection established.")
    except Exception as e:
        print(f"Error connecting to serial port: {e}")
        serial_conn = None

    # Start a thread that periodically updates weather data
    def update_weather():
        while True:
            logging.info("Attempting to update weather data...")
            weather = fetch_weather_data()
            if weather:
                logging.info(f"Updated weather data: {weather}")
            else:
                logging.warning("Failed to update weather data.")
            time.sleep(300)  # Example: Update every 5 minutes

    weather_thread = threading.Thread(target=update_weather, daemon=True)
    weather_thread.start()  # Start thread
    print("Weather update thread started.")  # Add log

    # Start a thread to send serial data
    serial_thread = threading.Thread(target=send_weather_to_arduino, daemon=True)
    serial_thread.start()  # Start thread
    print("Serial communication thread started.")  # Add log

    # Starting the Flask server
    app.run(host='0.0.0.0', port=5500, debug=True)