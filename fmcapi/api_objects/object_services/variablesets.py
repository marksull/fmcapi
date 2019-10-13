from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging
import warnings


class VariableSets(APIClassTemplate):
    """
    The VariableSets Object in the FMC.
    """

    VALID_JSON_DATA = ["id", "name", "type", "description"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/variablesets"

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for VariableSets class.")
        self.parse_kwargs(**kwargs)

    def post(self):
        logging.info("POST method for API for VariableSets not supported.")
        pass

    def put(self):
        logging.info("PUT method for API for VariableSets not supported.")
        pass

    def delete(self):
        logging.info("DELETE method for API for VariableSets not supported.")
        pass


class VariableSet(VariableSets):
    """Dispose of this Class after 20210101."""

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn("Deprecated: VariableSet() should be called via VariableSets().")
        super().__init__(fmc, **kwargs)
