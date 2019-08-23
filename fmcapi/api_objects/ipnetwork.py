from .apiclasstemplate import APIClassTemplate
from .helper_functions import *
import logging


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
