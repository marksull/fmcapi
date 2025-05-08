from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class TunnelSummaries(APIClassTemplate):
    """The TunnelSummaries Object in the FMC."""

    FIRST_SUPPORTED_FMC_VERSION = "7.3"
    VALID_JSON_DATA = [
        "tunnelCount",
        "tunnelUpCount",
        "tunnelDownCount",
        "tunnelUnknownCount",
        "type",
    ]
    VALID_GET_FILTERS = [
        "vpnTopologyId", # vpnTopologyId: uuid of vpn topo
        "deviceId", # deviceId: uuid of device
        "groupBy", # Topology|Device
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + VALID_GET_FILTERS + []

    URL_SUFFIX = "/health/tunnelsummaries"

    def __init__(self, fmc, **kwargs):
        """
        Initialize TunnelSummaries object.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: requests response
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for TunnelSummaries class.")
        self.parse_kwargs(**kwargs)

    def delete(self, **kwargs):
        """DELETE method for API for TunnelSummaries not supported."""
        logging.info("DELETE method for API for TunnelSummaries not supported.")
        pass

    def put(self):
        """PUT method for API for TunnelSummaries not supported."""
        logging.info("PUT method for API for TunnelSummaries not supported.")
        pass

    def post(self, **kwargs):
        """POST method for API for TunnelSummaries not supported."""
        logging.info("POST method for API for TunnelSummaries not supported.")
        pass