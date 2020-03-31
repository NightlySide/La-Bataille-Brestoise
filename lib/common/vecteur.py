import numpy as np


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
        return np.sqrt(np.pow(self.x, 2) + np.pow(self.y, 2))

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

    @staticmethod
    def est_entre(a, b, c, epsilon=1):
        """
        Va vérifier si un point b désigné par un Vecteur se situe
        entre les points a et c, avec une précision de epsilon.

        Args:
            a (Vecteur): point de départ
            b (Vecteur): point à tester
            c (Vecteur): point d'arrivée
            epsilon (float): précision
        """
        # On calcule le produit vectoriel pour savoir si les points
        # sont alignés
        produit_vect = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)
        if abs(produit_vect) > epsilon:
            return False
        # On calcule le dot product pour savoir si les vecteurs AB et AC sont dans la
        # même direction
        dot_prod = (c.x - a.x) * (b.x - a.x) + (c.y - a.y)*(b.y - a.y)
        if dot_prod < 0:
            return False

        # Dans ce cas B est bien entre A et C
        return True