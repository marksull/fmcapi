"""FTDDeviceCluster Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class FTDDeviceCluster(APIClassTemplate):
    """The FTDDeviceCluster Object in the FMC."""

    VALID_JSON_DATA = ["id", "name"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + [
        "slavedevices",
        "modelType",
        "version",
        "sw_version",
        "healthStatus",
        "healthPolicy",
        "model",
        "modelNumber",
        "accessPolicy",
    ]
    URL_SUFFIX = "/deviceclusters/ftddevicecluster"

    def __init__(self, fmc, **kwargs):
        """
        Initialize FTDDeviceCluster object.

        Set self.type to "DeviceCluster" and parse the kwargs.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for FTDDeviceCluster class.")
        self.parse_kwargs(**kwargs)
        self.type = "DeviceCluster"

    def post(self):
        """POST method for API for FTDDeviceCluster not supported."""
        logging.info("POST method for API for FTDDeviceCluster not supported.")
        pass

    def put(self):
        """PUT method for API for FTDDeviceCluster not supported."""
        logging.info("PUT method for API for FTDDeviceCluster not supported.")
        pass

    def delete(self):
        """DELETE method for API for FTDDeviceCluster not supported."""
        logging.info("DELETE method for API for FTDDeviceCluster not supported.")
        pass
