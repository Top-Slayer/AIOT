from flask import Flask, render_template, request, jsonify
import serial
import time
import psycopg2
from datetime import datetime
import pytz

app = Flask(__name__)

arduino = serial.Serial('COM9', 9600) 

time.sleep(2)  # ລໍຖ້າການເຊື່ອມຕໍ່ serial ເພື່ອສະຖຽນລະພາບ

# PostgreSQL ການຕັ້ງຄ່າການເຊື່ອມຕໍ່ຖານຂໍ້ມູນ
conn = psycopg2.connect(
    dbname="postgres",  # ໃຊ້ 'postgres' ເປັນຖານຂໍ້ມູນເລີ່ມຕົ້ນ
    user="postgres",
    password="1212",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()
# ຟັງຊັນເພື່ອປ່ຽນເປັນເວລາມາດຕະຖານ
def get_local_time(utc_time):
    kst = pytz.timezone('Asia/Vientiane')
    return utc_time.astimezone(kst).strftime('%Y-%m-%d %H:%M:%S')

# ຟັງຊັນເພື່ອສ້າງຕາຕະລາງຖ້າມັນບໍ່ມີ
def create_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS led_log (
            id SERIAL PRIMARY KEY,
            color VARCHAR(10) NOT NULL,
            action VARCHAR(4) NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

# ສ້າງຕາຕະລາງຖ້າມັນບໍ່ມີ
create_table()

# ຟັງຊັ່ນເພື່ອບັນທຶກການບັນທຶກໄຟ LED ໃສ່ຖານຂໍ້ມູນ
def log_led_action(color, action):
    cursor.execute(
        "INSERT INTO led_log (color, action) VALUES (%s, %s)",
        (color, action)
    )
    conn.commit()

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Template rendering error: {str(e)}")  # ລາຍ​ລະ​ອຽດ​ຄວາມ​ຜິດ​ພາດ​ຜົນ​ໄດ້​ຮັບ​
        return str(e), 500  # ສະ​ແດງ​ຂໍ້​ຄວາມ​ຜິດ​ພາດ​ໃນ​ຕົວ​ທ່ອງ​ເວັບ​

@app.route('/led', methods=['POST'])
def led():
    color = request.form['color']
    action = request.form['action']
    command = f"{color.upper()}_{action.upper()}"
    arduino.write(command.encode())  # ສົ່ງຄໍາສັ່ງ
    log_led_action(color, action)  # ເຂົ້າ​ສູ່​ລະ​ບົບ​ຖານ​ຂໍ້​ມູນ​
    return 'OK'

# API ການສອບຖາມບັນທຶກໄຟ LED
@app.route('/led_log', methods=['GET'])
def led_log():
    cursor.execute("SELECT color, action, timestamp FROM led_log ORDER BY timestamp DESC")
    logs = cursor.fetchall()
    return jsonify(logs)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)