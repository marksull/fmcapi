"""ConnectionProfiles Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class ConnectionProfiles(APIClassTemplate):
    """The ConnectionProfiles Object in the FMC."""

    REQUIRED_FOR_GET = ["container_uuid"]
    REQUIRED_FOR_POST = ["container_uuid","name"]
    REQUIRED_FOR_PUT = ["container_uuid", "id"]
    REQUIRED_FOR_DELETE = ["container_uuid", "id"]
    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
        "groupPolicy",
        "authenticationMethod",
        "ipv4AddressPool",
        "enableSecondaryAuthentication",
        "enableSecondaryAuthFallbackToLocal",
        "useLocalAsSecondaryAuthServer",
        "enablePrimaryAuthFallbackToLocal",
        "useLocalAsPrimaryAuthServer",
        "primaryAuthenticationServer",
        "allowConnectionOnlyIfAuthorized",
        "enablePasswordManagement",
        "stripGroupFromUsername",
        "stripRealmFromUsername"
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA  + ["container_uuid"]
    URL_SUFFIX = "/policy/ravpns"
    FIRST_SUPPORTED_FMC_VERSION = "7.2"

    def __init__(self, fmc, **kwargs):
        """
        Initialize ConnectionProfiles object.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ConnectionProfiles class.")
        self.type = "ConnectionProfiles"
        self.parse_kwargs(**kwargs)
        URL_CONTAINER_SUFFIX = f"/{self.container_uuid}/connectionprofiles"
        self.URL = self.URL + URL_CONTAINER_SUFFIX

    # POST, PUT and DELETE are valid endpoints in the api >7.4.1, however POST has a cycical dependency
    # with serveral other api endpoints - connectionprofiles, addressassignments, etc.
    # This is due to needing a container uuid of the ConnectionProfiles policy but also needing those objects to
    # create the ConnectionProfiles policy in the first place.

    def post(self):
        """POST method for API for ConnectionProfiles not supported."""
        logging.info("POST method for API for ConnectionProfiles not supported.")
        pass

    # def put(self):
    #     """PUT method for API for ConnectionProfiles not supported."""
    #     logging.info("PUT method for API for ConnectionProfiles not supported.")
    #     pass

    def delete(self):
        """DELETE method for API for ConnectionProfiles not supported."""
        logging.info("DELETE method for API for ConnectionProfiles not supported.")
        pass