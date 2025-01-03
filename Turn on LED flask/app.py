from flask import Flask, render_template, request
import psycopg2
import serial, serial.tools.list_ports
import time

def find_arduino():
    ports = serial.tools.list_ports.comports()
    arduino_port = None

    for port in ports:
        if "Arduino" in port.description or "ttyUSB" in port.device or "ttyACM" in port.device:
            arduino_port = port.device
            break

    if arduino_port:
        print(f"Arduino found on port: {arduino_port}")
        return arduino_port
    else:
        print("Not found Arduino port")
        return None

DB_PARAMS = {
    "host":"localhost",         # Your localhost default ip: 127.0.0.1
    "database":"sensor_data",   # Your database name
    "user":"postgres",          # User for login to database
    "password":"1212"             # Your password for login
}

app = Flask(__name__)
arduino = serial.Serial(find_arduino(), 9600)
time.sleep(2) 

@app.route('/')
def index():
    return render_template('index.html')

def led(status):
    if status == True:
        arduino.write(b'1')
    else:
        arduino.write(b'0')

# Insert data into database via 'http://localhost/insertData' url
@app.route('/insertData', methods=['POST'])
def insertData():
    conn = psycopg2.connect(**DB_PARAMS)
    led_status = True if request.form.get('status','') == 'on' else False
    query = "INSERT INTO led_data (status) VALUES (%s)"
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (led_status,))
            conn.commit()
            if (arduino != None):
                led(led_status)
    except Exception as e:
        print(e)
    finally:
        conn.close()

    return 'Successful'

# View all datas in postgres database via 'http://localhost/viewDatas' url
@app.route('/viewDatas', methods=['GET'])
def viewDatas():
    conn = psycopg2.connect(**DB_PARAMS)
    query = "SELECT * FROM led_data"
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
