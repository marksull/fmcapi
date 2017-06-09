"""
This module contains the class objects that represent the various objects in the FMC.
"""

import logging
import datetime
import requests
from .helper_functions import *
from . import export

logging.debug("In the {} module.".format(__name__))


class FMCObject(object):
    """
    This class is the base framework for all the objects in the FMC.
    """

    REQUIRED_FOR_POST = ['name']
    REQUIRED_FOR_PUT = ['id']
    REQUIRED_FOR_DELETE = ['id']
    FILTER_BY_NAME = False
    URL = None

    def __init__(self, fmc, **kwargs):
        logging.debug("In __init__() for fmc_object class.")
        self.fmc = fmc

    def parse_kwargs(self, **kwargs):
        logging.debug("In parse_kwargs() for fmc_object class.")
        if 'name' in kwargs:
            self.name = syntax_correcter(kwargs['name'])
        if 'description' in kwargs:
            self.description = kwargs['description']
        else:
            self.description = 'Created by fmcapi.'
        if 'metadata' in kwargs:
            self.metadata = kwargs['metadata']
        if 'overridable' in kwargs:
            self.overridable = kwargs['overridable']
        else:
            self.overridable = False
        if 'type' in kwargs:
            self.type = kwargs['type']
        if 'links' in kwargs:
            self.links = kwargs['links']
        if 'paging' in kwargs:
            self.paging = kwargs['paging']
        if 'id' in kwargs:
            self.id = kwargs['id']

    def valid_for_post(self):
        logging.debug("In valid_for_post() for fmc_object class.")
        for item in self.REQUIRED_FOR_POST:
            if item not in self.__dict__:
                return False
        return True

    def valid_for_put(self):
        logging.debug("In valid_for_put() for fmc_object class.")
        for item in self.REQUIRED_FOR_PUT:
            if item not in self.__dict__:
                return False
        return True

    def valid_for_delete(self):
        logging.debug("In valid_for_delete() for fmc_object class.")
        for item in self.REQUIRED_FOR_DELETE:
            if item not in self.__dict__:
                return False
        return True

    def post(self, **kwargs):
        logging.debug("In post() for fmc_object class.")
        self.parse_kwargs(**kwargs)
        if 'id' in self.__dict__:
            logging.info("ID value exists for this object.  Redirecting to put() method.")
            self.put()
        else:
            if self.valid_for_post():
                response = self.fmc.send_to_api(method='post', url=self.URL, json_data=self.format_data())
                self.parse_kwargs(**response)
                return True
            else:
                logging.warning("post() method failed due to failure to pass valid_for_post() test.")
                return False

    def get(self, **kwargs):
        """
        If no self.name or self.id exists then return a full listing of all objects of this type.
        Otherwise set "expanded=true" results for this specific object.
        :return:
        """
        logging.debug("In get() for fmc_object class.")
        self.parse_kwargs(**kwargs)
        if 'id' in self.__dict__:
            url = '{}/{}'.format(self.URL, self.id)
            response = self.fmc.send_to_api(method='get', url=url)
            self.parse_kwargs(**response)
        elif 'name' in self.__dict__:
            if self.FILTER_BY_NAME:
                url = '{}?name={}&expanded=true'.format(self.URL, self.name)
            else:
                url = '{}?expanded=true'.format(self.URL)
            response = self.fmc.send_to_api(method='get', url=url)
            for item in response['items']:
                if item['name'] == self.name:
                    self.id = item['id']
                    self.parse_kwargs(**item)
                    break
            if 'id' not in self.__dict__:
                logging.warning("\tGET query for {} is not found.\n\t\t"
                                "Response:{}".format(item['name'], response))
        else:
            logging.info("GET query for object with no name or id set.  Returning full list of these object types "
                         "instead.")
            url = '{}?expanded=true'.format(self.URL)
            response = self.fmc.send_to_api(method='get', url=url)
            return response

    def put(self, **kwargs):
        logging.debug("In put() for fmc_object class.")
        self.parse_kwargs(**kwargs)
        if self.valid_for_put():
            url = '{}/{}'.format(self.URL, self.id)
            response = self.fmc.send_to_api(method='put', url=url, json_data=self.format_data())
            self.parse_kwargs(**response)
            return True
        else:
            logging.warning("put() method failed due to failure to pass valid_for_put() test.")
            return False

    def delete(self, **kwargs):
        logging.debug("In delete() for fmc_object class.")
        self.parse_kwargs(**kwargs)
        if self.valid_for_delete():
            url = '{}/{}'.format(self.URL, self.id)
            response = self.fmc.send_to_api(method='delete', url=url, json_data=self.format_data())
            self.parse_kwargs(**response)
            return True
        else:
            logging.warning("delete() method failed due to failure to pass valid_for_delete() test.")
            return False


