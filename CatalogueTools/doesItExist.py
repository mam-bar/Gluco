class doesItExist:
    def __init__(self, catalogue, type, user, password):
        self.catalogue = catalogue
        self.type = type
        self.user = user
        self.password = password
        self.result = self.existence(
            self.catalogue, self.type, self.user, self.password
        )

    def existence(self, catalogue, type, user, password):
        flag = False
        for item in catalogue[type].keys():
            if item == user and catalogue[type][item] == password:
                flag = True
        if flag:
            return "Exists"
        else:
            return "Does not exist"
