import base64
import requests
import subprocess
import sys
import json

output = True if len(sys.argv) > 1 and sys.argv[1] == "-o" else False

def testProcess(name: str, res: requests):
    print(name, end="")
    print("... OK" if res.status_code == 200 else "... Failed")
    if output:
        print("Output: ")
        print(json.dumps(json.loads(res.content.decode("utf-8")), indent=4), end="\n\n")


def _test_imagePost() -> any:
    with open("./image/test.jpg", "rb") as img_file:
        encoded_image = base64.b64encode(img_file.read()).decode("utf-8")

    payload = {"image": encoded_image}

    return requests.post("http://127.0.0.1:5000/analyse-img", json=payload)


def _test_getDatas() -> any:
    return requests.get("http://127.0.0.1:5000/getAllDatas")


testProcess("POST image into API path: ", _test_imagePost())
testProcess("Get data from database test: ", _test_getDatas())

print("Adding new dependencies ... ", end='')
subprocess.run(["poetry", "run", "pip", "freeze", ">", "requirement.txt"]),
print("Success")