from machine_learning import DetectObject as do
from flask import Flask, render_template

app = Flask(__name__)

do.recognize("image/test.jpg", debug=True)

@app.route("/")
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()