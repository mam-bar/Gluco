import requests
import json


class registerService:
    def __init__(self, client_id, topic, sensor_id):
        self.client_id = client_id
        self.topic = topic
        self.sensor_id = sensor_id
        self.registerService()

    def registerService(self):
        service_data = {
            "type": "publisher",
            "client_id": self.client_id,
            "spec": {
                "address": "127.0.0.1:8081",
                "topic": self.topic,
                "sensor": self.sensor_id,
                "injection_address": f"inject/{self.client_id}",
            },
        }
        try:
            post = requests.post(
                url="http://127.0.0.1:8080/catalogue/services",
                data=json.dumps(service_data),
                headers={"Content-Type": "application/json"},
            )
        except:
            pass
