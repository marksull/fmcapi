"""Redundant Interfaces Classes."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .devicerecords import DeviceRecords
from fmcapi.api_objects.object_services.securityzones import SecurityZones
from .physicalinterfaces import PhysicalInterfaces
import logging


class RedundantInterfaces(APIClassTemplate):
    """The Bridge Group Interface Object in the FMC."""

    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
        "mode",
        "enabled",
        "MTU",
        "managementOnly",
        "ipAddress",
        "primaryInterface",
        "secondaryInterface",
        "redundantId",
        "macLearn",
        "ifname",
        "securityZone",
        "arpConfig",
        "ipv4",
        "ipv6",
        "macTable",
        "enableAntiSpoofing",
        "fragmentReassembly",
        "enableDNSLookup",
        "activeMACAddress",
        "standbyMACAddress",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + ["device_name"]
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\-\/\. ]"""
    PREFIX_URL = "/devices/devicerecords"
    URL_SUFFIX = None
    REQUIRED_FOR_POST = ["redundantId"]
    REQUIRED_FOR_PUT = ["id", "device_id"]
    VALID_FOR_IPV4 = ["static", "dhcp", "pppoe"]
    VALID_FOR_MODE = ["INLINE", "PASSIVE", "TAP", "ERSPAN", "NONE"]
    VALID_FOR_MTU = range(64, 9085)

    def __init__(self, fmc, **kwargs):
        """
        Initialize RedundantInterfaces object.

        Set self.type to "RedundantInterface" and parse the kwargs.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for RedundantInterfaces class.")
        self.parse_kwargs(**kwargs)
        self.type = "RedundantInterface"

    def parse_kwargs(self, **kwargs):
        """
        Parse the kwargs and set self variables to match.

        :return: None
        """
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for RedundantInterfaces class.")
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
                logging.warning(f"MTU {kwargs['MTU']} should be in the range 64-9000.")
                self.MTU = 1500

    def device(self, device_name):
        """
        Associate device to this redundant interface.

        :param device_name: (str) Name of device.
        :return: None
        """
        logging.debug("In device() for RedundantInterfaces class.")
        device1 = DeviceRecords(fmc=self.fmc)
        device1.get(name=device_name)
        if "id" in device1.__dict__:
            self.device_id = device1.id
            self.URL = f"{self.fmc.configuration_url}{self.PREFIX_URL}/{self.device_id}/redundantinterfaces"
            self.device_added_to_url = True
        else:
            logging.warning(
                f'Device "{device_name}" not found.  Cannot set up device for RedundantInterfaces.'
            )

    def sz(self, name):
        """
        Assign Security Zone to this redundant interface.

        :param name: (str) Name of Security Zone.
        :return: None
        """
        logging.debug("In sz() for RedundantInterfaces class.")
        sz = SecurityZones(fmc=self.fmc)
        sz.get(name=name)
        if "id" in sz.__dict__:
            new_zone = {"name": sz.name, "id": sz.id, "type": sz.type}
            self.securityZone = new_zone
        else:
            logging.warning(
                f'Security Zone, "{name}", not found.  Cannot add to RedundantInterfaces.'
            )

    def static(self, ipv4addr, ipv4mask):
        """
        Assign static IP to this redundant interface.

        :param ipv4addr: (str) x.x.x.x
        :param ipv4mask: (str) bitmask
        :return: None
        """
        logging.debug("In static() for RedundantInterfaces class.")
        self.ipv4 = {"static": {"address": ipv4addr, "netmask": ipv4mask}}

    def dhcp(self, enableDefault=True, routeMetric=1):
        """
        Configure this redundant interface with DHCP for addressing.

        :param enableDefault: (bool) Accept, or not, a default route via DHCP.
        :param routeMetric: (int) Set route metric.
        :return: None
        """
        logging.debug("In dhcp() for RedundantInterfaces class.")
        self.ipv4 = {
            "dhcp": {
                "enableDefaultRouteDHCP": enableDefault,
                "dhcpRouteMetric": routeMetric,
            }
        }

    def primary(self, p_interface, device_name):
        """
        Primary interface.

        :param p_interface: (str) Name of physical interface.
        :param device_name: (str) Name of device with interface.
        :return: None
        """
        logging.debug("In primary() for RedundantInterfaces class.")
        intf1 = PhysicalInterfaces(fmc=self.fmc)
        intf1.get(name=p_interface, device_name=device_name)
        if "id" in intf1.__dict__:
            self.primaryInterface = {
                "name": intf1.name,
                "id": intf1.id,
                "type": intf1.type,
            }
            if "MTU" not in self.__dict__:
                self.MTU = intf1.MTU
        else:
            logging.warning(
                f'PhysicalInterface, "{intf1.name}", not found.  Cannot add to RedundantInterfaces.'
            )

    def secondary(self, p_interface, device_name):
        """
        Secondary interface.

        :param p_interface: (str) Name of physical interface.
        :param device_name: (str) Name of device with interface.
        :return: None
        """
        logging.debug("In primary() for RedundantInterfaces class.")
        intf1 = PhysicalInterfaces(fmc=self.fmc)
        intf1.get(name=p_interface, device_name=device_name)
        if "id" in intf1.__dict__:
            self.secondaryInterface = {
                "name": intf1.name,
                "id": intf1.id,
                "type": intf1.type,
            }
        else:
            logging.warning(
                f'PhysicalInterface, "{intf1.name}", not found.  Cannot add to RedundantInterfaces.'
            )
