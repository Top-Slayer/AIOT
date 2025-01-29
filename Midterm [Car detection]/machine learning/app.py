from machine_learning import DetectObject as do
from flask import Flask,jsonify, request
import base64, serial

app = Flask(__name__)
barrier_status = False
object = []

try:
    arduino = serial.Serial('COM9', 9600, timeout=1)
except Exception as e:
    arduino = None

print(f"-> Arduino Port: {arduino}")

def interactToServo(status):
    global barrier_status

    barrier_status = status
    if arduino == None: return

    if status:
        arduino.write(b'1')
    else:
        arduino.write(b'0')

    arduino.close()

# def storeDatas():

@app.route("/analyse-img", methods=["POST"])
def analyseImg():
    global object

    data = request.get_json()

    if "image" not in data:
        return jsonify({"error": "Invalid json payload"}), 400

    object = do.recognize(base64.b64decode(data["image"]))
    interactToServo(object[0] == "CarObject")

    return jsonify({
            "title": object[0],
            "percent": object[1],
            "barrier-status": barrier_status,
        }), 200

@app.route("/change-status", methods=["POST"])
def changeStatus():
    global object

    interactToServo(not barrier_status)

    return jsonify({
            "title": object[0],
            "percent": object[1],
            "barrier-status": barrier_status,
        }), 200

if __name__ == '__main__':
    app.run()