from MyMQTT import MyMQTT as client
from SubInflux.MyInfluxDBclient import MyinfluxDBclient
import time
import json
import cherrypy
from RegisteryTools.RegisterSubscriber import registerService


class GlucoSub:
    exposed = True

    def __init__(self):
        self.client_id = "sub_influx_client"
        self.topic = "GlucoIoT/#"
        self.client = client(self.client_id, self)
        self.client.start()
        time.sleep(0.5)
        self.MyInfluxDBClient = MyinfluxDBclient()
        registerService(
            self.client_id,
            self.topic,
            self.MyInfluxDBClient.token,
            self.MyInfluxDBClient.org,
            self.MyInfluxDBClient.host,
        )
        # self.registerService()
        self.client.mySubscribe(self.topic)

    def GET(self, *uri, **params):
        if uri[0] == "GetLastNMinutes":
            summary = self.MyInfluxDBClient.LastN(uri[1], uri[2])
            return json.dumps(summary)

    def notify(self, topic, payload):
        msg = json.loads(payload)
        # write in influxdb cloud
        measurement = msg["e"][0]["v"]
        sensor_id = msg["bn"]
        client_id = topic.split("/")[1]
        self.MyInfluxDBClient.writeInflux(client_id, sensor_id, measurement)
        print(
            f"{measurement} from sensor id {sensor_id} of {client_id} was received and pushed to influxdb"
        )


if __name__ == "__main__":
    conf = {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.sessions.on": True,
        }
    }
    cherrypy.config.update(
        {"server.socket_host": "127.0.0.1", "server.socket_port": 8082}
    )

    cherrypy.tree.mount(GlucoSub(), "/influx", conf)
    cherrypy.engine.start()
    cherrypy.engine.block()
