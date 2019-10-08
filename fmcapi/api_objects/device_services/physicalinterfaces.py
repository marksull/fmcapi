from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from fmcapi.api_objects.object_services.securityzones import SecurityZones
from fmcapi.api_objects.device_services.devicerecords import DeviceRecords
import logging
import warnings


class PhysicalInterfaces(APIClassTemplate):
    """
    The Physical Interface Object in the FMC.
    """

    VALID_JSON_DATA = [
        "id",
        "name",
        "mode",
        "enabled",
        "hardware",
        "MTU",
        "managementOnly",
        "ifname",
        "securityZone",
        "type",
        "ipv4",
        "ipv6",
        "activeMACAddress",
        "standbyMACAddress",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + ["device_name"]
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\-\/\. ]"""
    PREFIX_URL = "/devices/devicerecords"
    URL_SUFFIX = None
    REQUIRED_FOR_PUT = ["id", "device_id"]
    VALID_FOR_IPV4 = ["static", "dhcp", "pppoe"]
    VALID_FOR_MODE = ["INLINE", "PASSIVE", "TAP", "ERSPAN", "NONE"]
    VALID_FOR_MTU = range(64, 9000)
    VALID_FOR_HARDWARE_SPEED = [
        "AUTO",
        "TEN",
        "HUNDRED",
        "THOUSAND",
        "TEN_THOUSAND",
        "FORTY_THOUSAND",
        "LAKH",
    ]
    VALID_FOR_HARDWARE_DUPLEX = ["AUTO", "FULL", "HALF"]

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for PhysicalInterface class.")
        self.parse_kwargs(**kwargs)

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for PhysicalInterface class.")
        if "device_name" in kwargs:
            self.device(device_name=kwargs["device_name"])
        if "ipv4" in kwargs:
            if list(kwargs["ipv4"].keys())[0] in self.VALID_FOR_IPV4:
                self.ipv4 = kwargs["ipv4"]
            else:
                logging.warning(f"Method {kwargs['ipv4']} is not a valid ipv4 type.")
        if "mode" in kwargs:
            if kwargs["mode"] in self.VALID_FOR_MODE:
                self.mode = kwargs["mode"]
            else:
                logging.warning(f"Mode {kwargs['mode']} is not a valid mode.")
        if "MTU" in kwargs:
            if kwargs["MTU"] in self.VALID_FOR_MTU:
                self.MTU = kwargs["MTU"]
            else:
                logging.warning(
                    f"MTU {kwargs['MTU']} should be in the range 64-9000, setting to 1500."
                )
                self.MTU = 1500

    def device(self, device_name):
        logging.debug("In device() for PhysicalInterface class.")
        device1 = DeviceRecords(fmc=self.fmc)
        device1.get(name=device_name)
        if "id" in device1.__dict__:
            self.device_id = device1.id
            self.URL = f"{self.fmc.configuration_url}{self.PREFIX_URL}/{self.device_id}/physicalinterfaces"
            self.device_added_to_url = True
        else:
            logging.warning(
                f"Device {device_name} not found.  Cannot set up device for physicalInterface."
            )

    def sz(self, name):
        logging.debug("In sz() for PhysicalInterface class.")
        sz = SecurityZones(fmc=self.fmc)
        sz.get(name=name)
        if "id" in sz.__dict__:
            new_zone = {"name": sz.name, "id": sz.id, "type": sz.type}
            self.securityZone = new_zone
        else:
            logging.warning(
                f'Security Zone, "{name}", not found.  Cannot add to PhysicalInterface.'
            )

    def static(self, ipv4addr, ipv4mask):
        logging.debug("In static() for PhysicalInterface class.")
        self.ipv4 = {"static": {"address": ipv4addr, "netmask": ipv4mask}}

    def dhcp(self, enableDefault=True, routeMetric=1):
        logging.debug("In dhcp() for PhysicalInterface class.")
        self.ipv4 = {
            "dhcp": {
                "enableDefaultRouteDHCP": enableDefault,
                "dhcpRouteMetric": routeMetric,
            }
        }

    def hwmode(self, mode):
        logging.debug("In hwmode() for PhysicalInterface class.")
        if mode in self.VALID_FOR_MODE:
            self.mode = mode
        else:
            logging.warning(f"Mode {mode} is not a valid mode.")

    def hardware(self, speed, duplex="FULL"):
        # There are probably some incompatibilities that need to be accounted for
        logging.debug("In hardware() for PhysicalInterface class.")
        if (
            speed in self.VALID_FOR_HARDWARE_SPEED
            and duplex in self.VALID_FOR_HARDWARE_DUPLEX
        ):
            self.hardware = {"duplex": duplex, "speed": speed}
        else:
            logging.warning(f"Speed {speed} or Duplex {duplex} is not a valid mode.")


class PhysicalInterface(PhysicalInterfaces):
    """Dispose of this Class after 20210101."""

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn(
            "Deprecated: PhysicalInterface() should be called via PhysicalInterfaces()."
        )
        super().__init__(fmc, **kwargs)
