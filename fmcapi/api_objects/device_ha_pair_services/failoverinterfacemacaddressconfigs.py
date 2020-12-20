"""FailoverInterfaceMACAddressConfigs class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .ftddevicehapairs import FTDDeviceHAPairs
from fmcapi.api_objects.device_services.physicalinterfaces import PhysicalInterfaces
import logging


class FailoverInterfaceMACAddressConfigs(APIClassTemplate):
    """The FailoverInterfaceMACAddressConfigs Object in the FMC."""

    VALID_JSON_DATA = [
        "id",
        "name",
        "physicalInterface",
        "failoverActiveMac",
        "failoverStandbyMac",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + ["ha_name"]
    PREFIX_URL = "/devicehapairs/ftddevicehapairs"
    REQUIRED_FOR_POST = ["physicalInterface", "failoverActiveMac", "failoverStandbyMac"]
    REQUIRED_FOR_PUT = ["id"]

    def __init__(self, fmc, **kwargs):
        """
        Initialize FailoverInterfaceMACAddressConfigs object.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for FailoverInterfaceMACAddressConfigs class.")
        self.parse_kwargs(**kwargs)

    def parse_kwargs(self, **kwargs):
        """
        Parse the kwargs and set self variables to match.

        :return: None
        """
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for FailoverInterfaceMACAddressConfigs class.")
        if "ha_name" in kwargs:
            self.device_ha(ha_name=kwargs["ha_name"])

    def device_ha(self, ha_name):
        """
        Add deviceha_id to URL.

        :param ha_name: (str) Name of Device HA.
        :return: None
        """
        logging.debug("In device_ha() for FailoverInterfaceMACAddressConfigs class.")
        deviceha1 = FTDDeviceHAPairs(fmc=self.fmc, name=ha_name)
        deviceha1.get()
        if "id" in deviceha1.__dict__:
            self.deviceha_id = deviceha1.id
            self.URL = (
                f"{self.fmc.configuration_url}{self.PREFIX_URL}/"
                f"{self.deviceha_id}/failoverinterfacemacaddressconfigs"
            )
            self.deviceha_added_to_url = True
        else:
            logging.warning(
                f"Device HA {ha_name} not found. "
                f"Cannot set up device for FailoverInterfaceMACAddressConfigs."
            )

    def p_interface(self, name, device_name):
        """
        Physical interface of device used for HA.

        :param name: (str) Name of interface.
        :param device_name (str) Name of device.
        :return: None
        """
        logging.debug("In p_interface() for FailoverInterfaceMACAddressConfigs class.")
        intf1 = PhysicalInterfaces(fmc=self.fmc)
        intf1.get(name=name, device_name=device_name)
        if "id" in intf1.__dict__:
            self.physicalInterface = {
                "name": intf1.name,
                "id": intf1.id,
                "type": intf1.type,
            }
        else:
            logging.warning(
                f'PhysicalInterface, "{name}", not found.  '
                f"Cannot add to FailoverInterfaceMACAddressConfigs."
            )

    def edit(self, name, ha_name):
        """
        Edit existing device HA and change physical interface params.

        :param name: (str)
        :param ha_name: (str)
        :return: None
        """
        logging.debug("In edit() for FailoverInterfaceMACAddressConfigs class.")
        deviceha1 = FTDDeviceHAPairs(fmc=self.fmc, name=ha_name)
        deviceha1.get()
        obj1 = FailoverInterfaceMACAddressConfigs(fmc=self.fmc)
        obj1.device_ha(ha_name=ha_name)
        failovermac_json = obj1.get()
        items = failovermac_json.get("items", [])
        found = False
        for item in items:
            if item["physicalInterface"]["name"] == name:
                found = True
                self.id = item["id"]
                self.name = item["physicalInterface"]["name"]
                self.failoverActiveMac = item["failoverActiveMac"]
                self.failoverStandbyMac = item["failoverStandbyMac"]
                self.deviceha_id = deviceha1.id
                self.URL = (
                    f"{self.fmc.configuration_url}{self.PREFIX_URL}/"
                    f"{self.deviceha_id}/failoverinterfacemacaddressconfigs"
                )
                break
        if found is False:
            logging.warning(
                f'PhysicalInterface, "{name}", not found.  Cannot add to FailoverInterfaceMACAddressConfigs.'
            )
