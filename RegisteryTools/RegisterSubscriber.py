import requests
import json


class registerService:
    def __init__(self, client_id, topic, token, org, host):
        self.client_id = client_id
        self.topic = topic
        self.token = token
        self.org = org
        self.host = host
        self.registerService()

    def registerService(self):
        service_data = {
            "type": "subinflux",
            "spec": {
                "id": self.client_id,
                "address": "127.0.0.1:8082",
                "topic": self.topic,
                "influx_token": self.token,
                "influx_org": self.org,
                "influx_host": self.host,
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
