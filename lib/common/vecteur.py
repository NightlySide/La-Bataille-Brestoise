import numpy as np


class Vecteur:

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def distance(self):
        return np.sqrt(np.pow(self.x, 2) + np.pow(self.y, 2))

    def normaliser(self):
        longueur = self.distance()
        return Vecteur(self.x/longueur, self.y/longueur)

    def __add__(self, autre):
        new_x = self.x + autre.x
        new_y = self.y + autre.y
        return Vecteur(new_x, new_y)

    def __sub__(self, autre):
        new_x = self.x - autre.x
        new_y = self.y - autre.y
        return Vecteur(new_x, new_y)

    def __mul__(self, autre):
        if isinstance(autre, int) or isinstance(autre, float):
            return Vecteur(self.x * autre, self.y * autre)
        return Vecteur(self.x * autre.x, self.y * autre.y)