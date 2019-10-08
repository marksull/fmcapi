from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging
import warnings


class ApplicationTags(APIClassTemplate):
    """
    The ApplicationTags Object in the FMC.
    """

    VALID_JSON_DATA = ["id", "name", "type"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/applicationtags"
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\-\/\. ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ApplicationTags class.")
        self.parse_kwargs(**kwargs)

    def post(self):
        logging.info("POST method for API for ApplicationTags not supported.")
        pass

    def put(self):
        logging.info("PUT method for API for ApplicationTags not supported.")
        pass

    def delete(self):
        logging.info("DELETE method for API for ApplicationTags not supported.")
        pass


class ApplicationTag(ApplicationTags):
    """Dispose of this Class after 20210101."""

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn(
            "Deprecated: ApplicationTag() should be called via ApplicationTags()."
        )
        super().__init__(fmc, **kwargs)
