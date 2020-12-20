"""FTD NAT Policies Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class FTDNatPolicies(APIClassTemplate):
    """The FTDNatPolicies Object in the FMC."""

    VALID_JSON_DATA = ["id", "name", "type"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/policy/ftdnatpolicies"
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        """
        Initialize FTDNatPolicies object.

        Set self.type to "FTDNatPolicy", parse the kwargs, and set up the self.URL.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for FTDNatPolicies class.")
        self.parse_kwargs(**kwargs)
        self.type = "FTDNatPolicy"
