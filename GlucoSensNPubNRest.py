from MyMQTT import MyMQTT as client
import time
import cherrypy
from RegisteryTools.RegisterPublisher import registerService
from RegisteryTools.RegisterClient import registerClient
from PubNRestTools.injectService import Inject
from PubNRestTools.sensorService import Sensor


class Gluco:
    exposed = True

    def __init__(self, sensor_id, client_id, password):
        self.sensor_id = sensor_id
        self.client_id = client_id
        self.password = password
        self.topic = f"GlucoIoT/{self.client_id}/{sensor_id}"
        # post user data into catalogue
        registerClient(self.client_id, self.password, self.sensor_id)
        # post service data into catalogue
        registerService(self.client_id, self.topic, self.sensor_id)
        self.client = client(sensor_id)
        self.client.start()
        time.sleep(0.5)
        self.msg = {
            "bn": sensor_id,
            "e": [
                {"n": "Glucose Level", "u": "mg/dL", "t": None, "v": None},
            ],
        }
        self.Injector = Inject()
        self.sensor = Sensor()

    """sensor part"""

    # publishes sensed data
    def sens_n_pub(self):
        self.msg["e"][0]["t"] = time.time()
        measurement = self.sensor.sense()
        self.msg["e"][0]["v"] = measurement
        if measurement > 140:
            msg = self.Injector.inject(self.client_id, self.sensor_id)
            print(msg)
            self.sensor.dropInsulin()
        # publish to broker
        self.client.myPublish(self.topic, self.msg)
        # just in case something is wrong
        unit = self.msg["e"][-1]["u"]
        print(f"{measurement} {unit} from {self.client_id} published to {self.topic}")
        time.sleep(1)

    """actuator part"""
    """actuation only available through rest api get"""

    def GET(self, *uri, **params):
        msg = ""
        if list(params)[0] == "clientid" and list(params)[1] == "sensorid":
            if (
                params["clientid"] == self.client_id
                and params["sensorid"] == self.sensor_id
            ):
                msg = self.Injector.inject(self.client_id)
                self.sensor.dropInsulin()
            else:
                msg = f"Invalid access. Either client id '{params['clientid']}' or sensor id '{params['sensorid']}' is invalid"

        else:
            msg = "Invalid command! Try with some other values."
        print(msg)
        return msg


if __name__ == "__main__":
    client_id = "mohammadbaratiit"
    password = "12345"
    sensor_id = "83473"
    c1 = Gluco(sensor_id, client_id, password)
    conf = {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.sessions.on": True,
        }
    }
    cherrypy.config.update(
        {"server.socket_host": "127.0.0.1", "server.socket_port": 8081}
    )
    cherrypy.tree.mount(c1, "/inject/", conf)
    cherrypy.engine.start()

    # cherrypy.engine.block() was not needed, as the while loop keeps the app going.
