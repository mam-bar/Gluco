import json
import os


class getSensor:
    def __init__(self):
        pass

    def getSensor(self, catalogue, user):
        try:
            sensor = catalogue["sensors"][user][-1]["sensor_id"]
            return sensor
        except:
            return "Sensor not found"


if __name__ == "__main__":

    path = os.path.join(os.path.dirname(__file__), "..", "Catalogue.json")

    with open(path, "r") as file:
        catalogue = json.load(file)
    print(getSensor().getSensor(catalogue, "Alireza"))
