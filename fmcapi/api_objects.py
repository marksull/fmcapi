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
            if 'name' in self.__dict__:
                logging.info('GET success. Object with name: "{}" and id: "{}" fetched from'
                             ' FMC.'.format(self.name, self.id))
            else:
                logging.info('GET success. Object with id: "{}" fetched from'
                             ' FMC.'.format(self.id))
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
            if 'name' in self.__dict__:
                logging.info('PUT success. Object with name: "{}" and id: "{}" updated '
                             'in FMC.'.format(self.name, self.id))
            else:
                logging.info('PUT success. Object with id: "{}" updated '
                             'in FMC.'.format(self.id))
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
            if 'name' in self.name:
                logging.info('DELETE success. Object with name: "{}" and id: "{}" deleted '
                             'in FMC.'.format(self.name, self.id))
            else:
                logging.info('DELETE success. Object id: "{}" deleted '
                             'in FMC.'.format(self.id))
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


class AnyProtocolPortObjects(APIClassTemplate):
    """
    The AnyProtocolPortObjects Object in the FMC.
    """

    URL_SUFFIX = '/object/anyprotocolportobjects'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for AnyProtocolPortObjects class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for AnyProtocolPortObjects class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'overrideTargetId' in self.__dict__:
            json_data['overrideTargetId'] = self.overrideTargetId
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for AnyProtocolPortObjects class.")

    def post(self):
        logging.info('POST method for API for AnyProtocolPortObjects not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for AnyProtocolPortObjects not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for AnyProtocolPortObjects not supported.')
        pass


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


class ApplicationFilter(APIClassTemplate):
    """
    The ApplicationFilter Object in the FMC.
    """

    URL_SUFFIX = '/object/applicationfilters'
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ApplicationFilter class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for ApplicationFilter class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'appConditions' in self.__dict__:
            json_data['appConditions'] = self.appConditions
        if 'applications' in self.__dict__:
            json_data['applications'] = self.applications
        if 'conditions' in self.__dict__:
            json_data['conditions'] = self.conditions
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for ApplicationFilter class.")

    def post(self):
        logging.info('POST method for API for ApplicationFilter not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for ApplicationFilter not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for ApplicationFilter not supported.')
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


class CertEnrollment(APIClassTemplate):
    """
    The CertEnrollment Object in the FMC.
    """

    URL_SUFFIX = '/object/certenrollments'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for CertEnrollment class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for CertEnrollment class.")
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
        logging.debug("In parse_kwargs() for CertEnrollment class.")

    def post(self):
        logging.info('POST method for API for CertEnrollment not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for CertEnrollment not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for CertEnrollment not supported.')
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


class ISESecurityGroupTags(APIClassTemplate):
    """
    The ISESecurityGroupTags Object in the FMC.
    """

    URL_SUFFIX = '/object/isesecuritygrouptags'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ISESecurityGroupTags class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for ISESecurityGroupTags class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'tag' in self.__dict__:
            json_data['tag'] = self.tag
        if 'iseId' in self.__dict__:
            json_data['iseId'] = self.iseId
        if 'overrides' in self.__dict__:
            json_data['overrides'] = self.overrides
        if 'overridable' in self.__dict__:
            json_data['overridable'] = self.overridable
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for ISESecurityGroupTags class.")

    def post(self):
        logging.info('POST method for API for ISESecurityGroupTags not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for ISESecurityGroupTags not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for ISESecurityGroupTags not supported.')
        pass


class Realms(APIClassTemplate):
    """
    The Realms Object in the FMC.
    """

    URL_SUFFIX = '/object/realms'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Realms class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for Realms class.")
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
        logging.debug("In parse_kwargs() for Realms class.")

    def post(self):
        logging.info('POST method for API for Realms not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for Realms not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for Realms not supported.')
        pass


class RealmUserGroups(APIClassTemplate):
    """
    The RealmUserGroups Object in the FMC.
    """

    URL_SUFFIX = '/object/realmusergroups'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for RealmUserGroups class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for RealmUserGroups class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'realmUuid' in self.__dict__:
            json_data['realmUuid'] = self.realmUuid
        if 'realm' in self.__dict__:
            json_data['realm'] = self.realm
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for RealmUserGroups class.")

    def post(self):
        logging.info('POST method for API for RealmUserGroups not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for RealmUserGroups not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for RealmUserGroups not supported.')
        pass


class RealmUsers(APIClassTemplate):
    """
    The RealmUsers Object in the FMC.
    """

    URL_SUFFIX = '/object/realmusers'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for RealmUsers class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for RealmUsers class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'realmUuid' in self.__dict__:
            json_data['realmUuid'] = self.realmUuid
        if 'realm' in self.__dict__:
            json_data['realm'] = self.realm
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for RealmUsers class.")

    def post(self):
        logging.info('POST method for API for RealmUsers not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for RealmUsers not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for RealmUsers not supported.')
        pass


class SecurityGroupTags(APIClassTemplate):
    """
    The SecurityGroupTags Object in the FMC.
    """

    URL_SUFFIX = '/object/securitygrouptags'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for SecurityGroupTags class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for SecurityGroupTags class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'tag' in self.__dict__:
            json_data['tag'] = self.tag
        if 'overrides' in self.__dict__:
            json_data['overrides'] = self.overrides
        if 'overridable' in self.__dict__:
            json_data['overridable'] = self.overridable
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for SecurityGroupTags class.")

    def post(self):
        logging.info('POST method for API for SecurityGroupTags not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for SecurityGroupTags not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for SecurityGroupTags not supported.')
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


class SIUrlFeeds(APIClassTemplate):
    """
    The SIUrlFeeds Object in the FMC.
    """

    URL_SUFFIX = '/object/siurlfeeds'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for SIUrlFeeds class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for SIUrlFeeds class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'checksumURL' in self.__dict__:
            json_data['checksumURL'] = self.checksumURL
        if 'feedURL' in self.__dict__:
            json_data['feedURL'] = self.feedURL
        if 'updateFrequency' in self.__dict__:
            json_data['updateFrequency'] = self.updateFrequency
        if 'overrides' in self.__dict__:
            json_data['overrides'] = self.overrides
        if 'overridable' in self.__dict__:
            json_data['overridable'] = self.overridable
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for SIUrlFeeds class.")

    def post(self):
        logging.info('POST method for API for SIUrlFeeds not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for SIUrlFeeds not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for SIUrlFeeds not supported.')
        pass


class SIUrlLists(APIClassTemplate):
    """
    The SIUrlLists Object in the FMC.
    """

    URL_SUFFIX = '/object/siurllists'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for SIUrlLists class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for SIUrlLists class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'overrides' in self.__dict__:
            json_data['overrides'] = self.overrides
        if 'overridable' in self.__dict__:
            json_data['overridable'] = self.overridable
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for SIUrlLists class.")

    def post(self):
        logging.info('POST method for API for SIUrlLists not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for SIUrlLists not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for SIUrlLists not supported.')
        pass


class TunnelTags(APIClassTemplate):
    """
    The TunnelTags Object in the FMC.
    """

    URL_SUFFIX = '/object/tunneltags'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for TunnelTags class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for TunnelTags class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'overrides' in self.__dict__:
            json_data['overrides'] = self.overrides
        if 'overridable' in self.__dict__:
            json_data['overridable'] = self.overridable
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for TunnelTags class.")

    def post(self):
        logging.info('POST method for API for TunnelTags not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for TunnelTags not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for TunnelTags not supported.')
        pass


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


