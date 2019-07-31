"""
Flask API main module.
"""
from __future__ import absolute_import
import logging
from flask import Flask
from flask_restplus import Api, Resource, fields
from pytom2.source.pdb_parser_module import PDB

logging.info("Initializing Flask objects...")
APP = Flask(__name__)
API = Api(APP)

logging.info("Initializing model for organism and dictionary...")
MODEL_ORGANISM = API.model("Organism", {"organism" : fields.String("Organism name")})
ORGANISMS = {}

logging.info("Initializing Swagger UI...")
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
        logging.info("GET Request received, creating parser...")
        parser = API.parser()

        logging.info("Adding arguments to parser...")
        parser.add_argument('user', location='args', help='Queried user')

        logging.info("Returning results...")
        return ORGANISMS

    @API.expect(MODEL_ORGANISM)
    def post(self):                                                             #pylint: disable=R0201
        """
        Post method.
        """
        logging.info("POST request received, creating payload...")
        new_organism = API.payload

        logging.info("Setting ID of new organism to %i...", len(ORGANISMS) + 1)
        new_organism["id"] = len(ORGANISMS) + 1

        #ORGANISMS[0]["ATOM"] = {}
        #ORGANISMS[0]["HETATM"] = {}
        #ORGANISMS[0]["TER"] = {}
        #ORGANISMS[0]["HELIX"] = {}
        #ORGANISMS[0]["SHEET"] = {}
        #ORGANISMS[0]["SSBOND"] = {}

        logging.info("Creating new object organism...")
        pdb_object = PDB(new_organism["organism"])

        logging.info("Setting payload data...")
        ORGANISMS[new_organism["organism"]] = pdb_object.pdb_dictionary

        logging.info("Returning results...")
        return {"result" : "organism added"}, 201

def start_api():
    """
    Initialize flask framework.
    """
    logging.info("Starting flask API RestPlus")
    APP.run(debug=True)
