"""Security Zones Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class SecurityZones(APIClassTemplate):
    """The SecurityZones Object in the FMC."""

    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
        "description",
        "interfaceMode",
        "interfaces",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/securityzones"
    REQUIRED_FOR_POST = ["name", "interfaceMode"]
    FILTER_BY_NAME = True

    def __init__(self, fmc, **kwargs):
        """
        Initialize SecurityZones object.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for SecurityZones class.")
        self.parse_kwargs(**kwargs)

    def parse_kwargs(self, **kwargs):
        """
        Parse the kwargs and set self variables to match.

        :return: None
        """
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for SecurityZones class.")
        if "interfaceMode" in kwargs:
            self.interfaceMode = kwargs["interfaceMode"]
        else:
            self.interfaceMode = "ROUTED"
