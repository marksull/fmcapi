from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class TerminateRAVPNSessions(APIClassTemplate):
    """The TerminateRAVPNSessions Object in the FMC."""

    FIRST_SUPPORTED_FMC_VERSION = "7.3"
    VALID_JSON_DATA = [
        "id",
        "name",
        "description",
        "usernames",
        "type",
        "deviceId",
        "terminateBy",
        "sessionIds",
        "version",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    REQUIRED_FOR_POST = ["terminateBy"]

    URL_SUFFIX = "/health/ravpnsessions/operational/terminateravpnsessions"

    def __init__(self, fmc, **kwargs):
        """
        Initialize TerminateRAVPNSessions object.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: requests response
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for TerminateRAVPNSessions class.")
        self.parse_kwargs(**kwargs)

    def get(self, **kwargs):
        """GET method for API for TerminateRAVPNSessions not supported."""
        logging.info("GET method for API for TerminateRAVPNSessions not supported.")
        pass

    def delete(self, **kwargs):
        """DELETE method for API for TerminateRAVPNSessions not supported."""
        logging.info("DELETE method for API for TerminateRAVPNSessions not supported.")
        pass

    def put(self):
        """PUT method for API for TerminateRAVPNSessions not supported."""
        logging.info("PUT method for API for TerminateRAVPNSessions not supported.")
        pass
