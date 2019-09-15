from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from fmcapi.api_objects.device_services.device import Device
from fmcapi.api_objects.device_ha_pair_services.devicehapairs import DeviceHAPairs
import logging
import warnings


class DeviceGroupRecords(APIClassTemplate):
    """
    The DeviceGroups Object in the FMC.
    """

    URL_SUFFIX = '/devicegroups/devicegrouprecords'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for DeviceGroups class.")
        self.type = 'DeviceGroup'
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for DeviceGroups class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'members' in self.__dict__:
            json_data['members'] = self.members
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for DeviceGroups class.")
        if 'members' in kwargs:
            self.members = kwargs['members']

    def devices(self, action, members=[]):
        logging.debug("In devices() for DeviceGroups class.")
        if action == 'add':
            for member in members:
                if member["type"] == 'device':
                    dev1 = Device(fmc=self.fmc)
                    dev1.get(name=member["name"])
                elif member["type"] == 'deviceHAPair':
                    dev1 = DeviceHAPairs(fmc=self.fmc)
                    dev1.get(name=member["name"])
                if 'id' in dev1.__dict__:
                    if 'members' in self.__dict__:
                        self.members.append({"id": dev1.id, "type": dev1.type, "name": dev1.name})
                    else:
                        self.members = [{"id": dev1.id, "type": dev1.type, "name": dev1.name}]
                    logging.info(f'Device "{dev1.name}" added to this DeviceGroup object.')
                else:
                    logging.warning(f'{member} not found.  Cannot add Device to DeviceGroup.')
        elif action == 'remove':
            if 'members' in self.__dict__:
                for member in members:
                    if member["type"] == 'device':
                        dev1 = Device(fmc=self.fmc)
                        dev1.get(name=member["name"])
                    elif member["type"] == 'deviceHAPair':
                        dev1 = DeviceHAPairs(fmc=self.fmc)
                        dev1.get(name=member["name"])
                    if 'id' in dev1.__dict__:
                        if member["type"] == 'device':
                            self.members = list(filter(lambda i: i['id'] != dev1.id, self.members))
                        elif member["type"] == 'deviceHAPair':
                            devHA1 = DeviceHAPairs(fmc=self.fmc)
                            devHA1.get(name=member["name"])
                            self.members = list(filter(lambda i: i['id'] != devHA1.primary["id"], self.members))
                            self.members = list(filter(lambda i: i['id'] != devHA1.secondary["id"], self.members))
                    else:
                        logging.warning(f'Device {member} not registered.  Cannot remove Device from DeviceGroup.')
            else:
                logging.warning('DeviceGroup has no members.  Cannot remove Device.')
        elif action == 'clear':
            if 'members' in self.__dict__:
                del self.members
                logging.info('All devices removed from this DeviceGroup object.')


class DeviceGroups(DeviceGroupRecords):
    warnings.warn("Deprecated: DeviceGroups() should be called via DeviceGroupRecords().")
