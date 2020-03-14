import numpy as np

from lib.client.global_client_registry import GCR
from lib.common.logger import Logger


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

    def __repr__(self):
        return f"Vecteur : ({self.x}, {self.y})"

    @staticmethod
    def produit_vectoriel(v1, v2):
        return v1.x * v2.y - v1.y * v2.x

    @staticmethod
    def est_entre(a, b, c, epsilon=1):
        produit_vect = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)
        if abs(produit_vect) > epsilon:
            return False
        dot_prod = (c.x - a.x) * (b.x - a.x) + (c.y - a.y)*(b.y - a.y)
        if dot_prod < 0:
            return False
        return True