"""Interface Objects Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class InterfaceObjects(APIClassTemplate):
    """The InterfaceObjects Object in the FMC."""

    URL_SUFFIX = "/object/interfaceobjects"
    FILTER_BY_NAME = True

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for InterfaceObjects class.")
        self.parse_kwargs(**kwargs)

    def post(self):
        """POST method for API for InterfaceObjects not supported."""
        logging.info("POST method for API for InterfaceObjects not supported.")
        pass

    def put(self):
        """PUT method for API for InterfaceObjects not supported."""
        logging.info("PUT method for API for InterfaceObjects not supported.")
        pass

    def delete(self):
        """DELETE method for API for InterfaceObjects not supported."""
        logging.info("DELETE method for API for InterfaceObjects not supported.")
        pass
