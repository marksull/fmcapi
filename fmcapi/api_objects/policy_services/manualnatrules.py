from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .ftdnatpolicies import FTDNatPolicies
from fmcapi.api_objects.object_services.networkaddresses import NetworkAddresses
from fmcapi.api_objects.object_services.networkgroups import NetworkGroups
from fmcapi.api_objects.object_services.portobjectgroups import PortObjectGroups
from fmcapi.api_objects.object_services.protocolportobjects import ProtocolPortObjects
from fmcapi.api_objects.object_services.interfaceobjects import InterfaceObjects
import logging


class ManualNatRules(APIClassTemplate):
    # Host,Network,NetworkGroup objects
    """
    The ManualNatRules Object in the FMC.
    """

    PREFIX_URL = '/policy/ftdnatpolicies'
    REQUIRED_FOR_POST = ["nat_id"]

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ManualNatRules class.")
        self.parse_kwargs(**kwargs)
        self.type = "FTDManualNatRule"

    def format_data(self):
        logging.debug("In format_data() for ManualNatRules class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'originalSource' in self.__dict__:
            json_data['originalSource'] = self.originalSource
        if 'originalDestination' in self.__dict__:
            json_data['originalDestination'] = self.originalDestination
        if 'translatedSource' in self.__dict__:
            json_data['translatedSource'] = self.translatedSource
        if 'translatedDestination' in self.__dict__:
            json_data['translatedDestination'] = self.translatedDestination
        if 'interfaceInTranslatedSource' in self.__dict__:
            json_data['interfaceInTranslatedSource'] = self.interfaceInTranslatedSource
        if 'interfaceInOriginalDestination' in self.__dict__:
            json_data['interfaceInOriginalDestination'] = self.interfaceInOriginalDestination
        if 'natType' in self.__dict__:
            json_data['natType'] = self.natType
        if 'interfaceIpv6' in self.__dict__:
            json_data['interfaceIpv6'] = self.interfaceIpv6
        if 'fallThrough' in self.__dict__:
            json_data['fallThrough'] = self.fallThrough
        if 'dns' in self.__dict__:
            json_data['dns'] = self.dns
        if 'routeLookup' in self.__dict__:
            json_data['routeLookup'] = self.routeLookup
        if 'noProxyArp' in self.__dict__:
            json_data['noProxyArp'] = self.noProxyArp
        if 'netToNet' in self.__dict__:
            json_data['netToNet'] = self.netToNet
        if 'sourceInterface' in self.__dict__:
            json_data['sourceInterface'] = self.sourceInterface
        if 'destinationInterface' in self.__dict__:
            json_data['destinationInterface'] = self.destinationInterface
        if 'originalSourcePort' in self.__dict__:
            json_data['originalSourcePort'] = self.originalSourcePort
        if 'translatedSourcePort' in self.__dict__:
            json_data['translatedSourcePort'] = self.translatedSourcePort
        if 'originalDestinationPort' in self.__dict__:
            json_data['originalDestinationPort'] = self.originalDestinationPort
        if 'translatedDestinationPort' in self.__dict__:
            json_data['translatedDestinationPort'] = self.translatedDestinationPort
        if 'patOptions' in self.__dict__:
            json_data['patOptions'] = self.patOptions
        if 'unidirectional' in self.__dict__:
            json_data['unidirectional'] = self.unidirectional
        if 'enabled' in self.__dict__:
            json_data['enabled'] = self.enabled
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for ManualNatRules class.")
        if 'originalSource' in kwargs:
            self.originalSource = kwargs['originalSource']
        if 'originalDestination' in kwargs:
            self.originalDestination = kwargs['originalDestination']
        if 'translatedSource' in kwargs and 'interfaceInTranslatedSource' is True:
            logging.warning("Cannot have both a translatedSource and interfaceInTranslatedSource")
        elif 'translatedSource' in kwargs:
            self.translatedSource = kwargs['translatedSource']
        elif 'interfaceInTranslatedSource' in kwargs:
            self.interfaceInTranslatedSource = kwargs['interfaceInTranslatedSource']
        if 'translatedDestination' in kwargs:
            self.translatedDestination = kwargs['translatedDestination']
        if 'interfaceInOriginalDestination' in kwargs:
            self.interfaceInOriginalDestination = kwargs['interfaceInOriginalDestination']
        if 'natType' in kwargs:
            self.natType = kwargs['natType']
        if 'interfaceIpv6' in kwargs:
            self.interfaceIpv6 = kwargs['interfaceIpv6']
        if 'fallThrough' in kwargs:
            self.fallThrough = kwargs['fallThrough']
        if 'dns' in kwargs:
            self.dns = kwargs['dns']
        if 'routeLookup' in kwargs:
            self.routeLookup = kwargs['routeLookup']
        if 'noProxyArp' in kwargs:
            self.noProxyArp = kwargs['noProxyArp']
        if 'netToNet' in kwargs:
            self.netToNet = kwargs['netToNet']
        if 'sourceInterface' in kwargs:
            self.sourceInterface = kwargs['sourceInterface']
        if 'destinationInterface' in kwargs:
            self.destinationInterface = kwargs['destinationInterface']
        if 'originalSourcePort' in kwargs:
            self.originalSourcePort = kwargs['originalSourcePort']
        if 'translatedSourcePort' in kwargs:
            self.translatedSourcePort = kwargs['translatedSourcePort']
        if 'originalDestinationPort' in kwargs:
            self.originalDestinationPort = kwargs['originalDestinationPort']
        if 'translatedDestinationPort' in kwargs:
            self.translatedDestinationPort = kwargs['translatedDestinationPort']
        if 'patOptions' in kwargs:
            self.patOptions = kwargs['patOptions']
        if 'unidirectional' in kwargs:
            self.unidirectional = kwargs['unidirectional']
        if 'enabled' in kwargs:
            self.enabled = kwargs['enabled']

    def nat_policy(self, name):
        logging.debug("In nat_policy() for ManualNatRules class.")
        ftd_nat = FTDNatPolicies(fmc=self.fmc)
        ftd_nat.get(name=name)
        if 'id' in ftd_nat.__dict__:
            self.nat_id = ftd_nat.id
            self.URL = f'{self.fmc.configuration_url}{self.PREFIX_URL}/{self.nat_id}/manualnatrules'
            self.nat_added_to_url = True
        else:
            logging.warning(f'FTD NAT Policy "{name}" not found.  Cannot set up ManualNatRule for NAT Policy.')

    def original_source(self, name):
        logging.debug("In original_source() for ManualNatRules class.")
        ipaddresses_json = NetworkAddresses(fmc=self.fmc).get()
        networkgroup_json = NetworkGroups(fmc=self.fmc).get()
        items = ipaddresses_json.get('items', [])
        new_net = None
        for item in items:
            if item['name'] == name:
                new_net = {'id': item['id'], 'type': item['type']}
                break
        if new_net is None:
            logging.warning(f'Network "{name}" is not found in FMC.  Cannot add to original_source.')
        else:
            self.originalSource = new_net
            logging.info(f'Adding "{name}" to original_source for this ManualNatRule.')

    def translated_source(self, name):
        logging.debug("In translated_source() for ManualNatRules class.")
        ipaddresses_json = NetworkAddresses(fmc=self.fmc).get()
        networkgroup_json = NetworkGroups(fmc=self.fmc).get()
        items = ipaddresses_json.get('items', [])
        new_net = None
        for item in items:
            if item['name'] == name:
                new_net = {'id': item['id'], 'type': item['type']}
                break
        if new_net is None:
            logging.warning(f'Network "{name}" is not found in FMC.  Cannot add to translated_source.')
        else:
            self.translatedSource = new_net
            logging.info(f'Adding "{name}" to translated_source for this ManualNatRule.')

    def original_destination(self, name):
        logging.debug("In original_destination() for ManualNatRules class.")
        ipaddresses_json = NetworkAddresses(fmc=self.fmc).get()
        networkgroup_json = NetworkGroups(fmc=self.fmc).get()
        items = ipaddresses_json.get('items', [])
        new_net = None
        for item in items:
            if item['name'] == name:
                new_net = {'id': item['id'], 'type': item['type']}
                break
        if new_net is None:
            logging.warning(f'Network "{name}" is not found in FMC.  Cannot add to original_destination.')
        else:
            self.originalDestination = new_net
            logging.info(f'Adding "{name}" to original_destination for this ManualNatRule.')

    def translated_destination(self, name):
        logging.debug("In translated_destination() for ManualNatRules class.")
        ipaddresses_json = NetworkAddresses(fmc=self.fmc).get()
        networkgroup_json = NetworkGroups(fmc=self.fmc).get()
        items = ipaddresses_json.get('items', [])
        new_net = None
        for item in items:
            if item['name'] == name:
                new_net = {'id': item['id'], 'type': item['type']}
                break
        if new_net is None:
            logging.warning(f'Network "{name}" is not found in FMC.  Cannot add to translated_destination.')
        else:
            self.translatedDestination = new_net
            logging.info(f'Adding "{name}" to translated_destination for this ManualNatRule.')

    def original_source_port(self, name):
        logging.debug("In original_source_port() for ManualNatRules class.")
        ports_json = ProtocolPortObjects(fmc=self.fmc).get()
        portgroup_json = PortObjectGroups(fmc=self.fmc).get()
        items = ports_json.get('items', []) + portgroup_json.get('items', [])
        new_port = None
        for item in items:
            if item['name'] == name:
                new_port = {'id': item['id'], 'type': item['type']}
                break
        if new_port is None:
            logging.warning(f'Port "{name}" is not found in FMC.  Cannot add to original_source_port.')
        else:
            self.originalSourcePort = new_port
            logging.info(f'Adding "{name}" to original_source_port for this ManualNatRule.')

    def translated_source_port(self, name):
        logging.debug("In translated_source_port() for ManualNatRules class.")
        ports_json = ProtocolPortObjects(fmc=self.fmc).get()
        portgroup_json = PortObjectGroups(fmc=self.fmc).get()
        items = ports_json.get('items', []) + portgroup_json.get('items', [])
        new_port = None
        for item in items:
            if item['name'] == name:
                new_port = {'id': item['id'], 'type': item['type']}
                break
        if new_port is None:
            logging.warning(f'Port "{name}" is not found in FMC.  Cannot add to translated_source_port.')
        else:
            self.translatedSourcePort = new_port
            logging.info(f'Adding "{name}" to translated_source_port for this ManualNatRule.')

    def original_destination_port(self, name):
        logging.debug("In original_destination_port() for ManualNatRules class.")
        ports_json = ProtocolPortObjects(fmc=self.fmc).get()
        portgroup_json = PortObjectGroups(fmc=self.fmc).get()
        items = ports_json.get('items', []) + portgroup_json.get('items', [])
        new_port = None
        for item in items:
            if item['name'] == name:
                new_port = {'id': item['id'], 'type': item['type']}
                break
        if new_port is None:
            logging.warning(f'Port "{name}" is not found in FMC.  Cannot add to original_destination_port.')
        else:
            self.originalDestinationPort = new_port
            logging.info(f'Adding "{name}" to original_destination_port for this ManualNatRule.')

    def translated_destination_port(self, name):
        logging.debug("In translated_destination_port() for ManualNatRules class.")
        ports_json = ProtocolPortObjects(fmc=self.fmc).get()
        portgroup_json = PortObjectGroups(fmc=self.fmc).get()
        items = ports_json.get('items', []) + portgroup_json.get('items', [])
        new_port = None
        for item in items:
            if item['name'] == name:
                new_port = {'id': item['id'], 'type': item['type']}
                break
        if new_port is None:
            logging.warning(f'Port "{name}" is not found in FMC.  Cannot add to translated_destination_port.')
        else:
            self.translatedDestinationPort = new_port
            logging.info(f'Adding "{name}" to translated_destination_port for this ManualNatRule.')

    def source_intf(self, name):
        logging.debug("In source_intf() for ManualNatRules class.")
        intf_obj = InterfaceObjects(fmc=self.fmc).get()
        items = intf_obj.get('items', [])
        new_intf = None
        for item in items:
            if item["name"] == name:
                new_intf = {'id': item['id'], 'type': item['type']}
                break
        if new_intf is None:
            logging.warning(f'Interface Object "{name}" is not found in FMC.  Cannot add to sourceInterface.')
        else:
            self.sourceInterface = new_intf
            logging.info(f'Interface Object "{name}" added to NAT Policy.')

    def destination_intf(self, name):
        logging.debug("In destination_intf() for ManualNatRules class.")
        intf_obj = InterfaceObjects(fmc=self.fmc).get()
        items = intf_obj.get('items', [])
        new_intf = None
        for item in items:
            if item["name"] == name:
                new_intf = {'id': item['id'], 'type': item['type']}
                break
        if new_intf is None:
            logging.warning(f'Interface Object "{name}" is not found in FMC.  Cannot add to destinationInterface.')
        else:
            self.destinationInterface = new_intf
            logging.info(f'Interface Object "{name}" added to NAT Policy.')

    def identity_nat(self, name):
        logging.debug("In identity_nat() for ManualNatRules class.")
        ipaddresses_json = NetworkAddresses(fmc=self.fmc).get()
        networkgroup_json = NetworkGroups(fmc=self.fmc).get()
        items = ipaddresses_json.get('items', []) + networkgroup_json.get('items', [])
        new_net = None
        for item in items:
            if item['name'] == name:
                new_net = {'id': item['id'], 'type': item['type']}
                break
        if new_net is None:
            logging.warning(f'Network "{name}" is not found in FMC.  Cannot add to this ManualNatRules.')
        else:
            self.natType = "STATIC"
            self.originalSource = new_net
            self.translatedSource = new_net
            logging.info(f'Adding "{name}" to ManualNatRules.')

    def patPool(self, name, options={}):
        ipaddresses_json = NetworkAddresses(fmc=self.fmc).get()
        networkgroup_json = NetworkGroups(fmc=self.fmc).get()
        items = ipaddresses_json.get('items', []) + networkgroup_json.get('items', [])
        new_net = None
        for item in items:
            if item['name'] == name:
                new_net = {'name': item['name'], 'id': item['id'], 'type': item['type']}
                break
        if new_net is None:
            logging.warning(f'Network "{name}" is not found in FMC.  Cannot add to patPool.')
        else:
            self.natType = "DYNAMIC"
            self.unidirectional = True
            self.patOptions = {"patPoolAddress": new_net}
            self.patOptions["interfacePat"] = options.interfacePat if "interfacePat" in options.keys() else False
            self.patOptions["includeReserve"] = options.includeReserve if "includeReserve" in options.keys() else False
            self.patOptions["roundRobin"] = options.roundRobin if "roundRobin" in options.keys() else True
            self.patOptions["extendedPat"] = options.extendedPat if "extendedPat" in options.keys() else False
            self.patOptions["flatPortRange"] = options.flatPortRange if "flatPortRange" in options.keys() else False
            logging.info(f'Adding "{name}" to patPool for this ManualNatRule.')
