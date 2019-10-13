from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class ExtendedAccessList(APIClassTemplate):
    """
    The ExtendedAccessList Object in the FMC.
    """

    VALID_JSON_DATA = ["id", "name", "type"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/extendedaccesslist"

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ExtendedAccessList class.")
        self.parse_kwargs(**kwargs)

    def post(self):
        logging.info("POST method for API for ExtendedAccessList not supported.")
        pass

    def put(self):
        logging.info("PUT method for API for ExtendedAccessList not supported.")
        pass

    def delete(self):
        logging.info("DELETE method for API for ExtendedAccessList not supported.")
        pass
