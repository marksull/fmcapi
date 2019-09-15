from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from fmcapi.api_objects.device_services.devicerecords import DeviceRecords
from fmcapi.api_objects.device_ha_pair_services.ftddevicehapairs import FTDDeviceHAPairs
import logging
import warnings


class DeviceGroupRecords(APIClassTemplate):
    """
    The DeviceGroupRecords Object in the FMC.
    """

    URL_SUFFIX = '/devicegroups/devicegrouprecords'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for DeviceGroupRecords class.")
        self.type = 'DeviceGroup'
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for DeviceGroupRecords class.")
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
        logging.debug("In parse_kwargs() for DeviceGroupRecords class.")
        if 'members' in kwargs:
            self.members = kwargs['members']

    def devices(self, action, members=[]):
        logging.debug("In devices() for DeviceGroupRecords class.")
        if action == 'add':
            for member in members:
                if member["type"] == 'device':
                    dev1 = DeviceRecords(fmc=self.fmc)
                    dev1.get(name=member["name"])
                elif member["type"] == 'deviceHAPair':
                    dev1 = FTDDeviceHAPairs(fmc=self.fmc)
                    dev1.get(name=member["name"])
                if 'id' in dev1.__dict__:
                    if 'members' in self.__dict__:
                        self.members.append({"id": dev1.id, "type": dev1.type, "name": dev1.name})
                    else:
                        self.members = [{"id": dev1.id, "type": dev1.type, "name": dev1.name}]
                    logging.info(f'DeviceRecord "{dev1.name}" added to this DeviceGroupRecords object.')
                else:
                    logging.warning(f'{member} not found.  Cannot add DeviceRecord to DeviceGroupRecords.')
        elif action == 'remove':
            if 'members' in self.__dict__:
                for member in members:
                    if member["type"] == 'device':
                        dev1 = DeviceRecords(fmc=self.fmc)
                        dev1.get(name=member["name"])
                    elif member["type"] == 'deviceHAPair':
                        dev1 = FTDDeviceHAPairs(fmc=self.fmc)
                        dev1.get(name=member["name"])
                    if 'id' in dev1.__dict__:
                        if member["type"] == 'device':
                            self.members = list(filter(lambda i: i['id'] != dev1.id, self.members))
                        elif member["type"] == 'deviceHAPair':
                            devHA1 = FTDDeviceHAPairs(fmc=self.fmc)
                            devHA1.get(name=member["name"])
                            self.members = list(filter(lambda i: i['id'] != devHA1.primary["id"], self.members))
                            self.members = list(filter(lambda i: i['id'] != devHA1.secondary["id"], self.members))
                    else:
                        logging.warning(f'DeviceRecord {member} not registered.  Cannot remove DeviceRecord'
                                        f' from DeviceGroupRecords.')
            else:
                logging.warning('DeviceGroupRecords has no members.  Cannot remove DeviceRecord.')
        elif action == 'clear':
            if 'members' in self.__dict__:
                del self.members
                logging.info('All device records removed from this DeviceGroupRecords object.')


class DeviceGroups(DeviceGroupRecords):
    warnings.warn("Deprecated: DeviceGroups() should be called via DeviceGroupRecords().")
