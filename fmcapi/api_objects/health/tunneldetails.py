from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class TunnelDetails(APIClassTemplate):
    """The TunnelDetails Object in the FMC."""

    FIRST_SUPPORTED_FMC_VERSION = "7.3"
    REQUIRED_FOR_GET = ["container_uuid"]
    VALID_JSON_DATA = [
        "type",
        "peerA",
        "peerB",
    ]

    VALID_FOR_KWARGS = VALID_JSON_DATA + ["container_uuid"]

    URL_SUFFIX = f"/health/tunnelstatuses"

    def __init__(self, fmc, **kwargs):
        """
        Initialize TunnelDetails object.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: requests response
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for TunnelDetails class.")
        self.parse_kwargs(**kwargs)
        URL_CONTAINER_SUFFIX = f"/{self.container_uuid}/tunneldetails"
        self.URL = self.URL + URL_CONTAINER_SUFFIX

    def delete(self, **kwargs):
        """DELETE method for API for TunnelDetails not supported."""
        logging.info("DELETE method for API for TunnelDetails not supported.")
        pass

    def put(self):
        """PUT method for API for TunnelDetails not supported."""
        logging.info("PUT method for API for TunnelDetails not supported.")
        pass

    def post(self, **kwargs):
        """POST method for API for TunnelDetails not supported."""
        logging.info("POST method for API for TunnelDetails not supported.")
        pass