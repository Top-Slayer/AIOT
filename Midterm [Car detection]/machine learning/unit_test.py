import base64
import requests

with open('./image/test1.png', 'rb') as img_file:
    encoded_image = base64.b64encode(img_file.read()).decode('utf-8')

payload = {
    "image": encoded_image
}

response = requests.post("http://127.0.0.1:5000/analyse-img", json=payload)
print(response.json())
