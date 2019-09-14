from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from fmcapi.api_objects.helper_functions import *
from .ipaddresses import IPAddresses
import logging


class NetworkGroup(APIClassTemplate):
    """
    The NetworkGroup Object in the FMC.
    """

    URL_SUFFIX = '/object/networkgroups'

    # Technically you can have objects OR literals but I'm not set up for "OR" logic, yet.
    REQUIRED_FOR_POST = ['name']

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
                    logging.warning(f'Network "{name}" is not found in FMC.  Cannot add to NetworkGroup.')
                else:
                    if 'objects' in self.__dict__:
                        duplicate = False
                        for obj in self.objects:
                            if obj['name'] == new_net['name']:
                                duplicate = True
                                break
                        if not duplicate:
                            self.objects.append(new_net)
                            logging.info(f'Adding "{name}" to NetworkGroup.')
                    else:
                        self.objects = [new_net]
                        logging.info(f'Adding "{name}" to NetworkGroup.')
        if action == 'addgroup':
            netg1 = NetworkGroup(fmc=self.fmc)
            response = netg1.get()
            if 'items' in response:
                new_net = None
                for item in response['items']:
                    if item['name'] == name:
                        new_net = {'name': item['name'], 'id': item['id'], 'type': item['type']}
                        break
                if new_net is None:
                    logging.warning(f'Network "{name}" is not found in FMC.  Cannot add to NetworkGroup.')
                else:
                    if 'objects' in self.__dict__:
                        duplicate = False
                        for obj in self.objects:
                            if obj['name'] == new_net['name']:
                                duplicate = True
                                break
                        if not duplicate:
                            self.objects.append(new_net)
                            logging.info(f'Adding "{name}" to NetworkGroup.')
                    else:
                        self.objects = [new_net]
                        logging.info(f'Adding "{name}" to NetworkGroup.')
        elif action == 'remove':
            if 'objects' in self.__dict__:
                objects_list = []
                for obj in self.objects:
                    if obj['name'] != name:
                        objects_list.append(obj)
                self.objects = objects_list
                logging.info(f'Removed "{name}" from NetworkGroup.')
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
                logging.error(f'Value "{value}" provided is not in a recognizable format.')
                return
            if 'literals' in self.__dict__:
                duplicate = False
                for obj in self.literals:
                    if obj['value'] == new_literal['value']:
                        duplicate = True
                        break
                if not duplicate:
                    self.literals.append(new_literal)
                    logging.info(f'Adding "{value}" to NetworkGroup.')
            else:
                self.literals = [new_literal]
                logging.info(f'Adding "{value}" to NetworkGroup.')
        elif action == 'remove':
            if 'literals' in self.__dict__:
                literals_list = []
                for obj in self.literals:
                    if obj['value'] != value:
                        literals_list.append(obj)
                self.literals = literals_list
                logging.info(f'Removed "{value}" from NetworkGroup.')
            else:
                logging.info("This NetworkGroup has no unnamed_networks.  Nothing to remove.")
        elif action == 'clear':
            if 'literals' in self.__dict__:
                del self.literals
                logging.info('All unnamed_networks removed from this NetworkGroup.')
