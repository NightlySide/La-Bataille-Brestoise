import json


class JsonLoader(dict):

    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        with open(self.filename, "r") as f:
            data = json.loads(f.read())
        for key in data:
            self[key] = data[key]

    def write(self):
        data = {}
        for key in self:
            data[key] = self[key]
        with open(self.filename, "w") as f:
            f.write(json.dumps(data, indent=4))

    @staticmethod
    def init_server_config(filename="server_config.json"):
        with open(filename, "w") as f:
            data = {"name": "Serveur de test local", "ip": "0.0.0.0", "port": 25566}
            f.write(json.dumps(data, indent=4))
