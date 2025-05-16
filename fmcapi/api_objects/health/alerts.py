from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class Alerts(APIClassTemplate):
    """The Alerts Object in the FMC."""

    FIRST_SUPPORTED_FMC_VERSION = "7.3"
    VALID_JSON_DATA = [
    ]
    VALID_GET_FILTERS = [
        "deviceUUIDs",
        "startTime",
        "endTime",
        "status",
        "moduleIDs",
    ]

    VALID_FOR_KWARGS = VALID_JSON_DATA + VALID_GET_FILTERS + []

    URL_SUFFIX = "/health/alerts"

    def __init__(self, fmc, **kwargs):
        """
        Initialize Alerts object.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: requests response
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Alerts class.")
        self.parse_kwargs(**kwargs)

    def get(self, **kwargs):
        """
        Prepare to send GET call to retrieve Prometheus Health Alerts from FMC.

        :param: deviceUUIDs=Optional List UUID of the device to be queried.
        :param: startTime=Optional start time in unix format seconds
        :param: endTime=Optional end time in unix format seconds
        :param: status=Optional List of status codes to filter delimited by comma, e.g. green,red,yellow.
        :param: moduleIDs=Optional List of module ids to filter, delimited by comma.
        :return: requests response
        """
        logging.debug("In get() for Alerts class.")

        return super().get(**kwargs)

    def delete(self, **kwargs):
        """DELETE method for API for Alerts not supported."""
        logging.info("DELETE method for API for Alerts not supported.")
        pass

    def put(self):
        """PUT method for API for Alerts not supported."""
        logging.info("PUT method for API for Alerts not supported.")
        pass

    def post(self, **kwargs):
        """POST method for API for Alerts not supported."""
        logging.info("POST method for API for Alerts not supported.")
        pass