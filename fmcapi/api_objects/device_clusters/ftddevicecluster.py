from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class FTDDeviceCluster(APIClassTemplate):
    """
    The FTDDeviceCluster Object in the FMC.
    """

    URL_SUFFIX = '/deviceclusters/ftddevicecluster'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for FTDDeviceCluster class.")
        self.parse_kwargs(**kwargs)
        self.type = 'DeviceCluster'

    def format_data(self):
        logging.debug("In format_data() for FTDDeviceCluster class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        return json_data

    def post(self):
        logging.info('POST method for API for FTDDeviceCluster not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for FTDDeviceCluster not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for FTDDeviceCluster not supported.')
        pass
