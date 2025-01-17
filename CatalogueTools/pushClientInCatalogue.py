import json
import os
import time

path = os.path.join(os.path.dirname(__file__), "..", "Catalogue.json")


class pushClientInCatalogue:
    def __init__(self, body, catalogue):
        self.body = body
        self.catalogue = catalogue
        self.sensor = {
            "sensor_id": 0,
            "type": "Dexcom",
            "unit": "ml",
            "start_date": "2024/01/14",
            "topic": "patient_id/sensor_id",
            "insulin_level_threshold": "type1",
        }
        self.pushClientInCatalogue(self.body, self.catalogue)

    def pushClientInCatalogue(self, body, catalogue):
        client_id = body["client_id"]
        sensor_id = body["sensor_id"]
        print(client_id, sensor_id)
        if (client_id not in catalogue["patients"].keys()) and (
            client_id not in catalogue["sensors"].keys()
        ):
            catalogue["patients"][client_id] = body["client_pass"]
            self.sensor["sensor_id"] = sensor_id
            self.sensor["topic"] = f"{client_id}/{sensor_id}"
            self.sensor["start_date"] = time.time()
            catalogue["sensors"][client_id] = []
            catalogue["sensors"][client_id].append(self.sensor)

        elif client_id in catalogue["patients"].keys():
            self.sensor["sensor_id"] = sensor_id
            self.sensor["topic"] = f"{client_id}/{sensor_id}"
            self.sensor["start_date"] = time.time()
            catalogue["sensors"][client_id].append(self.sensor)

        with open(path, "w") as file:
            json.dump(catalogue, file, indent=4)
