from .apiclasstemplate import APIClassTemplate
from .accesscontrolpolicy import AccessControlPolicy
import time
import logging


class Device(APIClassTemplate):
    """
    The Device Object in the FMC.
    """

    URL_SUFFIX = '/devices/devicerecords'
    REQUIRED_FOR_POST = ['accessPolicy', 'hostName', 'regKey']
    REQUIRED_FOR_PUT = ['id']
    LICENSES = ['BASE', 'MALWARE', 'URLFilter', 'THREAT', 'VPN']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Device class.")
        self.post_wait_time = 300
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for Device class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'hostName' in self.__dict__:
            json_data['hostName'] = self.hostName
        if 'natID' in self.__dict__:
            json_data['natID'] = self.natID
        if 'regKey' in self.__dict__:
            json_data['regKey'] = self.regKey
        if 'license_caps' in self.__dict__:
            json_data['license_caps'] = self.license_caps
        if 'accessPolicy' in self.__dict__:
            json_data['accessPolicy'] = self.accessPolicy
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for Device class.")
        if 'hostName' in kwargs:
            self.hostName = kwargs['hostName']
        if 'natID' in kwargs:
            self.natID = kwargs['natID']
        if 'regKey' in kwargs:
            self.regKey = kwargs['regKey']
        if 'license_caps' in kwargs:
            self.license_caps = kwargs['license_caps']
        if 'accessPolicy' in kwargs:
            self.accessPolicy = kwargs['accessPolicy']
        if 'acp_name' in kwargs:
            self.acp(name=kwargs['acp_name'])
        if 'model' in kwargs:
            self.model = kwargs['model']
        if 'modelId' in kwargs:
            self.modelId = kwargs['modelId']
        if 'modelNumber' in kwargs:
            self.modelNumber = kwargs['modelNumber']
        if 'modelType' in kwargs:
            self.modelType = kwargs['modelType']
        if 'healthStatus' in kwargs:
            self.healthStatus = kwargs['healthStatus']
        if 'healthPolicy' in kwargs:
            self.healthPolicy = kwargs['healthPolicy']
        if 'keepLocalEvents' in kwargs:
            self.keepLocalEvents = kwargs['keepLocalEvents']
        if 'prohibitPacketTransfer' in kwargs:
            self.prohibitPacketTransfer = kwargs['prohibitPacketTransfer']
        if 'post_wait_time' in kwargs:
            self.post_wait_time = kwargs['post_wait_time']

    def licensing(self, action, name='BASE'):
        logging.debug("In licensing() for Device class.")
        if action == 'add':
            if name in self.LICENSES:
                if 'license_caps' in self.__dict__:
                    self.license_caps.append(name)
                    self.license_caps = list(set(self.license_caps))
                else:
                    self.license_caps = [name]
                logging.info('License "{}" added to this Device object.'.format(name))

            else:
                logging.warning('{} not found in {}.  Cannot add license to Device.'.format(name, self.LICENSES))
        elif action == 'remove':
            if name in self.LICENSES:
                if 'license_caps' in self.__dict__:
                    try:
                        self.license_caps.remove(name)
                    except ValueError:
                        logging.warning('{} is not assigned to this device thus cannot be removed.'.format(name))
                    logging.info('License "{}" removed from this Device object.'.format(name))
                else:
                    logging.warning('{} is not assigned to this device thus cannot be removed.'.format(name))

            else:
                logging.warning('{} not found in {}.  Cannot remove license from '
                                'Device.'.format(name, self.LICENSES))
        elif action == 'clear':
            if 'license_caps' in self.__dict__:
                del self.license_caps
                logging.info('All licensing removed from this Device object.')

    def acp(self, name=''):
        logging.debug("In acp() for Device class.")
        acp = AccessControlPolicy(fmc=self.fmc)
        acp.get(name=name)
        if 'id' in acp.__dict__:
            self.accessPolicy = {'id': acp.id, 'type': acp.type}
        else:
            logging.warning('Access Control Policy {} not found.  Cannot set up accessPolicy for '
                            'Device.'.format(name))

    def post(self, **kwargs):
        logging.debug("In post() for Device class.")
        response = super().post(**kwargs)
        if 'post_wait_time' in kwargs:
            self.post_wait_time = kwargs['post_wait_time']
        logging.info(f'Device registration task submitted.  Waiting {self.post_wait_time} seconds for it to complete.')
        time.sleep(self.post_wait_time)
        return response
