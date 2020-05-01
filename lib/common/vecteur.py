import numpy as np

from lib.client.global_client_registry import GCR
from lib.common.logger import Logger


class Vecteur:
    """
    Représentation d'un vecteur à 2 dimensions.
    Utile pour tout ce qui est calcul vectoriel nécessaire dans
    ce projet.

    Args:
        x (float): abscisse
        y (float): ordonnée
    """

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def distance(self):
        """
        Retourne la distance eulerienne du vecteur
        """
        return np.sqrt(np.power(self.x, 2) + np.power(self.y, 2))

    def normaliser(self):
        """
        Retourne un vecteur normalisé, ie. de norme 1
        Très utilisé pour récupérer une direction
        """
        longueur = self.distance()
        return Vecteur(self.x/longueur, self.y/longueur)

    def __add__(self, autre):
        """
        Surcharge de l'opérateur pour être compatible avec les
        opérations vectorielles.

        Args:
            autre (Vecteur): autre vecteur
        """
        new_x = self.x + autre.x
        new_y = self.y + autre.y
        return Vecteur(new_x, new_y)

    def __sub__(self, autre):
        """
        Surcharge de l'opérateur pour être compatible avec les
        opérations vectorielles.

        Args:
            autre (Vecteur): autre vecteur
        """
        new_x = self.x - autre.x
        new_y = self.y - autre.y
        return Vecteur(new_x, new_y)

    def __mul__(self, autre):
        """
        Surcharge de l'opérateur pour être compatible avec les
        opérations vectorielles.

        Args:
            autre (Object): autre vecteur ou constante
        """
        # Si autre est une constante
        if isinstance(autre, int) or isinstance(autre, float):
            # On multiplie juste
            return Vecteur(self.x * autre, self.y * autre)
        return Vecteur(self.x * autre.x, self.y * autre.y)

    def __div__(self, autre):
        """
        Surcharge de l'opérateur pour être compatible avec les
        opérations vectorielles.

        Args:
            autre (Object): autre vecteur ou constante
        """
        # Si autre est une constante
        if isinstance(autre, int) or isinstance(autre, float):
            # On multiplie juste
            return Vecteur(self.x / autre, self.y / autre)
        return Vecteur(self.x / autre.x, self.y / autre.y)

    def __repr__(self):
        """
        Représentation du vecteur à fin de débug.
        """
        return f"Vecteur : ({self.x}, {self.y})"

    @staticmethod
    def produit_vectoriel(v1, v2):
        """
        Effectue le produit vectoriel de base entre deux vecteurs

        Args:
            v1 (Vecteur): premier vecteur
            v2 (Vecteur): second vecteur
        """
        return v1.x * v2.y - v1.y * v2.x

    def equal(self, autre):
        if self.x == autre.x and self.y == autre.y:
            return True
        return False

    def est_entre(self, a, b, epsilon=1):
        """
        Va vérifier si le point désigné par un Vecteur se situe
        entre les points a et b, avec une précision de epsilon.

        Args:
            a (Vecteur): point de départ
            b (Vecteur): point d'arrivée
            epsilon (float): précision
        """
        # On verifie si le point est à la bonne distance
        """ab = b - a
        ac = self - a
        if ab.distance() < ac.distance():
            print("Pas bonne distance")
            return False
        # On calcule le produit vectoriel pour savoir si les points
        # sont alignés
        produit_vect = (self.y - a.y) * (b.x - a.x) - (self.x - a.x) * (b.y - a.y)
        if abs(produit_vect) > epsilon:
            print("Pas sur la droite")
            return False
        # On calcule le dot product pour savoir si les vecteurs AB et AC sont dans la
        # même direction
        dot_prod = (self.x - a.x) * (b.x - a.x) + (self.y - a.y)*(b.y - a.y)
        if dot_prod < 0:
            print("Pas dans le bon sens")
            return False

        # Dans ce cas C est bien entre A et B
        return True"""

        # On calcule le produit vectoriel pour savoir si les points sont sur la meme droite
        prod_vectoriel = (self.y - a.y) * (b.x - a.x) - (self.x - a.x) * (b.y - a.y)
        # on le compare à un epsilon pour les valeurs flottantes
        if abs(prod_vectoriel) > epsilon:
            return False

        # on cherche à savoir si les points sont dans le meme sens
        produit_scalaire = (self.x - a.x) * (b.x - a.x) + (self.y - a.y) * (b.y - a.y)
        if produit_scalaire < 0:
            return False

        # On vérifie enfin si le point respecte la longueur
        longeur_carre = (b.x - a.x) * (b.x - a.x) + (b.y - a.y) * (b.y - a.y)
        if produit_scalaire > longeur_carre:
            return False

        # le point est bien sur le segment [a,b]
        return True


if __name__ == "__main__":
    a = Vecteur(0, 0)
    b = Vecteur(10, 0)
    c = Vecteur(5, 0)

    print(c.est_entre(a, b))