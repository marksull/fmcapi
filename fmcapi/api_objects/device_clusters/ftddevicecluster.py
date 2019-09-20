from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class FTDDeviceCluster(APIClassTemplate):
    """
    The FTDDeviceCluster Object in the FMC.
    """

    VALID_JSON_DATA = ['id', 'name']
    VALID_FOR_KWARGS = VALID_JSON_DATA + ['slavedevices',
                                          'modelType',
                                          'version', 'sw_version',
                                          'healthStatus',
                                          'healthPolicy',
                                          'model',
                                          'modelNumber',
                                          'accessPolicy',
                                          ]
    URL_SUFFIX = '/deviceclusters/ftddevicecluster'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for FTDDeviceCluster class.")
        self.parse_kwargs(**kwargs)
        self.type = 'DeviceCluster'

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for FTDDeviceCluster class.")
        if 'slaveDevices' in kwargs:
            self.slaveDevices = kwargs['slaveDevices']
        if 'modelType' in kwargs:
            self.modelType = kwargs['modelType']
        if 'version' in kwargs:
            self.version = kwargs['version']
        if 'sw_version' in kwargs:
            self.sw_version = kwargs['sw_version']
        if 'healthStatus' in kwargs:
            self.healthStatus = kwargs['healthStatus']
        if 'healthPolicy' in kwargs:
            self.healthPolicy = kwargs['healthPolicy']
        if 'model' in kwargs:
            self.model = kwargs['model']
        if 'modelNumber' in kwargs:
            self.modelNumber = kwargs['modelNumber']
        if 'accessPolicy' in kwargs:
            self.accessPolicy = kwargs['accessPolicy']

    def post(self):
        logging.info('POST method for API for FTDDeviceCluster not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for FTDDeviceCluster not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for FTDDeviceCluster not supported.')
        pass
