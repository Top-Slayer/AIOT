import base64
import requests
import subprocess


def testProcess(name: str, res: any):
    print(name, end="")
    print("...OK" if res else "...Failed")


def _test_imagePost() -> any:
    with open("./image/test.jpg", "rb") as img_file:
        encoded_image = base64.b64encode(img_file.read()).decode("utf-8")

    payload = {"image": encoded_image}

    return requests.post("http://127.0.0.1:5000/analyse-img", json=payload)


def _test_CORS() -> any:
    return subprocess.run(
        [
            "curl",
            "-H",
            "Origin: http://something.com",
            "-X",
            "POST",
            "http://127.0.0.1:5000/change-status",
            "-v",
        ],
        capture_output=True,
        text=True,
    ).stdout


testProcess("Test POST: ", _test_imagePost())
testProcess("CORS test: ", _test_CORS())
