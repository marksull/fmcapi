from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class AnyProtocolPortObjects(APIClassTemplate):
    """
    The AnyProtocolPortObjects Object in the FMC.
    """

    VALID_JSON_DATA = ["id", "name", "type", "overrideTargetId"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/anyprotocolportobjects"

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for AnyProtocolPortObjects class.")
        self.parse_kwargs(**kwargs)

    def post(self):
        logging.info("POST method for API for AnyProtocolPortObjects not supported.")
        pass

    def put(self):
        logging.info("PUT method for API for AnyProtocolPortObjects not supported.")
        pass

    def delete(self):
        logging.info("DELETE method for API for AnyProtocolPortObjects not supported.")
        pass
