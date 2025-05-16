from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class Metrics(APIClassTemplate):
    """The Metrics Object in the FMC."""

    FIRST_SUPPORTED_FMC_VERSION = "7.3"
    VALID_JSON_DATA = [
        "deviceUUID",
        "type",
        "metric",
    ]
    VALID_GET_FILTERS = [
        "deviceUUIDs",
        "metric",
        "startTime",
        "endTime",
        "step",
        "regexFilter",
        "queryFunction",
        "rateFunctionInterval",
    ]

    REQUIRED_GET_FILTERS = ["metric", "startTime", "endTime", "step"]

    VALID_FOR_KWARGS = VALID_JSON_DATA + VALID_GET_FILTERS + []

    URL_SUFFIX = "/health/metrics"

    def __init__(self, fmc, **kwargs):
        """
        Initialize Metrics object.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: requests response
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Metrics class.")
        self.parse_kwargs(**kwargs)

    def get(self, **kwargs):
        """
        Prepare to send GET call to retrieve Prometheus Health Metrics from FMC.

        :param: metric=Required name of the prometheus metric to be queried[cpu, mem, interface, asp_drops, vpn, etc.]
        :param: startTime=Required start time in unix format seconds
        :param: endTime=Required end time in unix format seconds
        :param: step=Required step interval in seconds over which the data is returned
        :param: deviceUUIDs=Optional List UUID of the device to be queried.
        :param: regexFilter=Optional filter to be applied on the metric names[snort.*|lina.*]
        :param: queryFunction=Optional query function which has to be applied to the query[avg, rate, min, max]
        :param: rateFunctionInterval=Optional interval which has to be applied to the rate function[1m, 5m, etc.]
        :return: requests response
        """
        logging.debug("In get() for Metrics class.")

        return super().get(**kwargs)

    def delete(self, **kwargs):
        """DELETE method for API for Metrics not supported."""
        logging.info("DELETE method for API for Metrics not supported.")
        pass

    def put(self):
        """PUT method for API for Metrics not supported."""
        logging.info("PUT method for API for Metrics not supported.")
        pass

    def post(self, **kwargs):
        """POST method for API for Metrics not supported."""
        logging.info("POST method for API for Metrics not supported.")
        pass
