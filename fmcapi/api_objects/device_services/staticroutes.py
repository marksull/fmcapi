from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .device import Device
import logging


class StaticRoutes(APIClassTemplate):
    """
    The StaticRoutes Object in the FMC.
    """

    PREFIX_URL = '/devices/devicerecords'
    URL_SUFFIX = None

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for StaticRoutes class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for StaticRoutes class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'continentId' in self.__dict__:
            json_data['continentId'] = self.continentId
        if 'continents' in self.__dict__:
            json_data['continents'] = self.continents
        if 'countries' in self.__dict__:
            json_data['countries'] = self.countries
        if 'continentUUID' in self.__dict__:
            json_data['continentUUID'] = self.continentUUID
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for StaticRoutes class.")

    def device(self, device_name):
        logging.debug("In device() for StaticRoutes class.")
        device1 = Device(fmc=self.fmc)
        device1.get(name=device_name)
        if 'id' in device1.__dict__:
            self.device_id = device1.id
            self.URL = f'{self.fmc.configuration_url}{self.PREFIX_URL}/{self.device_id}/routing/staticroutes'
            self.device_added_to_url = True
        else:
            logging.warning(f'Device "{device_name}" not found.  Cannot set up device for physicalInterface.')

    def post(self):
        logging.info('POST method for API for StaticRoutes not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for StaticRoutes not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for StaticRoutes not supported.')
        pass
