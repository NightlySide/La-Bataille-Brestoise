from abc import ABCMeta, abstractmethod

from lib.common.entite import Entite
from lib.common.logger import Logger
from lib.server.global_server_registry import GSR


class Etat(metaclass=ABCMeta):

    def __init__(self, parent):
        self.parent = parent
        self.en_vie = True

    @abstractmethod
    def update(self):
        pass


class FSM:
    """
    Machine à état fini. Permet de définir un automate qui controle les I.A.
    du jeu.

    Attributes:
        parent (Entite): parent de l'automate
        etat_initial (Etat): état de départ
        etat_courant (Etat): état actuel
        nom_etat_courant (str): nom de l'état actuel
        etats (dict): dictionnaire des états enregistrés dans l'automate
        prochain_etat (Etat): état à suivre
    """
    def __init__(self, parent: Entite, nom_etat_courant: str = None, etat_initial: Etat = None):
        self.parent = parent
        self.etat_initial = etat_initial
        self.etat_courant = self.etat_initial
        self.nom_etat_courant = nom_etat_courant
        self.etats = {}
        self._nom_prochain_etat = None
        self._prochain_etat = None

    def ajouter_etat(self, name: str, etat: Etat) -> None:
        """
        Permet d'ajouter un état à l'automate et de pouvoir l'identifier par un nom.

        Args:
            name (str): nom de l'état
            etat (Etat): état à ajouter
        """
        etat.parent = self.parent
        self.etats[name] = etat

    @property
    def prochain_etat(self) -> Etat:
        return self._prochain_etat

    @prochain_etat.setter
    def prochain_etat(self, name: str) -> None:
        """
        Permet de définir l'état suivant à partir de son nom

        Args:
            name (str): nom de l'état suivant
        """
        if name is None:
            self._prochain_etat = None
            self._nom_prochain_etat = None
        elif name in self.etats:
            self._prochain_etat = self.etats[name]
            self._nom_prochain_etat = name
        else:
            GSR.log.log(Logger.ERREUR, "FSM - état non reconnu : " + name)

    def update(self) -> None:
        """
        Met à jour l'automate et surtout met à jour l'état actuel.
        """
        # Si l'état courant existe bien
        if self.etat_courant is not None:
            # Si l'état courant est terminé on passe au suivant
            if not self.etat_courant.en_vie:
                self.etat_courant = self.prochain_etat
                self.etat_courant.en_vie = True
                self.nom_etat_courant = self._nom_prochain_etat
                self.prochain_etat = None
                self._nom_prochain_etat = None
            self.etat_courant.update()
        # Sinon si un autre état est prévu
        elif self.prochain_etat is not None:
            self.etat_courant = self.prochain_etat
            self.etat_courant.en_vie = True
            self.nom_etat_courant = self._nom_prochain_etat
            self.prochain_etat = None
            self._nom_prochain_etat = None
