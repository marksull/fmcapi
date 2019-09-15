from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .accesspolicies import AccessPolicies
import logging


class DefaultActions(APIClassTemplate):
    """
    The DefaultActions Object in the FMC.
    """

    PREFIX_URL = '/policy/accesspolicies'
    REQUIRED_FOR_PUT = ['acp_id', 'id', 'action']
    REQUIRED_FOR_GET = ['acp_id']
    VALID_ACTION = ['BLOCK', 'TRUST', 'PERMIT', 'NETWORK_DISCOVERY']

    def __init__(self, fmc, **kwargs):
        logging.debug("In __init__() for DefaultActions class.")
        super().__init__(fmc, **kwargs)
        self.parse_kwargs(**kwargs)
        self.type = 'AccessPolicyDefaultAction'
        self.URL = f'{self.URL}{self.URL_SUFFIX}'

    def format_data(self):
        logging.debug("In format_data() for FilePolicies class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'action' in self.__dict__:
            if self.action in self.VALID_ACTION:
                json_data['action'] = self.action
            else:
                logging.warning(f'action variable must be one of: {self.VALID_ACTION}.')
        if 'logEnd' in self.__dict__:
            json_data['logEnd'] = self.logEnd
        if 'logBegin' in self.__dict__:
            json_data['logBegin'] = self.logBegin
        if 'snmpConfig' in self.__dict__:
            json_data['snmpConfig'] = self.snmpConfig
        if 'intrusionPolicy' in self.__dict__:
            json_data['intrusionPolicy'] = self.intrusionPolicy
        if 'sendEventsToFMC' in self.__dict__:
            json_data['sendEventsToFMC'] = self.sendEventsToFMC
        if 'description' in self.__dict__:
            json_data['description'] = self.description
        if 'variableSet' in self.__dict__:
            json_data['variableSet'] = self.variableSet
        if 'version' in self.__dict__:
            json_data['version'] = self.version
        if 'syslogConfig' in self.__dict__:
            json_data['syslogConfig'] = self.syslogConfig
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for HitCounts class.")
        if 'acp_id' in kwargs:
            self.acp(acp_id=kwargs['acp_id'])
        if 'acp_name' in kwargs:
            self.acp(name=kwargs['acp_name'])
        if 'id' in kwargs:
            self.id = kwargs['id']
        if 'action' in kwargs:
            if kwargs['action'] in self.VALID_ACTION:
                self.action = kwargs['action']
            else:
                logging.warning(f'action variable must be one of: {self.VALID_ACTION}.')
            self.action = kwargs['action']
        if 'logEnd' in kwargs:
            self.logEnd = kwargs['logEnd']
        if 'logBegin' in kwargs:
            self.logBegin = kwargs['logBegin']
        if 'snmpConfig' in kwargs:
            self.snmpConfig = kwargs['snmpConfig']
        if 'intrusionPolicy' in kwargs:
            self.intrusionPolicy = kwargs['intrusionPolicy']
        if 'sendEventsToFMC' in kwargs:
            self.sendEventsToFMC = kwargs['sendEventsToFMC']
        if 'description' in kwargs:
            self.description = kwargs['description']
        if 'variableSet' in kwargs:
            self.variableSet = kwargs['variableSet']
        if 'version' in kwargs:
            self.version = kwargs['version']
        if 'syslogConfig' in kwargs:
            self.syslogConfig = kwargs['syslogConfig']
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'id' in kwargs:
            self.id = kwargs['id']
        if 'limit' in kwargs:
            self.limit = kwargs['limit']
        else:
            self.limit = self.fmc.limit

    def acp(self, name='', acp_id=''):
        # either name or id of the ACP should be given
        logging.debug("In acp() for DefaultActions class.")
        if acp_id != '':
            self.acp_id = acp_id
            self.URL = f'{self.fmc.configuration_url}{self.PREFIX_URL}/{self.acp_id}'
            self.acp_added_to_url = True
        elif name != '':
            acp1 = AccessPolicies(fmc=self.fmc)
            acp1.get(name=name)
            if 'id' in acp1.__dict__:
                self.acp_id = acp1.id
                self.URL = f'{self.fmc.configuration_url}{self.PREFIX_URL}/{self.acp_id}/defaultactions'
                self.acp_added_to_url = True
            else:
                logging.warning(f'Access Control Policy "{name}" not found.  Cannot configure acp for DefaultActions.')
        else:
            logging.error('No accessPolicy name or id was provided.')

    def delete(self, **kwargs):
        logging.info('API DELETE method for DefaultActions not supported.')
        pass

    def post(self):
        logging.info('API POST method for DefaultActions not supported.')
        pass
