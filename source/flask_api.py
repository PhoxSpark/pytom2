"""
Flask API main module.
"""
from __future__ import absolute_import
from flask import Flask
from flask_restplus import Api, Resource, fields
from pytom2.source.pdb_parser_module import PDB

APP = Flask(__name__)
API = Api(APP)

MODEL_ORGANISM = API.model("Organism", {"organism" : fields.String("Organism name")})
ORGANISMS = {}

APP.config["SWAGGER_UI_JSONEDITOR"] = True

@API.route('/pytom')
class Pytom(Resource):
    """
    Pytom main class for /pytom route.
    """

    def get(self):                                                              #pylint: disable=R0201
        """
        Get method.
        """
        parser = API.parser()
        parser.add_argument('user', location='args', help='Queried user')
        return ORGANISMS

    @API.expect(MODEL_ORGANISM)
    def post(self):                                                             #pylint: disable=R0201
        """
        Post method.
        """
        new_organism = API.payload
        new_organism["id"] = len(ORGANISMS) + 1

        #ORGANISMS[0]["ATOM"] = {}
        #ORGANISMS[0]["HETATM"] = {}
        #ORGANISMS[0]["TER"] = {}
        #ORGANISMS[0]["HELIX"] = {}
        #ORGANISMS[0]["SHEET"] = {}
        #ORGANISMS[0]["SSBOND"] = {}

        pdb_object = PDB(new_organism["organism"])
        ORGANISMS[new_organism["organism"]] = pdb_object.pdb_dictionary

        return {"result" : "organism added"}, 201

def start_api():
    """
    Initialize flask framework.
    """
    APP.run(debug=True)

if __name__ == "__main__":
    APP.run(debug=True)
