# Auteur : Alexandre FROEHLICH

import json


class JsonLoader(dict):
    """
    Classe outil permettant de charger un fichier JSON et de récupérer ses données

    Attributes:
        filename (str): le nom du fichier
    """
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        with open(self.filename, "r") as f:
            data = json.loads(f.read())
        for key in data:
            self[key] = data[key]

    def write(self) -> None:
        """
        Permet d'écrire dans le fichier les données modifiées.
        """
        data = {}
        for key in self:
            data[key] = self[key]
        with open(self.filename, "w") as f:
            f.write(json.dumps(data, indent=4))

    @staticmethod
    def init_server_config(filename="server_config.json")  -> None:
        """
        Fonction outil pour initialiser le fichier avec le serveur en local.

        Args:
            filename (str): le nom du fichier
        """
        with open(filename, "w") as f:
            data = {"name": "Serveur de test local", "ip": "0.0.0.0", "port": 25566}
            f.write(json.dumps(data, indent=4))
