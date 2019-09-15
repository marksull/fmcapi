from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .ftddevicehapairs import FTDDeviceHAPairs
import logging
import warnings


class MonitoredInterfaces(APIClassTemplate):
    """
    The MonitoredInterfaces Object in the FMC.
    """

    PREFIX_URL = '/devicehapairs/ftddevicehapairs'
    REQUIRED_FOR_PUT = ['id']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for MonitoredInterfaces class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for MonitoredInterfaces class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'ipv4Configuration' in self.__dict__:
            json_data['ipv4Configuration'] = self.ipv4Configuration
        if 'ipv6Configuration' in self.__dict__:
            json_data['ipv6Configuration'] = self.ipv6Configuration
        if 'monitorForFailures' in self.__dict__:
            json_data['monitorForFailures'] = self.monitorForFailures
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for MonitoredInterfaces class.")
        if 'ha_name' in kwargs:
            self.device_ha(ha_name=kwargs['ha_name'])
        if 'ipv4Configuration' in kwargs:
            self.ipv4Configuration = kwargs['ipv4Configuration']
        if 'ipv6Configuration' in kwargs:
            self.ipv6Configuration = kwargs['ipv6Configuration']
        if 'monitorForFailures' in kwargs:
            self.monitorForFailures = kwargs['monitorForFailures']

    def device_ha(self, ha_name):
        logging.debug("In device_ha() for MonitoredInterfaces class.")
        deviceha1 = FTDDeviceHAPairs(fmc=self.fmc, name=ha_name)
        deviceha1.get()
        if 'id' in deviceha1.__dict__:
            self.deviceha_id = deviceha1.id
            self.URL = f'{self.fmc.configuration_url}{self.PREFIX_URL}/{self.deviceha_id}/monitoredinterfaces'
            self.deviceha_added_to_url = True
        else:
            logging.warning(f'Device HA {ha_name} not found.  Cannot set up device for MonitoredInterfaces.')

    def ipv4(self, ipv4addr, ipv4mask, ipv4standbyaddr):
        logging.debug("In ipv4() for MonitoredInterfaces class.")
        self.ipv4Configuration = {
            "activeIPv4Address": ipv4addr,
            "activeIPv4Mask": ipv4mask,
            "standbyIPv4Address": ipv4standbyaddr}

    def post(self):
        logging.info('POST method for API for MonitoredInterfaces not supported.')
        pass


class DeviceHAMonitoredInterfaces(MonitoredInterfaces):
    """Dispose of this Class after 20210101."""

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn("Deprecated: DeviceHAMonitoredInterfaces() should be called via MonitoredInterfaces().")
        super().__init__(fmc, **kwargs)
