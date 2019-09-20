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
    """Dispose of this Class after 20210101."""

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn("Deprecated: AccessControlPolicy() should be called via AccessPolicies().")
        super().__init__(fmc, **kwargs)
