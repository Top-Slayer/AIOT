import base64
import requests
import subprocess
import sys
import json

output = True if len(sys.argv) > 1 and sys.argv[1] == "-o" else False

def _showOutput(json_datas: any, output: bool):
        if output:
            print("Output: ")
            print(json.dumps(json_datas, indent=4), end="\n\n")


def testProcess(name: str, res: requests, res_predict=None):
    try:
        json_datas = json.loads(res.content.decode("utf-8"))
        output_template = (f"\t| {res_predict} == {json_datas['title']} |\t").expandtabs(4)

        print(name, end="")
        print(f"{output_template} OK" if res.status_code == 200 and res_predict == json_datas['title'] else f"{output_template} Failed")
        _showOutput(json_datas, output)
    except:
        print(name, end="")
        print("... OK" if res.status_code == 200 else "... Failed")
        _showOutput(json_datas, output)
        pass


def _test_imagePost(path: str) -> any:
    with open(path, "rb") as img_file:
        encoded_image = base64.b64encode(img_file.read()).decode("utf-8")

    payload = {"image": encoded_image}

    return requests.post("http://127.0.0.1:5000/analyse-img", json=payload)


def _test_getDatas() -> any:
    return requests.get("http://127.0.0.1:5000/getAllDatas")


testProcess("POST image nothing:1 into API path: ", _test_imagePost("./image/test_nothing1.jpg"), "Nothing")
testProcess("POST image nothing:2 into API path: ", _test_imagePost("./image/test_nothing2.png"), "Nothing")
testProcess("POST image car:1 into API path: ", _test_imagePost("./image/test_car1.jpg"), "CarObject")
testProcess("POST image car:2 into API path: ", _test_imagePost("./image/test_car2.jpg"), "CarObject")
testProcess("Get data from database test: ", _test_getDatas())

print("Adding new dependencies ... ", end='')
subprocess.run(["poetry", "run", "pip", "freeze", ">", "requirement.txt"]),
print("Success")