"""
Module with object PDB containing all the information.
"""
from __future__ import absolute_import
import os
import urllib
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
        if arg_file_name == ".":
            arg_file_name = arg_organism
        self.save_location = arg_save_location
        self.organism = arg_organism
        self.file_name = arg_file_name + ".pdb"
        self.make_url(arg_url)
        self.download_url()
        if not self.failed:
            self.parse_pdb()

    def make_url(self, arg_url):
        """
        Takes the download URL without the file of the PDB database and the organism entry
        and converts it in to a download link for the PDB file.
        Returns the full URL for download.
        """
        self.url = arg_url + self.organism + ".pdb"

    def download_url(self):
        """
        Receive the url, file name and save location and download the file of the url called
        "pdb_name" and saves it on "pdb_save_location".

        Return True if the download was successful and False if it wasn't and the real PDB
        file location with his name.
        """
        file_exists = False

        if os.path.exists(self.save_location):
            pass
        else:
            try:
                os.makedirs(self.save_location)
            except OSError:
                self.failed = True
                file_exists = False
            else:
                if os.path.exists(self.save_location + self.file_name):
                    file_exists = True

        if not file_exists:
            self.failed = True
            while self.failed_count < 5 and self.failed:
                try:
                    urllib.request.urlretrieve(self.url, self.save_location + self.file_name)
                except urllib.error.URLError:
                    self.failed = True
                    self.failed_count += 1
                else:
                    self.failed = False
                    self.failed_count = 0

    def parse_pdb(self):
        """
        Takes all the atom information from the PDB and adds it in to a dictionary.
        """
        parser = PDBParser()
        structure = parser.get_structure(self.organism, self.save_location + self.file_name)
        for atom in structure.get_atoms():
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