class DNSServerGroups(APIClassTemplate):
    """
    The DNSServerGroups Object in the FMC.
    """

    URL_SUFFIX = '/object/dnsservergroups'
    REQUIRED_FOR_POST = ['name', 'timeout']
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for DNSServerGroups class.")
        self.parse_kwargs(**kwargs)
        self.type = 'DNSServerGroupObject'

    def format_data(self):
        logging.debug("In format_data() for DNSServerGroups class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'retries' in self.__dict__:
            json_data['retries'] = self.retries
        if 'timeout' in self.__dict__:
            json_data['timeout'] = self.timeout
        if 'dnsservers' in self.__dict__:
            json_data['dnsservers'] = self.dnsservers
        if 'defaultdomain' in self.__dict__:
            json_data['defaultdomain'] = self.defaultdomain
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for DNSServerGroups class.")
        if 'retries' in kwargs:
            self.retries = kwargs['retries']
        if 'timeout' in kwargs:
            self.timeout = kwargs['timeout']
        if 'dnsservers' in kwargs:
            self.dnsservers = kwargs['dnsservers']
        if 'defaultdomain' in kwargs:
            self.defaultdomain = kwargs['defaultdomain']

    def servers(self, action, name_servers):
        logging.debug("In servers() for DNSServerGroups class.")
        if action == 'add':
            for name_server in name_servers:
                if 'dnsservers' in self.__dict__:
                    self.dnsservers.append({"name-server":name_server})
                else:
                    self.dnsservers = [{"name-server":name_server}]
                logging.info('Name-server "{}" added to this DNSServerGroups object.'.format(name_server))
        elif action == 'remove':
            if 'dnsservers' in self.__dict__:
                for name_server in name_servers:
                    self.dnsservers = list(filter(lambda i: i['name-server'] != name_server, self.dnsservers))
            else:
                logging.warning('DNSServerGroups has no members.  Cannot remove name-server.')
        elif action == 'clear':
            if 'dnsservers' in self.__dict__:
                del self.dnsservers
                logging.info('All name-servers removed from this DNSServerGroups object.')


class EndPointDeviceTypes(APIClassTemplate):
    """
    The EndPointDeviceTypes Object in the FMC.
    """

    URL_SUFFIX = '/object/endpointdevicetypes'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for EndPointDeviceTypes class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for EndPointDeviceTypes class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'fqName' in self.__dict__:
            json_data['fqName'] = self.fqName
        if 'iseId' in self.__dict__:
            json_data['iseId'] = self.iseId
        if 'overrides' in self.__dict__:
            json_data['overrides'] = self.overrides
        if 'overridable' in self.__dict__:
            json_data['overridable'] = self.overridable
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for EndPointDeviceTypes class.")

    def post(self):
        logging.info('POST method for API for EndPointDeviceTypes not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for EndPointDeviceTypes not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for EndPointDeviceTypes not supported.')
        pass


class ExtendedAccessList(APIClassTemplate):
    """
    The ExtendedAccessList Object in the FMC.
    """

    URL_SUFFIX = '/object/extendedaccesslist'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ExtendedAccessList class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for ExtendedAccessList class.")
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
        logging.debug("In parse_kwargs() for ExtendedAccessList class.")

    def post(self):
        logging.info('POST method for API for ExtendedAccessList not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for ExtendedAccessList not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for ExtendedAccessList not supported.')
        pass


class FQDNS(APIClassTemplate):
    """
    The FQDNS Object in the FMC.
    """

    URL_SUFFIX = '/object/fqdns'
    VALID_FOR_DNS_RESOLUTION = ['IPV4_ONLY', 'IPV6_ONLY', 'IPV4_AND_IPV6']
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for FQDNS class.")
        self.parse_kwargs(**kwargs)
        self.type = 'FQDN'

    def format_data(self):
        logging.debug("In format_data() for FQDNS class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'overrideTargetId' in self.__dict__:
            json_data['overrideTargetId'] = self.overrideTargetId
        if 'value' in self.__dict__:
            json_data['value'] = self.value
        if 'dnsResolution' in self.__dict__:
            if self.dnsResolution in self.VALID_FOR_DNS_RESOLUTION:
                json_data['dnsResolution'] = self.dnsResolution
            else:
                logging.warning('dnsResolution {} not a valid type".'.format(self.dnsResolution))
        if 'overrides' in self.__dict__:
            json_data['overrides'] = self.overrides
        if 'overridable' in self.__dict__:
            json_data['overridable'] = self.overridable
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for FQDNS class.")
        if 'overrideTargetId' in kwargs:
            self.overrideTargetId = kwargs['overrideTargetId']
        if 'value' in kwargs:
            self.value = kwargs['value']
        if 'dnsResolution' in kwargs:
            if kwargs['dnsResolution'] in self.VALID_FOR_DNS_RESOLUTION:
                self.dnsResolution = kwargs['dnsResolution']
            else:
                logging.warning('dnsResolution {} not a valid type".'.format(kwargs['dnsResolution']))
        if 'overrides' in kwargs:
            self.overrides = kwargs['overrides']
        if 'overridable' in kwargs:
            self.overridable = kwargs['overridable']


class Geolocation(APIClassTemplate):
    """
    The Geolocation Object in the FMC.
    """

    URL_SUFFIX = '/object/geolocations'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Geolocation class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for Geolocation class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'continentId' in self.__dict__:
            json_data['continentId'] = self.continentId
        if 'continents' in self.__dict__:
            json_data['continents'] = self.continents
        if 'countries' in self.__dict__:
            json_data['countries'] = self.countries
        if 'continentUUID' in self.__dict__:
            json_data['continentUUID'] = self.continentUUID
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for Geolocation class.")

    def post(self):
        logging.info('POST method for API for Geolocation not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for Geolocation not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for Geolocation not supported.')
        pass


class ICMPv4Object(APIClassTemplate):
    """
    The ICMPv4Object Object in the FMC.
    """

    URL_SUFFIX = '/object/icmpv4objects'
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ICMPv4Object class.")
        self.parse_kwargs(**kwargs)
        self.type = 'ICMPV4Object'

    def format_data(self):
        logging.debug("In format_data() for ICMPv4Object class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'overrideTargetId' in self.__dict__:
            json_data['overrideTargetId'] = self.overrideTargetId
        if 'code' in self.__dict__:
            json_data['code'] = self.code
        if 'icmpType' in self.__dict__:
            json_data['icmpType'] = self.icmpType
        if 'overrides' in self.__dict__:
            json_data['overrides'] = self.overrides
        if 'overridable' in self.__dict__:
            json_data['overridable'] = self.overridable
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for ICMPv4Object class.")
        if 'overrideTargetId' in kwargs:
            self.overrideTargetId = kwargs['overrideTargetId']
        if 'code' in kwargs:
            self.code = kwargs['code']
        if 'icmpType' in kwargs:
            self.icmpType = kwargs['icmpType']
        if 'overrides' in kwargs:
            self.overrides = kwargs['overrides']
        if 'overridable' in kwargs:
            self.overridable = kwargs['overridable']


class ICMPv6Object(APIClassTemplate):
    """
    The ICMPv6Object Object in the FMC.
    """

    URL_SUFFIX = '/object/icmpv6objects'
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ICMPv6Object class.")
        self.parse_kwargs(**kwargs)
        self.type = 'ICMPV6Object'

    def format_data(self):
        logging.debug("In format_data() for ICMPv6Object class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'overrideTargetId' in self.__dict__:
            json_data['overrideTargetId'] = self.overrideTargetId
        if 'code' in self.__dict__:
            json_data['code'] = self.code
        if 'icmpType' in self.__dict__:
            json_data['icmpType'] = self.icmpType
        if 'overrides' in self.__dict__:
            json_data['overrides'] = self.overrides
        if 'overridable' in self.__dict__:
            json_data['overridable'] = self.overridable
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for ICMPv6Object class.")
        if 'overrideTargetId' in kwargs:
            self.overrideTargetId = kwargs['overrideTargetId']
        if 'code' in kwargs:
            self.code = kwargs['code']
        if 'icmpType' in kwargs:
            self.icmpType = kwargs['icmpType']
        if 'overrides' in kwargs:
            self.overrides = kwargs['overrides']
        if 'overridable' in kwargs:
            self.overridable = kwargs['overridable']


class IKEv1IpsecProposals(APIClassTemplate):
    """
    The IKEv1IpsecProposals Object in the FMC.
    """

    URL_SUFFIX = '/object/ikev1ipsecproposals'
    REQUIRED_FOR_POST = ['name', 'espEncryption', 'espHash']
    VALID_FOR_ENCRYPTION = ['DES', '3DES', 'AES-128', 'AES-192', 'AES-256', 'ESP-NULL']
    VALID_FOR_HASH = ['NONE', 'MD5', 'SHA']
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for IKEv1IpsecProposals class.")
        self.parse_kwargs(**kwargs)
        self.type = 'IKEv1IPsecProposal'

    def format_data(self):
        logging.debug("In format_data() for IKEv1IpsecProposals class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'espEncryption' in self.__dict__:
            json_data['espEncryption'] = self.espEncryption
        if 'espHash' in self.__dict__:
            json_data['espHash'] = self.espHash
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for IKEv1IpsecProposals class.")
        if 'espEncryption' in kwargs:
            self.espEncryption = kwargs['espEncryption']
        if 'espHash' in kwargs:
            self.espHash = kwargs['espHash']


class IKEv1Policies(APIClassTemplate):
    """
    The IKEv1Policies Object in the FMC.
    """

    URL_SUFFIX = '/object/ikev1policies'
    REQUIRED_FOR_POST = ['name', 'encryption', 'hash', 'diffieHellmanGroup', 'lifetimeInSeconds', 'authenticationMethod']
    VALID_FOR_ENCRYPTION = ['DES', '3DES', 'AES-128', 'AES-192', 'AES-256']
    VALID_FOR_HASH = ['MD5', 'SHA']
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for IKEv1Policies class.")
        self.parse_kwargs(**kwargs)
        self.type = 'Ikev1PolicyObject'

    def format_data(self):
        logging.debug("In format_data() for IKEv1Policies class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'encryption' in self.__dict__:
            if self.encryption in self.VALID_FOR_ENCRYPTION:
                json_data['encryption'] = self.encryption
            else:
                logging.warning('encryption {} not a valid type".'.format(self.encryption))
        if 'hash' in self.__dict__:
            if self.hash in self.VALID_FOR_HASH:
                json_data['hash'] = self.hash
            else:
                logging.warning('hash {} not a valid type".'.format(self.hash))
        if 'priority' in self.__dict__:
            json_data['priority'] = self.priority
        if 'diffieHellmanGroup' in self.__dict__:
            json_data['diffieHellmanGroup'] = self.diffieHellmanGroup
        if 'authenticationMethod' in self.__dict__:
            json_data['authenticationMethod'] = self.authenticationMethod
        if 'lifetimeInSeconds' in self.__dict__:
            json_data['lifetimeInSeconds'] = self.lifetimeInSeconds
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for IKEv1Policies class.")
        if 'encryption' in kwargs:
            self.encryption = kwargs['encryption']
        if 'hash' in kwargs:
            self.hash = kwargs['hash']
        if 'priority' in kwargs:
            self.priority = kwargs['priority']
        if 'diffieHellmanGroup' in kwargs:
            self.diffieHellmanGroup = kwargs['diffieHellmanGroup']
        if 'authenticationMethod' in kwargs:
            self.authenticationMethod = kwargs['authenticationMethod']
        if 'lifetimeInSeconds' in kwargs:
            self.lifetimeInSeconds = kwargs['lifetimeInSeconds']


class IKEv2IpsecProposals(APIClassTemplate):
    """
    The IKEv2IpsecProposals Object in the FMC.
    """

    URL_SUFFIX = '/object/ikev2ipsecproposals'
    REQUIRED_FOR_POST = ['name', 'encryptionAlgorithms', 'integrityAlgorithms']
    VALID_FOR_ENCRYPTION = ['DES', '3DES', 'AES', 'AES-192', 'AES-256', 'NULL', 'AES-GCM', 'AES-GCM-192', 'AES-GCM-256', 'AES-GMAC', 'AES-GMAC-192', 'AES-GMAC-256']
    VALID_FOR_HASH = ['NULL', 'MD5', 'SHA-1', 'SHA-256', 'SHA-384', 'SHA-512']
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for IKEv2IpsecProposals class.")
        self.parse_kwargs(**kwargs)
        self.type = 'IKEv2IPsecProposal'

    def format_data(self):
        logging.debug("In format_data() for IKEv2IpsecProposals class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'encryptionAlgorithms' in self.__dict__:
            json_data['encryptionAlgorithms'] = self.encryptionAlgorithms
        if 'integrityAlgorithms' in self.__dict__:
            json_data['integrityAlgorithms'] = self.integrityAlgorithms
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for IKEv2IpsecProposals class.")
        if 'encryptionAlgorithms' in kwargs:
            self.encryptionAlgorithms = kwargs['encryptionAlgorithms']
        if 'integrityAlgorithms' in kwargs:
            self.integrityAlgorithms = kwargs['integrityAlgorithms']

    def encryption(self, action, algorithms=[]):
        logging.debug("In encryption() for IKEv2IpsecProposals class.")
        if action == 'add':
            for algorithm in algorithms:
                if 'encryptionAlgorithms' in self.__dict__:
                        if algorithm in self.encryptionAlgorithms:
                            logging.warning('encryptionAlgorithms {} already exists".'.format(algorithm))
                        elif algorithm in self.VALID_FOR_ENCRYPTION:
                            self.encryptionAlgorithms.append(algorithm)
                        else:
                            logging.warning('encryptionAlgorithms {} not a valid type".'.format(algorithm))
                else:
                    self.encryptionAlgorithms = [algorithm]
        elif action == 'remove':
            if 'encryptionAlgorithms' in self.__dict__:
                for algorithm in algorithms:
                    self.encryptionAlgorithms = list(filter(lambda i: i != algorithm, self.encryptionAlgorithms))
            else:
                logging.warning('IKEv2IpsecProposals has no members.  Cannot remove encryptionAlgorithms.')
        elif action == 'clear':
            if 'encryptionAlgorithms' in self.__dict__:
                del self.encryptionAlgorithms
                logging.info('All encryptionAlgorithms removed from this IKEv2IpsecProposals object.')

    def hash(self, action, algorithms=[]):
        logging.debug("In hash() for IKEv2IpsecProposals class.")
        if action == 'add':
            for algorithm in algorithms:
                if 'integrityAlgorithms' in self.__dict__:
                        if algorithm in self.integrityAlgorithms:
                            logging.warning('integrityAlgorithms {} already exists".'.format(algorithm))
                        elif algorithm in self.VALID_FOR_HASH:
                            self.integrityAlgorithms.append(algorithm)
                        else:
                            logging.warning('integrityAlgorithms {} not a valid type".'.format(algorithm))
                else:
                    self.integrityAlgorithms = [algorithm]
        elif action == 'remove':
            if 'integrityAlgorithms' in self.__dict__:
                for algorithm in algorithms:
                    self.integrityAlgorithms = list(filter(lambda i: i != algorithm, self.integrityAlgorithms))
            else:
                logging.warning('IKEv2IpsecProposals has no members.  Cannot remove integrityAlgorithms.')
        elif action == 'clear':
            if 'integrityAlgorithms' in self.__dict__:
                del self.integrityAlgorithms
                logging.info('All integrityAlgorithms removed from this IKEv2IpsecProposals object.')


class IKEv2Policies(APIClassTemplate):
    """
    The IKEv2Policies Object in the FMC.
    """

    URL_SUFFIX = '/object/ikev2policies'
    REQUIRED_FOR_POST = ['name', 'integrityAlgorithms', 'prfIntegrityAlgorithms', 'encryptionAlgorithms', 'diffieHellmanGroups']
    VALID_FOR_ENCRYPTION = ['DES', '3DES', 'AES', 'AES-192', 'AES-256', 'NULL', 'AES-GCM', 'AES-GCM-192', 'AES-GCM-256']
    VALID_FOR_INTEGRITY = ['NULL', 'MD5', 'SHA', 'SHA-256', 'SHA-384', 'SHA-512']
    VALID_FOR_PRF_INTEGRITY = ['MD5', 'SHA', 'SHA-256', 'SHA-384', 'SHA-512']
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for IKEv2Policies class.")
        self.parse_kwargs(**kwargs)
        self.type = 'Ikev2PolicyObject'

    def format_data(self):
        logging.debug("In format_data() for IKEv2Policies class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'priority' in self.__dict__:
            json_data['priority'] = self.priority
        if 'diffieHellmanGroups' in self.__dict__:
            json_data['diffieHellmanGroups'] = self.diffieHellmanGroups
        if 'integrityAlgorithms' in self.__dict__:
            json_data['integrityAlgorithms'] = self.integrityAlgorithms
        if 'prfIntegrityAlgorithms' in self.__dict__:
            json_data['prfIntegrityAlgorithms'] = self.prfIntegrityAlgorithms
        if 'encryptionAlgorithms' in self.__dict__:
            json_data['encryptionAlgorithms'] = self.encryptionAlgorithms
        if 'lifetimeInSeconds' in self.__dict__:
            json_data['lifetimeInSeconds'] = self.lifetimeInSeconds
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for IKEv2Policies class.")
        if 'priority' in kwargs:
            self.priority = kwargs['priority']
        if 'diffieHellmanGroups' in kwargs:
            self.diffieHellmanGroups = kwargs['diffieHellmanGroups']
        if 'integrityAlgorithms' in kwargs:
            self.integrityAlgorithms = kwargs['integrityAlgorithms']
        if 'prfIntegrityAlgorithms' in kwargs:
            self.prfIntegrityAlgorithms = kwargs['prfIntegrityAlgorithms']
        if 'encryptionAlgorithms' in kwargs:
            self.encryptionAlgorithms = kwargs['encryptionAlgorithms']
        if 'lifetimeInSeconds' in kwargs:
            self.lifetimeInSeconds = kwargs['lifetimeInSeconds']

    def encryption(self, action, algorithms=[]):
        logging.debug("In encryption() for IKEv2Policies class.")
        if action == 'add':
            for algorithm in algorithms:
                if 'encryptionAlgorithms' in self.__dict__:
                        if algorithm in self.encryptionAlgorithms:
                            logging.warning('encryptionAlgorithms {} already exists".'.format(algorithm))
                        elif algorithm in self.VALID_FOR_ENCRYPTION:
                            self.encryptionAlgorithms.append(algorithm)
                        else:
                            logging.warning('encryptionAlgorithms {} not a valid type".'.format(algorithm))
                else:
                    self.encryptionAlgorithms = [algorithm]
        elif action == 'remove':
            if 'encryptionAlgorithms' in self.__dict__:
                for algorithm in algorithms:
                    self.encryptionAlgorithms = list(filter(lambda i: i != algorithm, self.encryptionAlgorithms))
            else:
                logging.warning('IKEv2Policies has no members.  Cannot remove encryptionAlgorithms.')
        elif action == 'clear':
            if 'encryptionAlgorithms' in self.__dict__:
                del self.encryptionAlgorithms
                logging.info('All encryptionAlgorithms removed from this IKEv2Policies object.')

    def hash(self, action, algorithms=[]):
        logging.debug("In hash() for IKEv2Policies class.")
        if action == 'add':
            for algorithm in algorithms:
                if 'integrityAlgorithms' in self.__dict__:
                        if algorithm in self.integrityAlgorithms:
                            logging.warning('integrityAlgorithms {} already exists".'.format(algorithm))
                        elif algorithm in self.VALID_FOR_INTEGRITY:
                            self.integrityAlgorithms.append(algorithm)
                        else:
                            logging.warning('integrityAlgorithms {} not a valid type".'.format(algorithm))
                else:
                    if algorithm in self.VALID_FOR_INTEGRITY:
                        self.integrityAlgorithms = [algorithm]
                    else:
                        logging.warning('integrityAlgorithms {} not a valid type".'.format(algorithm))
        elif action == 'remove':
            if 'integrityAlgorithms' in self.__dict__:
                for algorithm in algorithms:
                    self.integrityAlgorithms = list(filter(lambda i: i != algorithm, self.integrityAlgorithms))
            else:
                logging.warning('IKEv2Policies has no members.  Cannot remove integrityAlgorithms.')
        elif action == 'clear':
            if 'integrityAlgorithms' in self.__dict__:
                del self.integrityAlgorithms
                logging.info('All integrityAlgorithms removed from this IKEv2Policies object.')

    def prf_hash(self, action, algorithms=[]):
        logging.debug("In prf_hash() for IKEv2Policies class.")
        if action == 'add':
            for algorithm in algorithms:
                if 'prfIntegrityAlgorithms' in self.__dict__:
                        if algorithm in self.prfIntegrityAlgorithms:
                            logging.warning('prfIntegrityAlgorithms {} already exists".'.format(algorithm))
                        elif algorithm in self.VALID_FOR_PRF_INTEGRITY:
                            self.prfIntegrityAlgorithms.append(algorithm)
                        else:
                            logging.warning('prfIntegrityAlgorithms {} not a valid type".'.format(algorithm))
                else:
                    if algorithm in self.VALID_FOR_PRF_INTEGRITY:
                        self.prfIntegrityAlgorithms = [algorithm]
                    else:
                      logging.warning('prfIntegrityAlgorithms {} not a valid type".'.format(algorithm))  
        elif action == 'remove':
            if 'prfIntegrityAlgorithms' in self.__dict__:
                for algorithm in algorithms:
                    self.prfIntegrityAlgorithms = list(filter(lambda i: i != algorithm, self.prfIntegrityAlgorithms))
            else:
                logging.warning('IKEv2Policies has no members.  Cannot remove prfIntegrityAlgorithms.')
        elif action == 'clear':
            if 'prfIntegrityAlgorithms' in self.__dict__:
                del self.prfIntegrityAlgorithms
                logging.info('All prfIntegrityAlgorithms removed from this IKEv2Policies object.')


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


class BridgeGroupInterfaces(APIClassTemplate):
    """
    The Bridge Group Interface Object in the FMC.
    """
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\-\/\. ]"""
    PREFIX_URL = '/devices/devicerecords'
    URL_SUFFIX = None
    REQUIRED_FOR_POST = ['bridgeGroupId']
    REQUIRED_FOR_PUT = ['id', 'device_id']
    VALID_FOR_IPV4 = ['static', 'dhcp', 'pppoe']
    VALID_FOR_MODE = ['INLINE', 'PASSIVE', 'TAP', 'ERSPAN', 'NONE']
    VALID_FOR_MTU = range(64,9000)
    
    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for BridgeGroupInterfaces class.")
        self.parse_kwargs(**kwargs)
        self.type = "BridgeGroupInterface"

    def format_data(self):
        logging.debug("In format_data() for BridgeGroupInterfaces class.")
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
        if 'selectedInterfaces' in self.__dict__:
            json_data['selectedInterfaces'] = self.selectedInterfaces
        if 'bridgeGroupId' in self.__dict__:
            json_data['bridgeGroupId'] = self.bridgeGroupId
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
        logging.debug("In parse_kwargs() for BridgeGroupInterfaces class.")
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
        if 'securityZone' in kwargs:
             self.securityZone = kwargs['securityZone']
        if 'enabled' in kwargs:
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
        if 'ipAddress' in kwargs:
            self.ipAddress = kwargs['ipAddress']
        if 'selectedInterfaces' in kwargs:
            self.selectedInterfaces = kwargs['selectedInterfaces']
        if 'bridgeGroupId' in kwargs:
            self.bridgeGroupId = kwargs['bridgeGroupId']
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
        logging.debug("In device() for BridgeGroupInterfaces class.")
        device1 = Device(fmc=self.fmc)
        device1.get(name=device_name)
        if 'id' in device1.__dict__:
            self.device_id = device1.id
            self.URL = '{}{}/{}/bridgegroupinterfaces'.format(self.fmc.configuration_url, self.PREFIX_URL, self.device_id)
            self.device_added_to_url = True
        else:
            logging.warning('Device {} not found.  Cannot set up device for '
                            'BridgeGroupInterfaces.'.format(device_name))
    def sz(self, name):
        logging.debug("In sz() for BridgeGroupInterfaces class.")
        sz = SecurityZone(fmc=self.fmc)
        sz.get(name=name)
        if 'id' in sz.__dict__:
            new_zone = {'name': sz.name, 'id': sz.id, 'type': sz.type}
            self.securityZone = new_zone
        else:
            logging.warning('Security Zone, "{}", not found.  Cannot add to BridgeGroupInterfaces.'.format(name))

    def static(self, ipv4addr, ipv4mask):
        logging.debug("In static() for BridgeGroupInterfaces class.")
        self.ipv4 = {"static":{"address":ipv4addr,"netmask":ipv4mask }}

    def dhcp(self, enableDefault=True, routeMetric=1):
       logging.debug("In dhcp() for BridgeGroupInterfaces class.")
       self.ipv4 = {"dhcp":{"enableDefaultRouteDHCP":enableDefault,"dhcpRouteMetric":routeMetric }}

    def p_interfaces(self, p_interfaces, device_name):
        logging.debug("In p_interface() for BridgeGroupInterfaces class.")
        list = []
        for p_intf in p_interfaces:            
            intf1 = PhysicalInterface(fmc=self.fmc)
            intf1.get(name=p_intf,device_name=device_name)
            if 'id' in intf1.__dict__:
                list.append({'name': intf1.name, 'id': intf1.id, 'type': intf1.type})
            else:
                logging.warning('PhysicalInterface, "{}", not found.  Cannot add to BridgeGroupInterfaces.'.format(name))
        self.selectedInterfaces = list


class RedundantInterfaces(APIClassTemplate):
    """
    The Bridge Group Interface Object in the FMC.
    """
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\-\/\. ]"""
    PREFIX_URL = '/devices/devicerecords'
    URL_SUFFIX = None
    REQUIRED_FOR_POST = ['redundantId']
    REQUIRED_FOR_PUT = ['id', 'device_id']
    VALID_FOR_IPV4 = ['static', 'dhcp', 'pppoe']
    VALID_FOR_MODE = ['INLINE', 'PASSIVE', 'TAP', 'ERSPAN', 'NONE']
    VALID_FOR_MTU = range(64,9000)
    
    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for RedundantInterfaces class.")
        self.parse_kwargs(**kwargs)
        self.type = "RedundantInterface"

    def format_data(self):
        logging.debug("In format_data() for RedundantInterfaces class.")
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
        if 'primaryInterface' in self.__dict__:
            json_data['primaryInterface'] = self.primaryInterface
        if 'secondaryInterface' in self.__dict__:
            json_data['secondaryInterface'] = self.secondaryInterface
        if 'redundantId' in self.__dict__:
            json_data['redundantId'] = self.redundantId
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
        logging.debug("In parse_kwargs() for RedundantInterfaces class.")
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
        if 'securityZone' in kwargs:
             self.securityZone = kwargs['securityZone']
        if 'enabled' in kwargs:
            self.enabled = kwargs['enabled']
        if 'MTU' in kwargs:
            if kwargs['MTU'] in self.VALID_FOR_MTU:
                self.MTU = kwargs['MTU']
            else:
                logging.warning('MTU {} should be in the range 64-9000".'.format(kwargs['MTU'])) 
                self.MTU = 1500
        if 'managementOnly' in kwargs:
            self.managementOnly = kwargs['managementOnly']
        if 'ipAddress' in kwargs:
            self.ipAddress = kwargs['ipAddress']
        if 'primaryInterface' in kwargs:
            self.primaryInterface = kwargs['primaryInterface']
        if 'secondaryInterface' in kwargs:
            self.secondaryInterface = kwargs['secondaryInterface']
        if 'redundantId' in kwargs:
            self.redundantId = kwargs['redundantId']
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
        logging.debug("In device() for RedundantInterfaces class.")
        device1 = Device(fmc=self.fmc)
        device1.get(name=device_name)
        if 'id' in device1.__dict__:
            self.device_id = device1.id
            self.URL = '{}{}/{}/redundantinterfaces'.format(self.fmc.configuration_url, self.PREFIX_URL, self.device_id)
            self.device_added_to_url = True
        else:
            logging.warning('Device {} not found.  Cannot set up device for '
                            'RedundantInterfaces.'.format(device_name))
    def sz(self, name):
        logging.debug("In sz() for RedundantInterfaces class.")
        sz = SecurityZone(fmc=self.fmc)
        sz.get(name=name)
        if 'id' in sz.__dict__:
            new_zone = {'name': sz.name, 'id': sz.id, 'type': sz.type}
            self.securityZone = new_zone
        else:
            logging.warning('Security Zone, "{}", not found.  Cannot add to RedundantInterfaces.'.format(name))

    def static(self, ipv4addr, ipv4mask):
        logging.debug("In static() for RedundantInterfaces class.")
        self.ipv4 = {"static":{"address":ipv4addr,"netmask":ipv4mask }}

    def dhcp(self, enableDefault=True, routeMetric=1):
       logging.debug("In dhcp() for RedundantInterfaces class.")
       self.ipv4 = {"dhcp":{"enableDefaultRouteDHCP":enableDefault,"dhcpRouteMetric":routeMetric }}

    def primary(self, p_interface, device_name):
        logging.debug("In primary() for RedundantInterfaces class.")
        intf1 = PhysicalInterface(fmc=self.fmc)
        intf1.get(name=p_interface,device_name=device_name)
        if 'id' in intf1.__dict__:
            self.primaryInterface = {'name': intf1.name, 'id': intf1.id, 'type': intf1.type}
            if 'MTU' not in self.__dict__:
                self.MTU = intf1.MTU
        else:
            logging.warning('PhysicalInterface, "{}", not found.  Cannot add to RedundantInterfaces.'.format(name))

    def secondary(self, p_interface, device_name):
        logging.debug("In primary() for RedundantInterfaces class.")
        intf1 = PhysicalInterface(fmc=self.fmc)
        intf1.get(name=p_interface,device_name=device_name)
        if 'id' in intf1.__dict__:
            self.secondaryInterface = {'name': intf1.name, 'id': intf1.id, 'type': intf1.type}
        else:
            logging.warning('PhysicalInterface, "{}", not found.  Cannot add to RedundantInterfaces.'.format(name))


class EtherchannelInterfaces(APIClassTemplate):
    """
    The Etherchanel Interface Object in the FMC.
    """
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\-\/\. ]"""
    PREFIX_URL = '/devices/devicerecords'
    URL_SUFFIX = None
    REQUIRED_FOR_POST = ['etherChannelId', 'mode', 'MTU']
    REQUIRED_FOR_PUT = ['id', 'device_id']
    VALID_FOR_IPV4 = ['static', 'dhcp', 'pppoe']
    VALID_FOR_MODE = ['INLINE', 'PASSIVE', 'TAP', 'ERSPAN', 'NONE']
    VALID_FOR_LACP_MODE = ['ACTIVE', 'PASSIVE', 'ON']
    VALID_FOR_MTU = range(64,9000)
    
    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for RedundantInterfaces class.")
        self.parse_kwargs(**kwargs)
        self.type = "RedundantInterface"

    def format_data(self):
        logging.debug("In format_data() for EtherchannelInterfaces class.")
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
        if 'selectedInterfaces' in self.__dict__:
            json_data['selectedInterfaces'] = self.selectedInterfaces
        if 'etherChannelId' in self.__dict__:
            json_data['etherChannelId'] = self.etherChannelId
        if 'lacpMode' in self.__dict__:
            json_data['lacpMode'] = self.lacpMode
        if 'maxActivePhysicalInterface' in self.__dict__:
            json_data['maxActivePhysicalInterface'] = self.maxActivePhysicalInterface
        if 'minActivePhysicalInterface' in self.__dict__:
            json_data['minActivePhysicalInterface'] = self.minActivePhysicalInterface
        if 'hardware' in self.__dict__:
            json_data['hardware'] = self.hardware
        if 'erspanFlowId' in self.__dict__:
            json_data['erspanFlowId'] = self.erspanFlowId
        if 'erspanSourceIP' in self.__dict__:
            json_data['erspanSourceIP'] = self.erspanSourceIP
        if 'loadBalancing' in self.__dict__:
            json_data['loadBalancing'] = self.loadBalancing
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
        logging.debug("In parse_kwargs() for EtherchannelInterfaces class.")
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
        if 'securityZone' in kwargs:
             self.securityZone = kwargs['securityZone']
        if 'enabled' in kwargs:
            self.enabled = kwargs['enabled']
        if 'MTU' in kwargs:
            if kwargs['MTU'] in self.VALID_FOR_MTU:
                self.MTU = kwargs['MTU']
            else:
                logging.warning('MTU {} should be in the range 64-9000".'.format(kwargs['MTU'])) 
                self.MTU = 1500
        if 'managementOnly' in kwargs:
            self.managementOnly = kwargs['managementOnly']
        if 'ipAddress' in kwargs:
            self.ipAddress = kwargs['ipAddress']
        if 'selectedInterfaces' in kwargs:
            self.selectedInterfaces = kwargs['selectedInterfaces']
        if 'etherChannelId' in kwargs:
            self.etherChannelId = kwargs['etherChannelId']
        if 'lacpMode' in kwargs:
            if kwargs['lacpMode'] in self.VALID_FOR_LACP_MODE:
                self.lacpMode = kwargs['lacpMode']
            else:
                logging.warning('LACP Mode {} is not a valid mode".'.format(kwargs['lacpMode'])) 
        if 'maxActivePhysicalInterface' in kwargs:
            self.maxActivePhysicalInterface = kwargs['maxActivePhysicalInterface']
        if 'minActivePhysicalInterface' in kwargs:
            self.minActivePhysicalInterface = kwargs['minActivePhysicalInterface']
        if 'hardware' in kwargs:
            self.hardware = kwargs['hardware']
        if 'erspanFlowId' in kwargs:
            self.erspanFlowId = kwargs['erspanFlowId']
        if 'erspanSourceIP' in kwargs:
            self.erspanSourceIP = kwargs['erspanSourceIP']
        if 'loadBalancing' in kwargs:
            if kwargs['loadBalancing'] in self.VALID_FOR_LOAD_BALANCING:
                self.loadBalancing = kwargs['loadBalancing']
            else:
                logging.warning('Load balancing method {} is not a valid method".'.format(kwargs['loadBalancing'])) 
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
        logging.debug("In device() for EtherchannelInterfaces class.")
        device1 = Device(fmc=self.fmc)
        device1.get(name=device_name)
        if 'id' in device1.__dict__:
            self.device_id = device1.id
            self.URL = '{}{}/{}/etherchannelinterfaces'.format(self.fmc.configuration_url, self.PREFIX_URL, self.device_id)
            self.device_added_to_url = True
        else:
            logging.warning('Device {} not found.  Cannot set up device for '
                            'EtherchannelInterfaces.'.format(device_name))
    def sz(self, name):
        logging.debug("In sz() for EtherchannelInterfaces class.")
        sz = SecurityZone(fmc=self.fmc)
        sz.get(name=name)
        if 'id' in sz.__dict__:
            new_zone = {'name': sz.name, 'id': sz.id, 'type': sz.type}
            self.securityZone = new_zone
        else:
            logging.warning('Security Zone, "{}", not found.  Cannot add to RedundantInterfaces.'.format(name))

    def static(self, ipv4addr, ipv4mask):
        logging.debug("In static() for EtherchannelInterfaces class.")
        self.ipv4 = {"static":{"address":ipv4addr,"netmask":ipv4mask }}

    def dhcp(self, enableDefault=True, routeMetric=1):
       logging.debug("In dhcp() for EtherchannelInterfaces class.")
       self.ipv4 = {"dhcp":{"enableDefaultRouteDHCP":enableDefault,"dhcpRouteMetric":routeMetric }}

    def p_interfaces(self, p_interfaces, device_name):
        logging.debug("In p_interfaces() for EtherchannelInterfaces class.")
        list = []
        for p_intf in p_interfaces:            
            intf1 = PhysicalInterface(fmc=self.fmc)
            intf1.get(name=p_intf,device_name=device_name)
            if 'id' in intf1.__dict__:
                list.append({'name': intf1.name, 'id': intf1.id, 'type': intf1.type})
            else:
                logging.warning('PhysicalInterface, "{}", not found.  Cannot add to EtherchannelInterfaces.'.format(name))
        self.selectedInterfaces = list


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
    VALID_FOR_MTU = range(64,9000)
    
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
                logging.warning('Method {} is not a valid ipv4 type.'.format(kwargs['ipv4']))
        if 'device_name' in kwargs:
            self.device(device_name=kwargs['device_name'])
        if 'mode' in kwargs:
            if kwargs['mode'] in self.VALID_FOR_MODE:
                self.mode = kwargs['mode']
            else:
                logging.warning('Mode {} is not a valid mode.'.format(kwargs['mode']))
        if 'securityZone' in kwargs:
             self.securityZone = kwargs['securityZone']
        if 'enabled' in kwargs:
            self.enabled = kwargs['enabled']
        if 'MTU' in kwargs:
            if kwargs['MTU'] in self.VALID_FOR_MTU:
                self.MTU = kwargs['MTU']
            else:
                logging.warning('MTU {} should be in the range 64-9000".'.format(kwargs['MTU'])) 
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
            self.URL = '{}{}/{}/subinterfaces'.format(self.fmc.configuration_url, self.PREFIX_URL, self.device_id)
            self.device_added_to_url = True
        else:
            logging.warning('Device {} not found.  Cannot set up device for '
                            'SubInterfaces.'.format(device_name))
    def sz(self, name):
        logging.debug("In sz() for SubInterfaces class.")
        sz = SecurityZone(fmc=self.fmc)
        sz.get(name=name)
        if 'id' in sz.__dict__:
            new_zone = {'name': sz.name, 'id': sz.id, 'type': sz.type}
            self.securityZone = new_zone
        else:
            logging.warning('Security Zone, "{}", not found.  Cannot add to SubInterfaces.'.format(name))

    def static(self, ipv4addr, ipv4mask):
        logging.debug("In static() for SubInterfaces class.")
        self.ipv4 = {"static":{"address":ipv4addr,"netmask":ipv4mask }}

    def dhcp(self, enableDefault=True, routeMetric=1):
       logging.debug("In dhcp() for SubInterfaces class.")
       self.ipv4 = {"dhcp":{"enableDefaultRouteDHCP":enableDefault,"dhcpRouteMetric":routeMetric }}

    def p_interface(self, p_interface, device_name):
        logging.debug("In p_interface() for SubInterfaces class.")
        intf1 = PhysicalInterface(fmc=self.fmc)
        intf1.get(name=p_interface,device_name=device_name)
        if 'id' in intf1.__dict__:
            self.name = intf1.name
            if 'MTU' not in self.__dict__:
                self.MTU = intf1.MTU
        else:
            logging.warning('PhysicalInterface, "{}", not found.  Cannot add to SubInterfaces.'.format(name))


class StaticRoutes(APIClassTemplate):
    """
    The StaticRoutes Object in the FMC.
    """

    PREFIX_URL = '/devices/devicerecords'
    URL_SUFFIX = None

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for StaticRoutes class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for StaticRoutes class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'continentId' in self.__dict__:
            json_data['continentId'] = self.continentId
        if 'continents' in self.__dict__:
            json_data['continents'] = self.continents
        if 'countries' in self.__dict__:
            json_data['countries'] = self.countries
        if 'continentUUID' in self.__dict__:
            json_data['continentUUID'] = self.continentUUID
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for StaticRoutes class.")

    def device(self, device_name):
        logging.debug("In device() for StaticRoutes class.")
        device1 = Device(fmc=self.fmc)
        device1.get(name=device_name)
        if 'id' in device1.__dict__:
            self.device_id = device1.id
            self.URL = '{}{}/{}/routing/staticroutes'.format(self.fmc.configuration_url, self.PREFIX_URL, self.device_id)
            self.device_added_to_url = True
        else:
            logging.warning('Device {} not found.  Cannot set up device for '
                            'physicalInterface.'.format(device_name))

    def post(self):
        logging.info('POST method for API for StaticRoutes not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for StaticRoutes not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for StaticRoutes not supported.')
        pass


class IPv4StaticRoute(APIClassTemplate):
    """
    The IPv4StaticRoute Object in the FMC.
    """

    PREFIX_URL = '/devices/devicerecords'
    URL_SUFFIX = None
    REQUIRED_FOR_POST = ['interfaceName', 'selectedNetworks', 'gateway']
    REQUIRED_FOR_PUT = ['id', 'device_id']
    
    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for IPv4StaticRoute class.")
        self.type = 'IPv4StaticRoute'
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for IPv4StaticRoute class.")
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
        logging.debug("In parse_kwargs() for IPv4StaticRoute class.")
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
        logging.debug("In device() for IPv4StaticRoute class.")
        device1 = Device(fmc=self.fmc)
        device1.get(name=device_name)
        if 'id' in device1.__dict__:
            self.device_id = device1.id
            self.URL = '{}{}/{}/routing/ipv4staticroutes'.format(self.fmc.configuration_url, self.PREFIX_URL, self.device_id)
            self.device_added_to_url = True
        else:
            logging.warning('Device {} not found.  Cannot set up device for '
                            'IPv4StaticRoute.'.format(device_name))

    def networks(self, action, networks):
        logging.info("In networks() for IPv4StaticRoute class.")
        if action == 'add':
            # Valid objects are IPHost, IPNetwork and NetworkGroup.  Create a dictionary to contain all three object type.
            ipaddresses_json = IPAddresses(fmc=self.fmc).get()
            networkgroup_json = NetworkGroup(fmc=self.fmc).get()
            items = ipaddresses_json.get('items', []) + networkgroup_json.get('items', [])
            for network in networks:
                # Find the matching object name in the dictionary if it exists
                net1 = list(filter(lambda i: i['name'] == network, items))
                if len(net1) > 0:
                    if 'selectedNetworks' in self.__dict__:
                        # Check to see if network already exists
                        exists = list(filter(lambda i: i['id'] == net1[0]['id'], self.selectedNetworks))
                        if 'id' in exists:
                            logging.warning('Network {} already exists in selectedNetworks.'.format(network))
                        else:
                            self.selectedNetworks.append({"type":net1[0]['type'],"id":net1[0]['id'],"name":net1[0]['name']})
                    else:
                        self.selectedNetworks = [{"type":net1[0]['type'],"id":net1[0]['id'],"name":net1[0]['name']}]
                else:
                    logging.warning('Network {} not found.  Cannot set up device for '
                                    'IPv4StaticRoute.'.format(network))
        elif action == 'remove':
            ipaddresses_json = IPAddresses(fmc=self.fmc).get()
            networkgroup_json = NetworkGroup(fmc=self.fmc).get()
            items = ipaddresses_json.get('items', []) + networkgroup_json.get('items', [])
            for network in networks:
                net1 = list(filter(lambda i: i['name'] == network, items))
                if len(net1) > 0:
                    if 'selectedNetworks' in self.__dict__:
                        new_net1 = list(filter(lambda i: i['id'] != net1[0]['id'], self.selectedNetworks))
                    else:
                        logging.warning('No selectedNetworks found for this Device '
                            'IPv4StaticRoute.'.format(network))
                else:
                    logging.warning('Network {} not found.  Cannot set up device for '
                                    'IPv4StaticRoute.'.format(network))
        elif action == 'clear':
            if 'selectedNetworks' in self.__dict__:
                del self.selectedNetworks
                logging.info('All selectedNetworks removed from this IPv4StaticRoute object.')

    def gw(self, name):
        logging.info("In gw() for IPv4StaticRoute class.")
        gw1 = IPHost(fmc=self.fmc)
        gw1.get(name=name)
        if 'id' in gw1.__dict__:
                self.gateway = {
                    "object":{
                        "type": gw1.type,
                        "id": gw1.id,
                        "name": gw1.name}}
        else:
            logging.warning('Network {} not found.  Cannot set up device for '
                            'IPv4StaticRoute.'.format(name))
    def ipsla(self, name):
        logging.info("In ipsla() for IPv4StaticRoute class.")
        ipsla1 = SLAMonitor(fmc=self.fmc)
        ipsla1.get(name=name)
        if 'id' in ipsla1.__dict__:
                self.routeTracking = {
                    "type": ipsla1.type,
                    "id": ipsla1.id,
                    "name": ipsla1.name}
        else:
            logging.warning('Object {} not found.  Cannot set up device for '
                            'IPv4StaticRoute.'.format(name))


class IPv6StaticRoute(APIClassTemplate):
    """
    The IPv6StaticRoute Object in the FMC.
    """

    PREFIX_URL = '/devices/devicerecords'
    URL_SUFFIX = None
    REQUIRED_FOR_POST = ['interfaceName', 'selectedNetworks', 'gateway']
    REQUIRED_FOR_PUT = ['id', 'device_id']
    
    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for IPv6StaticRoute class.")
        self.type = 'IPv6StaticRoute'
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for IPv6StaticRoute class.")
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
        if 'metricValue' in self.__dict__:
            json_data['metricValue'] = self.metricValue
        if 'isTunneled' in self.__dict__:
            json_data['isTunneled'] = self.isTunneled
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for IPv6StaticRoute class.")
        if 'device_name' in kwargs:
            self.device(device_name=kwargs['device_name'])
        if 'interfaceName' in kwargs:
            self.interfaceName = kwargs['interfaceName']
        if 'selectedNetworks' in kwargs:
            self.selectedNetworks = kwargs['selectedNetworks']
        if 'gateway' in kwargs:
             self.gateway = kwargs['gateway']
        if 'metricValue' in kwargs:
            self.metricValue = kwargs['metricValue']
        if 'isTunneled' in kwargs:
            self.isTunneled = kwargs['isTunneled']

    def device(self, device_name):
        logging.debug("In device() for IPv6StaticRoute class.")
        device1 = Device(fmc=self.fmc)
        device1.get(name=device_name)
        if 'id' in device1.__dict__:
            self.device_id = device1.id
            self.URL = '{}{}/{}/routing/ipv6staticroutes'.format(self.fmc.configuration_url, self.PREFIX_URL, self.device_id)
            self.device_added_to_url = True
        else:
            logging.warning('Device {} not found.  Cannot set up device for '
                            'IPv6StaticRoute.'.format(device_name))

    def networks(self, action, networks):
        logging.info("In networks() for IPv6StaticRoute class.")
        if action == 'add':
            # Valid objects are IPHost, IPNetwork and NetworkGroup.  Create a dictionary to contain all three object type.
            ipaddresses_json = IPAddresses(fmc=self.fmc).get()
            networkgroup_json = NetworkGroup(fmc=self.fmc).get()
            items = ipaddresses_json.get('items', []) + networkgroup_json.get('items', [])
            for network in networks:
                # Find the matching object name in the dictionary if it exists
                net1 = list(filter(lambda i: i['name'] == network, items))
                if len(net1) > 0:
                    if 'selectedNetworks' in self.__dict__:
                        # Check to see if network already exists
                        exists = list(filter(lambda i: i['id'] == net1[0]['id'], self.selectedNetworks))
                        if 'id' in exists:
                            logging.warning('Network {} already exists in selectedNetworks.'.format(network))
                        else:
                            self.selectedNetworks.append({"type":net1[0]['type'],"id":net1[0]['id'],"name":net1[0]['name']})
                    else:
                        self.selectedNetworks = [{"type":net1[0]['type'],"id":net1[0]['id'],"name":net1[0]['name']}]
                else:
                    logging.warning('Network {} not found.  Cannot set up device for '
                                    'IPv6StaticRoute.'.format(network))
        elif action == 'remove':
            ipaddresses_json = IPAddresses(fmc=self.fmc).get()
            networkgroup_json = NetworkGroup(fmc=self.fmc).get()
            items = ipaddresses_json.get('items', []) + networkgroup_json.get('items', [])
            for network in networks:
                net1 = list(filter(lambda i: i['name'] == network, items))
                if len(net1) > 0:
                    if 'selectedNetworks' in self.__dict__:
                        new_net1 = list(filter(lambda i: i['id'] != net1[0]['id'], self.selectedNetworks))
                    else:
                        logging.warning('No selectedNetworks found for this Device '
                            'IPv6StaticRoute.'.format(network))
                else:
                    logging.warning('Network {} not found.  Cannot set up device for '
                                    'IPv6StaticRoute.'.format(network))
        elif action == 'clear':
            if 'selectedNetworks' in self.__dict__:
                del self.selectedNetworks
                logging.info('All selectedNetworks removed from this IPv6StaticRoute object.')

    def gw(self, name):
        logging.info("In gw() for IPv6StaticRoute class.")
        gw1 = IPHost(fmc=self.fmc)
        gw1.get(name=name)
        if 'id' in gw1.__dict__:
                self.gateway = {
                    "object":{
                        "type": gw1.type,
                        "id": gw1.id,
                        "name": gw1.name}}
        else:
            logging.warning('Network {} not found.  Cannot set up device for '
                            'IPv6StaticRoute.'.format(name))


class DeviceGroups(APIClassTemplate):
    """
    The DeviceGroups Object in the FMC.
    """

    URL_SUFFIX = '/devicegroups/devicegrouprecords'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for DeviceGroups class.")
        self.type = 'DeviceGroup'
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for DeviceGroups class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'members' in self.__dict__:
            json_data['members'] = self.members
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for DeviceGroups class.")
        if 'members' in kwargs:
            self.members = kwargs['members']

    def devices(self, action, members=[]):
        logging.debug("In devices() for DeviceGroups class.")
        if action == 'add':
            for member in members:
                if member["type"] == 'device':
                    dev1 = Device(fmc=self.fmc)
                    dev1.get(name=member["name"])
                elif member["type"] == 'deviceHAPair':
                    dev1 = DeviceHAPairs(fmc=self.fmc)
                    dev1.get(name=member["name"])
                if 'id' in dev1.__dict__:
                    if 'members' in self.__dict__:
                        self.members.append({"id":dev1.id, "type":dev1.type, "name":dev1.name})
                    else:
                        self.members = [{"id":dev1.id, "type":dev1.type, "name":dev1.name}]
                    logging.info('Device "{}" added to this DeviceGroup object.'.format(dev1.name))
                else:
                    logging.warning('{} not found.  Cannot add Device to DeviceGroup.'.format(member))
        elif action == 'remove':
            if 'members' in self.__dict__:
                for member in members:
                    if member["type"] == 'device':
                        dev1 = Device(fmc=self.fmc)
                        dev1.get(name=member["name"])
                    elif member["type"] == 'deviceHAPair':
                        dev1 = DeviceHAPairs(fmc=self.fmc)
                        dev1.get(name=member["name"])
                    if 'id' in dev1.__dict__:
                        if member["type"] == 'device':
                            self.members = list(filter(lambda i: i['id'] != dev1.id, self.members))
                        elif member["type"] == 'deviceHAPair':
                            devHA1 = DeviceHAPairs(fmc=self.fmc)
                            devHA1.get(name=member["name"])
                            self.members = list(filter(lambda i: i['id'] != devHA1.primary["id"], self.members))
                            self.members = list(filter(lambda i: i['id'] != devHA1.secondary["id"], self.members))
                    else:
                        logging.warning('Device {} not registered.  Cannot remove Device from DeviceGroup.'.format(member))
            else:
                logging.warning('DeviceGroup has no members.  Cannot remove Device.')
        elif action == 'clear':
            if 'members' in self.__dict__:
                del self.members
                logging.info('All devices removed from this DeviceGroup object.')


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
        if 'acp_id' in kwargs:
            self.acp(id=kwargs['acp_id'])
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

    def acp(self, name='', id=''):
        # either name or id of the ACP should be given
        logging.debug("In acp() for ACPRule class.")
        if id != '':
            self.acp_id = id
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
            fqdns_json = FQDNS(fmc=self.fmc).get()
            items = ipaddresses_json.get('items', []) + networkgroup_json.get('items', []) + fqdns_json.get('items', [])
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
            fqdns_json = FQDNS(fmc=self.fmc).get()
            items = ipaddresses_json.get('items', []) + networkgroup_json.get('items', []) + fqdns_json.get('items', [])
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
            self.patOptions["roundRobin"] = options.roundRobin if "roundRobin" in options.keys() else True
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
            self.unidirectional = True
            self.patOptions = {"patPoolAddress": new_net}
            self.patOptions["interfacePat"] = options.interfacePat if "interfacePat" in options.keys() else False
            self.patOptions["includeReserve"] = options.includeReserve if "includeReserve" in options.keys() else False
            self.patOptions["roundRobin"] = options.roundRobin if "roundRobin" in options.keys() else True
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


class PolicyAssignments(APIClassTemplate):
    """
    The PolicyAssignments Object in the FMC.
    """
    REQUIRED_FOR_POST = ['targets','policy']
    REQUIRED_FOR_PUT = ['id','targets','policy']
    URL_SUFFIX = '/assignment/policyassignments'
    FILTER_BY_NAME = True

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for PolicyAssignments class.")
        self.parse_kwargs(**kwargs)
        self.type = "PolicyAssignment"

    def format_data(self):
        logging.debug("In format_data() for PolicyAssignments class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'targets' in self.__dict__:
            json_data['targets'] = self.targets
        if 'policy' in self.__dict__:
            json_data['policy'] = self.policy
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for PolicyAssignments class.")
        if 'targets' in kwargs:
            self.targets = kwargs['targets']
        if 'policy' in kwargs:
            self.policy = kwargs['policy']

    def ftd_natpolicy(self, name, devices):
        logging.debug("In ftd_natpolicy() for PolicyAssignments class.")
        targets = []
        pol1 = FTDNatPolicy(fmc=self.fmc)
        pol1.get(name=name)
        if 'id' in pol1.__dict__:
            self.policy = {"type":pol1.type, "name":pol1.name, "id":pol1.id}
        else:
            logging.warning('FTD NAT Policy {} not found.  Cannot set up'
                            'PolicyAssignment.'.format(name))
        for device in devices:
            if device["type"] == 'device':
                dev1 = Device(fmc=self.fmc)
                dev1.get(name=device["name"])
            elif device["type"] == 'deviceHAPair':
                dev1 = DeviceHAPairs(fmc=self.fmc)
                dev1.get(name=device["name"])
            if 'id' in dev1.__dict__:
                logging.info('Adding "{}" to targets for this FTDNat PolicyAssignment.'.format(dev1.name))
                targets.append({"type":dev1.type, "id":dev1.id, "name":dev1.name})
            else:
                logging.warning('Device/DeviceHA {} not found.  Cannot add to '
                                'PolicyAssignment.'.format(dev1.name))
        self.targets = targets

    def accesspolicy(self, name, devices):
        logging.debug("In accesspolicy() for PolicyAssignments class.")
        targets = []
        pol1 = AccessControlPolicy(fmc=self.fmc)
        pol1.get(name=name)
        if 'id' in pol1.__dict__:
            self.policy = {"type":pol1.type, "name":pol1.name, "id":pol1.id}
        else:
            logging.warning('Access Control Policy {} not found.  Cannot set up'
                            'PolicyAssignment.'.format(name))
        for device in devices:
            if device["type"] == 'device':
                dev1 = Device(fmc=self.fmc)
                dev1.get(name=device["name"])
            elif device["type"] == 'deviceHAPair':
                dev1 = DeviceHAPairs(fmc=self.fmc)
                dev1.get(name=device["name"])
            if 'id' in dev1.__dict__:
                logging.info('Adding "{}" to targets for this Access Control Policy PolicyAssignment.'.format(dev1.name))
                targets.append({"type":dev1.type, "id":dev1.id, "name":dev1.name})
            else:
                logging.warning('Device/DeviceHA {} not found.  Cannot add to '
                                'PolicyAssignment.'.format(dev1.name))
        self.targets = targets

    def delete(self):
        logging.info('DELETE method for API for PolicyAssignments not supported.')
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


class UpgradePackage(APIClassTemplate):
    """
    The UpgradePackage Object in the FMC.
    """

    URL_SUFFIX = '/updates/upgradepackages'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for UpgradePackage class.")
        self.type = 'UpgradePackage'
        self.URL = '{}{}'.format(self.fmc.platform_url, self.URL_SUFFIX)
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for UpgradePackage class.")
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
        logging.debug("In parse_kwargs() for UpgradePackage class.")

    def post(self):
        logging.info('POST method for API for UpgradePackage not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for UpgradePackage not supported.')
        pass


class ApplicableDevices(APIClassTemplate):
    """
    The ApplicableDevices Object in the FMC.
    """

    URL_SUFFIX = '/updates/upgradepackages'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ApplicableDevices class.")
        self.type = 'UpgradePackage'
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for ApplicableDevices class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'upgadePackage' in self.__dict__:
            json_data['upgadePackage'] = self.upgadePackage
        if 'model' in self.__dict__:
            json_data['model'] = self.model
        if 'modelId' in self.__dict__:
            json_data['modelId'] = self.modelId
        if 'modelNumber' in self.__dict__:
            json_data['modelNumber'] = self.modelNumber
        if 'modelType' in self.__dict__:
            json_data['modelType'] = self.modelType
        if 'healthStatus' in self.__dict__:
            json_data['healthStatus'] = self.healthStatus
        if 'sw_version' in self.__dict__:
            json_data['sw_version'] = self.sw_version
        if 'isPartofContainer' in self.__dict__:
            json_data['isPartofContainer'] = self.isPartofContainer
        if 'containerType' in self.__dict__:
            json_data['containerType'] = self.containerType
        if 'healthPolicy' in self.__dict__:
            json_data['healthPolicy'] = self.healthPolicy
        if 'accessPolicy' in self.__dict__:
            json_data['accessPolicy'] = self.accessPolicy
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for ApplicableDevices class.")

    def upgrade_package(self, package_name):
        logging.debug("In upgrade_package() for ApplicableDevices class.")
        package1 = UpgradePackage(fmc=self.fmc)
        package1.get(name=package_name)
        if 'id' in package1.__dict__:
            self.package_id = package1.id
            self.URL = '{}{}/{}/applicabledevices'.format(self.fmc.platform_url, self.URL_SUFFIX, self.package_id)
            self.package_added_to_url = True
        else:
            logging.warning('UpgradePackage {} not found.  Cannot get list of '
                            'ApplicableDevices.'.format(package_name))

    def post(self):
        logging.info('POST method for API for ApplicableDevices not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for ApplicableDevices not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for ApplicableDevices not supported.')
        pass


class Upgrades(APIClassTemplate):
    """
    The Upgrades Object in the FMC.
    """

    URL_SUFFIX = '/updates/upgrades'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Upgrades class.")
        self.type = 'Upgrade'
        self.URL = '{}{}'.format(self.fmc.platform_url, self.URL_SUFFIX)
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for Upgrades class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'upgradePackage' in self.__dict__:
            json_data['upgradePackage'] = self.upgradePackage
        if 'targets' in self.__dict__:
            json_data['targets'] = self.targets
        if 'pushUpgradeFileOnly' in self.__dict__:
            json_data['pushUpgradeFileOnly'] = self.pushUpgradeFileOnly
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for Upgrades class.")
        if 'upgradePackage' in kwargs:
            self.upgradePackage = kwargs['upgradePackage']
        if 'targets' in kwargs:
            self.targets = kwargs['targets']
        if 'pushUpgradeFileOnly' in kwargs:
            self.pushUpgradeFileOnly = kwargs['pushUpgradeFileOnly']

    def upgrade_package(self, package_name):
        logging.debug("In upgrade_package() for Upgrades class.")
        package1 = UpgradePackage(fmc=self.fmc)
        package1.get(name=package_name)
        if 'id' in package1.__dict__:
            self.upgradePackage = {"id":package1.id, "type":package1.type}
        else:
            logging.warning('UpgradePackage {} not found.  Cannot add package to '
                            'Upgrades.'.format(package_name))

    def devices(self, devices):
        logging.debug("In devices() for Upgrades class.")
        for device in devices:
            device1 = Device(fmc=self.fmc)
            device1.get(name=device)
            if 'id' in device1.__dict__ and 'targets' in self.__dict__:
                self.targets.append({"id":device1.id, "type":device1.type, "name":device1.name})
            elif 'id' in device1.__dict__:
                self.targets = [{"id":device1.id, "type":device1.type, "name":device1.name}]
            else:
                logging.warning('Device {} not found.  Cannot prepare devices for '
                                'Upgrades.'.format(device))

    def get(self):
        logging.info('GET method for API for Upgrades not supported.')
        pass

    def post(self, **kwargs):
        # returns a task status object
        logging.debug("In post() for Upgrades class.")
        self.fmc.autodeploy = False
        return super().post(**kwargs)

    def put(self):
        logging.info('PUT method for API for Upgrades not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for Upgrades not supported.')
        pass