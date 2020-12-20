"""FTDDeviceHAPairs Classes."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from fmcapi.api_objects.device_services.devicerecords import DeviceRecords
import logging


class FTDDeviceHAPairs(APIClassTemplate):
    """The FTDDeviceHAPairs Object in the FMC."""

    VALID_JSON_DATA = [
        "id",
        "name",
        "primary",
        "secondary",
        "ftdHABootstrap",
        "action",
        "forceBreak",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/devicehapairs/ftddevicehapairs"
    REQUIRED_FOR_POST = ["primary", "secondary", "ftdHABootstrap"]
    REQUIRED_FOR_PUT = ["id"]

    def __init__(self, fmc, **kwargs):
        """
        Initialize FTDDeviceHAPairs object.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for FTDDeviceHAPairs class.")
        self.parse_kwargs(**kwargs)

    def device(self, primary_name="", secondary_name=""):
        """
        Add primary and secondary devices to HA Pair.

        :param primary_name: (str) 1st Device.
        :param secondary_name: (str) 2nd Device.
        :return: None
        """
        logging.debug("In device() for FTDDeviceHAPairs class.")
        primary = DeviceRecords(fmc=self.fmc)
        primary.get(name=primary_name)
        secondary = DeviceRecords(fmc=self.fmc)
        secondary.get(name=secondary_name)
        if "id" in primary.__dict__:
            self.primary_id = primary.id
        else:
            logging.warning(
                f"Device {primary_name} not found.  Cannot set up device for FTDDeviceHAPairs."
            )
        if "id" in secondary.__dict__:
            self.secondary_id = secondary.id
        else:
            logging.warning(
                f"Device {secondary_name} not found.  Cannot set up device for FTDDeviceHAPairs."
            )

    def primary(self, name):
        """
        Identify primary device.

        :param name: (str) Name of primary device.
        :return: None
        """
        logging.debug("In primary() for FTDDeviceHAPairs class.")
        primary = DeviceRecords(fmc=self.fmc)
        primary.get(name=name)
        if "id" in primary.__dict__:
            self.primary = {"id": primary.id}
        else:
            logging.warning(
                f"Device {primary.name} not found.  Cannot set up device for FTDDeviceHAPairs."
            )

    def secondary(self, name):
        """
        Identify secondary device.

        :param name: (str) Name of secondary device.
        :return: None
        """
        logging.debug("In secondary() for DeviceHAPairs class.")
        secondary = DeviceRecords(fmc=self.fmc)
        secondary.get(name=name)
        if "id" in secondary.__dict__:
            self.secondary = {"id": secondary.id}
        else:
            logging.warning(
                f"Device {secondary.name} not found.  Cannot set up device for FTDDeviceHAPairs."
            )

    def switch_ha(self):
        """
        Set up HA SWITCH.

        :return: None
        """
        logging.debug("In switch_ha() for FTDDeviceHAPairs class.")
        ha1 = DeviceHAPairs(fmc=self.fmc)
        ha1.get(name=self.name)
        if "id" in ha1.__dict__:
            self.id = ha1.id
            self.action = "SWITCH"
        else:
            logging.warning(
                f"FTDDeviceHAPairs {self.name} not found.  Cannot set up HA for SWITCH."
            )

    def break_ha(self):
        """
        Destroy HA pair.

        :return: None
        """
        logging.debug("In break_ha() for FTDDeviceHAPairs class.")
        ha1 = DeviceHAPairs(fmc=self.fmc)
        ha1.get(name=self.name)
        if "id" in ha1.__dict__:
            self.id = ha1.id
            self.action = "HABREAK"
            self.forceBreak = True
        else:
            logging.warning(
                f"FTDDeviceHAPairs {self.name} not found.  Cannot set up HA for BREAK."
            )

    def post(self, **kwargs):
        """
        Disable autodeploy and then POST.

        :return: requests response
        """
        logging.debug("In post() for FTDDeviceHAPairs class.")
        # Attempting to "Deploy" during Device registration causes issues.
        self.fmc.autodeploy = False
        return super().post(**kwargs)

    def put(self, **kwargs):
        """
        Disable autodeploy and then PUT.

        :return: requests response
        """
        logging.debug("In put() for FTDDeviceHAPairs class.")
        # Attempting to "Deploy" during Device registration causes issues.
        self.fmc.autodeploy = False
        return super().put(**kwargs)
