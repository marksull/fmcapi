"""
This module contains the class objects that represent the various objects in the FMC.
"""

from .helper_functions import *

logging.debug("In the {} module.".format(__name__))


class APIClassTemplate(object):
    """
    This class is the base framework for all the objects in the FMC.
    """

    REQUIRED_FOR_POST = ['name']
    REQUIRED_FOR_PUT = ['id']
    REQUIRED_FOR_DELETE = ['id']
    FILTER_BY_NAME = False
    URL = ''
    URL_SUFFIX = ''
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
        if 'items' in kwargs:
            self.items = kwargs['items']

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
                if response:
                    self.parse_kwargs(**response)
                    if 'name' in self.__dict__ and 'id' in self.__dict__:
                        logging.info('POST success. Object with name: "{}" and id: "{}" created '
                                     'in FMC.'.format(self.name, self.id))
                    else:
                        logging.info('POST success but no "id" or "name" values in API response.')
                else:
                    logging.warning('POST failure.  No data in API response.')
                return response
            else:
                logging.warning("post() method failed due to failure to pass valid_for_post() test.")
                return False

    def format_data(self):
        logging.debug("In format_data() for APIClassTemplate class.")

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
            return response
        elif 'name' in self.__dict__:
            if self.FILTER_BY_NAME:
                url = '{}?name={}&expanded=true'.format(self.URL, self.name)
            else:
                url = '{}?expanded=true'.format(self.URL)
            response = self.fmc.send_to_api(method='get', url=url)
            for item in response['items']:
                if 'name' in item:
                    if item['name'] == self.name:
                        self.id = item['id']
                        self.parse_kwargs(**item)
                        logging.info('GET success. Object with name: "{}" and id: "{}" fetched from'
                                     ' FMC.'.format(self.name, self.id))
                        return item
                else:
                    logging.warning('No "name" attribute associated with '
                                    'this item to check against {}.'.format(self.name))
            if 'id' not in self.__dict__:
                logging.warning("\tGET query for {} is not found.\n\t\t"
                                "Response: {}".format(self.name, json.dumps(response)))
            return response
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
            return response
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
            return response
        else:
            logging.warning("delete() method failed due to failure to pass valid_for_delete() test.")
            return False

# ################# API-Explorer Object Category Things ################# #


class IPAddresses(APIClassTemplate):
    """
    The IPAddresses Object in the FMC.
    """

    URL_SUFFIX = '/object/networkaddresses'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for IPAddresses class.")
        self.parse_kwargs(**kwargs)

    def post(self):
        logging.info('POST method for API for IPAddresses not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for IPAddresses not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for IPAddresses not supported.')
        pass


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
                        for obj in self.objects:
                            if obj['name'] == new_net['name']:
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
                logging.info("This NetworkGroup has no named_networks.  Nothing to remove.")
        elif action == 'clear':
            if 'objects' in self.__dict__:
                del self.objects
                logging.info('All named_networks removed from this NetworkGroup.')

    def unnamed_networks(self, action, value=''):
        logging.debug("In unnamed_networks() for NetworkGroup class.")
        new_literal = []
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
                logging.info("This NetworkGroup has no unnamed_networks.  Nothing to remove.")
        elif action == 'clear':
            if 'literals' in self.__dict__:
                del self.literals
                logging.info('All unnamed_networks removed from this NetworkGroup.')


class ApplicationCategory(APIClassTemplate):
    """
    The ApplicationCategory Object in the FMC.
    """

    URL_SUFFIX = '/object/applicationcategories'
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ApplicationCategory class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for ApplicationCategory class.")
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
        logging.debug("In parse_kwargs() for ApplicationCategory class.")

    def post(self):
        logging.info('POST method for API for ApplicationCategory not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for ApplicationCategory not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for ApplicationCategory not supported.')
        pass


class ApplicationProductivity(APIClassTemplate):
    """
    The ApplicationProductivity Object in the FMC.
    """

    URL_SUFFIX = '/object/applicationproductivities'
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ApplicationProductivity class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for ApplicationProductivity class.")
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
        logging.debug("In parse_kwargs() for ApplicationProductivity class.")

    def post(self):
        logging.info('POST method for API for ApplicationProductivity not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for ApplicationProductivity not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for ApplicationProductivity not supported.')
        pass


class ApplicationRisk(APIClassTemplate):
    """
    The ApplicationRisk Object in the FMC.
    """

    URL_SUFFIX = '/object/applicationrisks'
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ApplicationRisk class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for ApplicationRisk class.")
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
        logging.debug("In parse_kwargs() for ApplicationRisk class.")

    def post(self):
        logging.info('POST method for API for ApplicationRisk not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for ApplicationRisk not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for ApplicationRisk not supported.')
        pass


class Application(APIClassTemplate):
    """
    The Application Object in the FMC.
    """

    URL_SUFFIX = '/object/applications'
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\-\/\. ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Application class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for Application class.")
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
        logging.debug("In parse_kwargs() for Application class.")
        if 'appProductivity' in kwargs:
            self.appProductivity = kwargs['appProductivity']
        if 'appCategories' in kwargs:
            self.appCategories = kwargs['appCategories']
        if 'appTags' in kwargs:
            self.appTags = kwargs['appTags']
        if 'appId' in kwargs:
            self.appId = kwargs['appId']
        if 'risk' in kwargs:
            self.risk = kwargs['risk']
        if 'applicationTypes' in kwargs:
            self.applicationTypes = kwargs['applicationTypes']

    def post(self):
        logging.info('POST method for API for Application not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for Application not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for Application not supported.')
        pass


class ApplicationTag(APIClassTemplate):
    """
    The ApplicationTag Object in the FMC.
    """

    URL_SUFFIX = '/object/applicationtags'
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\-\/\. ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ApplicationTag class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for ApplicationTag class.")
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
        logging.debug("In parse_kwargs() for ApplicationTag class.")

    def post(self):
        logging.info('POST method for API for ApplicationTag not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for ApplicationTag not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for ApplicationTag not supported.')
        pass


class ApplicationType(APIClassTemplate):
    """
    The ApplicationType Object in the FMC.
    """

    URL_SUFFIX = '/object/applicationtypes'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ApplicationTag class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for ApplicationType class.")
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
        logging.debug("In parse_kwargs() for ApplicationType class.")

    def post(self):
        logging.info('POST method for API for ApplicationType not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for ApplicationType not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for ApplicationType not supported.')
        pass

