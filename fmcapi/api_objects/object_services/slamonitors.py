from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .securityzones import SecurityZones
import logging
import warnings


class SLAMonitors(APIClassTemplate):
    """
    The SLAMonitors Object in the FMC.
    """
    URL_SUFFIX = '/object/slamonitors'
    REQUIRED_FOR_POST = ['name', 'slaId', 'monitorAddress', 'interfaceObjects', 'type']
    REQUIRED_FOR_PUT = ['id', 'type']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for SLAMonitors class.")
        self.parse_kwargs(**kwargs)
        self.type = "SLAMonitor"

    def format_data(self):
        logging.debug("In format_data() for SLAMonitors class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'timeout' in self.__dict__:
            json_data['timeout'] = self.timeout
        if 'threshold' in self.__dict__:
            json_data['threshold'] = self.threshold
        if 'frequency' in self.__dict__:
            json_data['frequency'] = self.frequency
        if 'slaId' in self.__dict__:
            json_data['slaId'] = self.slaId
        if 'dataSize' in self.__dict__:
            json_data['dataSize'] = self.dataSize
        if 'tos' in self.__dict__:
            json_data['tos'] = self.tos
        if 'noOfPackets' in self.__dict__:
            json_data['noOfPackets'] = self.noOfPackets
        if 'monitorAddress' in self.__dict__:
            json_data['monitorAddress'] = self.monitorAddress
        if 'interfaceObjects' in self.__dict__:
            json_data['interfaceObjects'] = self.interfaceObjects
        if 'description' in self.__dict__:
            json_data['description'] = self.description
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for SLAMonitors class.")
        if 'timeout' in kwargs:
            self.timeout = kwargs['timeout']
        if 'threshold' in kwargs:
            self.securityZone = kwargs['threshold']
        if 'frequency' in kwargs:
            self.frequency = kwargs['frequency']
        if 'slaId' in kwargs:
            self.slaId = kwargs['slaId']
        if 'dataSize' in kwargs:
            self.dataSize = kwargs['dataSize']
        if 'tos' in kwargs:
            self.tos = kwargs['tos']
        if 'noOfPackets' in kwargs:
            self.noOfPackets = kwargs['noOfPackets']
        if 'monitorAddress' in kwargs:
            self.monitorAddress = kwargs['monitorAddress']
        if 'interfaceObjects' in kwargs:
            self.interfaceObjects = kwargs['interfaceObjects']
        if 'description' in kwargs:
            self.description = kwargs['description']

    def interfaces(self, names):
        logging.debug("In interfaces() for SLAMonitors class.")
        zones = []
        for name in names:
            # Supports passing list of str
            sz = SecurityZones(fmc=self.fmc)
            sz.get(name=name)
            if 'id' in sz.__dict__:
                zones.append({'name': sz.name, 'id': sz.id, 'type': sz.type})
            else:
                logging.warning(f'Security Zone, "{name}", not found.  Cannot add to SLAMonitors.')
        if len(zones) != 0:
            # Make sure we found at least one zone
            self.interfaceObjects = zones
        else:
            logging.warning(f'No valid Security Zones found: "{names}".  Cannot add to SLAMonitosr.')


class SLAMonitor(SLAMonitors):
    warnings.warn("Deprecated: SLAMonitor() should be called via SLAMonitors().")
