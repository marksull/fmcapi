from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class ISESecurityGroupTags(APIClassTemplate):
    """
    The ISESecurityGroupTags Object in the FMC.
    """

    VALID_JSON_DATA = ["id", "name", "type", "tag", "iseId", "overrides", "overridable"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/isesecuritygrouptags"

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ISESecurityGroupTags class.")
        self.parse_kwargs(**kwargs)

    def post(self):
        logging.info("POST method for API for ISESecurityGroupTags not supported.")
        pass

    def put(self):
        logging.info("PUT method for API for ISESecurityGroupTags not supported.")
        pass

    def delete(self):
        logging.info("DELETE method for API for ISESecurityGroupTags not supported.")
        pass
