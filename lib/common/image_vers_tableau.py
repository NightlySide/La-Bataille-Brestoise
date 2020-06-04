# Auteur : Alexandre FROEHLICH

import numpy as np
from PIL import Image


def img_vers_array(img_path):
    """
    Retourne un tableau de données correspondant
    à une image en noir et blanc. Un pixel noir égal un mur,
    un pixel blanc égal une case libre.

    Args:
        img_path (str): chemin relatif de l'image d'entrée
    """
    # On ouvre l'image
    image = Image.open(img_path)
    # On charge les pixels
    pixels = image.load()
    # On crée le tableau de sortie
    data = np.zeros(image.size)
    p, q = image.size
    # Pour chaque pixel
    for i in range(p):
        for j in range(q):
            # On ajoute la case correspondante
            data[i, j] = 0 if pixels[i, j][0] < 50 else 1
    return data


if __name__ == "__main__":
    print(img_vers_array("../../assets/carte_rade_brest.jpg"))