# ################# API-Explorer Object Category Things ################# #


@export
class HostObject(FMCObject):
    """
    The Host Object in the FMC.
    """

    URL = '/object/hosts'
    REQUIRED_FOR_POST = ['name', 'value']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for HostObject class.")
        self.parse_kwargs(**kwargs)
        if 'value' in kwargs:
            value_type = get_networkaddress_type(kwargs['value'])
            if value_type == 'range':
                logging.warning("value, {}, is of type {}.  Limited functionality for this object due to it being "
                                "created via the HostObject function.".format(kwargs['value'], value_type))
            if value_type == 'network':
                logging.warning("value, {}, is of type {}.  Limited functionality for this object due to it being "
                                "created via the HostObject function.".format(kwargs['value'], value_type))
            if validate_ip_bitmask_range(value=kwargs['value'], value_type=value_type):
                self.value = kwargs['value']
            else:
                logging.error("Provided value, {}, has an error with the IP address(es).".format(kwargs['value']))

    def format_data(self):
        logging.debug("In format_data() for HostObject class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'value' in self.__dict__:
            json_data['value'] = self.value
        if 'description' in self.__dict__:
            json_data['description'] = self.description
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for HostObject class.")
        if 'value' in kwargs:
            self.value = kwargs['value']


@export
class NetworkObject(FMCObject):
    """
    The Networkt Object in the FMC.
    """

    URL = '/object/networks'
    REQUIRED_FOR_POST = ['name', 'value']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for NetworkObject class.")
        self.parse_kwargs(**kwargs)
        if 'value' in kwargs:
            value_type = get_networkaddress_type(kwargs['value'])
            if value_type == 'range':
                logging.warning("value, {}, is of type {}.  Limited functionality for this object due to it being "
                                "created via the NetworkObject function.".format(kwargs['value'], value_type))
            if value_type == 'host':
                logging.warning("value, {}, is of type {}.  Limited functionality for this object due to it being "
                                "created via the NetworkObject function.".format(kwargs['value'], value_type))
            if validate_ip_bitmask_range(value=kwargs['value'], value_type=value_type):
                self.value = kwargs['value']
            else:
                logging.error("Provided value, {}, has an error with the IP address(es).".format(kwargs['value']))

    def format_data(self):
        logging.debug("In format_data() for NetworkObject class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'value' in self.__dict__:
            json_data['value'] = self.value
        if 'description' in self.__dict__:
            json_data['description'] = self.description
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for NetworkObject class.")
        if 'value' in kwargs:
            self.value = kwargs['value']


@export
class RangeObject(FMCObject):
    """
    The Range Object in the FMC.
    """

    URL = '/object/ranges'
    REQUIRED_FOR_POST = ['name', 'value']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for RangeObject class.")
        self.parse_kwargs(**kwargs)
        if 'value' in kwargs:
            value_type = get_networkaddress_type(kwargs['value'])
            if value_type == 'host':
                logging.warning("value, {}, is of type {}.  Limited functionality for this object due to it being "
                                "created via the RangeObject function.".format(kwargs['value'], value_type))
            if value_type == 'network':
                logging.warning("value, {}, is of type {}.  Limited functionality for this object due to it being "
                                "created via the RangeObject function.".format(kwargs['value'], value_type))
            if validate_ip_bitmask_range(value=kwargs['value'], value_type=value_type):
                self.value = kwargs['value']
            else:
                logging.error("Provided value, {}, has an error with the IP address(es).".format(kwargs['value']))

    def format_data(self):
        logging.debug("In format_data() for RangeObject class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'value' in self.__dict__:
            json_data['value'] = self.value
        if 'description' in self.__dict__:
            json_data['description'] = self.description
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for RangeObject class.")
        if 'value' in kwargs:
            self.value = kwargs['value']


@export
class URLObject(FMCObject):
    """
    The URL Object in the FMC.
    """

    URL = '/object/urls'
    REQUIRED_FOR_POST = ['name', 'url']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for URLObject class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for URLObject class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'url' in self.__dict__:
            json_data['url'] = self.url
        if 'description' in self.__dict__:
            json_data['description'] = self.description
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for URLObject class.")
        if 'url' in kwargs:
            self.url = kwargs['url']


@export
class VariableSet(FMCObject):
    """
    The VariableSet Object in the FMC.
    """

    URL = '/object/variablesets'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for VariableSet class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for VariableSet class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'description' in self.__dict__:
            json_data['description'] = self.description
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for VariableSet class.")

    def post(self):
        logging.info('POST method for API for VariableSets not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for VariableSets not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for VariableSets not supported.')
        pass


@export
class PortObject(FMCObject):
    """
    The Port Object in the FMC.
    """

    URL = '/object/protocolportobjects'
    REQUIRED_FOR_POST = ['name', 'port', 'protocol']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for PortObject class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for PortObject class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'description' in self.__dict__:
            json_data['description'] = self.description
        if 'port' in self.__dict__:
            json_data['port'] = self.port
        if 'protocol' in self.__dict__:
            json_data['protocol'] = self.protocol
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for PortObject class.")
        if 'port' in kwargs:
            self.port = kwargs['port']
        if 'protocol' in kwargs:
            self.protocol = kwargs['protocol']


@export
class SecurityZoneObject(FMCObject):
    """
    The Security Zone Object in the FMC.
    """

    URL = '/object/securityzones'
    REQUIRED_FOR_POST = ['name', 'interfaceMode']
    FILTER_BY_NAME = True

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for SecurityZoneObject class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for SecurityZoneObject class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'description' in self.__dict__:
            json_data['description'] = self.description
        if 'interfaceMode' in self.__dict__:
            json_data['interfaceMode'] = self.interfaceMode
        if 'interfaces' in self.__dict__:
            json_data['interfaces'] = self.interfaces
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for SecurityZoneObject class.")
        if 'interfaceMode' in kwargs:
            self.interfaceMode = kwargs['interfaceMode']
        else:
            self.interfaceMode = 'ROUTED'
        if 'interfaces' in kwargs:
            self.interfaces = kwargs['interfaces']


# ################# API-Explorer Devices Category Things ################# #


@export
class DeviceObject(FMCObject):
    """
    The Device Object in the FMC.
    """

    URL = '/devices/devicerecords'
    REQUIRED_FOR_POST = ['name', 'accessPolicy', 'hostName', 'regKey']
    LICENSES = ['BASE', 'PROTECT', 'MALWARE', 'URLFilter', 'CONTROL', 'VPN']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for DeviceObject class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for DeviceObject class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'hostName' in self.__dict__:
            json_data['hostName'] = self.hostName
        if 'natID' in self.__dict__:
            json_data['natID'] = self.natID
        if 'regKey' in self.__dict__:
            json_data['regKey'] = self.regKey
        if 'license_caps' in self.__dict__:
            json_data['license_caps'] = self.license_caps
        if 'accessPolicy' in self.__dict__:
            json_data['accessPolicy'] = self.accessPolicy
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for DeviceObject class.")
        if 'hostName' in kwargs:
            self.hostName = kwargs['hostName']
        if 'natID' in kwargs:
            self.natID = kwargs['natID']
        if 'regKey' in kwargs:
            self.regKey = kwargs['regKey']
        if 'license_caps' in kwargs:
            self.license_caps = kwargs['license_caps']
        if 'accessPolicy' in kwargs:
            self.accessPolicy = kwargs['accessPolicy']
        if 'acp_name' in kwargs:
            self.acp(name=kwargs['acp_name'])

    def license_add(self, name='BASE'):
        logging.debug("In license_add() for DeviceObject class.")
        if name in self.LICENSES:
            if 'license_caps' in self.__dict__:
                self.license_caps.append(name)
                self.license_caps = list(set(self.license_caps))
            else:
                self.license_caps = [name]

        else:
            logging.warning('{} not found in {}.  Cannot add license to DeviceObject.'.format(name, self.LICENSES))

    def license_remove(self, name=''):
        logging.debug("In license_remove() for DeviceObject class.")
        if name in self.LICENSES:
            if 'license_caps' in self.__dict__:
                try:
                    self.license_caps.remove(name)
                except ValueError:
                    logging.warning('{} is not assigned to this device thus cannot be removed.'.format(name))
            else:
                logging.warning('{} is not assigned to this device thus cannot be removed.'.format(name))

        else:
            logging.warning('{} not found in {}.  Cannot remove license from '
                            'DeviceObject.'.format(name, self.LICENSES))

    def acp(self, name=''):
        logging.debug("In acp() for DeviceObject class.")
        acp = ACPPolicy(fmc=self.fmc)
        acp.get(name=name)
        if 'id' in acp.__dict__:
            self.accessPolicy = {'id': acp.id, 'type': acp.type}
        else:
            logging.warning('Access Control Policy {} not found.  Cannot set up accessPolicy for '
                            'DeviceObject.'.format(name))


# ################# API-Explorer Policy Category Things ################# #


@export
class IntrusionPolicy(FMCObject):
    """
    The Intrusion Policy Object in the FMC.
    """

    URL = '/policy/intrusionpolicies'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for IntrusionPolicy class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for IntrusionPolicy class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for IntrusionPolicy class.")
        if 'name' in kwargs:
            self.name = kwargs['name']

    def post(self):
        logging.info('POST method for API for IntrusionPolicy not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for IntrusionPolicy not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for IntrusionPolicy not supported.')
        pass


@export
class ACPPolicy(FMCObject):
    """
    The Access Control Policy Object in the FMC.
    """

    URL = '/policy/accesspolicies'
    REQUIRED_FOR_POST = ['name']
    DEFAULT_ACTION_OPTIONS = ['BLOCK', 'NETWORK_DISCOVERY', 'IPS']  # Not implemented yet.
    FILTER_BY_NAME = True

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ACPPolicy class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for ACPPolicy class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'description' in self.__dict__:
            json_data['description'] = self.description
        if 'defaultAction' in self.__dict__:
            json_data = self.defaultAction
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for ACPPolicy class.")
        if 'defaultAction' in kwargs:
            self.defaultAction = kwargs['defaultAction']
        else:
            self.defaultAction = {'action': 'BLOCK'}


@export
class ACPRule(FMCObject):
    """
    The ACP Rule Object in the FMC.
    """

    PREFIX_URL = '/policy/accesspolicies'
    URL = None
    REQUIRED_FOR_POST = ['name', 'acp_id']
    VALID_FOR_ACTION = ['ALLOW', 'TRUST', 'BLOCK', 'MONITOR', 'BLOCK_RESET', 'BLOCK_INTERACTIVE',
                        'BLOCK_RESET_INTERACTIVE']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ACPRule class.")
        self.parse_kwargs(**kwargs)

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
            json_data['sourceNetworks'] = self.sourceNetworks
        if 'destinationNetworks' in self.__dict__:
            json_data['destinationNetworks'] = self.destinationNetworks
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
        else:
            self.variable_set()
        if 'ipsPolicy' in kwargs:
            self.ipsPolicy = kwargs['ipsPolicy']

        if 'vlanTags' in kwargs:
            self.vlanTags = kwargs['vlanTags']
        if 'sourcePorts' in kwargs:
            self.sourcePorts = kwargs['sourcePorts']
        if 'destinationPorts' in kwargs:
            self.destinationPorts = kwargs['destinationPorts']
        if 'urls' in kwargs:
            self.urls = kwargs['urls']
        if 'sourceNetworks' in kwargs:
            self.sourceNetworks = kwargs['sourceNetworks']
        if 'destinationNetworks' in kwargs:
            self.destinationNetworks = kwargs['destinationNetworks']
        if 'applications' in kwargs:
            self.applications = kwargs['applications']

    def acp(self, name):
        logging.debug("In acp() for ACPRule class.")
        acp = ACPPolicy(fmc=self.fmc)
        acp.get(name=name)
        if 'id' in acp.__dict__:
            self.acp_id = acp.id
            self.URL = '{}/{}/accessrules'.format(self.PREFIX_URL, self.acp_id)
        else:
            logging.warning('Access Control Policy {} not found.  Cannot set up accessPolicy for '
                            'ACPRule.'.format(name))

    def variable_set(self, name='Default-Set'):
        vs = VariableSet(fmc=self.fmc)
        vs.get(name=name)
        self.variableSet = {'name': vs.name, 'id': vs.id}

    def source_zone_add(self, name):
        logging.debug("In source_zone_add() for ACPRule class.")
        sz = SecurityZoneObject(fmc=self.fmc)
        sz.get(name=name)
        if 'id' in sz.__dict__:
            if 'sourceZones' in self.__dict__:
                new_zone = {'name': sz.name, 'id': sz.id}
                duplicate = False
                for object in self.sourceZones['objects']:
                    if object['name'] == new_zone['name']:
                        duplicate = True
                        break
                if not duplicate:
                    self.sourceZones['objects'].append(new_zone)
            else:
                self.sourceZones = {'objects': [{'name': sz.name, 'id': sz.id}]}
        else:
            logging.warning('Security Zone, {}, not found.  Cannot add to ACPRule.'.format(name))

    def source_zone_remove(self, name):
        logging.debug("In source_zone_remove() for ACPRule class.")
        sz = SecurityZoneObject(fmc=self.fmc)
        sz.get(name=name)
        if 'id' in sz.__dict__:
            if 'sourceZones' in self.__dict__:
                objects = []
                for object in self.sourceZones['objects']:
                    if object['name'] != name:
                        objects.append(object)
                self.sourceZones['objects'] = objects
            else:
                logging.info("sourceZones doesn't exist for this ACPRule.  Nothing to remove.")
        else:
            logging.warning('Security Zone, {}, not found.  Cannot remove from ACPRule.'.format(name))

    def destination_zone_add(self, name):
        logging.debug("In destination_zone_add() for ACPRule class.")
        sz = SecurityZoneObject(fmc=self.fmc)
        sz.get(name=name)
        if 'id' in sz.__dict__:
            if 'destinationZones' in self.__dict__:
                new_zone = {'name': sz.name, 'id': sz.id}
                duplicate = False
                for object in self.destinationZones['objects']:
                    if object['name'] == new_zone['name']:
                        duplicate = True
                        break
                if not duplicate:
                    self.destinationZones['objects'].append(new_zone)
            else:
                self.destinationZones = {'objects': [{'name': sz.name, 'id': sz.id}]}
        else:
            logging.warning('Security Zone, {}, not found.  Cannot add to ACPRule.'.format(name))

    def destination_zone_remove(self, name):
        logging.debug("In destination_zone_remove() for ACPRule class.")
        sz = SecurityZoneObject(fmc=self.fmc)
        sz.get(name=name)
        if 'id' in sz.__dict__:
            if 'destinationZones' in self.__dict__:
                objects = []
                for object in self.destinationZones['objects']:
                    if object['name'] != name:
                        objects.append(object)
                self.destinationZones['objects'] = objects
            else:
                logging.info("destinationZones doesn't exist for this ACPRule.  Nothing to remove.")
        else:
            logging.warning('Security Zone, {}, not found.  Cannot remove from ACPRule.'.format(name))

    def intrusion_policy(self, name=''):
        logging.debug("In intrusion_policy_set() for ACPRule class.")
        if name == '':
            del self.ipsPolicy
        else:
            ips = IntrusionPolicy(fmc=self.fmc, name=name)
            ips.get()
            self.ipsPolicy = {'name': ips.name, 'id': ips.id}
