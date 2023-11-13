"""Extended Access List Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class ExtendedAccessList(APIClassTemplate):
    """The ExtendedAccessList Object in the FMC."""

    VALID_JSON_DATA = ["id", "name", "entries"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/extendedaccesslists"
    REQUIRED_FOR_POST = ["name", "entries"]
    REQUIRED_FOR_PUT = ["id", "entries"]

    def __init__(self, fmc, **kwargs):
        """
        Initialize ExtendedAccessList object.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ExtendedAccessList class.")
        self.parse_kwargs(**kwargs)


class ExtendedAccessListAce(object):
    """The ExtendedAccessListAce Object for creating ACEs or Lines in Extended ACLs"""

    VALID_JSON_DATA = [
        "action",
        "logging",
        "logLevel",
        "logInterval",
        "sourceNetworks",
        "sourcePorts",
        "destinationNetworks",
        "destinationPorts",
    ]

    def __init__(self, **kwargs) -> None:
        """
        Initialize ExtendedAccessListAce Object with default values.
        These defaults to permit any source/destination network and ports!!!

        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        self.action = "PERMIT"
        self.logging = "DEFAULT"
        self.logLevel = "INFORMATIONAL"
        self.logInterval = 300
        self.sourceNetworks = {}
        self.sourceNetworksObjects = []
        self.sourceNetworksLiterals = []
        self.sourcePorts = {}
        self.sourcePortsObjects = []
        self.sourcePortsLiterals = []
        self.destinationNetworks = {}
        self.destinationNetworksObjects = []
        self.destinationNetworksLiterals = []
        self.destinationPorts = {}
        self.destinationPortsObjects = []
        self.destinationPortsLiterals = []

    def build_ace(self, **kwargs):
        """
        Constructs dict that represents 1 ACE/Line in an Extended ACL.

        :param kwargs: Any other values passed during instantiation.
        :return: (dict) json_data
        """
        if self.sourceNetworksObjects:
            self.sourceNetworks["objects"] = self.sourceNetworksObjects

        if self.sourceNetworksLiterals:
            self.sourceNetworks["literals"] = self.sourceNetworksLiterals

        if self.sourcePortsObjects:
            self.sourcePorts["objects"] = self.sourcePortsObjects

        if self.sourcePortsLiterals:
            self.sourcePorts["literals"] = self.sourcePortsLiterals

        if self.destinationNetworksObjects:
            self.destinationNetworks["objects"] = self.destinationNetworksObjects

        if self.destinationNetworksLiterals:
            self.destinationNetworks["literals"] = self.destinationNetworksLiterals

        if self.destinationPortsObjects:
            self.destinationPorts["objects"] = self.destinationPortsObjects

        if self.destinationPortsLiterals:
            self.destinationPorts["literals"] = self.destinationPortsLiterals

        json_data = {}
        for key_value in self.__dict__:
            if key_value in self.VALID_JSON_DATA:
                if self.__dict__.get(key_value):
                    json_data[key_value] = self.__dict__.get(key_value)
        return json_data
