from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from fmcapi.api_objects.device_services.devicerecords import Device
import logging
import warnings


class FTDDeviceHAPairs(APIClassTemplate):
    """
    The FTDDeviceHAPairs Object in the FMC.
    """

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
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for FTDDeviceHAPairs class.")
        self.parse_kwargs(**kwargs)

    def device(self, primary_name="", secondary_name=""):
        logging.debug("In device() for FTDDeviceHAPairs class.")
        primary = Device(fmc=self.fmc)
        primary.get(name=primary_name)
        secondary = Device(fmc=self.fmc)
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
        logging.debug("In primary() for FTDDeviceHAPairs class.")
        primary = Device(fmc=self.fmc)
        primary.get(name=name)
        if "id" in primary.__dict__:
            self.primary = {"id": primary.id}
        else:
            logging.warning(
                f"Device {primary.name} not found.  Cannot set up device for FTDDeviceHAPairs."
            )

    def secondary(self, name):
        logging.debug("In secondary() for DeviceHAPairs class.")
        secondary = Device(fmc=self.fmc)
        secondary.get(name=name)
        if "id" in secondary.__dict__:
            self.secondary = {"id": secondary.id}
        else:
            logging.warning(
                f"Device {secondary.name} not found.  Cannot set up device for FTDDeviceHAPairs."
            )

    def switch_ha(self):
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
        logging.debug("In post() for FTDDeviceHAPairs class.")
        # Attempting to "Deploy" during Device registration causes issues.
        self.fmc.autodeploy = False
        return super().post(**kwargs)

    def put(self, **kwargs):
        logging.debug("In put() for FTDDeviceHAPairs class.")
        # Attempting to "Deploy" during Device registration causes issues.
        self.fmc.autodeploy = False
        return super().put(**kwargs)


class DeviceHAPairs(FTDDeviceHAPairs):
    """Dispose of this Class after 20210101."""

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn(
            "Deprecated: DeviceHAPairs() should be called via FTDDeviceHAPairs()."
        )
        super().__init__(fmc, **kwargs)
