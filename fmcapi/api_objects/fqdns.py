from .apiclasstemplate import APIClassTemplate
import logging


class FQDNS(APIClassTemplate):
    """
    The FQDNS Object in the FMC.
    """

    URL_SUFFIX = '/object/fqdns'
    VALID_FOR_DNS_RESOLUTION = ['IPV4_ONLY', 'IPV6_ONLY', 'IPV4_AND_IPV6']
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""
    FIRST_SUPPORTED_FMC_VERSION = '6.3.0'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for FQDNS class.")
        self.parse_kwargs(**kwargs)
        self.type = 'FQDN'
        if self.fmc.serverVersion < self.FIRST_SUPPORTED_FMC_VERSION:
            logging.warning(f'The FQDNS API feature was released in version {self.FIRST_SUPPORTED_FMC_VERSION}.  '
                            f'Your FMC version is {self.fmc.serverVersion}.  Upgrade to use this feature.')

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
                logging.warning(f'dnsResolution {self.dnsResolution} not a valid type.')
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
                logging.warning(f"dnsResolution {kwargs['dnsResolution']} not a valid type.")
        if 'overrides' in kwargs:
            self.overrides = kwargs['overrides']
        if 'overridable' in kwargs:
            self.overridable = kwargs['overridable']
