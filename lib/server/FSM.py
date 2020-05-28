from abc import ABCMeta, abstractmethod

from lib.common.logger import Logger
from lib.server.global_server_registry import GSR


class FSM:

    def __init__(self, parent, nom_etat_courant = None, etat_initial=None):
        self.parent = parent
        self.etat_initial = etat_initial
        self.etat_courant = self.etat_initial
        self.nom_etat_courant = nom_etat_courant
        self.etats = {}
        self._nom_prochain_etat = None
        self._prochain_etat = None

    def ajouter_etat(self, name, etat):
        etat.parent = self.parent
        self.etats[name] = etat

    @property
    def prochain_etat(self):
        return self._prochain_etat

    @prochain_etat.setter
    def prochain_etat(self, name):
        if name is None:
            self._prochain_etat = None
            self._nom_prochain_etat = None
        elif name in self.etats:
            self._prochain_etat = self.etats[name]
            self._nom_prochain_etat = name
        else:
            GSR.log.log(Logger.ERREUR, "FSM - état non reconnu : " + name)

    def update(self):
        # Si l'état courant existe bien
        if self.etat_courant is not None:
            # Si l'état courant est terminé on passe au suivant
            if not self.etat_courant.en_vie:
                self.etat_courant = self.prochain_etat
                self.nom_etat_courant = self._nom_prochain_etat
                self.prochain_etat = None
                self._nom_prochain_etat = None
            self.etat_courant.update()
        # Sinon si un autre état est prévu
        elif self.prochain_etat is not None:
            self.etat_courant = self.prochain_etat
            self.nom_etat_courant = self._nom_prochain_etat
            self.prochain_etat = None
            self._nom_prochain_etat = None



class Etat(metaclass=ABCMeta):

    def __init__(self):
        self.en_vie = True
        self.parent = None

    @abstractmethod
    def update(self):
        pass
