from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class FTDDeviceCluster(APIClassTemplate):
    """
    The FTDDeviceCluster Object in the FMC.
    """

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
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for FTDDeviceCluster class.")
        self.parse_kwargs(**kwargs)
        self.type = "DeviceCluster"

    def post(self):
        logging.info("POST method for API for FTDDeviceCluster not supported.")
        pass

    def put(self):
        logging.info("PUT method for API for FTDDeviceCluster not supported.")
        pass

    def delete(self):
        logging.info("DELETE method for API for FTDDeviceCluster not supported.")
        pass