class SLAMonitor(APIClassTemplate):
    """
    The SLAMonitor Object in the FMC.
    """
    URL_SUFFIX = '/object/slamonitors'
    REQUIRED_FOR_POST = ['name', 'slaId', 'monitorAddress', 'interfaceObjects', 'type']
    REQUIRED_FOR_PUT = ['id','type']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for SLAMonitor class.")
        self.parse_kwargs(**kwargs)
        self.type = "SLAMonitor"

    def format_data(self):
        logging.debug("In format_data() for SLAMonitor class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'timeout' in self.__dict__:
            json_data['timeout'] = self.timeout
        if 'threshold' in self.__dict__:
            json_data['threshold'] = self.threshold
        if 'frequency' in self.__dict__:
            json_data['frequency'] = self.frequency
        if 'slaId' in self.__dict__:
            json_data['slaId'] = self.slaId
        if 'dataSize' in self.__dict__:
            json_data['dataSize'] = self.dataSize
        if 'tos' in self.__dict__:
            json_data['tos'] = self.tos
        if 'noOfPackets' in self.__dict__:
            json_data['noOfPackets'] = self.noOfPackets
        if 'monitorAddress' in self.__dict__:
            json_data['monitorAddress'] = self.monitorAddress
        if 'interfaceObjects' in self.__dict__:
            json_data['interfaceObjects'] = self.interfaceObjects
        if 'description' in self.__dict__:
            json_data['description'] = self.description
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for SLAMonitor class.")
        if 'timeout' in kwargs:
            self.timeout = kwargs['timeout']
        if 'threshold' in kwargs:
             self.securityZone = kwargs['threshold']
        if 'frequency' in kwargs:
            self.frequency = kwargs['frequency']
        if 'slaId' in kwargs:
            self.slaId = kwargs['slaId']
        if 'dataSize' in kwargs:
            self.dataSize = kwargs['dataSize']
        if 'tos' in kwargs:
            self.tos = kwargs['tos']
        if 'noOfPackets' in kwargs:
            self.noOfPackets = kwargs['noOfPackets']
        if 'monitorAddress' in kwargs:
            self.monitorAddress = kwargs['monitorAddress']
        if 'interfaceObjects' in kwargs:
            self.interfaceObjects = kwargs['interfaceObjects']
        if 'description' in kwargs:
            self.description = kwargs['description']

    def interfaces(self, names):
        logging.debug("In interfaces() for SLAMonitor class.")
        zones = []
        for name in names:
            #Supports passing list of str
            sz = SecurityZone(fmc=self.fmc)
            sz.get(name=name)
            if 'id' in sz.__dict__:
                zones.append({'name': sz.name, 'id': sz.id, 'type': sz.type})
            else:
                logging.warning('Security Zone, "{}", not found.  Cannot add to SLAMonitor.'.format(name))
        if len(zones) != 0:
            #Make sure we found at least one zone
            self.interfaceObjects = zones
        else:
            logging.warning('No valid Security Zones found: "{}".  Cannot add to SLAMonitor.'.format(names))

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


class URLGroup(APIClassTemplate):
    """
    The URLGroup Object in the FMC.
    """

    URL_SUFFIX = '/object/urlgroups'

    # Technically you can have objects OR literals but I'm not set up for "OR" logic, yet.
    REQUIRED_FOR_POST = ['name', 'objects']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for URLGroup class.")
        self.parse_kwargs(**kwargs)
        self.type = 'URLGroup'

    def format_data(self):
        logging.debug("In format_data() for URLGroup class.")
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
        logging.debug("In parse_kwargs() for URLGroup class.")
        if 'objects' in kwargs:
            self.objects = kwargs['objects']
        if 'literals' in kwargs:
            self.literals = kwargs['literals']

    def named_urls(self, action, name=''):
        logging.debug("In named_urls() for URLGroup class.")
        if action == 'add':
            url1 = URL(fmc=self.fmc)
            response = url1.get()
            if 'items' in response:
                new_url = None
                for item in response['items']:
                    if item['name'] == name:
                        new_url = {'name': item['name'], 'id': item['id'], 'type': item['type']}
                        break
                if new_url is None:
                    logging.warning('URL "{}" is not found in FMC.  Cannot add to URLGroup.'.format(name))
                else:
                    if 'objects' in self.__dict__:
                        duplicate = False
                        for obj in self.objects:
                            if obj['name'] == new_url['name']:
                                duplicate = True
                                break
                        if not duplicate:
                            self.objects.append(new_url)
                            logging.info('Adding "{}" to URLGroup.'.format(name))
                    else:
                        self.objects = [new_url]
                        logging.info('Adding "{}" to URLGroup.'.format(name))
        elif action == 'remove':
            if 'objects' in self.__dict__:
                objects_list = []
                for obj in self.objects:
                    if obj['name'] != name:
                        objects_list.append(obj)
                self.objects = objects_list
                logging.info('Removed "{}" from URLGroup.'.format(name))
            else:
                logging.info("This URLGroup has no named_urls.  Nothing to remove.")
        elif action == 'clear':
            if 'objects' in self.__dict__:
                del self.objects
                logging.info('All named_urls removed from this URLGroup.')

    def unnamed_urls(self, action, value=''):
        logging.debug("In unnamed_urls() for URLGroup class.")
        if action == 'add':
            if value == '':
                logging.error('Value assignment required to add unamed_url to URLGroup.')
                return
            value_type = 'Url'
            new_literal = {'type': value_type, 'url': value}
            if 'literals' in self.__dict__:
                duplicate = False
                for obj in self.literals:
                    if obj['url'] == new_literal['url']:
                        duplicate = True
                        break
                if not duplicate:
                    self.literals.append(new_literal)
                    logging.info('Adding "{}" to URLGroup.'.format(value))
            else:
                self.literals = [new_literal]
                logging.info('Adding "{}" to URLGroup.'.format(value))
        elif action == 'remove':
            if 'literals' in self.__dict__:
                literals_list = []
                for obj in self.literals:
                    if obj['url'] != value:
                        literals_list.append(obj)
                self.literals = literals_list
                logging.info('Removed "{}" from URLGroup.'.format(value))
            else:
                logging.info("This URLGroup has no unnamed_urls.  Nothing to remove.")
        elif action == 'clear':
            if 'literals' in self.__dict__:
                del self.literals
                logging.info('All unnamed_urls removed from this URLGroup.')


class URLCategory(APIClassTemplate):
    """
    The URLCategory Object in the FMC.
    """

    URL_SUFFIX = '/object/urlcategories'
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\-\/\.\(\) ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for URLCategory class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for URLCategory class.")
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
        logging.debug("In parse_kwargs() for URLCategory class.")

    def post(self):
        logging.info('POST method for API for URLCategory not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for URLCategory not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for URLCategory not supported.')
        pass


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
        start_vlan, end_vlan = validate_vlans(start_vlan=start_vlan, end_vlan=end_vlan)
        self.data = {'startTag': start_vlan, 'endTag': end_vlan}


class VlanGroupTag(APIClassTemplate):
    """
    The NetworkGroup Object in the FMC.
    """

    URL_SUFFIX = '/object/vlangrouptags'

    # Technically you can have objects OR literals but I'm not set up for "OR" logic, yet.
    REQUIRED_FOR_POST = ['name', 'objects']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for VlanGroupTag class.")
        self.parse_kwargs(**kwargs)
        self.type = 'VlanGroupTag'

    def format_data(self):
        logging.debug("In format_data() for VlanGroupTag class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'description' in self.__dict__:
            json_data['description'] = self.description
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'objects' in self.__dict__:
            json_data['objects'] = self.objects
        if 'literals' in self.__dict__:
            json_data['literals'] = self.literals
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for VlanGroupTag class.")
        if 'objects' in kwargs:
            self.objects = kwargs['objects']
        if 'literals' in kwargs:
            self.literals = kwargs['literals']

    def named_vlantags(self, action, name=''):
        logging.debug("In named_vlantags() for VlanGroupTag class.")
        if action == 'add':
            vlan1 = VlanTag(fmc=self.fmc)
            response = vlan1.get()
            if 'items' in response:
                new_vlan = None
                for item in response['items']:
                    if item['name'] == name:
                        new_vlan = {'name': item['name'], 'id': item['id'], 'type': item['type']}
                        break
                if new_vlan is None:
                    logging.warning('VlanTag "{}" is not found in FMC.  Cannot add to VlanGroupTag.'.format(name))
                else:
                    if 'objects' in self.__dict__:
                        duplicate = False
                        for obj in self.objects:
                            if obj['name'] == new_vlan['name']:
                                duplicate = True
                                break
                        if not duplicate:
                            self.objects.append(new_vlan)
                            logging.info('Adding "{}" to VlanGroupTag.'.format(name))
                    else:
                        self.objects = [new_vlan]
                        logging.info('Adding "{}" to VlanGroupTag.'.format(name))
        elif action == 'remove':
            if 'objects' in self.__dict__:
                objects_list = []
                for obj in self.objects:
                    if obj['name'] != name:
                        objects_list.append(obj)
                self.objects = objects_list
                logging.info('Removed "{}" from VlanGroupTag.'.format(name))
            else:
                logging.info("This VlanGroupTag has no named_vlantags.  Nothing to remove.")
        elif action == 'clear':
            if 'objects' in self.__dict__:
                del self.objects
                logging.info('All named_vlantags removed from this VlanGroupTag.')

    def unnamed_vlantags(self, action, startvlan='', endvlan=''):
        logging.debug("In unnamed_vlantags() for VlanGroupTag class.")
        if action == 'add':
            startvlan, endvlan = validate_vlans(start_vlan=startvlan, end_vlan=endvlan)
            new_literal = {'startTag': startvlan, 'endTag': endvlan, 'type': ''}
            if 'literals' in self.__dict__:
                duplicate = False
                for obj in self.literals:
                    if obj['startTag'] == new_literal['startTag'] and obj['endTag'] == new_literal['endTag']:
                        duplicate = True
                        break
                if not duplicate:
                    self.literals.append(new_literal)
                    logging.info('Adding "{}/{}" to VlanGroupTag.'.format(startvlan, endvlan))
            else:
                self.literals = [new_literal]
                logging.info('Adding "{}/{}" to VlanGroupTag.'.format(startvlan, endvlan))
        elif action == 'remove':
            startvlan, endvlan = validate_vlans(start_vlan=startvlan, end_vlan=endvlan)
            if 'literals' in self.__dict__:
                literals_list = []
                for obj in self.literals:
                    if obj['startTag'] != startvlan and obj['endTag'] != endvlan:
                        literals_list.append(obj)
                self.literals = literals_list
                logging.info('Removed "{}/{}" from VlanGroupTag.'.format(startvlan, endvlan))
            else:
                logging.info("This VlanGroupTag has no unnamed_vlantags.  Nothing to remove.")
        elif action == 'clear':
            if 'literals' in self.__dict__:
                del self.literals
                logging.info('All unnamed_vlantags removed from this VlanGroupTag.')


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


class Ports(APIClassTemplate):
    """
    The Ports Object in the FMC.
    """

    URL_SUFFIX = '/object/ports'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Ports class.")
        self.parse_kwargs(**kwargs)

    def post(self):
        logging.info('POST method for API for Ports not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for Ports not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for Ports not supported.')
        pass


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

class InterfaceObject(APIClassTemplate):
    """
    The Interface Object Object in the FMC.
    """

    URL_SUFFIX = '/object/interfaceobjects'
    REQUIRED_FOR_POST = ['name', 'interfaceMode']
    FILTER_BY_NAME = True

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for InterfaceObject class.")
        self.parse_kwargs(**kwargs)

    def post(self):
        logging.info('POST method for API for InterfaceObject not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for InterfaceObject not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for InterfaceObject not supported.')
        pass

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

class InterfaceGroup(APIClassTemplate):
    """
    The InterfaceGroup Object in the FMC.
    """

    URL_SUFFIX = '/object/interfacegroups'
    REQUIRED_FOR_POST = ['name', 'interfaceMode']
    REQUIRED_FOR_PUT = ['id']
    FILTER_BY_NAME = True

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for InterfaceGroup class.")
        self.parse_kwargs(**kwargs)
        self.type = 'InterfaceGroup'

    def format_data(self):
        logging.debug("In format_data() for InterfaceGroup class.")
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
        logging.debug("In parse_kwargs() for InterfaceGroup class.")
        if 'interfaceMode' in kwargs:
            self.interfaceMode = kwargs['interfaceMode']
        else:
            self.interfaceMode = 'ROUTED'
        if 'interfaces' in kwargs:
            self.interfaces = kwargs['interfaces']

    def p_interface(self, device_name="", action="add", names=[]):
        logging.debug("In interfaces() for InterfaceGroup class.")
        if action == 'add':
            intfs = []
            for name in names:
                intf = PhysicalInterface(fmc=self.fmc)
                intf.get(name=name,device_name=device_name)
                if 'id' in intf.__dict__ and 'ifname' in intf.__dict__:
                    intfs.append({'name': intf.name, 'id': intf.id, 'type': intf.type})
                elif 'id' in intf.__dict__:
                    logging.warning('PhysicalInterface, "{}", found without logical ifname.  Cannot add to InterfaceGroup.'.format(name))
                else:
                    logging.warning('PhysicalInterface, "{}", not found.  Cannot add to InterfaceGroup.'.format(name))
            if len(intfs) != 0:
                #Make sure we found at least one intf
                self.interfaces = intfs
            else:
                logging.warning('No valid PhysicalInterface found: "{}".  Cannot remove from InterfaceGroup.'.format(names))
        elif action == 'remove':
            if 'interfaces' in self.__dict__:
                intfs = []
                for interface in self.interfaces:
                    if interface["name"] not in names:
                        intfs.append(interface)
                    else:
                        logging.info('Removed "{}" from InterfaceGroup.'.format(interface["name"]))
                self.interfaces = intfs
            else:
                logging.warning("This InterfaceObject has no interfaces.  Nothing to remove.")
        elif action == 'clear-all':
            if 'interfaces' in self.__dict__:
                del self.interfaces
                logging.info('All PhysicalInterfaces removed from this InterfaceGroup.')

class Continent(APIClassTemplate):
    """
    The Continent Object in the FMC.
    """

    URL_SUFFIX = '/object/continents'
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Continent class.")
        self.parse_kwargs(**kwargs)
        self.type = 'Continent'

    def format_data(self):
        logging.debug("In format_data() for Continent class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'countries' in self.__dict__:
            json_data['countries'] = self.countries
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for Continent class.")
        if 'countries' in kwargs:
            self.countries = kwargs['countries']

    def post(self):
        logging.info('POST method for API for Continent not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for Continent not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for Continent not supported.')
        pass


class Country(APIClassTemplate):
    """
    The Country Object in the FMC.
    """

    URL_SUFFIX = '/object/countries'
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Country class.")
        self.parse_kwargs(**kwargs)
        self.type = 'Country'

    def format_data(self):
        logging.debug("In format_data() for Country class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'iso2' in self.__dict__:
            json_data['iso2'] = self.iso2
        if 'iso3' in self.__dict__:
            json_data['iso3'] = self.iso3
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for Country class.")
        if 'iso2' in kwargs:
            self.iso2 = kwargs['iso2']
        if 'iso3' in kwargs:
            self.iso3 = kwargs['iso3']

    def post(self):
        logging.info('POST method for API for Country not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for Country not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for Country not supported.')
        pass


class PortObjectGroup(APIClassTemplate):
    """
    The PortObjectGroup Object in the FMC.
    """

    URL_SUFFIX = '/object/portobjectgroups'

    # Technically you can have objects OR literals but I'm not set up for "OR" logic, yet.
    REQUIRED_FOR_POST = ['name', 'objects']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for PortObjectGroup class.")
        self.parse_kwargs(**kwargs)
        self.type = 'NetworkGroup'

    def format_data(self):
        logging.debug("In format_data() for PortObjectGroup class.")
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
        logging.debug("In parse_kwargs() for PortObjectGroup class.")
        if 'objects' in kwargs:
            self.objects = kwargs['objects']
        if 'literals' in kwargs:
            self.literals = kwargs['literals']

    def named_ports(self, action, name=''):
        logging.debug("In named_ports() for PortObjectGroup class.")
        if action == 'add':
            port1 = Ports(fmc=self.fmc)
            response = port1.get()
            if 'items' in response:
                new_port = None
                for item in response['items']:
                    if item['name'] == name:
                        new_port = {'name': item['name'], 'id': item['id'], 'type': item['type']}
                        break
                if new_port is None:
                    logging.warning('Port "{}" is not found in FMC.  Cannot add to PortObjectGroup.'.format(name))
                else:
                    if 'objects' in self.__dict__:
                        duplicate = False
                        for obj in self.objects:
                            if obj['name'] == new_port['name']:
                                duplicate = True
                                break
                        if not duplicate:
                            self.objects.append(new_port)
                            logging.info('Adding "{}" to PortObjectGroup.'.format(name))
                    else:
                        self.objects = [new_port]
                        logging.info('Adding "{}" to PortObjectGroup.'.format(name))
        elif action == 'remove':
            if 'objects' in self.__dict__:
                objects_list = []
                for obj in self.objects:
                    if obj['name'] != name:
                        objects_list.append(obj)
                self.objects = objects_list
                logging.info('Removed "{}" from PortObjectGroup.'.format(name))
            else:
                logging.info("This PortObjectGroup has no named_ports.  Nothing to remove.")
        elif action == 'clear':
            if 'objects' in self.__dict__:
                del self.objects
                logging.info('All named_ports removed from this PortObjectGroup.')

# ################# API-Explorer Devices Category Things ################# #


class Device(APIClassTemplate):
    """
    The Device Object in the FMC.
    """

    URL_SUFFIX = '/devices/devicerecords'
    REQUIRED_FOR_POST = ['accessPolicy', 'hostName', 'regKey']
    REQUIRED_FOR_PUT = ['id']
    LICENSES = ['BASE', 'MALWARE', 'URLFilter', 'THREAT', 'VPN']

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
        if 'model' in kwargs:
            self.model = kwargs['model']
        if 'modelId' in kwargs:
            self.modelId = kwargs['modelId']
        if 'modelNumber' in kwargs:
            self.modelNumber = kwargs['modelNumber']
        if 'modelType' in kwargs:
            self.modelType = kwargs['modelType']
        if 'healthStatus' in kwargs:
            self.healthStatus = kwargs['healthStatus']
        if 'healthPolicy' in kwargs:
            self.healthPolicy = kwargs['healthPolicy']
        if 'keepLocalEvents' in kwargs:
            self.keepLocalEvents = kwargs['keepLocalEvents']
        if 'prohibitPacketTransfer' in kwargs:
            self.prohibitPacketTransfer = kwargs['prohibitPacketTransfer']

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

    def post(self, **kwargs):
        logging.debug("In post() for Device class.")
        # Attempting to "Deploy" during Device registration causes issues.
        self.fmc.autodeploy = False
        return super().post(**kwargs)


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
    VALID_FOR_MTU = range(64,9000)
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
            #This doesn't seem to be working
            self.enabled = kwargs['enabled']
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
            logging.warning('Device {} not found.  Cannot set up device for '
                            'physicalInterface.'.format(device_name))
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
        self.ipv4 = {"static":{"address":ipv4addr,"netmask":ipv4mask }}

    def dhcp(self, enableDefault=True, routeMetric=1):
       logging.debug("In dhcp() for PhysicalInterface class.")
       self.ipv4 = {"dhcp":{"enableDefaultRouteDHCP":enableDefault,"dhcpRouteMetric":routeMetric }}

    def hwmode(self, mode):
        logging.debug("In hwmode() for PhysicalInterface class.")
        if mode in self.VALID_FOR_MODE:
            self.mode = mode
        else:
            logging.warning('Mode {} is not a valid mode.'.format(mode))

    def hardware(self, speed, duplex="FULL"):
        #There are probably some incompatibilities that need to be accounted for
        logging.debug("In hardware() for PhysicalInterface class.")
        if speed in self.VALID_FOR_HARDWARE_SPEED and duplex in self.VALID_FOR_HARDWARE_DUPLEX:
            self.hardware = {"duplex":duplex,"speed":speed}
        else:
            logging.warning('Speed {} or Duplex {} is not a valid mode.'.format(speed, duplex))


class IPv4StaticRoutes(APIClassTemplate):
    """
    The IPv4StaticRoutes Object in the FMC.
    """

    PREFIX_URL = '/devices/devicerecords'
    URL_SUFFIX = None
    REQUIRED_FOR_POST = ['interfaceName', 'selectedNetworks', 'gateway']
    REQUIRED_FOR_PUT = ['id', 'device_id']
    
    '''
    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for IPv4StaticRoutes class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for IPv4StaticRoutes class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'interfaceName' in self.__dict__:
            json_data['interfaceName'] = self.interfaceName
        if 'selectedNetworks' in self.__dict__:
            json_data['selectedNetworks'] = self.selectedNetworks
        if 'gateway' in self.__dict__:
            json_data['gateway'] = self.gateway
        if 'routeTracking' in self.__dict__:
            json_data['routeTracking'] = self.routeTracking
        if 'metricValue' in self.__dict__:
            json_data['metricValue'] = self.metricValue
        if 'isTunneled' in self.__dict__:
            json_data['isTunneled'] = self.isTunneled
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for IPv4StaticRoutes class.")
        if 'device_name' in kwargs:
            self.device(device_name=kwargs['device_name'])
        if 'interfaceName' in kwargs:
            self.interfaceName = kwargs['interfaceName']
        if 'selectedNetworks' in kwargs:
            self.selectedNetworks = kwargs['selectedNetworks']
        if 'gateway' in kwargs:
             self.gateway = kwargs['gateway']
        if 'routeTracking' in kwargs:
            self.routeTracking = kwargs['routeTracking']
        if 'metricValue' in kwargs:
            self.metricValue = kwargs['metricValue']
        if 'isTunneled' in kwargs:
            self.isTunneled = kwargs['isTunneled']

    def device(self, device_name):
        logging.debug("In device() for IPv4StaticRoutes class.")
        device1 = Device(fmc=self.fmc)
        device1.get(name=device_name)
        if 'id' in device1.__dict__:
            self.device_id = device1.id
            self.URL = '{}{}/{}/routing/ipv4staticroutes'.format(self.fmc.configuration_url, self.PREFIX_URL, self.device_id)
            self.device_added_to_url = True
        else:
            logging.warning('Device {} not found.  Cannot set up device for '
                            'IPv4StaticRoutes.'.format(device_name))

    def edit(self, device_name, ifname, gateway):
        logging.debug("In edit() for IPv4StaticRoutes class.")
        obj1 = IPv4StaticRoutes(fmc=self.fmc, device_name=device_name)
        route_json = obj1.get()
        items = route_json.get('items', [])
        found = False
        for item in items:
            if item["gateway"]["object"]["name"] == gateway and item["interfaceName"] == ifname:
                found = True
                self.selectedNetworks = item["selectedNetworks"]
                self.interfaceName = item["interfaceName"]
                self.gateway = item["gateway"]
                self.id = item["id"]
                break
        if found == False:
            logging.warning('Gateway {} and interface {} combination not found.  Cannot set up device for '
                            'IPv4StaticRoutes.'.format(gateway, ifname))

    def selectedNetworks(self, action, names):
        logging.warning("In selectedNetworks() for Device class.")
        if action == 'add':
            if 'selectedNetworks' in self.__dict__: 
                for name in names:
                    net = IPAddresses(fmc=self.fmc)
                    net.get(name=name)
                    if 'id' in net.__dict__:
                        new_net = {
                            "type": net.type,
                            "id": net.id,
                            "name": net.name
                        }
                        self.selectedNetworks.append(new_net)
                    else:
                        logging.warning('Network {} not found.  Cannot set up device for '
                                        'IPv4StaticRoutes.'.format(name))
            else:
                self.selectedNetworks = []
                for name in names:
                    net = IPAddresses(fmc=self.fmc)
                    net.get(name=name)
                    if 'id' in net.__dict__:
                        new_net = {
                            "type": net.type,
                            "id": net.id,
                            "name": net.name
                        }
                        self.selectedNetworks.append(new_net)
                    else:
                        logging.warning('Network {} not found.  Cannot set up device for '
                                        'IPv4StaticRoutes.'.format(name))
    def gw(self, name):
        gateway = IPAddresses(fmc=self.fmc)
        gateway.get(name=name)
        if 'id' in gateway.__dict__:
                self.gateway = {
                    "object":{
                        "type": gateway.type,
                        "id": gateway.id,
                        "name": gateway.name}}
        else:
            logging.warning('Network {} not found.  Cannot set up device for '
                            'IPv4StaticRoutes.'.format(name))
    def ipsla(self, name):
        route_track = SLAMonitor(fmc=self.fmc)
        route_track.get(name=name)
        if 'id' in route_track.__dict__:
                self.routeTracking = {
                    "type": route_track.type,
                    "id": route_track.id,
                    "name": route_track.name}
        else:
            logging.warning('Object {} not found.  Cannot set up device for '
                            'IPv4StaticRoutes.'.format(name))
    '''
            
class DeviceHAPairs(APIClassTemplate):
    """
    The DeviceHAPairs Object in the FMC.
    """

    URL_SUFFIX = '/devicehapairs/ftddevicehapairs'
    REQUIRED_FOR_POST = ['primary', 'secondary', 'ftdHABootstrap']
    REQUIRED_FOR_PUT = ['id']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for DeviceHAPairs class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for DeviceHAPairs class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'primary' in self.__dict__:
            json_data['primary'] = self.primary
        if 'secondary' in self.__dict__:
            json_data['secondary'] = self.secondary
        if 'ftdHABootstrap' in self.__dict__:
            json_data['ftdHABootstrap'] = self.ftdHABootstrap
        if 'action' in self.__dict__:
            json_data['action'] = self.action
        if 'forceBreak' in self.__dict__:
            json_data['forceBreak'] = self.forceBreak
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for DeviceHAPairs class.")
        if 'primary' in kwargs:
            self.primary = kwargs['primary']
        if 'secondary' in kwargs:
            self.secondary = kwargs['secondary']
        if 'ftdHABootstrap' in kwargs:
            self.ftdHABootstrap = kwargs['ftdHABootstrap']
        if 'action' in kwargs:
            self.action = kwargs['action']
        if 'forceBreak' in kwargs:
            self.forceBreak = kwargs['forceBreak']

    def device(self, primary_name="", secondary_name=""):
        logging.debug("In device() for DeviceHAPairs class.")
        primary = Device(fmc=self.fmc)
        primary.get(name=primary_name)
        secondary = Device(fmc=self.fmc)
        secondary.get(name=secondary_name)
        if 'id' in primary.__dict__:
            self.primary_id = primary.id
        else:
            logging.warning('Device {} not found.  Cannot set up device for '
                            'DeviceHAPairs.'.format(primary_name))
        if 'id' in secondary.__dict__:
            self.secondary_id = secondary.id
        else:
            logging.warning('Device {} not found.  Cannot set up device for '
                            'DeviceHAPairs.'.format(secondary_name))

    def primary(self, name):
        logging.debug("In primary() for DeviceHAPairs class.")
        primary = Device(fmc=self.fmc)
        primary.get(name=name)
        if 'id' in primary.__dict__:
            self.primary = {"id": primary.id}
        else:
            logging.warning('Device {} not found.  Cannot set up device for '
                            'DeviceHAPairs.'.format(primary_name))

    def secondary(self, name):
        logging.debug("In secondary() for DeviceHAPairs class.")
        secondary = Device(fmc=self.fmc)
        secondary.get(name=name)
        if 'id' in secondary.__dict__:
            self.secondary = {"id": secondary.id}
        else:
            logging.warning('Device {} not found.  Cannot set up device for '
                            'DeviceHAPairs.'.format(primary_name))

    def switch_ha(self):
        logging.debug("In switch_ha() for DeviceHAPairs class.")
        ha1 = DeviceHAPairs(fmc=self.fmc)
        ha1.get(name=self.name)
        if 'id' in ha1.__dict__:
            self.id = ha1.id
            self.action = "SWITCH"
        else:
            logging.warning('DeviceHAPair {} not found.  Cannot set up HA for SWITCH.'.format(self.name))

    def break_ha(self):
        logging.debug("In break_ha() for DeviceHAPairs class.")
        ha1 = DeviceHAPairs(fmc=self.fmc)
        ha1.get(name=self.name)
        if 'id' in ha1.__dict__:
            self.id = ha1.id
            self.action = "HABREAK"
            self.forceBreak = True
        else:
            logging.warning('DeviceHAPair {} not found.  Cannot set up HA for BREAK.'.format(self.name))

    def post(self, **kwargs):
        logging.debug("In post() for DeviceHAPairs class.")
        # Attempting to "Deploy" during Device registration causes issues.
        self.fmc.autodeploy = False
        return super().post(**kwargs)

    def put(self, **kwargs):
        logging.debug("In put() for DeviceHAPairs class.")
        # Attempting to "Deploy" during Device registration causes issues.
        self.fmc.autodeploy = False
        return super().put(**kwargs)

class DeviceHAMonitoredInterfaces(APIClassTemplate):
    """
    The DeviceHAMonitoredInterfaces Object in the FMC.
    """

    PREFIX_URL = '/devicehapairs/ftddevicehapairs'
    REQUIRED_FOR_PUT = ['id']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for DeviceHAMonitoredInterfaces class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for DeviceHAMonitoredInterfaces class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'ipv4Configuration' in self.__dict__:
            json_data['ipv4Configuration'] = self.ipv4Configuration
        if 'ipv6Configuration' in self.__dict__:
            json_data['ipv6Configuration'] = self.ipv6Configuration
        if 'monitorForFailures' in self.__dict__:
            json_data['monitorForFailures'] = self.monitorForFailures
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for DeviceHAMonitoredInterfaces class.")
        if 'ha_name' in kwargs:
            self.device_ha(ha_name=kwargs['ha_name'])
        if 'ipv4Configuration' in kwargs:
            self.ipv4Configuration = kwargs['ipv4Configuration']
        if 'ipv6Configuration' in kwargs:
            self.ipv6Configuration = kwargs['ipv6Configuration']
        if 'monitorForFailures' in kwargs:
            self.monitorForFailures = kwargs['monitorForFailures']

    def device_ha(self, ha_name):
        logging.debug("In device_ha() for DeviceHAMonitoredInterfaces class.")
        deviceha1 = DeviceHAPairs(fmc=self.fmc, name=ha_name)
        deviceha1.get()
        if 'id' in deviceha1.__dict__:
            self.deviceha_id = deviceha1.id
            self.URL = '{}{}/{}/monitoredinterfaces'.format(self.fmc.configuration_url, self.PREFIX_URL, self.deviceha_id)
            self.deviceha_added_to_url = True
        else:
            logging.warning('Device HA {} not found.  Cannot set up device for '
                            'DeviceHAMonitoredInterfaces.'.format(ha_name))

    def ipv4(self, ipv4addr, ipv4mask, ipv4standbyaddr):
        logging.debug("In ipv4() for DeviceHAMonitoredInterfaces class.")
        self.ipv4Configuration = {
            "activeIPv4Address": ipv4addr,
            "activeIPv4Mask": ipv4mask,
            "standbyIPv4Address": ipv4standbyaddr}

    def post(self):
        logging.info('POST method for API for DeviceHAMonitoredInterfaces not supported.')
        pass

class DeviceHAFailoverMAC(APIClassTemplate):
    """
    The DeviceHAFailoverMAC Object in the FMC.
    """

    PREFIX_URL = '/devicehapairs/ftddevicehapairs'
    REQUIRED_FOR_POST = ['physicalInterface', 'failoverActiveMac', 'failoverStandbyMac']
    REQUIRED_FOR_PUT = ['id']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for DeviceHAFailoverMAC class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for DeviceHAFailoverMAC class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'physicalInterface' in self.__dict__:
            json_data['physicalInterface'] = self.physicalInterface
        if 'failoverActiveMac' in self.__dict__:
            json_data['failoverActiveMac'] = self.failoverActiveMac
        if 'failoverStandbyMac' in self.__dict__:
            json_data['failoverStandbyMac'] = self.failoverStandbyMac
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for DeviceHAFailoverMAC class.")
        if 'ha_name' in kwargs:
            self.device_ha(ha_name=kwargs['ha_name'])
        if 'physicalInterface' in kwargs:
            self.physicalInterface = kwargs['physicalInterface']
        if 'failoverActiveMac' in kwargs:
            self.failoverActiveMac = kwargs['failoverActiveMac']
        if 'failoverStandbyMac' in kwargs:
            self.failoverStandbyMac = kwargs['failoverStandbyMac']

    def device_ha(self, ha_name):
        logging.debug("In device_ha() for DeviceHAFailoverMAC class.")
        deviceha1 = DeviceHAPairs(fmc=self.fmc, name=ha_name)
        deviceha1.get()
        if 'id' in deviceha1.__dict__:
            self.deviceha_id = deviceha1.id
            self.URL = '{}{}/{}/failoverinterfacemacaddressconfigs'.format(self.fmc.configuration_url, self.PREFIX_URL, self.deviceha_id)
            self.deviceha_added_to_url = True
        else:
            logging.warning('Device HA {} not found.  Cannot set up device for '
                            'DeviceHAFailoverMAC.'.format(ha_name))

    def p_interface(self, name, device_name):
        logging.debug("In p_interface() for DeviceHAFailoverMAC class.")
        intf1 = PhysicalInterface(fmc=self.fmc)
        intf1.get(name=name,device_name=device_name)
        if 'id' in intf1.__dict__:
            self.physicalInterface = {'name': intf1.name, 'id': intf1.id, 'type': intf1.type}
        else:
            logging.warning('PhysicalInterface, "{}", not found.  Cannot add to DeviceHAFailoverMAC.'.format(name))

    def edit(self, name, ha_name):
        logging.debug("In edit() for DeviceHAFailoverMAC class.")
        deviceha1 = DeviceHAPairs(fmc=self.fmc, name=ha_name)
        deviceha1.get()
        obj1 = DeviceHAFailoverMAC(fmc=self.fmc)
        obj1.device_ha(ha_name=ha_name)
        failovermac_json = obj1.get()
        items = failovermac_json.get('items', [])
        found = False
        for item in items:
            if item['physicalInterface']['name'] == name:
                found = True
                self.id = item['id']
                self.name = item['physicalInterface']['name']
                self.failoverActiveMac = item['failoverActiveMac']
                self.failoverStandbyMac = item['failoverStandbyMac']
                self.deviceha_id = deviceha1.id
                self.URL = '{}{}/{}/failoverinterfacemacaddressconfigs'.format(self.fmc.configuration_url, self.PREFIX_URL, self.deviceha_id)
                break
        if found is False:
            logging.warning('PhysicalInterface, "{}", not found.  Cannot add to DeviceHAFailoverMAC.'.format(name))


# ################# API-Explorer Policy Category Things ################# #


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


class ACPRule(APIClassTemplate):
    """
    The ACP Rule Object in the FMC.
    """

    PREFIX_URL = '/policy/accesspolicies'
    URL_SUFFIX = None
    REQUIRED_FOR_POST = ['name', 'acp_id']
    VALID_FOR_ACTION = ['ALLOW', 'TRUST', 'BLOCK', 'MONITOR', 'BLOCK_RESET', 'BLOCK_INTERACTIVE',
                        'BLOCK_RESET_INTERACTIVE']
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

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
            self.acp_added_to_url = True
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
                logging.warning('Protocol Port or Protocol Port Group: "{}", not found.  Cannot add to ACPRule.'.format(name))
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
                logging.warning('Protocol Port or Protocol Port Group: "{}", not found.  Cannot add to ACPRule.'.format(name))
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
                logging.warning('Protocol Port or Protocol Port Group: "{}", not found.  Cannot add to ACPRule.'.format(name))
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
                logging.warning('Protocol Port or Protocol Port Group: "{}", not found.  Cannot add to ACPRule.'.format(name))
        elif action == 'clear':
            if 'destinationPorts' in self.__dict__:
                del self.destinationPorts
                logging.info('All Destination Ports removed from this ACPRule object.')

    def source_network(self, action, name=''):
        logging.debug("In source_network() for ACPRule class.")
        if action == 'add':
            ipaddresses_json = IPAddresses(fmc=self.fmc).get()
            networkgroup_json = NetworkGroup(fmc=self.fmc).get()
            items = ipaddresses_json.get('items', []) + networkgroup_json.get('items', [])
            new_net = None
            for item in items:
                if item['name'] == name:
                    new_net = {'name': item['name'], 'id': item['id'], 'type': item['type']}
                    break
            if new_net is None:
                logging.warning('Network "{}" is not found in FMC.  Cannot add to sourceNetworks.'.format(name))
            else:
                if 'sourceNetworks' in self.__dict__:
                    duplicate = False
                    for obj in self.sourceNetworks['objects']:
                        if obj['name'] == new_net['name']:
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
                for obj in self.sourceNetworks['objects']:
                    if obj['name'] != name:
                        objects.append(obj)
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
            ipaddresses_json = IPAddresses(fmc=self.fmc).get()
            networkgroup_json = NetworkGroup(fmc=self.fmc).get()
            items = ipaddresses_json.get('items', []) + networkgroup_json.get('items', [])
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
                    duplicate = False
                    for obj in self.destinationNetworks['objects']:
                        if obj['name'] == new_net['name']:
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
                for obj in self.destinationNetworks['objects']:
                    if obj['name'] != name:
                        objects.append(obj)
                self.destinationNetworks['objects'] = objects
                logging.info('Removed "{}" from destinationNetworks for this ACPRule.'.format(name))
            else:
                logging.info("destinationNetworks doesn't exist for this ACPRule.  Nothing to remove.")
        elif action == 'clear':
            if 'destinationNetworks' in self.__dict__:
                del self.destinationNetworks
                logging.info('All Destination Networks removed from this ACPRule object.')

class FTDNatPolicy(APIClassTemplate):
    """
    The FTDNATPolicy Object in the FMC.
    """

    URL_SUFFIX = '/policy/ftdnatpolicies'
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for FTDNatPolicy class.")
        self.parse_kwargs(**kwargs)
        self.type = "FTDNatPolicy"

    def format_data(self):
        logging.debug("In format_data() for FTDNatPolicy class.")
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
        logging.debug("In parse_kwargs() for FTDNatPolicy class.")

class AutoNatRules(APIClassTemplate):
    """
    The AutoNatRules Object in the FMC.
    """

    PREFIX_URL = '/policy/ftdnatpolicies'
    REQUIRED_FOR_POST = ["nat_id"]

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for AutoNatRules class.")
        self.parse_kwargs(**kwargs)
        self.type = "FTDAutoNatRule"

    def format_data(self):
        logging.debug("In format_data() for AutoNatRules class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'originalNetwork' in self.__dict__:
            json_data['originalNetwork'] = self.originalNetwork
        if 'translatedNetwork' in self.__dict__:
            json_data['translatedNetwork'] = self.translatedNetwork
        if 'interfaceInTranslatedNetwork' in self.__dict__:
            json_data['interfaceInTranslatedNetwork'] = self.interfaceInTranslatedNetwork
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
        if 'originalPort' in self.__dict__:
            json_data['originalPort'] = self.originalPort
        if 'translatedPort' in self.__dict__:
            json_data['translatedPort'] = self.translatedPort
        if 'serviceProtocol' in self.__dict__:
            json_data['serviceProtocol'] = self.serviceProtocol
        if 'patOptions' in self.__dict__:
            json_data['patOptions'] = self.patOptions
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for AutoNatRules class.")
        if 'originalNetwork' in kwargs:
            self.originalNetwork = kwargs['originalNetwork']
        if 'translatedNetwork' in kwargs and 'interfaceInTranslatedNetwork' is True:
            logging.warning("Cannot have both a translatedNetwork and interfaceInTranslatedNetwork")
        elif 'translatedNetwork' in kwargs:
            self.translatedNetwork = kwargs['translatedNetwork']
        elif 'interfaceInTranslatedNetwork' in kwargs:
            self.interfaceInTranslatedNetwork = kwargs['interfaceInTranslatedNetwork']
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
        if 'originalPort' in kwargs:
            self.originalPort = kwargs['originalPort']
        if 'translatedPort' in kwargs:
            self.translatedPort = kwargs['translatedPort']
        if 'serviceProtocol' in kwargs:
            self.serviceProtocol = kwargs['serviceProtocol']
        if 'patOptions' in kwargs:
            self.patOptions = kwargs['patOptions']

    def nat_policy(self,name):
        logging.debug("In nat_policy() for AutoNatRules class.")
        ftd_nat = FTDNatPolicy(fmc=self.fmc)
        ftd_nat.get(name=name)
        if 'id' in ftd_nat.__dict__:
            self.nat_id = ftd_nat.id
            self.URL = '{}{}/{}/autonatrules'.format(self.fmc.configuration_url, self.PREFIX_URL, self.nat_id)
            self.nat_added_to_url = True
        else:
            logging.warning('FTD NAT Policy {} not found.  Cannot set up AutoNatRule for '
                            'NAT Policy.'.format(name))

    def original_network(self, name):
        logging.debug("In original_network() for AutoNatRules class.")
        ipaddresses_json = IPAddresses(fmc=self.fmc).get()
        items = ipaddresses_json.get('items', [])
        new_net = None
        for item in items:
            if item['name'] == name:
                new_net = {'id': item['id'], 'type': item['type']}
                break
        if new_net is None:
            logging.warning('Network "{}" is not found in FMC.  Cannot add to originalNetwork.'.format(name))
        else:
            self.originalNetwork = new_net
            logging.info('Adding "{}" to sourceNetworks for this AutoNatRule.'.format(name))

    def translated_network(self,name):
        #Auto Nat rules can't use network group objects
        logging.debug("In translated_network() for AutoNatRules class.")
        ipaddresses_json = IPAddresses(fmc=self.fmc).get()
        items = ipaddresses_json.get('items', [])
        new_net = None
        for item in items:
            if item['name'] == name:
                new_net = {'id': item['id'], 'type': item['type']}
                break
        if new_net is None:
            logging.warning('Network "{}" is not found in FMC.  Cannot add to translatedNetwork.'.format(name))
        else:
            self.translatedNetwork = new_net
            logging.info('Adding "{}" to destinationNetworks for this AutoNatRule.'.format(name))

    def source_intf(self,name):
        logging.debug("In source_intf() for AutoNatRules class.")
        intf_obj = InterfaceObject(fmc=self.fmc).get()
        items = intf_obj.get('items', [])
        new_intf = None
        for item in items:
            if item["name"] == name:
                new_intf = {'id': item['id'], 'type': item['type']}
                break
        if new_intf == None:
            logging.warning('Interface Object "{}" is not found in FMC.  Cannot add to sourceInterface.'.format(name))
        else:
            if new_intf.type == "InterfaceGroup" and len(new_intf.interfaces) > 1:
                logging.warning('Interface Object "{}" contains more than one physical interface.  Cannot add to sourceInterface.'.format(name))
            else:
                self.sourceInterface = new_intf
                logging.info('Interface Object "{}" added to NAT Policy.'.format(name))

    def destination_intf(self,name):
        logging.debug("In destination_intf() for AutoNatRules class.")
        intf_obj = InterfaceObject(fmc=self.fmc).get()
        items = intf_obj.get('items', [])
        new_intf = None
        for item in items:
            if item["name"] == name:
                new_intf = {'id': item['id'], 'type': item['type']}
                break
        if new_intf == None:
            logging.warning('Interface Object "{}" is not found in FMC.  Cannot add to destinationInterface.'.format(name))
        else:
            if new_intf.type == "InterfaceGroup" and len(new_intf.interfaces) > 1:
                logging.warning('Interface Object "{}" contains more than one physical interface.  Cannot add to destinationInterface.'.format(name))
            else:
                self.destinationInterface = new_intf
                logging.info('Interface Object "{}" added to NAT Policy.'.format(name))

    def identity_nat(self, name):
        logging.debug("In identity_nat() for AutoNatRules class.")
        ipaddresses_json = IPAddresses(fmc=self.fmc).get()
        items = ipaddresses_json.get('items', [])
        new_net = None
        for item in items:
            if item['name'] == name:
                new_net = {'id': item['id'], 'type': item['type']}
                break
        if new_net is None:
            logging.warning('Network "{}" is not found in FMC.  Cannot add to this AutoNatRule.'.format(name))
        else:
            self.natType = "STATIC"
            self.originalNetwork = new_net
            self.translatedNetwork = new_net
            logging.info('Adding "{}" to AutoNatRule.'.format(name))

    def patPool(self, name, options={}):
        #Network Group Object permitted for patPool
        ipaddresses_json = IPAddresses(fmc=self.fmc).get()
        networkgroup_json = NetworkGroup(fmc=self.fmc).get()
        items = ipaddresses_json.get('items', []) + networkgroup_json.get('items', [])
        new_net = None
        for item in items:
            if item['name'] == name:
                new_net = {'name': item['name'], 'id': item['id'], 'type': item['type']}
                break
        if new_net is None:
            logging.warning('Network "{}" is not found in FMC.  Cannot add to patPool.'.format(name))
        else:
            self.natType = "DYNAMIC"
            self.patOptions = {"patPoolAddress": new_net}
            self.patOptions["interfacePat"] = options.interfacePat if "interfacePat" in options.keys() else False
            self.patOptions["includeReserve"] = options.includeReserve if "includeReserve" in options.keys() else False
            self.patOptions["roundRobin"] = options.roundRobin if "roundRobin" in options.keys() else False
            self.patOptions["extendedPat"] = options.extendedPat if "extendedPat" in options.keys() else False
            self.patOptions["flatPortRange"] = options.flatPortRange if "flatPortRange" in options.keys() else False
            logging.info('Adding "{}" to patPool for this AutoNatRule.'.format(name))

class ManualNatRules(APIClassTemplate):
    #Host,Network,NetworkGroup objects
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

    def nat_policy(self,name):
        logging.debug("In nat_policy() for ManualNatRules class.")
        ftd_nat = FTDNatPolicy(fmc=self.fmc)
        ftd_nat.get(name=name)
        if 'id' in ftd_nat.__dict__:
            self.nat_id = ftd_nat.id
            self.URL = '{}{}/{}/manualnatrules'.format(self.fmc.configuration_url, self.PREFIX_URL, self.nat_id)
            self.nat_added_to_url = True
        else:
            logging.warning('FTD NAT Policy {} not found.  Cannot set up ManualNatRule for '
                            'NAT Policy.'.format(name))

    def original_source(self, name):
        logging.debug("In original_source() for ManualNatRules class.")
        ipaddresses_json = IPAddresses(fmc=self.fmc).get()
        networkgroup_json = NetworkGroup(fmc=self.fmc).get()
        items = ipaddresses_json.get('items', [])
        new_net = None
        for item in items:
            if item['name'] == name:
                new_net = {'id': item['id'], 'type': item['type']}
                break
        if new_net is None:
            logging.warning('Network "{}" is not found in FMC.  Cannot add to original_source.'.format(name))
        else:
            self.originalSource = new_net
            logging.info('Adding "{}" to original_source for this ManualNatRule.'.format(name))

    def translated_source(self,name):
        logging.debug("In translated_source() for ManualNatRules class.")
        ipaddresses_json = IPAddresses(fmc=self.fmc).get()
        networkgroup_json = NetworkGroup(fmc=self.fmc).get()
        items = ipaddresses_json.get('items', [])
        new_net = None
        for item in items:
            if item['name'] == name:
                new_net = {'id': item['id'], 'type': item['type']}
                break
        if new_net is None:
            logging.warning('Network "{}" is not found in FMC.  Cannot add to translated_source.'.format(name))
        else:
            self.translatedSource = new_net
            logging.info('Adding "{}" to translated_source for this ManualNatRule.'.format(name))

    def original_destination(self, name):
        logging.debug("In original_destination() for ManualNatRules class.")
        ipaddresses_json = IPAddresses(fmc=self.fmc).get()
        networkgroup_json = NetworkGroup(fmc=self.fmc).get()
        items = ipaddresses_json.get('items', [])
        new_net = None
        for item in items:
            if item['name'] == name:
                new_net = {'id': item['id'], 'type': item['type']}
                break
        if new_net is None:
            logging.warning('Network "{}" is not found in FMC.  Cannot add to original_destination.'.format(name))
        else:
            self.originalDestination = new_net
            logging.info('Adding "{}" to original_destination for this ManualNatRule.'.format(name))

    def translated_destination(self,name):
        logging.debug("In translated_destination() for ManualNatRules class.")
        ipaddresses_json = IPAddresses(fmc=self.fmc).get()
        networkgroup_json = NetworkGroup(fmc=self.fmc).get()
        items = ipaddresses_json.get('items', [])
        new_net = None
        for item in items:
            if item['name'] == name:
                new_net = {'id': item['id'], 'type': item['type']}
                break
        if new_net is None:
            logging.warning('Network "{}" is not found in FMC.  Cannot add to translated_destination.'.format(name))
        else:
            self.translatedDestination = new_net
            logging.info('Adding "{}" to translated_destination for this ManualNatRule.'.format(name))

    def original_source_port(self, name):
        logging.debug("In original_source_port() for ManualNatRules class.")
        ports_json = ProtocolPort(fmc=self.fmc).get()
        portgroup_json = PortObjectGroup(fmc=self.fmc).get()
        items = ports_json.get('items', []) + portgroup_json.get('items', [])
        new_port = None
        for item in items:
            if item['name'] == name:
                new_port = {'id': item['id'], 'type': item['type']}
                break
        if new_port is None:
            logging.warning('Port "{}" is not found in FMC.  Cannot add to original_source_port.'.format(name))
        else:
            self.originalSourcePort = new_port
            logging.info('Adding "{}" to original_source_port for this ManualNatRule.'.format(name))

    def translated_source_port(self, name):
        logging.debug("In translated_source_port() for ManualNatRules class.")
        ports_json = ProtocolPort(fmc=self.fmc).get()
        portgroup_json = PortObjectGroup(fmc=self.fmc).get()
        items = ports_json.get('items', []) + portgroup_json.get('items', [])
        new_port = None
        for item in items:
            if item['name'] == name:
                new_port = {'id': item['id'], 'type': item['type']}
                break
        if new_port is None:
            logging.warning('Port "{}" is not found in FMC.  Cannot add to translated_source_port.'.format(name))
        else:
            self.translatedSourcePort = new_port
            logging.info('Adding "{}" to translated_source_port for this ManualNatRule.'.format(name))

    def original_destination_port(self, name):
        logging.debug("In original_destination_port() for ManualNatRules class.")
        ports_json = ProtocolPort(fmc=self.fmc).get()
        portgroup_json = PortObjectGroup(fmc=self.fmc).get()
        items = ports_json.get('items', []) + portgroup_json.get('items', [])
        new_port = None
        for item in items:
            if item['name'] == name:
                new_port = {'id': item['id'], 'type': item['type']}
                break
        if new_port is None:
            logging.warning('Port "{}" is not found in FMC.  Cannot add to original_destination_port.'.format(name))
        else:
            self.originalDestinationPort = new_port
            logging.info('Adding "{}" to original_destination_port for this ManualNatRule.'.format(name))

    def translated_destination_port(self, name):
        logging.debug("In translated_destination_port() for ManualNatRules class.")
        ports_json = ProtocolPort(fmc=self.fmc).get()
        portgroup_json = PortObjectGroup(fmc=self.fmc).get()
        items = ports_json.get('items', []) + portgroup_json.get('items', [])
        new_port = None
        for item in items:
            if item['name'] == name:
                new_port = {'id': item['id'], 'type': item['type']}
                break
        if new_port is None:
            logging.warning('Port "{}" is not found in FMC.  Cannot add to translated_destination_port.'.format(name))
        else:
            self.translatedDestinationPort = new_port
            logging.info('Adding "{}" to translated_destination_port for this ManualNatRule.'.format(name))

    def source_intf(self,name):
        logging.debug("In source_intf() for ManualNatRules class.")
        intf_obj = InterfaceObject(fmc=self.fmc).get()
        items = intf_obj.get('items', [])
        new_intf = None
        for item in items:
            if item["name"] == name:
                new_intf = {'id': item['id'], 'type': item['type']}
                break
        if new_intf == None:
            logging.warning('Interface Object "{}" is not found in FMC.  Cannot add to sourceInterface.'.format(name))
        else:
            self.sourceInterface = new_intf
            logging.info('Interface Object "{}" added to NAT Policy.'.format(name))

    def destination_intf(self,name):
        logging.debug("In destination_intf() for ManualNatRules class.")
        intf_obj = InterfaceObject(fmc=self.fmc).get()
        items = intf_obj.get('items', [])
        new_intf = None
        for item in items:
            if item["name"] == name:
                new_intf = {'id': item['id'], 'type': item['type']}
                break
        if new_intf == None:
            logging.warning('Interface Object "{}" is not found in FMC.  Cannot add to destinationInterface.'.format(name))
        else:
            if new_intf.type == "InterfaceGroup" and len(new_intf.items) > 1:                    
                self.destinationInterface = new_intf
                logging.info('Interface Object "{}" added to NAT Policy.'.format(name))

    def identity_nat(self, name):
        logging.debug("In identity_nat() for ManualNatRules class.")
        ipaddresses_json = IPAddresses(fmc=self.fmc).get()
        networkgroup_json = NetworkGroup(fmc=self.fmc).get()
        items = ipaddresses_json.get('items', []) + networkgroup_json.get('items', [])
        new_net = None
        for item in items:
            if item['name'] == name:
                new_net = {'id': item['id'], 'type': item['type']}
                break
        if new_net is None:
            logging.warning('Network "{}" is not found in FMC.  Cannot add to this ManualNatRules.'.format(name))
        else:
            self.natType = "STATIC"
            self.originalSource = new_net
            self.translatedSource = new_net
            logging.info('Adding "{}" to ManualNatRules.'.format(name))

    def patPool(self, name, options={}):
        ipaddresses_json = IPAddresses(fmc=self.fmc).get()
        networkgroup_json = NetworkGroup(fmc=self.fmc).get()
        items = ipaddresses_json.get('items', []) + networkgroup_json.get('items', [])
        new_net = None
        for item in items:
            if item['name'] == name:
                new_net = {'name': item['name'], 'id': item['id'], 'type': item['type']}
                break
        if new_net is None:
            logging.warning('Network "{}" is not found in FMC.  Cannot add to patPool.'.format(name))
        else:
            self.natType = "DYNAMIC"
            self.patOptions = {"patPoolAddress": new_net}
            self.patOptions["interfacePat"] = options.interfacePat if "interfacePat" in options.keys() else False
            self.patOptions["includeReserve"] = options.includeReserve if "includeReserve" in options.keys() else False
            self.patOptions["roundRobin"] = options.roundRobin if "roundRobin" in options.keys() else False
            self.patOptions["extendedPat"] = options.extendedPat if "extendedPat" in options.keys() else False
            self.patOptions["flatPortRange"] = options.flatPortRange if "flatPortRange" in options.keys() else False
            logging.info('Adding "{}" to patPool for this AutoNatRule.'.format(name))

class NatRules(APIClassTemplate):
    """
    The NatRules Object in the FMC.
    """

    PREFIX_URL = '/policy/ftdnatpolicies'
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for NatRules class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for NatRules class.")
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
        logging.debug("In parse_kwargs() for NatRules class.")

    def nat_policy(self,name):
        logging.debug("In nat_policy() for NatRules class.")
        ftd_nat = FTDNatPolicy(fmc=self.fmc)
        ftd_nat.get(name=name)
        if 'id' in ftd_nat.__dict__:
            self.nat_id = ftd_nat.id
            self.URL = '{}{}/{}/natrules'.format(self.fmc.configuration_url, self.PREFIX_URL, self.nat_id)
            self.nat_added_to_url = True
        else:
            logging.warning('FTD NAT Policy {} not found.  Cannot set up NatRules for '
                            'NAT Policy.'.format(name))

    def post(self):
        logging.info('POST method for API for NatRules not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for NatRules not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for NatRules not supported.')
        pass

class TaskStatuses(APIClassTemplate):
    """
    The Task Status Object in the FMC.
    """

    URL_SUFFIX = '/job/taskstatuses'
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for TaskStatuses class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for TaskStatuses class.")
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
        logging.debug("In parse_kwargs() for TaskStatuses class.")

    def post(self):
        logging.info('POST method for API for TaskStatuses not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for TaskStatuses not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for TaskStatuses not supported.')
        pass