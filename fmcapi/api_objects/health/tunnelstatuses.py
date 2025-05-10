from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class TunnelStatuses(APIClassTemplate):
    """The TunnelStatuses Object in the FMC."""

    FIRST_SUPPORTED_FMC_VERSION = "7.3"
    VALID_JSON_DATA = [
        "id",
        "type",
        "state",
        "lastChange",
        "vpnTopology",
        "peerA",
        "peerB",
    ]
    VALID_GET_FILTERS = [
        "vpnTopologyId", # vpnTopologyId: uuid of vpn topo
        "deviceId", # deviceId: uuid of device
        "status", # status: TUNNEL_UP|TUNNEL_DOWN|UNKNOWN
        "deployedStatus", # deployedStatus: Deployed|Configured|Both
        "sortBy", # sortBy: :|<|> Topology|Device|Status|LastChange (sortBy<Device == sort by device in ascending order)
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + VALID_GET_FILTERS + []

    URL_SUFFIX = "/health/tunnelstatuses"

    def __init__(self, fmc, **kwargs):
        """
        Initialize TunnelStatuses object.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: requests response
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for TunnelStatuses class.")
        self.parse_kwargs(**kwargs)

    def delete(self, **kwargs):
        """DELETE method for API for TunnelStatuses not supported."""
        logging.info("DELETE method for API for TunnelStatuses not supported.")
        pass

    def put(self):
        """PUT method for API for TunnelStatuses not supported."""
        logging.info("PUT method for API for TunnelStatuses not supported.")
        pass

    def post(self, **kwargs):
        """POST method for API for TunnelStatuses not supported."""
        logging.info("POST method for API for TunnelStatuses not supported.")
        pass