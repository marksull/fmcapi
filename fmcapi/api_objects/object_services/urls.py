"""URLs Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging
import warnings


class URLs(APIClassTemplate):
    """The URLs Object in the FMC."""

    VALID_JSON_DATA = ["id", "name", "url", "description"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/urls"
    REQUIRED_FOR_POST = ["name", "url"]

    def __init__(self, fmc, **kwargs):
        """
        Initialize URLs object.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for URLs class.")
        self.parse_kwargs(**kwargs)


class URL(URLs):
    """
    Dispose of this Class after 20210101.

    Use URLs() instead.
    """

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn("Deprecated: URL() should be called via URLs().")
        super().__init__(fmc, **kwargs)
