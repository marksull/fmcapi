from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging
import warnings


class AccessPolicies(APIClassTemplate):
    """
    The AccessPolicies Object in the FMC.
    """

    URL_SUFFIX = '/policy/accesspolicies'
    REQUIRED_FOR_POST = ['name']
    DEFAULT_ACTION_OPTIONS = ['BLOCK', 'NETWORK_DISCOVERY', 'IPS']  # Not implemented yet.
    FILTER_BY_NAME = True

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for AccessPolicies class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for AccessPolicies class.")
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
        logging.debug("In parse_kwargs() for AccessPolicies class.")
        if 'defaultAction' in kwargs:
            self.defaultAction = kwargs['defaultAction']
        else:
            self.defaultAction = {'action': 'BLOCK'}

    def put(self, **kwargs):
        logging.info('The put() method for the AccessPolicies() class can work but I need to write a '
                     'DefaultAction() class and accommodate for such before "putting".')
        pass


class AccessControlPolicy(AccessPolicies):
    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn("Deprecated: AccessControlPolicy() should be called via AccessPolicies().")
        super().__init__(fmc, **kwargs)
