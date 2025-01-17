import requests
import json


data = {"a": 3, "b": 5}

# Convert the dictionary to a JSON string
data = json.dumps(data)
# get = requests.get(url="http://127.0.0.1:8080/catalogue/patients/mohammadbaratiit/12345")

# put = requests.put(
#     url="http://127.0.0.1:8080/",
#     data=data,
#
# )
# data = {"mohammad": "12345"}


# data = {"client_id": "mammad", "client_pass": "12345", "sensor_id": "123456"}
# try:
#     response = requests.post(
#         url="http://127.0.0.1:8080/catalogue/register/patients",
#         data=json.dumps(data),
#         headers={"Content-Type": "application/json"},
#     )
# except requests.exceptions.RequestException as e:
#     print(f"An error occurred: {e}")

# print(response.text)
params = {"clientid": "Aisa", "sensorid": "83476"}
get = requests.get(url="http://127.0.0.1:8081/inject/Aisa", params=params)

# "mohammadbaratiit": "12345"
# print(get.status_code)
print(get.text)
