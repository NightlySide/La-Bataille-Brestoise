import numpy as np
from PyQt5.QtCore import Qt


class Carte(np.ndarray):

    def __new__(cls, size, cell_size, data):
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
        return self[x, y]

    def render(self, qp):
        p, q = self.shape
        for i in range(p):
            for j in range(q):
                if self.get_tile(i, j) == 1:
                    qp.setPen(Qt.black)
                    qp.setBrush(Qt.darkBlue)
                else:
                    qp.setPen(Qt.black)
                    qp.setBrush(Qt.blue)
                qp.drawRect(i * self.cell_size[0], j * self.cell_size[1], self.cell_size[0], self.cell_size[1])
