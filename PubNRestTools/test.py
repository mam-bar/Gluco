from sensorService import Sensor
import cherrypy
import time


class test:
    exposed = True

    def __init__(self):
        self.sensor = Sensor()

    def GET(self, *uri, **params):
        if uri[0] == "inject":
            self.sensor.dropInsulin()
            print("Injected")


if __name__ == "__main__":
    conf = {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.sessions.on": True,
        }
    }
    a = test()
    cherrypy.tree.mount(a, "/", conf)
    cherrypy.engine.start()
    while True:
        print(a.sensor.sense())
        time.sleep(1)
