"""
Module with object PDB containing all the information.
"""
from __future__ import absolute_import
import os
import urllib
import logging
from Bio.PDB import PDBParser

class PDB():
    """
    Class containing the atributes and methos to storage and parse the PDB.
    """
    pdb_dictionary = {"ATOM" : {}}
    organism = None
    save_location = None
    url = None
    file_name = None
    failed = False
    failed_count = 0

    def __init__(self, arg_organism, arg_url="https://files.rcsb.org/download/", \
    arg_save_location="tmp/", arg_file_name="."):
        """
        Initialization of PDB Object.
        """
        logging.info("Initializing PDB Object...")

        logging.info("Checking if file name was specified...")
        if arg_file_name == ".":
            logging.info("File name not specified, it will be the organism name.")
            arg_file_name = arg_organism
        
        logging.info("Setting save location to %s", arg_save_location)
        self.save_location = arg_save_location

        logging.info("Setting organism to %s", arg_organism)
        self.organism = arg_organism

        logging.info("Setting file name to %s.pdb", arg_file_name)
        self.file_name = arg_file_name + ".pdb"

        logging.info("Calling make_url function...")
        self.make_url(arg_url)

        logging.info("Calling download_url function...")
        self.download_url()

        if not self.failed:
            logging.info("Process not failed, initializing PDB parser function...")
            self.parse_pdb()

    def make_url(self, arg_url):
        """
        Takes the download URL without the file of the PDB database and the organism entry
        and converts it in to a download link for the PDB file.
        Returns the full URL for download.
        """
        logging.info("Creating URL...")
        self.url = arg_url + self.organism + ".pdb"
        logging.info("The URL for download is %s", self.url)
        

    def download_url(self):
        """
        Receive the url, file name and save location and download the file of the url called
        "pdb_name" and saves it on "pdb_save_location".

        Return True if the download was successful and False if it wasn't and the real PDB
        file location with his name.
        """

        logging.info("Starting the download procedure...")

        file_exists = False

        logging.info("Checking if save location '%s' exists...", self.save_location)
        if not os.path.exists(self.save_location):
            logging.info("Save location don't exists, trying to create it...")
            try:
                os.makedirs(self.save_location)
            except OSError:
                logging.error("Failed to create the save location '%s' using makedirs. \
                               Download can't proceed.", self.save_location)
                self.failed = True
                file_exists = False
            else:
                logging.info("Checking if file exists...")
                if os.path.exists(self.save_location + self.file_name):
                    logging.warning("File exists, download will not proceed.")
                    file_exists = True

        if not file_exists and not self.failed:
            logging.info("Trying to download the file from %s on %s", self.url, self.save_location)
            while self.failed_count < 5 and self.failed:
                try:
                    urllib.request.urlretrieve(self.url, self.save_location + self.file_name)
                except urllib.error.URLError:
                    logging.error("Download failed! Trying again. %s tryies left.", \
                                 (5 - self.failed_count))
                    self.failed = True
                    self.failed_count += 1
                else:
                    logging.info("Download successful in %i tryies.", self.failed_count + 1)
                    self.failed = False
                    self.failed_count = 0

    def parse_pdb(self):
        """
        Takes all the atom information from the PDB and adds it in to a dictionary.
        """
        logging.info("parse_pdb starting...")
        parser = PDBParser()

        logging.info("Transforming PDB in to an object...")
        structure = parser.get_structure(self.organism, self.save_location + self.file_name)

        logging.info("Parsing ATOM entries...")
        for atom in structure.get_atoms():
            logging.debug("Parsing atom number %i named %s.", atom.get_serial_number(), \
                                                              atom.get_name())
            self.pdb_dictionary["ATOM"][atom.get_serial_number()] = {\
            "serial_number" : atom.get_serial_number(),\
            "name" : atom.get_name(),\
            "id" : atom.get_id(),\
            "x" : float(atom.get_coord()[0]),\
            "y" : float(atom.get_coord()[1]),\
            "z" : float(atom.get_coord()[2]),\
            "bfactor" : atom.get_bfactor(),\
            "occupancy" : atom.get_occupancy(),\
            "fullname" : atom.get_fullname(),\
            "altloc" : atom.get_altloc(),\
            "level" : atom.get_level()}
