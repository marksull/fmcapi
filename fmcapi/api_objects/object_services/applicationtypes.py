from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging
import warnings


class ApplicationTypes(APIClassTemplate):
    """
    The ApplicationTypes Object in the FMC.
    """

    VALID_JSON_DATA = ["id", "name", "type"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/applicationtypes"

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ApplicationTypes class.")
        self.parse_kwargs(**kwargs)

    def post(self):
        logging.info("POST method for API for ApplicationTypes not supported.")
        pass

    def put(self):
        logging.info("PUT method for API for ApplicationTypes not supported.")
        pass

    def delete(self):
        logging.info("DELETE method for API for ApplicationTypes not supported.")
        pass


class ApplicationType(ApplicationTypes):
    """Dispose of this Class after 20210101."""

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn(
            "Deprecated: ApplicationType() should be called via ApplicationTypes()."
        )
        super().__init__(fmc, **kwargs)
