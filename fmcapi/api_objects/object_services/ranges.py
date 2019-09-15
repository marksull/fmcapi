from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from fmcapi.api_objects.helper_functions import *
import logging
import warnings


class Ranges(APIClassTemplate):
    """
    The Ranges Object in the FMC.
    """

    URL_SUFFIX = '/object/ranges'
    REQUIRED_FOR_POST = ['name', 'value']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Ranges class.")
        self.parse_kwargs(**kwargs)
        if 'value' in kwargs:
            value_type = get_networkaddress_type(kwargs['value'])
            if value_type == 'host' or value_type == 'network':
                logging.warning(f"value, {kwargs['value']}, is of type {value_type}.  Limited functionality for this "
                                f"object due to it being created via the Ranges function.")
            if validate_ip_bitmask_range(value=kwargs['value'], value_type=value_type):
                self.value = kwargs['value']
            else:
                logging.error(f"Provided value, {kwargs['value']}, has an error with the IP address(es).")

    def format_data(self):
        logging.debug("In format_data() for Ranges class.")
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
        logging.debug("In parse_kwargs() for Ranges class.")
        if 'value' in kwargs:
            self.value = kwargs['value']


class IPRange(Ranges):
    """Dispose of this Class after 20210101."""

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn("Deprecated: IPRange() should be called via Ranges().")
        super().__init__(fmc, **kwargs)
