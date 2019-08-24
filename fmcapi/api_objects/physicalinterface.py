from .apiclasstemplate import APIClassTemplate
from .securityzone import SecurityZone
from .device import Device
import logging


class PhysicalInterface(APIClassTemplate):
    """
    The Physical Interface Object in the FMC.
    """
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\-\/\. ]"""
    PREFIX_URL = '/devices/devicerecords'
    URL_SUFFIX = None
    REQUIRED_FOR_PUT = ['id', 'device_id']
    VALID_FOR_IPV4 = ['static', 'dhcp', 'pppoe']
    VALID_FOR_MODE = ['INLINE', 'PASSIVE', 'TAP', 'ERSPAN', 'NONE']
    VALID_FOR_MTU = range(64, 9000)
    VALID_FOR_HARDWARE_SPEED = ['AUTO', 'TEN', 'HUNDRED', 'THOUSAND', 'TEN_THOUSAND', 'FORTY_THOUSAND', 'LAKH']
    VALID_FOR_HARDWARE_DUPLEX = ['AUTO', 'FULL', 'HALF']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for PhysicalInterface class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for PhysicalInterface class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'mode' in self.__dict__:
            json_data['mode'] = self.mode
        if 'enabled' in self.__dict__:
            json_data['enabled'] = self.enabled
        if 'hardware' in self.__dict__:
            json_data['hardware'] = self.hardware
        if 'MTU' in self.__dict__:
            json_data['MTU'] = self.MTU
        if 'managementOnly' in self.__dict__:
            json_data['managementOnly'] = self.managementOnly
        if 'ifname' in self.__dict__:
            json_data['ifname'] = self.ifname
        if 'securityZone' in self.__dict__:
            json_data['securityZone'] = self.securityZone
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'ipv4' in self.__dict__:
            json_data['ipv4'] = self.ipv4
        if 'ipv6' in self.__dict__:
            json_data['ipv6'] = self.ipv6
        if 'activeMACAddress' in self.__dict__:
            json_data['activeMACAddress'] = self.activeMACAddress
        if 'standbyMACAddress' in self.__dict__:
            json_data['standbyMACAddress'] = self.standbyMACAddress
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for PhysicalInterface class.")
        if 'ipv4' in kwargs:
            if list(kwargs['ipv4'].keys())[0] in self.VALID_FOR_IPV4:
                self.ipv4 = kwargs['ipv4']
            else:
                logging.warning('Method {} is not a valid ipv4 type.'.format(kwargs['ipv4']))
        if 'device_name' in kwargs:
            self.device(device_name=kwargs['device_name'])
        if 'mode' in kwargs:
            if kwargs['mode'] in self.VALID_FOR_MODE:
                self.mode = kwargs['mode']
            else:
                logging.warning('Mode {} is not a valid mode.'.format(kwargs['mode']))
        if 'hardware' in kwargs:
            self.hardware = kwargs['hardware']
        if 'securityZone' in kwargs:
            self.securityZone = kwargs['securityZone']
        if 'enabled' in kwargs:
            self.enabled = kwargs['enabled']  # This doesn't seem to be working
        else:
            self.enabled = False
        if 'MTU' in kwargs:
            if kwargs['MTU'] in self.VALID_FOR_MTU:
                self.MTU = kwargs['MTU']
            else:
                logging.warning('MTU {} should be in the range 64-9000".'.format(kwargs['MTU']))
                self.MTU = 1500
        if 'managementOnly' in kwargs:
            self.managementOnly = kwargs['managementOnly']
        if 'ifname' in kwargs:
            self.ifname = kwargs['ifname']
        if 'ipv6' in kwargs:
            self.ipv6 = kwargs['ipv6']
        if 'activeMACAddress' in kwargs:
            self.activeMACAddress = kwargs['activeMACAddress']
        if 'standbyMACAddress' in kwargs:
            self.standbyMACAddress = kwargs['standbyMACAddress']

    def device(self, device_name):
        logging.debug("In device() for PhysicalInterface class.")
        device1 = Device(fmc=self.fmc)
        device1.get(name=device_name)
        if 'id' in device1.__dict__:
            self.device_id = device1.id
            self.URL = '{}{}/{}/physicalinterfaces'.format(self.fmc.configuration_url, self.PREFIX_URL, self.device_id)
            self.device_added_to_url = True
        else:
            logging.warning('Device {} not found.  Cannot set up device for physicalInterface.'.format(device_name))

    def sz(self, name):
        logging.debug("In sz() for PhysicalInterface class.")
        sz = SecurityZone(fmc=self.fmc)
        sz.get(name=name)
        if 'id' in sz.__dict__:
            new_zone = {'name': sz.name, 'id': sz.id, 'type': sz.type}
            self.securityZone = new_zone
        else:
            logging.warning('Security Zone, "{}", not found.  Cannot add to PhysicalInterface.'.format(name))

    def static(self, ipv4addr, ipv4mask):
        logging.debug("In static() for PhysicalInterface class.")
        self.ipv4 = {"static": {"address": ipv4addr, "netmask": ipv4mask}}

    def dhcp(self, enableDefault=True, routeMetric=1):
        logging.debug("In dhcp() for PhysicalInterface class.")
        self.ipv4 = {"dhcp": {"enableDefaultRouteDHCP": enableDefault, "dhcpRouteMetric": routeMetric}}

    def hwmode(self, mode):
        logging.debug("In hwmode() for PhysicalInterface class.")
        if mode in self.VALID_FOR_MODE:
            self.mode = mode
        else:
            logging.warning('Mode {} is not a valid mode.'.format(mode))

    def hardware(self, speed, duplex="FULL"):
        # There are probably some incompatibilities that need to be accounted for
        logging.debug("In hardware() for PhysicalInterface class.")
        if speed in self.VALID_FOR_HARDWARE_SPEED and duplex in self.VALID_FOR_HARDWARE_DUPLEX:
            self.hardware = {"duplex": duplex, "speed": speed}
        else:
            logging.warning('Speed {} or Duplex {} is not a valid mode.'.format(speed, duplex))
