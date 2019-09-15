from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .vlantags import VlanTags
from fmcapi.api_objects.helper_functions import validate_vlans
import logging
import warnings


class VlanGroupTags(APIClassTemplate):
    """
    The VlanGroupTags Object in the FMC.
    """

    URL_SUFFIX = '/object/vlangrouptags'

    # Technically you can have objects OR literals but I'm not set up for "OR" logic, yet.
    REQUIRED_FOR_POST = ['name', 'objects']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for VlanGroupTags class.")
        self.parse_kwargs(**kwargs)
        self.type = 'VlanGroupTag'

    def format_data(self):
        logging.debug("In format_data() for VlanGroupTags class.")
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
        logging.debug("In parse_kwargs() for VlanGroupTags class.")
        if 'objects' in kwargs:
            self.objects = kwargs['objects']
        if 'literals' in kwargs:
            self.literals = kwargs['literals']

    def named_vlantags(self, action, name=''):
        logging.debug("In named_vlantags() for VlanGroupTags class.")
        if action == 'add':
            vlan1 = VlanTags(fmc=self.fmc)
            response = vlan1.get()
            if 'items' in response:
                new_vlan = None
                for item in response['items']:
                    if item['name'] == name:
                        new_vlan = {'name': item['name'], 'id': item['id'], 'type': item['type']}
                        break
                if new_vlan is None:
                    logging.warning(f'VlanTag "{name}" is not found in FMC.  Cannot add to VlanGroupTags.')
                else:
                    if 'objects' in self.__dict__:
                        duplicate = False
                        for obj in self.objects:
                            if obj['name'] == new_vlan['name']:
                                duplicate = True
                                break
                        if not duplicate:
                            self.objects.append(new_vlan)
                            logging.info(f'Adding "{name}" to VlanGroupTags.')
                    else:
                        self.objects = [new_vlan]
                        logging.info(f'Adding "{name}" to VlanGroupTags.')
        elif action == 'remove':
            if 'objects' in self.__dict__:
                objects_list = []
                for obj in self.objects:
                    if obj['name'] != name:
                        objects_list.append(obj)
                self.objects = objects_list
                logging.info(f'Removed "{name}" from VlanGroupTags.')
            else:
                logging.info("This VlanGroupTags has no named_vlantags.  Nothing to remove.")
        elif action == 'clear':
            if 'objects' in self.__dict__:
                del self.objects
                logging.info('All named_vlantags removed from this VlanGroupTags.')

    def unnamed_vlantags(self, action, startvlan='', endvlan=''):
        logging.debug("In unnamed_vlantags() for VlanGroupTags class.")
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
                    logging.info(f'Adding "{startvlan}/{endvlan}" to VlanGroupTags.')
            else:
                self.literals = [new_literal]
                logging.info(f'Adding "{startvlan}/{endvlan}" to VlanGroupTags.')
        elif action == 'remove':
            startvlan, endvlan = validate_vlans(start_vlan=startvlan, end_vlan=endvlan)
            if 'literals' in self.__dict__:
                literals_list = []
                for obj in self.literals:
                    if obj['startTag'] != startvlan and obj['endTag'] != endvlan:
                        literals_list.append(obj)
                self.literals = literals_list
                logging.info(f'Removed "{startvlan}/{endvlan}" from VlanGroupTags.')
            else:
                logging.info("This VlanGroupTag has no unnamed_vlantags.  Nothing to remove.")
        elif action == 'clear':
            if 'literals' in self.__dict__:
                del self.literals
                logging.info('All unnamed_vlantags removed from this VlanGroupTags.')


class VlanGroupTag(VlanGroupTags):
    warnings.warn("Deprecated: VlanGroupTag() should be called via VlanGroupTags().")
