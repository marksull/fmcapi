"""Usage Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from fmcapi.api_objects.helper_functions import *
import logging


class Usage(APIClassTemplate):
    """The Usage Object in the FMC."""

    VALID_JSON_DATA = []
    VALID_GET_FILTERS = [
        "uuid",
        "type",
    ]  # uuid:String, type:String[Network,Port,VLAN,URL]
    REQUIRED_GET_FILTERS = ["uuid", "type"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + VALID_GET_FILTERS + []
    URL_SUFFIX = "/object/operational/usage"

    def __init__(self, fmc, **kwargs):
        """
        Initialize Usage object.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Usage class.")
        self.parse_kwargs(**kwargs)
