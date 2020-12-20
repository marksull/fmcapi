"""Continents Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class Continents(APIClassTemplate):
    """The Continents Object in the FMC."""

    VALID_JSON_DATA = ["id", "name", "countries"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/continents"
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        """
        Initialize Continents object.

        Set self.type to "Continent" and parse the kwargs.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Continents class.")
        self.parse_kwargs(**kwargs)
        self.type = "Continent"

    def post(self):
        """POST method for API for Continents not supported."""
        logging.info("POST method for API for Continents not supported.")
        pass

    def put(self):
        """PUT method for API for Continents not supported."""
        logging.info("PUT method for API for Continents not supported.")
        pass

    def delete(self):
        """DELETE method for API for Continents not supported."""
        logging.info("DELETE method for API for Continents not supported.")
        pass
