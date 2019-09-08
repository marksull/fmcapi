from .apiclasstemplate import APIClassTemplate
from .device import Device
from .securityzone import SecurityZone
from .physicalinterface import PhysicalInterface
import logging


class SubInterfaces(APIClassTemplate):
    """
    The Subinterface Object in the FMC.
    """
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\-\/\. ]"""
    PREFIX_URL = '/devices/devicerecords'
    URL_SUFFIX = None
    REQUIRED_FOR_POST = ['name', 'subIntfId', 'MTU']
    REQUIRED_FOR_PUT = ['id', 'device_id']
    VALID_FOR_IPV4 = ['static', 'dhcp', 'pppoe']
    VALID_FOR_MODE = ['INLINE', 'PASSIVE', 'TAP', 'ERSPAN', 'NONE']
    VALID_FOR_MTU = range(64, 9000)

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for SubInterfaces class.")
        self.parse_kwargs(**kwargs)
        self.type = "SubInterface"

    def format_data(self):
        logging.debug("In format_data() for SubInterfaces class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'mode' in self.__dict__:
            json_data['mode'] = self.mode
        if 'enabled' in self.__dict__:
            json_data['enabled'] = self.enabled
        if 'MTU' in self.__dict__:
            json_data['MTU'] = self.MTU
        if 'managementOnly' in self.__dict__:
            json_data['managementOnly'] = self.managementOnly
        if 'ipAddress' in self.__dict__:
            json_data['ipAddress'] = self.ipAddress
        if 'subIntfId' in self.__dict__:
            json_data['subIntfId'] = self.subIntfId
        if 'vlanId' in self.__dict__:
            json_data['vlanId'] = self.vlanId
        if 'macLearn' in self.__dict__:
            json_data['macLearn'] = self.macLearn
        if 'ifname' in self.__dict__:
            json_data['ifname'] = self.ifname
        if 'securityZone' in self.__dict__:
            json_data['securityZone'] = self.securityZone
        if 'arpConfig' in self.__dict__:
            json_data['arpConfig'] = self.arpConfig
        if 'ipv4' in self.__dict__:
            json_data['ipv4'] = self.ipv4
        if 'ipv6' in self.__dict__:
            json_data['ipv6'] = self.ipv6
        if 'macTable' in self.__dict__:
            json_data['macTable'] = self.macTable
        if 'enableAntiSpoofing' in self.__dict__:
            json_data['enableAntiSpoofing'] = self.enableAntiSpoofing
        if 'fragmentReassembly' in self.__dict__:
            json_data['fragmentReassembly'] = self.fragmentReassembly
        if 'enableDNSLookup' in self.__dict__:
            json_data['enableDNSLookup'] = self.enableDNSLookup
        if 'activeMACAddress' in self.__dict__:
            json_data['activeMACAddress'] = self.activeMACAddress
        if 'standbyMACAddress' in self.__dict__:
            json_data['standbyMACAddress'] = self.standbyMACAddress
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for SubInterfaces class.")
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'ipv4' in kwargs:
            if list(kwargs['ipv4'].keys())[0] in self.VALID_FOR_IPV4:
                self.ipv4 = kwargs['ipv4']
            else:
                logging.warning(f"""Method "{kwargs['ipv4']}" is not a valid ipv4 type.""")
        if 'device_name' in kwargs:
            self.device(device_name=kwargs['device_name'])
        if 'mode' in kwargs:
            if kwargs['mode'] in self.VALID_FOR_MODE:
                self.mode = kwargs['mode']
            else:
                logging.warning(f"""Mode "{kwargs['mode']}" is not a valid mode.""")
        if 'securityZone' in kwargs:
            self.securityZone = kwargs['securityZone']
        if 'enabled' in kwargs:
            self.enabled = kwargs['enabled']
        if 'MTU' in kwargs:
            if kwargs['MTU'] in self.VALID_FOR_MTU:
                self.MTU = kwargs['MTU']
            else:
                logging.warning(f"""MTU "{kwargs['MTU']}" should be in the range 64-9000.""")
                self.MTU = 1500
        if 'managementOnly' in kwargs:
            self.managementOnly = kwargs['managementOnly']
        if 'ipAddress' in kwargs:
            self.ipAddress = kwargs['ipAddress']
        if 'subIntfId' in kwargs:
            self.subIntfId = kwargs['subIntfId']
        if 'vlanId' in kwargs:
            self.vlanId = kwargs['vlanId']
        if 'macLearn' in kwargs:
            self.macLearn = kwargs['macLearn']
        if 'ifname' in kwargs:
            self.ifname = kwargs['ifname']
        if 'arpConfig' in kwargs:
            self.arpConfig = kwargs['arpConfig']
        if 'ipv6' in kwargs:
            self.ipv6 = kwargs['ipv6']
        if 'macTable' in kwargs:
            self.macTable = kwargs['macTable']
        if 'enableAntiSpoofing' in kwargs:
            self.enableAntiSpoofing = kwargs['enableAntiSpoofing']
        if 'fragmentReassembly' in kwargs:
            self.fragmentReassembly = kwargs['fragmentReassembly']
        if 'enableDNSLookup' in kwargs:
            self.enableDNSLookup = kwargs['enableDNSLookup']
        if 'activeMACAddress' in kwargs:
            self.activeMACAddress = kwargs['activeMACAddress']
        if 'standbyMACAddress' in kwargs:
            self.standbyMACAddress = kwargs['standbyMACAddress']

    def device(self, device_name):
        logging.debug("In device() for SubInterfaces class.")
        device1 = Device(fmc=self.fmc)
        device1.get(name=device_name)
        if 'id' in device1.__dict__:
            self.device_id = device1.id
            self.URL = f'{self.fmc.configuration_url}{self.PREFIX_URL}/{self.device_id}/subinterfaces'
            self.device_added_to_url = True
        else:
            logging.warning(f'Device "{device_name}" not found.  Cannot set up device for SubInterfaces.')

    def sz(self, name):
        logging.debug("In sz() for SubInterfaces class.")
        sz = SecurityZone(fmc=self.fmc)
        sz.get(name=name)
        if 'id' in sz.__dict__:
            new_zone = {'name': sz.name, 'id': sz.id, 'type': sz.type}
            self.securityZone = new_zone
        else:
            logging.warning(f'Security Zone, "{name}", not found.  Cannot add to SubInterfaces.')

    def static(self, ipv4addr, ipv4mask):
        logging.debug("In static() for SubInterfaces class.")
        self.ipv4 = {"static": {"address": ipv4addr, "netmask": ipv4mask}}

    def dhcp(self, enableDefault=True, routeMetric=1):
        logging.debug("In dhcp() for SubInterfaces class.")
        self.ipv4 = {"dhcp": {"enableDefaultRouteDHCP": enableDefault, "dhcpRouteMetric": routeMetric}}

    def p_interface(self, p_interface, device_name):
        logging.debug("In p_interface() for SubInterfaces class.")
        intf1 = PhysicalInterface(fmc=self.fmc)
        intf1.get(name=p_interface, device_name=device_name)
        if 'id' in intf1.__dict__:
            self.name = intf1.name
            if 'MTU' not in self.__dict__:
                self.MTU = intf1.MTU
        else:
            logging.warning(f'PhysicalInterface, "{intf1.name}", not found.  Cannot add to SubInterfaces.')
