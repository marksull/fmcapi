"""RAVpn Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class RAVpn(APIClassTemplate):
    """The RAVpn Object in the FMC."""

    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
        "connectionProfiles",
        "groupPolicies",
        "accessInterfaceSettings",
        "ikev2Policies",
        "addressAssignmentSettings",
        "anyConnectClientImages",
        "externalBrowserPackage",
        "ipsecCryptoMaps",
        "certificateMapSettings",
        "ipsecAdvancedSettings",
        "secureClientCustomizationSettings",
        "dapPolicy",
        "ldapAttributeMaps",
        "loadBalanceSettings",
        "configureSSL",
        "configureIpsec"
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/policy/ravpns"
    FIRST_SUPPORTED_FMC_VERSION = "7.2"

    def __init__(self, fmc, **kwargs):
        """
        Initialize RAVpn object.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for RAVPN class.")
        self.type = "RAVpn"
        self.parse_kwargs(**kwargs)

    # POST, PUT and DELETE are valid endpoints in the api >7.4.1, however POST has a cycical dependency
    # with serveral other api endpoints - connectionprofiles, addressassignments, etc.
    # This is due to needing a container uuid of the RAVPN policy but also needing those objects to
    # create the RAVPN policy in the first place.

    def post(self):
        """POST method for API for RAVPN not supported."""
        logging.info("POST method for API for RAVPN not supported.")
        pass

    def put(self):
        """PUT method for API for RAVPN not supported."""
        logging.info("PUT method for API for RAVPN not supported.")
        pass

    def delete(self):
        """DELETE method for API for RAVPN not supported."""
        logging.info("DELETE method for API for RAVPN not supported.")
        pass