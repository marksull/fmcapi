from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from fmcapi.api_objects.policy_services.accesspolicies import AccessPolicies
import time
import logging
import warnings


class DeviceRecords(APIClassTemplate):
    """
    The DeviceRecords Object in the FMC.
    """

    VALID_JSON_DATA = ['id', 'name', 'hostName', 'natID', 'regKey', 'license_caps', 'accessPolicy']
    VALID_FOR_KWARGS = VALID_JSON_DATA + ['acp_name', 'acp_id', 'model', 'modelId', 'modelNumber', 'modelType',
                                          'healthStatus', 'healthPolicy', 'keepLocalEvents', 'prohibitPacketTransfer',
                                          ]
    URL_SUFFIX = '/devices/devicerecords'
    REQUIRED_FOR_POST = ['accessPolicy', 'hostName', 'regKey']
    REQUIRED_FOR_PUT = ['id']
    LICENSES = ['BASE', 'MALWARE', 'URLFilter', 'THREAT', 'VPN']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for DeviceRecords class.")
        self.parse_kwargs(**kwargs)

    def licensing(self, action, name='BASE'):
        logging.debug("In licensing() for DeviceRecords class.")
        if action == 'add':
            if name in self.LICENSES:
                if 'license_caps' in self.__dict__:
                    self.license_caps.append(name)
                    self.license_caps = list(set(self.license_caps))
                else:
                    self.license_caps = [name]
                logging.info(f'License "{name}" added to this DeviceRecords object.')

            else:
                logging.warning(f'{name} not found in {self.LICENSES}.  Cannot add license to DeviceRecords.')
        elif action == 'remove':
            if name in self.LICENSES:
                if 'license_caps' in self.__dict__:
                    try:
                        self.license_caps.remove(name)
                    except ValueError:
                        logging.warning(f'{name} is not assigned to this devicerecord thus cannot be removed.')
                    logging.info(f'License "{name}" removed from this DeviceRecords object.')
                else:
                    logging.warning(f'{name} is not assigned to this devicerecord thus cannot be removed.')

            else:
                logging.warning(f'{name} not found in {self.LICENSES}.  Cannot remove license from DeviceRecords.')
        elif action == 'clear':
            if 'license_caps' in self.__dict__:
                del self.license_caps
                logging.info('All licensing removed from this DeviceRecords object.')

    def acp(self, name=''):
        logging.debug("In acp() for Device class.")
        acp = AccessPolicies(fmc=self.fmc)
        acp.get(name=name)
        if 'id' in acp.__dict__:
            self.accessPolicy = {'id': acp.id, 'type': acp.type}
        else:
            logging.warning(f'Access Control Policy {name} not found.  Cannot set up accessPolicy for DeviceRecords.')

    def post(self, **kwargs):
        logging.debug("In post() for Device class.")
        response = super().post(**kwargs)
        if 'post_wait_time' in kwargs:
            self.post_wait_time = kwargs['post_wait_time']
        else:
            self.post_wait_time = 300
        logging.info(f'DeviceRecords registration task submitted.  '
                     f'Waiting {self.post_wait_time} seconds for it to complete.')
        time.sleep(self.post_wait_time)
        return response


class Device(DeviceRecords):
    """Dispose of this Class after 20210101."""

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn("Deprecated: Device() should be called via DeviceRecords().")
        super().__init__(fmc, **kwargs)
