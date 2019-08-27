from .apiclasstemplate import APIClassTemplate
from .accesscontrolpolicy import AccessControlPolicy
from .intrusionpolicy import IntrusionPolicy
from .variableset import VariableSet
from .securityzone import SecurityZone
from .vlantag import VlanTag
from .portobjectgroup import PortObjectGroup
from .protocolport import ProtocolPort
from .fqdns import FQDNS
from .networkgroup import NetworkGroup
from .ipaddresses import IPAddresses
from .helper_functions import get_networkaddress_type
import logging


class ACPRule(APIClassTemplate):
    """
    The ACP Rule Object in the FMC.
    """
    PREFIX_URL = '/policy/accesspolicies'
    REQUIRED_FOR_POST = ['name', 'acp_id']
    VALID_FOR_ACTION = ['ALLOW', 'TRUST', 'BLOCK', 'MONITOR', 'BLOCK_RESET', 'BLOCK_INTERACTIVE',
                        'BLOCK_RESET_INTERACTIVE']
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    @property
    def URL_SUFFIX(self):
        """
        Add the URL suffixes for categories, insertBefore and insertAfter
        NOTE: You must specify these at the time the object is initialized (created) for this feature
        to work correctly. Example:
            This works:
                new_rule = ACPRule(fmc=fmc, acp_name='acp1', insertBefore=2)

            This does not:
                new_rule = ACPRule(fmc=fmc, acp_name='acp1')
                new_rule.insertBefore = 2
        """
        url = '?'

        if 'category' in self.__dict__:
            url = '{}category={}&'.format(url, self.category)
        if 'insertBefore' in self.__dict__:
            url = '{}insertBefore={}&'.format(url, self.insertBefore)
        if 'insertAfter' in self.__dict__:
            url = '{}insertAfter={}&'.format(url, self.insertAfter)
        if 'insertBefore' in self.__dict__ and 'insertAfter' in self.__dict__:
            logging.warning('ACP rule has both insertBefore and insertAfter params')
        if 'section' in self.__dict__:
            url = '{}section={}&'.format(url, self.section)

        return url[:-1]

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ACPRule class.")
        self.type = 'AccessRule'
        self.parse_kwargs(**kwargs)
        self.URL = '{}{}'.format(self.URL, self.URL_SUFFIX)

    def format_data(self):
        logging.debug("In format_data() for ACPRule class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'action' in self.__dict__:
            json_data['action'] = self.action
        if 'enabled' in self.__dict__:
            json_data['enabled'] = self.enabled
        if 'sendEventsToFMC' in self.__dict__:
            json_data['sendEventsToFMC'] = self.sendEventsToFMC
        if 'logFiles' in self.__dict__:
            json_data['logFiles'] = self.logFiles
        if 'logBegin' in self.__dict__:
            json_data['logBegin'] = self.logBegin
        if 'logEnd' in self.__dict__:
            json_data['logEnd'] = self.logEnd
        if 'variableSet' in self.__dict__:
            json_data['variableSet'] = self.variableSet
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'originalSourceNetworks' in self.__dict__:
            json_data['originalSourceNetworks'] = self.originalSourceNetworks
        if 'vlanTags' in self.__dict__:
            json_data['vlanTags'] = self.vlanTags
        if 'sourceNetworks' in self.__dict__:
            json_data['sourceNetworks'] = {'objects': self.sourceNetworks['objects']}
            json_data['sourceNetworks']['literals'] = \
                [{'type': v, 'value': k} for k, v in self.sourceNetworks['literals'].items()]
        if 'destinationNetworks' in self.__dict__:
            json_data['destinationNetworks'] = {'objects': self.destinationNetworks['objects']}
            json_data['destinationNetworks']['literals'] = \
                [{'type': v, 'value': k} for k, v in self.destinationNetworks['literals'].items()]
        if 'sourcePorts' in self.__dict__:
            json_data['sourcePorts'] = self.sourcePorts
        if 'destinationPorts' in self.__dict__:
            json_data['destinationPorts'] = self.destinationPorts
        if 'ipsPolicy' in self.__dict__:
            json_data['ipsPolicy'] = self.ipsPolicy
        if 'urls' in self.__dict__:
            json_data['urls'] = self.urls
        if 'sourceZones' in self.__dict__:
            json_data['sourceZones'] = self.sourceZones
        if 'destinationZones' in self.__dict__:
            json_data['destinationZones'] = self.destinationZones
        if 'applications' in self.__dict__:
            json_data['applications'] = self.applications

        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for ACPRule class.")
        if 'action' in kwargs:
            if kwargs['action'] in self.VALID_FOR_ACTION:
                self.action = kwargs['action']
            else:
                logging.warning('Action {} is not a valid action.'.format(kwargs['action']))
        else:
            self.action = 'BLOCK'
        if 'acp_id' in kwargs:
            self.acp(acp_id=kwargs['acp_id'])
        if 'acp_name' in kwargs:
            self.acp(name=kwargs['acp_name'])
        if 'enabled' in kwargs:
            self.enabled = kwargs['enabled']
        else:
            self.enabled = True
        if 'sendEventsToFMC' in kwargs:
            self.sendEventsToFMC = kwargs['sendEventsToFMC']
        else:
            self.sendEventsToFMC = True
        if 'logFiles' in kwargs:
            self.logFiles = kwargs['logFiles']
        else:
            self.logFiles = False
        if 'logBegin' in kwargs:
            self.logBegin = kwargs['logBegin']
        else:
            self.logBegin = False
        if 'logEnd' in kwargs:
            self.logEnd = kwargs['logEnd']
        else:
            self.logEnd = False
        if 'originalSourceNetworks' in kwargs:
            self.originalSourceNetworks = kwargs['originalSourceNetworks']
        if 'sourceZones' in kwargs:
            self.sourceZones = kwargs['sourceZones']
        if 'destinationZones' in kwargs:
            self.destinationZones = kwargs['destinationZones']
        if 'variableSet' in kwargs:
            self.variableSet = kwargs['variableSet']
        if 'ipsPolicy' in kwargs:
            self.ipsPolicy = kwargs['ipsPolicy']
        if 'vlanTags' in kwargs:
            self.vlanTags = kwargs['vlanTags']
        if 'sourcePorts' in kwargs:
            self.sourcePorts = kwargs['sourcePorts']
        if 'destinationPorts' in kwargs:
            self.destinationPorts = kwargs['destinationPorts']
        if 'sourceNetworks' in kwargs:
            self.sourceNetworks = {'objects': [], 'literals': {}}

            if kwargs['sourceNetworks'].get('objects'):
                self.sourceNetworks['objects'] = kwargs['sourceNetworks']['objects']

            if kwargs['sourceNetworks'].get('literals'):
                for literal in kwargs['sourceNetworks']['literals']:
                    self.sourceNetworks['literals'][literal['value']] = literal['type']

        if 'destinationNetworks' in kwargs:
            self.destinationNetworks = {'objects': [], 'literals': {}}

            if kwargs['destinationNetworks'].get('objects'):
                self.destinationNetworks['objects'] = kwargs['destinationNetworks']['objects']

            if kwargs['destinationNetworks'].get('literals'):
                for literal in kwargs['destinationNetworks']['literals']:
                    self.destinationNetworks['literals'][literal['value']] = literal['type']

        if 'urls' in kwargs:
            self.urls = kwargs['urls']
        if 'applications' in kwargs:
            self.applications = kwargs['applications']
        if 'category' in kwargs:
            self.category = kwargs['category']
        if 'insertBefore' in kwargs:
            self.insertBefore = kwargs['insertBefore']
        if 'insertAfter' in kwargs:
            self.insertAfter = kwargs['insertAfter']
        if 'section' in kwargs:
            self.section = kwargs['section']

        # Check if suffix should be added to URL
        # self.url_suffix()

    def acp(self, name='', acp_id=''):
        # either name or id of the ACP should be given
        logging.debug("In acp() for ACPRule class.")
        if acp_id != '':
            self.acp_id = acp_id
            self.URL = '{}{}/{}/accessrules'.format(self.fmc.configuration_url, self.PREFIX_URL, self.acp_id)
            self.acp_added_to_url = True
        elif name != '':
            acp1 = AccessControlPolicy(fmc=self.fmc)
            acp1.get(name=name)
            if 'id' in acp1.__dict__:
                self.acp_id = acp1.id
                self.URL = '{}{}/{}/accessrules'.format(self.fmc.configuration_url, self.PREFIX_URL, self.acp_id)
                self.acp_added_to_url = True
            else:
                logging.warning('Access Control Policy {} not found.  Cannot set up accessPolicy for '
                                'ACPRule.'.format(name))
        else:
            logging.error('No accessPolicy name or ID was provided.')

    def intrusion_policy(self, action, name=''):
        logging.debug("In intrusion_policy() for ACPRule class.")
        if action == 'clear':
            if 'ipsPolicy' in self.__dict__:
                del self.ipsPolicy
                logging.info('Intrusion Policy removed from this ACPRule object.')
        elif action == 'set':
            ips = IntrusionPolicy(fmc=self.fmc, name=name)
            ips.get()
            self.ipsPolicy = {'name': ips.name, 'id': ips.id, 'type': ips.type}
            logging.info('Intrusion Policy set to "{}" for this ACPRule object.'.format(name))

    def variable_set(self, action, name='Default-Set'):
        logging.debug("In variable_set() for ACPRule class.")
        if action == 'clear':
            if 'variableSet' in self.__dict__:
                del self.variableSet
                logging.info('Variable Set removed from this ACPRule object.')
        elif action == 'set':
            vs = VariableSet(fmc=self.fmc)
            vs.get(name=name)
            self.variableSet = {'name': vs.name, 'id': vs.id, 'type': vs.type}
            logging.info('VariableSet set to "{}" for this ACPRule object.'.format(name))

    def source_zone(self, action, name=''):
        logging.debug("In source_zone() for ACPRule class.")
        if action == 'add':
            sz = SecurityZone(fmc=self.fmc)
            sz.get(name=name)
            if 'id' in sz.__dict__:
                if 'sourceZones' in self.__dict__:
                    new_zone = {'name': sz.name, 'id': sz.id, 'type': sz.type}
                    duplicate = False
                    for obj in self.sourceZones['objects']:
                        if obj['name'] == new_zone['name']:
                            duplicate = True
                            break
                    if not duplicate:
                        self.sourceZones['objects'].append(new_zone)
                        logging.info('Adding "{}" to sourceZones for this ACPRule.'.format(name))
                else:
                    self.sourceZones = {'objects': [{'name': sz.name, 'id': sz.id, 'type': sz.type}]}
                    logging.info('Adding "{}" to sourceZones for this ACPRule.'.format(name))
            else:
                logging.warning('Security Zone, "{}", not found.  Cannot add to ACPRule.'.format(name))
        elif action == 'remove':
            sz = SecurityZone(fmc=self.fmc)
            sz.get(name=name)
            if 'id' in sz.__dict__:
                if 'sourceZones' in self.__dict__:
                    objects = []
                    for obj in self.sourceZones['objects']:
                        if obj['name'] != name:
                            objects.append(obj)
                    self.sourceZones['objects'] = objects
                    logging.info('Removed "{}" from sourceZones for this ACPRule.'.format(name))
                else:
                    logging.info("sourceZones doesn't exist for this ACPRule.  Nothing to remove.")
            else:
                logging.warning('Security Zone, "{}", not found.  Cannot remove from ACPRule.'.format(name))
        elif action == 'clear':
            if 'sourceZones' in self.__dict__:
                del self.sourceZones
                logging.info('All Source Zones removed from this ACPRule object.')

    def destination_zone(self, action, name=''):
        logging.debug("In destination_zone() for ACPRule class.")
        if action == 'add':
            sz = SecurityZone(fmc=self.fmc)
            sz.get(name=name)
            if 'id' in sz.__dict__:
                if 'destinationZones' in self.__dict__:
                    new_zone = {'name': sz.name, 'id': sz.id, 'type': sz.type}
                    duplicate = False
                    for obj in self.destinationZones['objects']:
                        if obj['name'] == new_zone['name']:
                            duplicate = True
                            break
                    if not duplicate:
                        self.destinationZones['objects'].append(new_zone)
                        logging.info('Adding "{}" to destinationZones for this ACPRule.'.format(name))
                else:
                    self.destinationZones = {'objects': [{'name': sz.name, 'id': sz.id, 'type': sz.type}]}
                    logging.info('Adding "{}" to destinationZones for this ACPRule.'.format(name))
            else:
                logging.warning('Security Zone, "{}", not found.  Cannot add to ACPRule.'.format(name))
        elif action == 'remove':
            sz = SecurityZone(fmc=self.fmc)
            sz.get(name=name)
            if 'id' in sz.__dict__:
                if 'destinationZones' in self.__dict__:
                    objects = []
                    for obj in self.destinationZones['objects']:
                        if obj['name'] != name:
                            objects.append(obj)
                    self.destinationZones['objects'] = objects
                    logging.info('Removed "{}" from destinationZones for this ACPRule.'.format(name))
                else:
                    logging.info("destinationZones doesn't exist for this ACPRule.  Nothing to remove.")
            else:
                logging.warning('Security Zone, {}, not found.  Cannot remove from ACPRule.'.format(name))
        elif action == 'clear':
            if 'destinationZones' in self.__dict__:
                del self.destinationZones
                logging.info('All Destination Zones removed from this ACPRule object.')

    def vlan_tags(self, action, name=''):
        logging.debug("In vlan_tags() for ACPRule class.")
        if action == 'add':
            vlantag = VlanTag(fmc=self.fmc)
            vlantag.get(name=name)
            if 'id' in vlantag.__dict__:
                if 'vlanTags' in self.__dict__:
                    new_vlan = {'name': vlantag.name, 'id': vlantag.id, 'type': vlantag.type}
                    duplicate = False
                    for obj in self.vlanTags['objects']:
                        if obj['name'] == new_vlan['name']:
                            duplicate = True
                            break
                    if not duplicate:
                        self.vlanTags['objects'].append(new_vlan)
                        logging.info('Adding "{}" to vlanTags for this ACPRule.'.format(name))
                else:
                    self.vlanTags = {'objects': [{'name': vlantag.name, 'id': vlantag.id, 'type': vlantag.type}]}
                    logging.info('Adding "{}" to vlanTags for this ACPRule.'.format(name))
            else:
                logging.warning('VLAN Tag, "{}", not found.  Cannot add to ACPRule.'.format(name))
        elif action == 'remove':
            vlantag = VlanTag(fmc=self.fmc)
            vlantag.get(name=name)
            if 'id' in vlantag.__dict__:
                if 'vlanTags' in self.__dict__:
                    objects = []
                    for obj in self.vlanTags['objects']:
                        if obj['name'] != name:
                            objects.append(obj)
                    self.vlanTags['objects'] = objects
                    logging.info('Removed "{}" from vlanTags for this ACPRule.'.format(name))
                else:
                    logging.info("vlanTags doesn't exist for this ACPRule.  Nothing to remove.")
            else:
                logging.warning('VLAN Tag, {}, not found.  Cannot remove from ACPRule.'.format(name))
        elif action == 'clear':
            if 'vlanTags' in self.__dict__:
                del self.vlanTags
                logging.info('All VLAN Tags removed from this ACPRule object.')

    def source_port(self, action, name=''):
        logging.debug("In source_port() for ACPRule class.")
        if action == 'add':
            pport_json = ProtocolPort(fmc=self.fmc)
            pport_json.get(name=name)
            if 'id' in pport_json.__dict__:
                item = pport_json
            else:
                item = PortObjectGroup(fmc=self.fmc)
                item.get(name=name)
            if 'id' in item.__dict__:
                if 'sourcePorts' in self.__dict__:
                    new_port = {'name': item.name, 'id': item.id, 'type': item.type}
                    duplicate = False
                    for obj in self.sourcePorts['objects']:
                        if obj['name'] == new_port['name']:
                            duplicate = True
                            break
                    if not duplicate:
                        self.sourcePorts['objects'].append(new_port)
                        logging.info('Adding "{}" to sourcePorts for this ACPRule.'.format(name))
                else:
                    self.sourcePorts = {'objects': [{'name': item.name, 'id': item.id, 'type': item.type}]}
                    logging.info('Adding "{}" to sourcePorts for this ACPRule.'.format(name))
            else:
                logging.warning('Protocol Port or Protocol Port Group: "{}", not found.  Cannot add to ACPRule.'
                                .format(name))
        elif action == 'remove':
            pport_json = ProtocolPort(fmc=self.fmc)
            pport_json.get(name=name)
            if 'id' in pport_json.__dict__:
                item = pport_json
            else:
                item = PortObjectGroup(fmc=self.fmc)
                item.get(name=name)
            if 'id' in item.__dict__:
                if 'sourcePorts' in self.__dict__:
                    objects = []
                    for obj in self.sourcePorts['objects']:
                        if obj['name'] != name:
                            objects.append(obj)
                    self.sourcePorts['objects'] = objects
                    logging.info('Removed "{}" from sourcePorts for this ACPRule.'.format(name))
                else:
                    logging.info("sourcePorts doesn't exist for this ACPRule.  Nothing to remove.")
            else:
                logging.warning('Protocol Port or Protocol Port Group: "{}", not found.  Cannot add to ACPRule.'
                                .format(name))
        elif action == 'clear':
            if 'sourcePorts' in self.__dict__:
                del self.sourcePorts
                logging.info('All Source Ports removed from this ACPRule object.')

    def destination_port(self, action, name=''):
        logging.debug("In destination_port() for ACPRule class.")
        if action == 'add':
            pport_json = ProtocolPort(fmc=self.fmc)
            pport_json.get(name=name)
            if 'id' in pport_json.__dict__:
                item = pport_json
            else:
                item = PortObjectGroup(fmc=self.fmc)
                item.get(name=name)
            if 'id' in item.__dict__:
                if 'destinationPorts' in self.__dict__:
                    new_port = {'name': item.name, 'id': item.id, 'type': item.type}
                    duplicate = False
                    for obj in self.destinationPorts['objects']:
                        if obj['name'] == new_port['name']:
                            duplicate = True
                            break
                    if not duplicate:
                        self.destinationPorts['objects'].append(new_port)
                        logging.info('Adding "{}" to destinationPorts for this ACPRule.'.format(name))
                else:
                    self.destinationPorts = {'objects': [{'name': item.name, 'id': item.id, 'type': item.type}]}
                    logging.info('Adding "{}" to destinationPorts for this ACPRule.'.format(name))
            else:
                logging.warning('Protocol Port or Protocol Port Group: "{}", not found.  Cannot add to ACPRule.'
                                .format(name))
        elif action == 'remove':
            pport_json = ProtocolPort(fmc=self.fmc)
            pport_json.get(name=name)
            if 'id' in pport_json.__dict__:
                item = pport_json
            else:
                item = PortObjectGroup(fmc=self.fmc)
                item.get(name=name)
            if 'id' in item.__dict__:
                if 'destinationPorts' in self.__dict__:
                    objects = []
                    for obj in self.destinationPorts['objects']:
                        if obj['name'] != name:
                            objects.append(obj)
                    self.destinationPorts['objects'] = objects
                    logging.info('Removed "{}" from destinationPorts for this ACPRule.'.format(name))
                else:
                    logging.info("destinationPorts doesn't exist for this ACPRule.  Nothing to remove.")
            else:
                logging.warning('Protocol Port or Protocol Port Group: "{}", not found.  Cannot add to ACPRule.'
                                .format(name))
        elif action == 'clear':
            if 'destinationPorts' in self.__dict__:
                del self.destinationPorts
                logging.info('All Destination Ports removed from this ACPRule object.')

    def source_network(self, action, name='', literal=None):
        """
        Adds Either object having name=name or literal with {value:<>, type:<>} to the sourceNetworks
        field of acprule object
        Args:
            action: the action to be done
            name: name of the object in question
            literal: the literal in question
        Returns:
            None
        """
        # using dict() as default value is dangerous here, any thoughts/workarounds on this?
        logging.debug("In source_network() for ACPRule class.")
        if literal and name != '':
            raise ValueError('Only one of literals or name (object name) should be set while creating a source network')

        if not hasattr(self, 'sourceNetworks'):
            self.sourceNetworks = {'objects': [], 'literals': {}}

        if action == 'add':

            if literal:
                type_ = get_networkaddress_type(literal)
                self.sourceNetworks['literals'][literal] = type_
                logging.info('Adding literal "{}" of type "{}" to sourceNetworks for this ACPRule.'
                             .format(literal, type_))

            else:
                ipaddresses_json = IPAddresses(fmc=self.fmc).get()
                networkgroup_json = NetworkGroup(fmc=self.fmc).get()
                if self.fmc.serverVersion >= '6.4':
                    fqdns_json = FQDNS(fmc=self.fmc).get()
                else:
                    fqdns_json = {'items': ''}
                items = ipaddresses_json.get('items', []) + \
                    networkgroup_json.get('items', []) + fqdns_json.get('items', [])
                new_net = None
                for item in items:
                    if item['name'] == name:
                        new_net = {'name': item['name'], 'id': item['id'], 'type': item['type']}
                        break
                if new_net is None:
                    logging.warning('Network "{}" is not found in FMC.  Cannot add to sourceNetworks.'.format(name))
                else:
                    if 'sourceNetworks' in self.__dict__:
                        # thus either some objects are already present in sourceNetworks,
                        # or only literals are present in sourceNetworks
                        if 'objects' in self.__dict__['sourceNetworks']:
                            # some objects are already present
                            duplicate = False
                            # see if its a duplicate or not. If not, append to the list of
                            # existing objects in sourceNetworks
                            for obj in self.sourceNetworks['objects']:
                                if obj['name'] == new_net['name']:
                                    duplicate = True
                                    break
                            if not duplicate:
                                self.sourceNetworks['objects'].append(new_net)
                                logging.info('Adding "{}" to sourceNetworks for this ACPRule.'.format(name))
                        else:
                            # this means no objects were present in sourceNetworks,
                            # and sourceNetworks contains literals only
                            self.sourceNetworks.update({'objects': [new_net]})
                            # So update the sourceNetworks dict which contained 'literals' key initially
                            # to have a 'objects' key as well
                            logging.info('Adding "{}" to sourceNetworks for this ACPRule.'.format(name))
                    else:
                        # None of literals or objects are present in sourceNetworks,
                        # so initialize it with objects and update the provided object
                        self.sourceNetworks = {'objects': [new_net]}
                        logging.info('Adding "{}" to sourceNetworks for this ACPRule.'.format(name))
        elif action == 'remove':
            if 'sourceNetworks' in self.__dict__:
                if name != '':
                    # an object's name has been provided to be removed
                    objects = []
                    for obj in self.sourceNetworks['objects']:
                        if obj['name'] != name:
                            objects.append(obj)
                    if len(objects) == 0:
                        # it was the last object which was deleted now
                        del self.sourceNetworks
                        logging.info('Removed "{}" from sourceNetworks for this ACPRule'.format(name))
                        logging.info('All Source Networks removed from this ACPRule object.')
                    else:
                        self.sourceNetworks['objects'] = objects
                        logging.info('Removed "{}" from sourceNetworks for this ACPRule.'.format(name))
                else:
                    # a literal value has been provided to be removed
                    type_ = self.sourceNetworks['literals'].get(literal)
                    if type_:
                        self.sourceNetworks['literals'].pop(literal)
                        logging.info('Removed literal "{}" of type "{}" from sourceNetworks for this ACPRule.'
                                     .format(literal, type_))
                    else:
                        logging.info('Unable to removed literal "{}" from sourceNetworks as it was not found'
                                     .format(literal))
            else:
                logging.info("sourceNetworks doesn't exist for this ACPRule.  Nothing to remove.")
        elif action == 'clear':
            if 'sourceNetworks' in self.__dict__:
                del self.sourceNetworks
                logging.info('All Source Networks removed from this ACPRule object.')

    def destination_network(self, action, name='', literal=None):
        """
        Adds Either object having name=name or literal with {value:<>, type:<>} to the sourceNetworks
        field of acprule object
        Args:
            action: the action to be done
            name: name of the object in question
            literal: the literal in question
        Returns:
            None
        """
        # using dict() as default value is dangerous here, any thoughts/workarounds on this?

        logging.debug("In destination_network() for ACPRule class.")
        if literal and name != '':
            raise ValueError('Only one of literals or name (object name) should be set while creating a source network')

        if not hasattr(self, 'destinationNetworks'):
            self.destinationNetworks = {'objects': [], 'literals': {}}

        if action == 'add':

            if literal:
                type_ = get_networkaddress_type(literal)
                self.destinationNetworks['literals'][literal] = type_
                logging.info('Adding literal "{}" of type "{}" to destinationNetworks for this ACPRule.'
                             .format(literal, type_))

            else:
                ipaddresses_json = IPAddresses(fmc=self.fmc).get()
                networkgroup_json = NetworkGroup(fmc=self.fmc).get()
                if self.fmc.serverVersion >= '6.4':
                    fqdns_json = FQDNS(fmc=self.fmc).get()
                else:
                    fqdns_json = {'items': ''}
                items = ipaddresses_json.get('items', []) + \
                    networkgroup_json.get('items', []) + fqdns_json.get('items', [])
                new_net = None
                for item in items:
                    if item['name'] == name:
                        new_net = {'name': item['name'], 'id': item['id'], 'type': item['type']}
                        break
                if new_net is None:
                    logging.warning('Network "{}" is not found in FMC.  Cannot add to '
                                    'destinationNetworks.'.format(name))
                else:
                    if 'destinationNetworks' in self.__dict__:
                        # thus either some objects are already present in destinationNetworks,
                        # or only literals are present in destinationNetworks
                        if 'objects' in self.__dict__['destinationNetworks']:
                            # some objects are already present
                            duplicate = False
                            for obj in self.destinationNetworks['objects']:
                                if obj['name'] == new_net['name']:
                                    duplicate = True
                                    break
                            if not duplicate:
                                self.destinationNetworks['objects'].append(new_net)
                                logging.info('Adding "{}" to destinationNetworks for this ACPRule.'.format(name))
                        else:
                            # this means no objects were present in destinationNetworks,
                            # and destinationNetworks contains literals only
                            self.destinationNetworks.update({'objects': [new_net]})
                            # So update the destinationNetworks dict which contained 'literals' key initially
                            # to have a 'objects' key as well
                            logging.info('Adding "{}" to destinationNetworks for this ACPRule.'.format(name))
                    else:
                        # None of literals or objects are present in destinationNetworks,
                        # so initialize it with objects and update the provided object
                        self.destinationNetworks = {'objects': [new_net]}
                        logging.info('Adding "{}" to destinationNetworks for this ACPRule.'.format(name))
        elif action == 'remove':
            if 'destinationNetworks' in self.__dict__:
                if name != '':
                    # an object's name has been provided to be removed
                    objects = []
                    for obj in self.destinationNetworks['objects']:
                        if obj['name'] != name:
                            objects.append(obj)
                    if len(objects) == 0:
                        # it was the last object which was deleted now
                        del self.destinationNetworks
                        logging.info('Removed "{}" from destinationNetworks for this ACPRule'.format(name))
                        logging.info('All Destination Networks removed from this ACPRule object.')
                    else:
                        self.destinationNetworks['objects'] = objects
                        logging.info('Removed "{}" from destinationNetworks for this ACPRule.'.format(name))
                else:
                    # a literal value has been provided to be removed
                    type_ = self.destinationNetworks['literals'].get(literal)
                    if type_:
                        self.destinationNetworks['literals'].pop(literal)
                        logging.info('Removed literal "{}" of type "{}" from destinationNetworks for this ACPRule.'
                                     .format(literal, type_))
                    else:
                        logging.info('Unable to removed literal "{}" from destinationNetworks as it was not found'
                                     .format(literal))
            else:
                logging.info("destinationNetworks doesn't exist for this ACPRule.  Nothing to remove.")
        elif action == 'clear':
            if 'destinationNetworks' in self.__dict__:
                del self.destinationNetworks
                logging.info('All Destination Networks removed from this ACPRule object.')
