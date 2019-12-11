"""Application Tags Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging
import warnings


class ApplicationTags(APIClassTemplate):
    """The ApplicationTags Object in the FMC."""

    VALID_JSON_DATA = ["id", "name", "type"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/applicationtags"
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\-\/\. ]"""

    def __init__(self, fmc, **kwargs):
        """
        Initialize ApplicationTags object.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ApplicationTags class.")
        self.parse_kwargs(**kwargs)

    def post(self):
        """POST method for API for ApplicationTags not supported."""
        logging.info("POST method for API for ApplicationTags not supported.")
        pass

    def put(self):
        """PUT method for API for ApplicationTags not supported."""
        logging.info("PUT method for API for ApplicationTags not supported.")
        pass

    def delete(self):
        """DELETE method for API for ApplicationTags not supported."""
        logging.info("DELETE method for API for ApplicationTags not supported.")
        pass


class ApplicationTag(ApplicationTags):
    """
    Dispose of this Class after 20210101.

    Use ApplicationTags() instead.
    """

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn(
            "Deprecated: ApplicationTag() should be called via ApplicationTags()."
        )
        super().__init__(fmc, **kwargs)
