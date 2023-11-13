"""Network Addresses Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class NetworkAddresses(APIClassTemplate):
    """The NetworkAddresses Object in the FMC."""

    VALID_JSON_DATA = []
    VALID_GET_FILTERS = [
        "unusedOnly",
        "nameOrValue",
        "type",
        "includeWildcard",
    ]  # unusedOnly:Bool, nameOrValue:String, type:String CSV [FQDN,RANGE,HOST,NETWORK], includeWildcard:Bool
    VALID_FOR_KWARGS = VALID_JSON_DATA + VALID_GET_FILTERS + []
    URL_SUFFIX = "/object/networkaddresses"

    def __init__(self, fmc, **kwargs):
        """
        Initialize NetworkAddresses object.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for NetworkAddresses class.")
        self.parse_kwargs(**kwargs)

    def post(self):
        """POST method for API for NetworkAddresses not supported."""
        logging.info("POST method for API for NetworkAddresses not supported.")
        pass

    def put(self):
        """PUT method for API for NetworkAddresses not supported."""
        logging.info("PUT method for API for NetworkAddresses not supported.")
        pass

    def delete(self):
        """DELETE method for API for NetworkAddresses not supported."""
        logging.info("DELETE method for API for NetworkAddresses not supported.")
        pass
