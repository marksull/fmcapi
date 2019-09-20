from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .accesspolicies import AccessPolicies
import logging


class DefaultActions(APIClassTemplate):
    """
    The DefaultActions Object in the FMC.
    """

    VALID_JSON_DATA = []
    VALID_FOR_KWARGS = VALID_JSON_DATA + ['acp_id', 'acp_name', 'device_id', 'device_name', 'fetchZeroHitCount',
                                          'limit',
                                          ]
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
        json_data = super().format_data()
        logging.debug("In format_data() for FilePolicies class.")
        if 'action' in self.__dict__:
            if self.action in self.VALID_ACTION:
                json_data['action'] = self.action
            else:
                logging.warning(f'action variable must be one of: {self.VALID_ACTION}.')
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
