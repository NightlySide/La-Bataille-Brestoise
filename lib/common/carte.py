import numpy as np
from PyQt5.QtCore import Qt

from lib.client.global_client_registry import GCR


class Carte(np.ndarray):
    """
    Classe représentant la carte et ses données.

    Args:
        size (int, int): couple hauteur/largeur du nombre de tuiles sur la carte
        cell_size (int, int): couple hauteur/largeur d'une case en pixels
        data (np.ndarray): données de la carte
    """

    def __new__(cls, size, cell_size, data):
        """
        Constructeur de la classe Carte.
        Args:
            size (int, int): couple hauteur/largeur du nombre de tuiles sur la carte
            cell_size (int, int): couple hauteur/largeur d'une case en pixels
            data (np.ndarray): données de la carte
        """

        # Au lieu de renvoyer directement le nouvel array on va
        # l'assigner à une variable
        new_array = super(Carte, cls).__new__(cls, size)
        # on rajoute nombre_joueurs dans cette instance nouvellement créée
        new_array.cell_size = cell_size
        new_array[:, :] = data
        # et finalement on la renvoie
        return new_array

    def __init__(self, size, cell_size, data):
        pass

    def __array_finalize__(self, obj):
        # quand on créé une instance "à la main" la variable "obj" vaut None
        # et on n'a rien à faire de spécial dans cette méthode  vu que __new__
        # a été appellé
        if obj is None:
            return
        # Par contre si on créé une instance via un slicing du tableau de
        # départ alors obj sera l'objet qu'on est en train de découper, on
        # va donc recopier ses variables d'instance qui sont spécifiques
        self.cell_size = getattr(obj, 'cell_size', None)

    def get_tile(self, x, y):
        """
        Retourne la tuile aux coordonnées x, y.

        Args:
            x (int): coordonnée selon les abscisses
            y (int): coordonnée selon les ordonnées
        """
        p, q = self.shape
        # Garde-fou : on vérifie que la position existe bien
        if 0 < x < p - 1 and 0 < y < q - 1:
            return self[x, y]
        return None

    def render(self, qp, window_size):
        """

        Args:
            qp (QPainter): le painter du canvas qui demande à
                être rendu.
            window_size (int, int): taille de la fenetre dans laquelle
                rendre la carte.
        """
        # On récupère le centre de la fenètre
        center = (window_size[0] // 2, window_size[1] // 2)
        center_in_cells = (center[0] // self.cell_size[0], center[1] // self.cell_size[1])
        # On récupère la position du joueur
        i0, j0 = GCR.joueur.position.x, GCR.joueur.position.y
        # On dessine autour du joueur au milieu de l'écran
        for i in range(-center_in_cells[0], center_in_cells[0]):
            for j in range(-center_in_cells[1], center_in_cells[1]):
                # On récupère la tuile
                tile = self.get_tile(int(i0 + i), int(j0 + j))
                # Si la tuile n'existe pas on la fait en noir
                if tile is None:
                    qp.setPen(Qt.black)
                    qp.setBrush(Qt.black)
                # Si la tuile est un mur
                elif tile == 1:
                    qp.setPen(Qt.black)
                    qp.setBrush(Qt.darkBlue)
                # Si la tuile est vide
                else:
                    qp.setPen(Qt.black)
                    qp.setBrush(Qt.blue)
                # On trace la tuile
                qp.drawRect(center[0] + i * self.cell_size[0],
                            center[1] + j * self.cell_size[1],
                            self.cell_size[0],
                            self.cell_size[1])