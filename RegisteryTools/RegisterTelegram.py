import requests
import json


class registerService:
    def __init__(self, client_id, token):
        self.client_id = client_id
        self.token = token
        self.registerService()

    def registerService(self):
        try:
            service_data = {
                "type": "telegrambot",
                "spec": {
                    "client_id": self.client_id,
                    "token": self.token,
                    "package_used": "Telepot",
                },
            }
            post = requests.post(
                url="http://127.0.0.1:8080/catalogue/services",
                data=json.dumps(service_data),
                headers={"Content-Type": "application/json"},
            )
        except:
            pass


if __name__ == "__main__":
    registerService("Aisa", "12345")
