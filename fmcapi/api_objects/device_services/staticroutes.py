"""Static Routes Classes."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .devicerecords import DeviceRecords
import logging


class StaticRoutes(APIClassTemplate):
    """The StaticRoutes Object in the FMC."""

    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
        "continentId",
        "continents",
        "countries",
        "continentUUID",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    PREFIX_URL = "/devices/devicerecords"
    URL_SUFFIX = None

    def __init__(self, fmc, **kwargs):
        """
        Initialize StaticRoutes object.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for StaticRoutes class.")
        self.parse_kwargs(**kwargs)

    def device(self, device_name):
        """
        Associate device to this static route.

        :param device_name: (str) Name of device.
        :return: None
        """
        logging.debug("In device() for StaticRoutes class.")
        device1 = DeviceRecords(fmc=self.fmc)
        device1.get(name=device_name)
        if "id" in device1.__dict__:
            self.device_id = device1.id
            self.URL = f"{self.fmc.configuration_url}{self.PREFIX_URL}/{self.device_id}/routing/staticroutes"
            self.device_added_to_url = True
        else:
            logging.warning(
                f'Device "{device_name}" not found.  Cannot set up device for physicalInterface.'
            )

    def post(self):
        """POST method for API for StaticRoutes not supported."""
        logging.info("POST method for API for StaticRoutes not supported.")
        pass

    def put(self):
        """PUT method for API for StaticRoutes not supported."""
        logging.info("PUT method for API for StaticRoutes not supported.")
        pass

    def delete(self):
        """DELETE method for API for StaticRoutes not supported."""
        logging.info("DELETE method for API for StaticRoutes not supported.")
        pass
