from machine_learning import DetectObject as do
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import base64, serial, sqlite3, os

app = Flask(__name__)
CORS(app)

barrier_status = False
object = []

# Initial databse and base table
path = "./datas.db"
if not os.path.exists(path):
    with open(path, "w") as f:
        pass
conn = sqlite3.connect(path, check_same_thread=False)
conn.execute(
    "CREATE TABLE IF NOT EXISTS CarStatus( \
        ID INTEGER PRIMARY KEY AUTOINCREMENT, \
        Title VARCHAR(40) NOT NULL, \
        DetectTime DATETIME \
    );"
)
conn.commit()

# Arduino port connection
try:
    arduino = serial.Serial("COM9", 9600, timeout=1)
except Exception as e:
    arduino = None

print(f"-> Arduino Port: {arduino}")


def interactToServo(status):
    global barrier_status

    barrier_status = status
    if arduino == None:
        return
    arduino.write(b"1" if status else b"0")


def storeDatas(title: str):
    cur = conn.cursor()
    _dateset = datetime.today().strftime("%d/%m/%Y %H:%M:%S")

    cur.execute(
        "INSERT INTO CarStatus(Title, DetectTime) \
        VALUES(?,?)",
        (title, _dateset),
    )

    conn.commit()


# Analyse object and decide open barrier
@app.route("/analyse-img", methods=["POST"])
def analyseImg():
    global object

    data = request.get_json()

    if "image" not in data:
        return jsonify({"error": "Invalid json payload"}), 400

    object = do.recognize(base64.b64decode(data["image"]))

    interactToServo(object[0] == "CarObject")
    if object[0] != "Nothing":
        storeDatas(object[0])

    return (
        jsonify(
            {
                "title": object[0],
                "percent": object[1],
                "barrier-status": barrier_status,
            }
        ),
        200,
    )


# Change status of barrier instanctly
# @app.route("/change-status", methods=["POST"])
# def changeStatus():
#     global object

#     interactToServo(True)

#     return jsonify({"barrier-status": barrier_status}), 200


# Query data from database
@app.route("/getAllDatas", methods=["GET"])
def getAllData():
    cur = conn.cursor()
    cur.execute("SELECT ID, Title, DetectTime FROM CarStatus")
    fetchDatas = cur.fetchall()

    datas = [
        {"id": d[0], "title": d[1], "time": d[2]}
        for d in fetchDatas
    ]

    return jsonify(datas)


if __name__ == "__main__":
    app.run()
