import json
import cherrypy
from CatalogueTools.pushServiceInCatalogue import pushServiceInCatalogue
from CatalogueTools.pushClientInCatalogue import pushClientInCatalogue
from CatalogueTools.doesItExist import doesItExist
from CatalogueTools.getSensor import getSensor


class Catalogue(object):
    exposed = True

    def __init__(self, path):
        self.path = path

    def GET(self, *uri, **params):
        with open(self.path, "r") as file:
            catalogue = json.load(file)
            # checks if the patient or doctor exists in the catalogue
        if uri[0] == "patients":
            return doesItExist(catalogue, uri[0], uri[1], uri[2]).result
        elif uri[0] == "sensors":
            return getSensor().getSensor(catalogue, uri[1])

    @cherrypy.tools.json_in()
    def POST(self, *uri, **params):
        body = cherrypy.request.json
        with open(self.path, "r") as file:
            catalogue = json.load(file)
        if uri[0] == "register":
            pushClientInCatalogue(body, catalogue)
        elif uri[0] == "services":
            pushServiceInCatalogue(body, catalogue)
        else:
            return "invalid entry"


if __name__ == "__main__":

    path = "Catalogue.json"  # Provide the correct relative or absolute file path
    conf = {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.sessions.on": True,
        }
    }
    cherrypy.tree.mount(Catalogue(path), "/catalogue/", conf)
    cherrypy.engine.start()
    cherrypy.engine.block()
