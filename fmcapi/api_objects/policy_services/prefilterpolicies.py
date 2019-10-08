from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging
import warnings


class PreFilterPolicies(APIClassTemplate):
    """
    The PreFilterPolicies Object in the FMC.
    """

    VALID_JSON_DATA = ["id", "name"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/policy/prefilterpolicies"
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for PreFilterPolicies class.")
        self.parse_kwargs(**kwargs)
        self.type = "PreFilterPolicy"

    def post(self):
        logging.info("POST method for API for PreFilterPolicies not supported.")
        pass

    def put(self):
        logging.info("PUT method for API for PreFilterPolicies not supported.")
        pass

    def delete(self):
        logging.info("DELETE method for API for PreFilterPolicies not supported.")
        pass


class PreFilterPolicy(PreFilterPolicies):
    """Dispose of this Class after 20210101."""

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn(
            "Deprecated: PreFilterPolicy() should be called via PreFilterPolicies()."
        )
        super().__init__(fmc, **kwargs)
