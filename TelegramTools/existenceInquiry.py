import requests


class TAuthentication:
    def __init__(self):
        pass

    def patient(self, user, password):
        url = f"http://127.0.0.1:8080/catalogue/patients/{user}/{password}"
        try:
            get = requests.get(url=url)
            if get.text == "Exists":
                return True
            else:
                return False
        except:
            pass


if __name__ == "__main__":
    print(TAuthentication().patient("Alireza", "12345"))
