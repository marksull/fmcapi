from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class Ports(APIClassTemplate):
    """
    The Ports Object in the FMC.
    """

    URL_SUFFIX = "/object/ports"

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Ports class.")
        self.parse_kwargs(**kwargs)

    def post(self):
        logging.info("POST method for API for Ports not supported.")
        pass

    def put(self):
        logging.info("PUT method for API for Ports not supported.")
        pass

    def delete(self):
        logging.info("DELETE method for API for Ports not supported.")
        pass
