import requests
import json


class pullObservations:
    def __init__(self):
        self.influxdb_uri = "http://127.0.0.1:8082/influx"

    def getLastN(self, user, minutes):
        url = f"{self.influxdb_uri}/GetLastNMinutes/{user}/{minutes}"
        get = requests.get(url)
        return json.loads(get.text)


if __name__ == "__main__":
    print(pullObservations().getLastN("Aisa", 5))
