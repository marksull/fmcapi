from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from fmcapi.api_objects.helper_functions import validate_vlans
import logging
import warnings


class VlanTags(APIClassTemplate):
    """
    The VlanTags Object in the FMC.
    """

    URL_SUFFIX = '/object/vlantags'
    REQUIRED_FOR_POST = ['name', 'data']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for VlanTags class.")
        self.type = 'VlanTag'
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for VlanTasg class.")
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
        logging.debug("In parse_kwargs() for VlanTags class.")
        if 'data' in kwargs:
            self.data = kwargs['data']

    def vlans(self, start_vlan, end_vlan=''):
        logging.debug("In vlans() for VlanTags class.")
        start_vlan, end_vlan = validate_vlans(start_vlan=start_vlan, end_vlan=end_vlan)
        self.data = {'startTag': start_vlan, 'endTag': end_vlan}


class VlanTag(VlanTags):
    warnings.warn("Deprecated: VlanTag() should be called via VlanTags().")
