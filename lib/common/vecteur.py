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

    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def distance(self) -> float:
        """
        Retourne la distance eulerienne du vecteur

        Returns:
            distance (float): la longueur eulérienne du vecteur
        """
        return np.sqrt(np.power(self.x, 2) + np.power(self.y, 2))

    def normaliser(self) -> "Vecteur":
        """
        Retourne un vecteur normalisé, ie. de norme 1
        Très utilisé pour récupérer une direction

        Returns:
            v_norm (Vecteur): vecteur normalisé en longueur
        """
        longueur = self.distance()
        if longueur != 0:
            return Vecteur(self.x/longueur, self.y/longueur)
        return Vecteur()

    def __add__(self, autre: "Vecteur") -> "Vecteur":
        """
        Surcharge de l'opérateur pour être compatible avec les
        opérations vectorielles.

        Args:
            autre (Vecteur): autre vecteur

        Returns:
            nouveau (Vecteur): vecteur sommé des deux précédents
        """
        new_x = self.x + autre.x
        new_y = self.y + autre.y
        return Vecteur(new_x, new_y)

    def __sub__(self, autre: "Vecteur") -> "Vecteur":
        """
        Surcharge de l'opérateur pour être compatible avec les
        opérations vectorielles.

        Args:
            autre (Vecteur): autre vecteur

        Returns:
            nouveau (Vecteur): vecteur soustrait des deux précédents
        """
        new_x = self.x - autre.x
        new_y = self.y - autre.y
        return Vecteur(new_x, new_y)

    def __mul__(self, autre: "Vecteur" or int) -> "Vecteur":
        """
        Surcharge de l'opérateur pour être compatible avec les
        opérations vectorielles.

        Args:
            autre (Object): autre vecteur ou constante

        Returns:
            nouveau (Vecteur): vecteur multiplié des deux précédents
        """
        # Si autre est une constante
        if isinstance(autre, int) or isinstance(autre, float):
            # On multiplie juste
            return Vecteur(self.x * autre, self.y * autre)
        return Vecteur(self.x * autre.x, self.y * autre.y)

    def __div__(self, autre: "Vecteur") -> "Vecteur":
        """
        Surcharge de l'opérateur pour être compatible avec les
        opérations vectorielles.

        Args:
            autre (Object): autre vecteur ou constante

        Returns:
            nouveau (Vecteur): vecteur divisé des deux précédents
        """
        # Si autre est une constante
        if isinstance(autre, int) or isinstance(autre, float):
            # On multiplie juste
            return Vecteur(self.x / autre, self.y / autre)
        return Vecteur(self.x / autre.x, self.y / autre.y)

    def __repr__(self) -> str:
        """
        Représentation du vecteur à fin de débug.
        """
        return f"Vecteur : ({self.x}, {self.y})"

    @staticmethod
    def produit_vectoriel(v1: "Vecteur", v2: "Vecteur") -> float:
        """
        Effectue le produit vectoriel de base entre deux vecteurs

        Args:
            v1 (Vecteur): premier vecteur
            v2 (Vecteur): second vecteur

        Returns:
            produit_vectoriel (float): le produit vectoriel des deux vecteurs
        """
        return v1.x * v2.y - v1.y * v2.x

    def equal(self, autre: "Vecteur") -> bool:
        """
        Permet de vérifier si deux vecteurs sont égaux en comparant leurs attributs.

        Args:
            autre (Vecteur): vecteur à comparer

        Returns:
            equal (bool): est-ce que les deux vecteurs sont égaux en attributs?
        """
        if self.x == autre.x and self.y == autre.y:
            return True
        return False

    def est_entre(self, a: "Vecteur", b: "Vecteur", epsilon: int = 1) -> bool:
        """
        Va vérifier si le point désigné par un Vecteur se situe
        entre les points a et b, avec une précision de epsilon.

        Args:
            a (Vecteur): point de départ
            b (Vecteur): point d'arrivée
            epsilon (float): précision

        Returns:
            est_entre (bool): est ce que le vecteur est entre a et b?
        """

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