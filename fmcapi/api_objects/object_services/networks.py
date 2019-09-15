from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from fmcapi.api_objects.helper_functions import *
import logging
import warnings


class Networks(APIClassTemplate):
    """
    The Networks Object in the FMC.
    """

    URL_SUFFIX = '/object/networks'
    REQUIRED_FOR_POST = ['name', 'value']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Networks class.")
        self.parse_kwargs(**kwargs)
        if 'value' in kwargs:
            value_type = get_networkaddress_type(kwargs['value'])
            if value_type == 'range' or value_type == 'host':
                logging.warning(f"value, {kwargs['value']}, is of type {value_type}.  Limited functionality for this "
                                f"object due to it being created via the Networks function.")
            if validate_ip_bitmask_range(value=kwargs['value'], value_type=value_type):
                self.value = kwargs['value']
            else:
                logging.error(f"Provided value, {kwargs['value']}, has an error with the IP address(es).")

    def format_data(self):
        logging.debug("In format_data() for Networks class.")
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
        logging.debug("In parse_kwargs() for Networks class.")
        if 'value' in kwargs:
            self.value = kwargs['value']


class IPNetwork(Networks):
    warnings.warn("Deprecated: IPNetwork() should be called via Networks().")
