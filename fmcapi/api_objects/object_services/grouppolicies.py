"""Group Policies Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class GroupPolicies(APIClassTemplate):
    """The GroupPolicies Object in the FMC."""

    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
        "generalSettings",  # Dict
        "anyConnectSettings",  # Dict
        "advancedSettings",  # Dict
        "enableSSLProtocol",  # Bool
        "enableIPsecIKEv2Protocol",  # Bool
    ]
    VALID_GET_FILTERS = [
        "unusedOnly",  # Bool
        "nameOrValue",  # String
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + VALID_GET_FILTERS + []
    URL_SUFFIX = "/object/grouppolicies"
    REQUIRED_FOR_PUT = [
        "id",
        "name",
        "generalSettings",  # Dict
        "anyConnectSettings",  # Dict
        "advancedSettings",  # Dict
        "enableSSLProtocol",  # Bool
        "enableIPsecIKEv2Protocol",  # Bool
    ]

    def __init__(self, fmc, **kwargs):
        """
        Initialize GroupPolicies object.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for GroupPolicies class.")
        self.type = "GroupPolicy"
        self.parse_kwargs(**kwargs)
