class Inject:
    def __init__(self):
        self.capacity = 100

    def reduceCapacity(self, client_id):
        # assuming that each injection takes 20 percent of capacity
        if self.capacity >= 20:
            self.capacity -= 20
            return f"Injection completed for {client_id}. {self.capacity//20} shots remaining"
        else:
            return "Out of insulin. Change the injector!"

    def inject(self, client_id):
        # assuming that each injection takes 20 percent of capacity
        msg = self.reduceCapacity(client_id)
        return msg
