from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import io
from tabulate import tabulate

model = load_model("model/keras_model.h5", compile=False)
class_names = [line.strip() for line in open("model/labels.txt", "r").readlines()]

np.set_printoptions(suppress=True)

def recognize(img_bytes, debug=False) -> np.ndarray:
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(io.BytesIO(img_bytes)).convert("RGB")

    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    image_array = np.asarray(image)

    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    data[0] = normalized_image_array
    predicted = model.predict(data)

    # Display each info for Class
    if debug:
        datas = []
        headers = ["Class", "Percent"]
        print("\nDebug output: ")
        for i, v in enumerate(predicted[0]):
            datas.append([class_names[i][2:], f"{v} %"])
        print(tabulate(datas, headers, tablefmt="grid"),end="\n\n")
    
    index = np.argmax(predicted)

    return np.array([class_names[index][2:], round(predicted[0][index] * 100, 2)])