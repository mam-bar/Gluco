import requests
import json


class registerClient:
    def __init__(self, client_id, password, sensor_id):
        self.client_id = client_id
        self.password = password
        self.sensor_id = sensor_id
        self.registerClient()

    def registerClient(self):
        data = {
            "client_id": self.client_id,
            "client_pass": self.password,
            "sensor_id": self.sensor_id,
        }
        try:
            response = requests.post(
                url="http://127.0.0.1:8080/catalogue/register/patients",
                data=json.dumps(data),
                headers={"Content-Type": "application/json"},
            )
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
