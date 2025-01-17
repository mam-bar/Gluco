import requests


class Injection:
    def __init__(self):
        self.actuator_url = "http://127.0.0.1:8081/inject"
        self.catalogue_url = "http://127.0.0.1:8080/catalogue/sensors"

    def getSensor(self, username):
        url = f"{self.catalogue_url}/{username}"
        get = requests.get(url)
        return get.text

    def injectionCommand(self, username, sensor_id):
        url = f"{self.actuator_url}/{username}"
        params = {"clientid": username, "sensorid": sensor_id}
        get = requests.get(url, params=params)
        return get.text


if __name__ == "__main__":
    sensor = Injection().getSensor("Alireza")
    print(sensor)
    # print(Injection().injectionCommand("Aisa", "83476"))
