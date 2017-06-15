"""
This module contains the class objects that represent the various objects in the FMC.
"""

import logging
import datetime
import requests
from .helper_functions import *
from . import export

logging.debug("In the {} module.".format(__name__))


class APIClassTemplate(object):
    """
    This class is the base framework for all the objects in the FMC.
    """

    REQUIRED_FOR_POST = ['name']
    REQUIRED_FOR_PUT = ['id']
    REQUIRED_FOR_DELETE = ['id']
    FILTER_BY_NAME = False
    URL = None
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\-]"""

    def __init__(self, fmc, **kwargs):
        logging.debug("In __init__() for APIClassTemplate class.")
        self.fmc = fmc
        self.URL = '{}{}'.format(self.fmc.configuration_url, self.URL_SUFFIX)

    def parse_kwargs(self, **kwargs):
        logging.debug("In parse_kwargs() for APIClassTemplate class.")
        if 'name' in kwargs:
            self.name = syntax_correcter(kwargs['name'], permitted_syntax=self.VALID_CHARACTERS_FOR_NAME)
            if self.name != kwargs['name']:
                logging.info("""Adjusting name "{}" to "{}" due to containing invalid characters."""
                             .format(kwargs['name'], self.name))
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
        logging.debug("In valid_for_post() for APIClassTemplate class.")
        for item in self.REQUIRED_FOR_POST:
            if item not in self.__dict__:
                return False
        return True

    def valid_for_put(self):
        logging.debug("In valid_for_put() for APIClassTemplate class.")
        for item in self.REQUIRED_FOR_PUT:
            if item not in self.__dict__:
                return False
        return True

    def valid_for_delete(self):
        logging.debug("In valid_for_delete() for APIClassTemplate class.")
        for item in self.REQUIRED_FOR_DELETE:
            if item not in self.__dict__:
                return False
        return True

    def post(self, **kwargs):
        logging.debug("In post() for APIClassTemplate class.")
        if 'id' in self.__dict__:
            logging.info("ID value exists for this object.  Redirecting to put() method.")
            self.put()
        else:
            if self.valid_for_post():
                response = self.fmc.send_to_api(method='post', url=self.URL, json_data=self.format_data())
                self.parse_kwargs(**response)
                logging.info('POST success. Object with name: "{}" and id: "{}" created '
                             'in FMC.'.format(self.name, self.id))
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
        logging.debug("In get() for APIClassTemplate class.")
        self.parse_kwargs(**kwargs)
        if 'id' in self.__dict__:
            url = '{}/{}'.format(self.URL, self.id)
            response = self.fmc.send_to_api(method='get', url=url)
            self.parse_kwargs(**response)
            logging.info('GET success. Object with name: "{}" and id: "{}" fetched from'
                         ' FMC.'.format(self.name, self.id))
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
                    logging.info('GET success. Object with name: "{}" and id: "{}" fetched from'
                                 ' FMC.'.format(self.name, self.id))
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
        logging.debug("In put() for APIClassTemplate class.")
        self.parse_kwargs(**kwargs)
        if self.valid_for_put():
            url = '{}/{}'.format(self.URL, self.id)
            response = self.fmc.send_to_api(method='put', url=url, json_data=self.format_data())
            self.parse_kwargs(**response)
            logging.info('PUT success. Object with name: "{}" and id: "{}" updated '
                         'in FMC.'.format(self.name, self.id))
            return True
        else:
            logging.warning("put() method failed due to failure to pass valid_for_put() test.")
            return False

    def delete(self, **kwargs):
        logging.debug("In delete() for APIClassTemplate class.")
        self.parse_kwargs(**kwargs)
        if self.valid_for_delete():
            url = '{}/{}'.format(self.URL, self.id)
            response = self.fmc.send_to_api(method='delete', url=url, json_data=self.format_data())
            self.parse_kwargs(**response)
            logging.info('DELETE success. Object with name: "{}" and id: "{}" deleted '
                         'in FMC.'.format(self.name, self.id))
            return True
        else:
            logging.warning("delete() method failed due to failure to pass valid_for_delete() test.")
            return False

    '''# Trying to deal with 'name' being set without using the syntax_correcter()
    def namer(self, name):
        logging.debug("In @name.setter name() method for APIClassTemplate class.")
        self.name = syntax_correcter(kwargs['name'], permitted_syntax=self.VALID_CHARACTERS_FOR_NAME)
        if self.name != kwargs['name']:
            logging.info("""Adjusting name "{}" to "{}" due to containing invalid characters."""
                         .format(kwargs['name'], self.name))

    @namer.setter
    def namer(self, name):
        logging.debug("In @name.setter name() method for APIClassTemplate class.")
        self.name = syntax_correcter(kwargs['name'], permitted_syntax=self.VALID_CHARACTERS_FOR_NAME)
        if self.name != kwargs['name']:
            logging.info("""Adjusting name "{}" to "{}" due to containing invalid characters."""
                         .format(kwargs['name'], self.name))
     '''

# ################# API-Explorer Object Category Things ################# #


@export
class IPAddresses(APIClassTemplate):
    """
    The IPAddresses Object in the FMC.
    """

    URL_SUFFIX = '/object/networkaddresses'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for IPAddresses class.")
        self.parse_kwargs(**kwargs)

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for IPAddresses class.")
        if 'items' in kwargs:
            self.items = kwargs['items']

    def post(self):
        logging.info('POST method for API for IPAddresses not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for IPAddresses not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for IPAddresses not supported.')
        pass


@export
class NetworkGroup(APIClassTemplate):
    """
    The NetworkGroup Object in the FMC.
    """

    URL_SUFFIX = '/object/networkgroups'

    # Technically you can have objects OR literals but I'm not set up for "OR" logic, yet.
    REQUIRED_FOR_POST = ['name', 'objects']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for NetworkGroup class.")
        self.parse_kwargs(**kwargs)
        self.type = 'NetworkGroup'

    def format_data(self):
        logging.debug("In format_data() for NetworkGroup class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'objects' in self.__dict__:
            json_data['objects'] = self.objects
        if 'literals' in self.__dict__:
            json_data['literals'] = self.literals
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for NetworkGroup class.")
        if 'objects' in kwargs:
            self.objects = kwargs['objects']
        if 'literals' in kwargs:
            self.literals = kwargs['literals']

    def named_networks(self, action, name=''):
        logging.debug("In named_networks() for NetworkGroup class.")
        if action == 'add':
            net1 = IPAddresses(fmc=self.fmc)
            response = net1.get()
            if 'items' in response:
                new_net = None
                for item in response['items']:
                    if item['name'] == name:
                        new_net = {'name': item['name'], 'id': item['id'], 'type': item['type']}
                        break
                if new_net is None:
                    logging.warning('Network "{}" is not found in FMC.  Cannot add to NetworkGroup.'.format(name))
                else:
                    if 'objects' in self.__dict__:
                        duplicate = False
                        for object in self.objects:
                            if object['name'] == new_net['name']:
                                duplicate = True
                                break
                        if not duplicate:
                            self.objects.append(new_net)
                            logging.info('Adding "{}" to NetworkGroup.'.format(name))
                    else:
                        self.objects = [new_net]
                        logging.info('Adding "{}" to NetworkGroup.'.format(name))
        elif action == 'remove':
            if 'objects' in self.__dict__:
                objects_list = []
                for obj in self.objects:
                    if obj['name'] != name:
                        objects_list.append(obj)
                self.objects = objects_list
                logging.info('Removed "{}" from NetworkGroup.'.format(name))
            else:
                logging.info("This NetworkObject has no named_networks.  Nothing to remove.")
        elif action == 'clear':
            if 'objects' in self.__dict__:
                del self.objects
                logging.info('All named_networks removed from this NetworkGroup.')

    def unnamed_networks(self, action, value=''):
        logging.debug("In unnamed_networks() for NetworkGroup class.")
        if action == 'add':
            if value == '':
                logging.error('Value assignment required to add unamed_network to NetworkGroup.')
                return
            literal_type = get_networkaddress_type(value=value)
            if literal_type == 'host' or literal_type == 'network':
                new_literal = {'value': value, 'type': literal_type}
            elif literal_type == 'range':
                logging.error('Ranges are not supported as unnamed_networks in a NetworkGroup.')
            else:
                logging.error('Value "{}" provided is not in a recognizable format.'.format(value))
                return
            if 'literals' in self.__dict__:
                duplicate = False
                for obj in self.literals:
                    if obj['value'] == new_literal['value']:
                        duplicate = True
                        break
                if not duplicate:
                    self.literals.append(new_literal)
                    logging.info('Adding "{}" to NetworkGroup.'.format(value))
            else:
                self.literals = [new_literal]
                logging.info('Adding "{}" to NetworkGroup.'.format(value))
        elif action == 'remove':
            if 'literals' in self.__dict__:
                literals_list = []
                for obj in self.literals:
                    if obj['value'] != value:
                        literals_list.append(obj)
                self.literals = literals_list
                logging.info('Removed "{}" from NetworkGroup.'.format(value))
            else:
                logging.info("This NetworkObject has no unnamed_networks.  Nothing to remove.")
        elif action == 'clear':
            if 'literals' in self.__dict__:
                del self.literals
                logging.info('All unnamed_networks removed from this NetworkGroup.')


@export
class IPHost(APIClassTemplate):
    """
    The Host Object in the FMC.
    """

    URL_SUFFIX = '/object/hosts'
    REQUIRED_FOR_POST = ['name', 'value']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for IPHost class.")
        self.parse_kwargs(**kwargs)
        if 'value' in kwargs:
            value_type = get_networkaddress_type(kwargs['value'])
            if value_type == 'range':
                logging.warning("value, {}, is of type {}.  Limited functionality for this object due to it being "
                                "created via the IPHost function.".format(kwargs['value'], value_type))
            if value_type == 'network':
                logging.warning("value, {}, is of type {}.  Limited functionality for this object due to it being "
                                "created via the IPHost function.".format(kwargs['value'], value_type))
            if validate_ip_bitmask_range(value=kwargs['value'], value_type=value_type):
                self.value = kwargs['value']
            else:
                logging.error("Provided value, {}, has an error with the IP address(es).".format(kwargs['value']))

    def format_data(self):
        logging.debug("In format_data() for IPHost class.")
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
        logging.debug("In parse_kwargs() for IPHost class.")
        if 'value' in kwargs:
            self.value = kwargs['value']


@export
class IPNetwork(APIClassTemplate):
    """
    The Network Object in the FMC.
    """

    URL_SUFFIX = '/object/networks'
    REQUIRED_FOR_POST = ['name', 'value']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for IPNetwork class.")
        self.parse_kwargs(**kwargs)
        if 'value' in kwargs:
            value_type = get_networkaddress_type(kwargs['value'])
            if value_type == 'range':
                logging.warning("value, {}, is of type {}.  Limited functionality for this object due to it being "
                                "created via the IPNetwork function.".format(kwargs['value'], value_type))
            if value_type == 'host':
                logging.warning("value, {}, is of type {}.  Limited functionality for this object due to it being "
                                "created via the IPNetwork function.".format(kwargs['value'], value_type))
            if validate_ip_bitmask_range(value=kwargs['value'], value_type=value_type):
                self.value = kwargs['value']
            else:
                logging.error("Provided value, {}, has an error with the IP address(es).".format(kwargs['value']))

    def format_data(self):
        logging.debug("In format_data() for IPNetwork class.")
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
        logging.debug("In parse_kwargs() for IPNetwork class.")
        if 'value' in kwargs:
            self.value = kwargs['value']


@export
class IPRange(APIClassTemplate):
    """
    The Range Object in the FMC.
    """

    URL_SUFFIX = '/object/ranges'
    REQUIRED_FOR_POST = ['name', 'value']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for IPRange class.")
        self.parse_kwargs(**kwargs)
        if 'value' in kwargs:
            value_type = get_networkaddress_type(kwargs['value'])
            if value_type == 'host':
                logging.warning("value, {}, is of type {}.  Limited functionality for this object due to it being "
                                "created via the IPRange function.".format(kwargs['value'], value_type))
            if value_type == 'network':
                logging.warning("value, {}, is of type {}.  Limited functionality for this object due to it being "
                                "created via the IPRange function.".format(kwargs['value'], value_type))
            if validate_ip_bitmask_range(value=kwargs['value'], value_type=value_type):
                self.value = kwargs['value']
            else:
                logging.error("Provided value, {}, has an error with the IP address(es).".format(kwargs['value']))

    def format_data(self):
        logging.debug("In format_data() for IPRange class.")
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
        logging.debug("In parse_kwargs() for IPRange class.")
        if 'value' in kwargs:
            self.value = kwargs['value']


@export
class URL(APIClassTemplate):
    """
    The URL Object in the FMC.
    """

    URL_SUFFIX = '/object/urls'
    REQUIRED_FOR_POST = ['name', 'url']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for URL class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for URL class.")
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
        logging.debug("In parse_kwargs() for URL class.")
        if 'url' in kwargs:
            self.url = kwargs['url']


@export
class VlanTag(APIClassTemplate):
    """
    The URL Object in the FMC.
    """

    URL_SUFFIX = '/object/vlantags'
    REQUIRED_FOR_POST = ['name', 'data']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for VlanTag class.")
        self.type = 'VlanTag'
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for VlanTag class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'data' in self.__dict__:
            json_data['data'] = self.data
        if 'description' in self.__dict__:
            json_data['description'] = self.description
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for VlanTag class.")
        if 'data' in kwargs:
            self.data = kwargs['data']

    def vlans(self, start_vlan, end_vlan=''):
        logging.debug("In vlans() for VlanTag class.")
        if self.validate_vlans(start_vlan=start_vlan, end_vlan=end_vlan):
            if end_vlan == '':
                end_vlan = start_vlan
            if int(end_vlan) < int(start_vlan):
                tmp = end_vlan
                end_vlan = start_vlan
                start_vlan = tmp
            self.data = {'startTag': start_vlan, 'endTag': end_vlan}
        else:
            logging.info('VLANs: {}-{} given are not valid.'.format(start_vlan, end_vlan) )

    def validate_vlans(self, start_vlan, end_vlan):
        logging.debug("In validate_vlans() for VlanTag class.")
        if int(start_vlan) > 0 and int(start_vlan) < 4095 and int(end_vlan) > 0 and int(end_vlan) < 4095:
            return True
        return False


@export
class VariableSet(APIClassTemplate):
    """
    The VariableSet Object in the FMC.
    """

    URL_SUFFIX = '/object/variablesets'

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
class ProtocolPort(APIClassTemplate):
    """
    The Port Object in the FMC.
    """

    URL_SUFFIX = '/object/protocolportobjects'
    REQUIRED_FOR_POST = ['name', 'port', 'protocol']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ProtocolPort class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for ProtocolPort class.")
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
        logging.debug("In parse_kwargs() for ProtocolPort class.")
        if 'port' in kwargs:
            self.port = kwargs['port']
        if 'protocol' in kwargs:
            self.protocol = kwargs['protocol']


@export
class SecurityZone(APIClassTemplate):
    """
    The Security Zone Object in the FMC.
    """

    URL_SUFFIX = '/object/securityzones'
    REQUIRED_FOR_POST = ['name', 'interfaceMode']
    FILTER_BY_NAME = True

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for SecurityZone class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for SecurityZone class.")
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
        logging.debug("In parse_kwargs() for SecurityZone class.")
        if 'interfaceMode' in kwargs:
            self.interfaceMode = kwargs['interfaceMode']
        else:
            self.interfaceMode = 'ROUTED'
        if 'interfaces' in kwargs:
            self.interfaces = kwargs['interfaces']


# ################# API-Explorer Devices Category Things ################# #


@export
class Device(APIClassTemplate):
    """
    The Device Object in the FMC.
    """

    URL_SUFFIX = '/devices/devicerecords'
    REQUIRED_FOR_POST = ['name', 'accessPolicy', 'hostName', 'regKey']
    LICENSES = ['BASE', 'PROTECT', 'MALWARE', 'URLFilter', 'CONTROL', 'VPN']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Device class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for Device class.")
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
        logging.debug("In parse_kwargs() for Device class.")
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

    def licensing(self, action, name='BASE'):
        logging.debug("In licensing() for Device class.")
        if action == 'add':
            if name in self.LICENSES:
                if 'license_caps' in self.__dict__:
                    self.license_caps.append(name)
                    self.license_caps = list(set(self.license_caps))
                else:
                    self.license_caps = [name]
                logging.info('License "{}" added to this Device object.'.format(name))

            else:
                logging.warning('{} not found in {}.  Cannot add license to Device.'.format(name, self.LICENSES))
        elif action == 'remove':
            if name in self.LICENSES:
                if 'license_caps' in self.__dict__:
                    try:
                        self.license_caps.remove(name)
                    except ValueError:
                        logging.warning('{} is not assigned to this device thus cannot be removed.'.format(name))
                    logging.info('License "{}" removed from this Device object.'.format(name))
                else:
                    logging.warning('{} is not assigned to this device thus cannot be removed.'.format(name))

            else:
                logging.warning('{} not found in {}.  Cannot remove license from '
                                'Device.'.format(name, self.LICENSES))
        elif action == 'clear':
            if 'license_caps' in self.__dict__:
                del self.license_caps
                logging.info('All licensing removed from this Device object.')

    def acp(self, name=''):
        logging.debug("In acp() for Device class.")
        acp = AccessControlPolicy(fmc=self.fmc)
        acp.get(name=name)
        if 'id' in acp.__dict__:
            self.accessPolicy = {'id': acp.id, 'type': acp.type}
        else:
            logging.warning('Access Control Policy {} not found.  Cannot set up accessPolicy for '
                            'Device.'.format(name))


# ################# API-Explorer Policy Category Things ################# #


@export
class IntrusionPolicy(APIClassTemplate):
    """
    The Intrusion Policy Object in the FMC.
    """

    URL_SUFFIX = '/policy/intrusionpolicies'
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""


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
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for IntrusionPolicy class.")

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
class AccessControlPolicy(APIClassTemplate):
    """
    The Access Control Policy Object in the FMC.
    """

    URL_SUFFIX = '/policy/accesspolicies'
    REQUIRED_FOR_POST = ['name']
    DEFAULT_ACTION_OPTIONS = ['BLOCK', 'NETWORK_DISCOVERY', 'IPS']  # Not implemented yet.
    FILTER_BY_NAME = True

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for AccessControlPolicy class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for AccessControlPolicy class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'description' in self.__dict__:
            json_data['description'] = self.description
        if 'defaultAction' in self.__dict__:
            json_data['defaultAction'] = self.defaultAction
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for AccessControlPolicy class.")
        if 'defaultAction' in kwargs:
            self.defaultAction = kwargs['defaultAction']
        else:
            self.defaultAction = {'action': 'BLOCK'}

    def put(self, **kwargs):
        logging.info('The put() method for the AccessControlPolicy() class can work but I need to write a '
                     'DefaultAction() class and accommodate for such before "putting".')
        pass


@export
class ACPRule(APIClassTemplate):
    """
    The ACP Rule Object in the FMC.
    """

    PREFIX_URL = '/policy/accesspolicies'
    URL_SUFFIX = None
    REQUIRED_FOR_POST = ['name', 'acp_id']
    VALID_FOR_ACTION = ['ALLOW', 'TRUST', 'BLOCK', 'MONITOR', 'BLOCK_RESET', 'BLOCK_INTERACTIVE',
                        'BLOCK_RESET_INTERACTIVE']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ACPRule class.")
        self.type = 'AccessRule'
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
            self.variable_set(action='set')
        if 'ipsPolicy' in kwargs:
            self.ipsPolicy = kwargs['ipsPolicy']
        if 'vlanTags' in kwargs:
            self.vlanTags = kwargs['vlanTags']
        if 'sourcePorts' in kwargs:
            self.sourcePorts = kwargs['sourcePorts']
        if 'destinationPorts' in kwargs:
            self.destinationPorts = kwargs['destinationPorts']
        if 'sourceNetworks' in kwargs:
            self.sourceNetworks = kwargs['sourceNetworks']
        if 'destinationNetworks' in kwargs:
            self.destinationNetworks = kwargs['destinationNetworks']
        if 'urls' in kwargs:
            self.urls = kwargs['urls']
        if 'applications' in kwargs:
            self.applications = kwargs['applications']

    def acp(self, name):
        logging.debug("In acp() for ACPRule class.")
        acp1 = AccessControlPolicy(fmc=self.fmc)
        acp1.get(name=name)
        if 'id' in acp1.__dict__:
            self.acp_id = acp1.id
            self.URL = '{}{}/{}/accessrules'.format(self.fmc.configuration_url, self.PREFIX_URL, self.acp_id)
        else:
            logging.warning('Access Control Policy {} not found.  Cannot set up accessPolicy for '
                            'ACPRule.'.format(name))

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
                    for object in self.sourceZones['objects']:
                        if object['name'] == new_zone['name']:
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
                    for object in self.sourceZones['objects']:
                        if object['name'] != name:
                            objects.append(object)
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
                    for object in self.destinationZones['objects']:
                        if object['name'] == new_zone['name']:
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
                    for object in self.destinationZones['objects']:
                        if object['name'] != name:
                            objects.append(object)
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
                    for object in self.vlanTags['objects']:
                        if object['name'] == new_vlan['name']:
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
                    for object in self.vlanTags['objects']:
                        if object['name'] != name:
                            objects.append(object)
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
            pport = ProtocolPort(fmc=self.fmc)
            pport.get(name=name)
            if 'id' in pport.__dict__:
                if 'sourcePorts' in self.__dict__:
                    new_port = {'name': pport.name, 'id': pport.id, 'type': pport.type}
                    duplicate = False
                    for object in self.sourcePorts['objects']:
                        if object['name'] == new_port['name']:
                            duplicate = True
                            break
                    if not duplicate:
                        self.sourcePorts['objects'].append(new_port)
                        logging.info('Adding "{}" to sourcePorts for this ACPRule.'.format(name))
                else:
                    self.sourcePorts = {'objects': [{'name': pport.name, 'id': pport.id, 'type': pport.type}]}
                    logging.info('Adding "{}" to sourcePorts for this ACPRule.'.format(name))
            else:
                logging.warning('Protocol Port, "{}", not found.  Cannot add to ACPRule.'.format(name))
        elif action == 'remove':
            pport = ProtocolPort(fmc=self.fmc)
            pport.get(name=name)
            if 'id' in pport.__dict__:
                if 'sourcePorts' in self.__dict__:
                    objects = []
                    for object in self.sourcePorts['objects']:
                        if object['name'] != name:
                            objects.append(object)
                    self.sourcePorts['objects'] = objects
                    logging.info('Removed "{}" from sourcePorts for this ACPRule.'.format(name))
                else:
                    logging.info("sourcePorts doesn't exist for this ACPRule.  Nothing to remove.")
            else:
                logging.warning('Protocol Port, "{}", not found.  Cannot remove from ACPRule.'.format(name))
        elif action == 'clear':
            if 'sourcePorts' in self.__dict__:
                del self.sourcePorts
                logging.info('All Source Ports removed from this ACPRule object.')

    def destination_port(self, action, name=''):
        logging.debug("In destination_port() for ACPRule class.")
        if action == 'add':
            pport = ProtocolPort(fmc=self.fmc)
            pport.get(name=name)
            if 'id' in pport.__dict__:
                if 'destinationPorts' in self.__dict__:
                    new_port = {'name': pport.name, 'id': pport.id, 'type': pport.type}
                    duplicate = False
                    for object in self.destinationPorts['objects']:
                        if object['name'] == new_port['name']:
                            duplicate = True
                            break
                    if not duplicate:
                        self.destinationPorts['objects'].append(new_port)
                        logging.info('Adding "{}" to destinationPorts for this ACPRule.'.format(name))
                else:
                    self.destinationPorts = {'objects': [{'name': pport.name, 'id': pport.id, 'type': pport.type}]}
                    logging.info('Adding "{}" to destinationPorts for this ACPRule.'.format(name))
            else:
                logging.warning('Protocol Port, "{}", not found.  Cannot add to ACPRule.'.format(name))
        elif action == 'remove':
            pport = ProtocolPort(fmc=self.fmc)
            pport.get(name=name)
            if 'id' in pport.__dict__:
                if 'destinationPorts' in self.__dict__:
                    objects = []
                    for object in self.destinationPorts['objects']:
                        if object['name'] != name:
                            objects.append(object)
                    self.destinationPorts['objects'] = objects
                    logging.info('Removed "{}" from destinationPorts for this ACPRule.'.format(name))
                else:
                    logging.info("destinationPorts doesn't exist for this ACPRule.  Nothing to remove.")
            else:
                logging.warning('Protocol Port, {}, not found.  Cannot remove from ACPRule.'.format(name))
        elif action == 'clear':
            if 'destinationPorts' in self.__dict__:
                del self.destinationPorts
                logging.info('All Destination Ports removed from this ACPRule object.')

    def source_network(self, action, name=''):
        logging.debug("In source_network() for ACPRule class.")
        if action == 'add':
            net1 = IPAddresses(fmc=self.fmc)
            response = net1.get()
            if 'items' in response:
                new_net = None
                for item in response['items']:
                    if item['name'] == name:
                        new_net = {'name': item['name'], 'id': item['id'], 'type': item['type']}
                        break
                if new_net is None:
                    logging.warning('Network "{}" is not found in FMC.  Cannot add to sourceNetworks.'.format(name))
                else:
                    if 'sourceNetworks' in self.__dict__:
                        duplicate = False
                        for object in self.sourceNetworks['objects']:
                            if object['name'] == new_net['name']:
                                duplicate = True
                                break
                        if not duplicate:
                            self.sourceNetworks['objects'].append(new_net)
                            logging.info('Adding "{}" to sourceNetworks for this ACPRule.'.format(name))
                    else:
                        self.sourceNetworks = {'objects': [new_net]}
                        logging.info('Adding "{}" to sourceNetworks for this ACPRule.'.format(name))
        elif action == 'remove':
            if 'sourceNetworks' in self.__dict__:
                objects = []
                for object in self.sourceNetworks['objects']:
                    if object['name'] != name:
                        objects.append(object)
                self.sourceNetworks['objects'] = objects
                logging.info('Removed "{}" from sourceNetworks for this ACPRule.'.format(name))
            else:
                logging.info("sourceNetworks doesn't exist for this ACPRule.  Nothing to remove.")
        elif action == 'clear':
            if 'sourceNetworks' in self.__dict__:
                del self.sourceNetworks
                logging.info('All Source Networks removed from this ACPRule object.')

    def destination_network(self, action, name=''):
        logging.debug("In destination_network() for ACPRule class.")
        if action == 'add':
            net1 = IPAddresses(fmc=self.fmc)
            response = net1.get()
            if 'items' in response:
                new_net = None
                for item in response['items']:
                    if item['name'] == name:
                        new_net = {'name': item['name'], 'id': item['id'], 'type': item['type']}
                        break
                if new_net is None:
                    logging.warning('Network "{}" is not found in FMC.  Cannot add to destinationNetworks.'.format(name))
                else:
                    if 'destinationNetworks' in self.__dict__:
                        duplicate = False
                        for object in self.destinationNetworks['objects']:
                            if object['name'] == new_net['name']:
                                duplicate = True
                                break
                        if not duplicate:
                            self.destinationNetworks['objects'].append(new_net)
                            logging.info('Adding "{}" to destinationNetworks for this ACPRule.'.format(name))
                    else:
                        self.destinationNetworks = {'objects': [new_net]}
                        logging.info('Adding "{}" to destinationNetworks for this ACPRule.'.format(name))
        elif action == 'remove':
            if 'destinationNetworks' in self.__dict__:
                objects = []
                for object in self.destinationNetworks['objects']:
                    if object['name'] != name:
                        objects.append(object)
                self.destinationNetworks['objects'] = objects
                logging.info('Removed "{}" from destinationNetworks for this ACPRule.'.format(name))
            else:
                logging.info("destinationNetworks doesn't exist for this ACPRule.  Nothing to remove.")
        elif action == 'clear':
            if 'destinationNetworks' in self.__dict__:
                del self.destinationNetworks
                logging.info('All Destination Networks removed from this ACPRule object.')
