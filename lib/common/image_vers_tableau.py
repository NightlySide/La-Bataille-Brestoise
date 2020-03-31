import numpy as np
from PIL import Image


def img_vers_array(img_path):
    image = Image.open(img_path)
    pixels = image.load()
    data = np.zeros(image.size)
    p, q = image.size
    for i in range(p):
        for j in range(q):
            data[i, j] = 0 if pixels[i, j][0] < 50 else 1
    return data


if __name__ == "__main__":
    print(img_vers_array("../../assets/carte_rade_brest.jpg"))