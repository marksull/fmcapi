"""MonitoredInterfaces Classes."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .ftddevicehapairs import FTDDeviceHAPairs
import logging


class MonitoredInterfaces(APIClassTemplate):
    """The MonitoredInterfaces Object in the FMC."""

    VALID_JSON_DATA = [
        "id",
        "name",
        "ipv4Configuration",
        "ipv6Configuration",
        "monitorForFailures",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + ["ha_name"]
    PREFIX_URL = "/devicehapairs/ftddevicehapairs"
    REQUIRED_FOR_PUT = ["id"]

    def __init__(self, fmc, **kwargs):
        """
        Initialize MonitoredInterfaces object.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for MonitoredInterfaces class.")
        self.parse_kwargs(**kwargs)

    def parse_kwargs(self, **kwargs):
        """
        Parse the kwargs and set self variables to match.

        :return: None
        """
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for MonitoredInterfaces class.")
        if "ha_name" in kwargs:
            self.device_ha(ha_name=kwargs["ha_name"])

    def device_ha(self, ha_name):
        """
        Add deviceha_id to URL.

        :param ha_name: (str) Name of Device HA.
        :return: None
        """
        logging.debug("In device_ha() for MonitoredInterfaces class.")
        deviceha1 = FTDDeviceHAPairs(fmc=self.fmc, name=ha_name)
        deviceha1.get()
        if "id" in deviceha1.__dict__:
            self.deviceha_id = deviceha1.id
            self.URL = f"{self.fmc.configuration_url}{self.PREFIX_URL}/{self.deviceha_id}/monitoredinterfaces"
            self.deviceha_added_to_url = True
        else:
            logging.warning(
                f"Device HA {ha_name} not found.  Cannot set up device for MonitoredInterfaces."
            )

    def ipv4(self, ipv4addr, ipv4mask, ipv4standbyaddr):
        """
        IPv4 address info for monitored device.

        :param ipv4addr: (str) x.x.x.x
        :param ipv4mask: (str) bitmask
        :param ipv4standbyaddr: (str) x.x.x.x
        """
        logging.debug("In ipv4() for MonitoredInterfaces class.")
        self.ipv4Configuration = {
            "activeIPv4Address": ipv4addr,
            "activeIPv4Mask": ipv4mask,
            "standbyIPv4Address": ipv4standbyaddr,
        }

    def post(self):
        """POST method for API for MonitoredInterfaces not supported."""
        logging.info("POST method for API for MonitoredInterfaces not supported.")
        pass
