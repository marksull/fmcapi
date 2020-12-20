"""Hosts Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from fmcapi.api_objects.helper_functions import *
import logging


class Hosts(APIClassTemplate):
    """The Host Object in the FMC."""

    VALID_JSON_DATA = ["id", "name", "type", "value", "description"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/hosts"
    REQUIRED_FOR_POST = ["name", "value"]
    REQUIRED_FOR_PUT = ["id", "name", "value"]

    def __init__(self, fmc, **kwargs):
        """
        Initialize Hosts object.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for IPHost class.")
        self.parse_kwargs(**kwargs)

    def parse_kwargs(self, **kwargs):
        """
        Parse the kwargs and set self variables to match.

        :return: None
        """
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for Hosts class.")
        if "value" in kwargs:
            value_type = get_networkaddress_type(kwargs["value"])
            if value_type == "range" or value_type == "network":
                logging.warning(
                    f"value, {kwargs['value']}, is of type {value_type}. Limited functionality for this "
                    f"object due to it being created via the IPHost function."
                )
            if validate_ip_bitmask_range(value=kwargs["value"], value_type=value_type):
                self.value = kwargs["value"]
            else:
                logging.error(
                    f"Provided value, {kwargs['value']}, has an error with the IP address(es)."
                )
