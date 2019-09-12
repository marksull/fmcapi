from .apiclasstemplate import APIClassTemplate
from .accesscontrolpolicy import AccessControlPolicy
from .device import Device
import logging


class HitCount(APIClassTemplate):
    """
    The HitCount Object in the FMC.
    """

    PREFIX_URL = '/policy/accesspolicies'
    REQUIRED_FOR_PUT = ['acp_id']
    REQUIRED_FOR_DELETE = ['acp_id']
    REQUIRED_FOR_GET = ['acp_id']
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""
    FIRST_SUPPORTED_FMC_VERSION = '6.4'

    @property
    def URL_SUFFIX(self):
        """
        Add the URL suffixes for filter.
        """
        self.filter_init = '?filter="'
        self.filter = self.filter_init

        self.URL = self.URL.split('?')[0]

        if 'device_id' in self.__dict__:
            self.filter += f'deviceId:{self.device_id};'
        # if 'prefilter_ids' in self.__dict__:  # Haven't build prefilter Class yet but putting in here for that moment.
        #     self.filter += f'ids:{self.prefilter_ids};'
        if '_fetchZeroHitCount' in self.__dict__:
            self.filter += f'fetchZeroHitCount:{self._fetchZeroHitCount};'

        if self.filter is self.filter_init:
            self.filter += '"'
        self.filter = f'{self.filter[:-1]}"&expanded=true'

        if 'limit' in self.__dict__:
            self.filter += f'&limit={self.limit}'
        return self.filter

    @property
    def fetchZeroHitCount(self):
        return self._fetchZeroHitCount

    @fetchZeroHitCount.setter
    def fetchZeroHitCount(self, value=False):
        self._fetchZeroHitCount = value
        # Rebuild the URL with possible new information
        self.URL = self.URL.split('?')[0]
        self.URL = f'{self.URL}{self.URL_SUFFIX}'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for HitCount class.")
        self.parse_kwargs(**kwargs)
        self.type = 'HitCount'
        self.filter = ''
        self.fetchZeroHitCount = False
        self.device_id = False
        self.prefilter_ids = False
        self.URL = f'{self.URL}{self.URL_SUFFIX}'

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for HitCount class.")
        if 'acp_id' in kwargs:
            self.acp(acp_id=kwargs['acp_id'])
        if 'acp_name' in kwargs:
            self.acp(name=kwargs['acp_name'])
        if 'device_id' in kwargs:
            self.device(id=kwargs['device_id'])
        if 'device_name' in kwargs:
            self.device(name=kwargs['device_name'])
        if 'fetchZeroHitCount' in kwargs:
            self.fetchZeroHitCount = kwargs['fetchZeroHitCount']
        if 'limit' in kwargs:
            self.limit = kwargs['limit']
        else:
            self.limit = self.fmc.limit

    def acp(self, name='', acp_id=''):
        # either name or id of the ACP should be given
        logging.debug("In acp() for HitCount class.")
        if acp_id != '':
            self.acp_id = acp_id
            self.URL = f'{self.fmc.configuration_url}{self.PREFIX_URL}/{self.acp_id}/operational/hitcounts'
            self.acp_added_to_url = True
        elif name != '':
            acp1 = AccessControlPolicy(fmc=self.fmc)
            acp1.get(name=name)
            if 'id' in acp1.__dict__:
                self.acp_id = acp1.id
                self.URL = f'{self.fmc.configuration_url}{self.PREFIX_URL}/{self.acp_id}/operational/hitcounts'
                self.acp_added_to_url = True
            else:
                logging.warning(f'Access Control Policy "{name}" not found.  Cannot configure acp for HitCount.')
        else:
            logging.error('No accessPolicy name or id was provided.')
        # Rebuild the URL with possible new information
        self.URL = self.URL.split('?')[0]
        self.URL = f'{self.URL}{self.URL_SUFFIX}'

    def device(self, name='', id=''):
        logging.debug("In device() for HitCount class")
        if id != '':
            self.device_id = id
        elif name != '':
            device1 = Device(fmc=self.fmc)
            device1.get(name=name)
            if 'id' in device1.__dict__:
                self.device_id = device1.id
            else:
                logging.warning(f'Device "{name}" not found.  Cannot configure device for HitCount.')
        else:
            logging.error('No device name or id was provided.')
        # Rebuild the URL with possible new information
        self.URL = self.URL.split('?')[0]
        self.URL = f'{self.URL}{self.URL_SUFFIX}'

    def get(self, **kwargs):
        """
        Get HitCounts based on filter criteria
        :return:
        """
        logging.debug("In get() for HitCount class.")
        self.parse_kwargs(**kwargs)
        if self.fmc.serverVersion < self.FIRST_SUPPORTED_FMC_VERSION:
            logging.error(f'Your FMC version, {self.fmc.serverVersion} does not support GET of this feature.')
            return {'items': []}
        if self.valid_for_get() and (self.device_id or self.prefilter_ids):
            if self.dry_run:
                logging.info('Dry Run enabled.  Not actually sending to FMC.  Here is what would have been sent:')
                logging.info('\tMethod = GET')
                logging.info(f'\tURL = {self.URL}')
                return False
            response = self.fmc.send_to_api(method='get', url=self.URL)
            self.parse_kwargs(**response)
            if 'items' not in response:
                response['items'] = []
            return response
        else:
            logging.warning("get() method failed due to failure to pass valid_for_get() test.")
            return False

    def post(self):
        logging.info('API POST method for HitCount not supported.')
        pass
