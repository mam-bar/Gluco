from GlucoSensNPubNRest import Gluco
import cherrypy


if __name__ == "__main__":
    conf = {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.sessions.on": True,
        }
    }
    cherrypy.config.update(
        {"server.socket_host": "127.0.0.1", "server.socket_port": 8081}
    )

    clients = ["Mohammad", "Alireza", "Aisa"]
    passwords = ["12345", "12345", "12345"]
    sensors = ["83473", "83475", "83476"]

    clients_list = [
        Gluco(sensors[i], clients[i], passwords[i]) for i in range(len(clients))
    ]

    for i in range(len(clients_list)):
        cherrypy.tree.mount(clients_list[i], f"/inject/{clients[i]}", conf)

    cherrypy.engine.start()

    while True:
        for i in range(len(clients_list)):
            clients_list[i].sens_n_pub()
