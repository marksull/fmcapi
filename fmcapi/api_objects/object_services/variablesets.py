"""Variable Sets Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging
import warnings


class VariableSets(APIClassTemplate):
    """The VariableSets Object in the FMC."""

    VALID_JSON_DATA = ["id", "name", "type", "description"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/variablesets"

    def __init__(self, fmc, **kwargs):
        """
        Initialize VariableSets object.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for VariableSets class.")
        self.parse_kwargs(**kwargs)

    def post(self):
        """POST method for API for VariableSets not supported."""
        logging.info("POST method for API for VariableSets not supported.")
        pass

    def put(self):
        """PUT method for API for VariableSets not supported."""
        logging.info("PUT method for API for VariableSets not supported.")
        pass

    def delete(self):
        """DELETE method for API for VariableSets not supported."""
        logging.info("DELETE method for API for VariableSets not supported.")
        pass


class VariableSet(VariableSets):
    """
    Dispose of this Class after 20210101.

    Use VariableSets() instead.
    """

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn("Deprecated: VariableSet() should be called via VariableSets().")
        super().__init__(fmc, **kwargs)
