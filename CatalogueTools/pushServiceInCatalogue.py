import json
import os

path = os.path.join(os.path.dirname(__file__), "..", "Catalogue.json")


class pushServiceInCatalogue:
    def __init__(self, body, catalogue):
        self.body = body
        self.catalogue = catalogue
        self.pushServiceInCatalogue(self.body, self.catalogue)

    def pushServiceInCatalogue(self, body, catalogue):
        service_type = body["type"]
        if service_type == "subinflux":
            catalogue["services"][service_type] = body["spec"]
        elif service_type == "publisher":
            client_id = body["client_id"]
            if client_id not in catalogue["services"][service_type]:
                catalogue["services"][service_type][client_id] = []
                catalogue["services"][service_type][client_id].append(body["spec"])
            else:
                catalogue["services"][service_type].append(body["spec"])
        elif service_type == "telegrambot":
            catalogue["services"][service_type] = body["spec"]

        with open(path, "w") as file:
            json.dump(catalogue, file, indent=4)
