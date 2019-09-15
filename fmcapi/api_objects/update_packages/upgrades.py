from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from fmcapi.api_objects.device_services.devicerecords import Device
from .upgradepackage import UpgradePackage
import logging


class Upgrades(APIClassTemplate):
    """
    The Upgrades Object in the FMC.
    """

    URL_SUFFIX = '/updates/upgrades'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Upgrades class.")
        self.type = 'Upgrade'
        self.URL = f'{self.fmc.platform_url}{self.URL_SUFFIX}'
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for Upgrades class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'upgradePackage' in self.__dict__:
            json_data['upgradePackage'] = self.upgradePackage
        if 'targets' in self.__dict__:
            json_data['targets'] = self.targets
        if 'pushUpgradeFileOnly' in self.__dict__:
            json_data['pushUpgradeFileOnly'] = self.pushUpgradeFileOnly
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for Upgrades class.")
        if 'upgradePackage' in kwargs:
            self.upgradePackage = kwargs['upgradePackage']
        if 'targets' in kwargs:
            self.targets = kwargs['targets']
        if 'pushUpgradeFileOnly' in kwargs:
            self.pushUpgradeFileOnly = kwargs['pushUpgradeFileOnly']

    def upgrade_package(self, package_name):
        logging.debug("In upgrade_package() for Upgrades class.")
        package1 = UpgradePackage(fmc=self.fmc)
        package1.get(name=package_name)
        if 'id' in package1.__dict__:
            self.upgradePackage = {"id": package1.id, "type": package1.type}
        else:
            logging.warning(f'UpgradePackage "{package_name}" not found.  Cannot add package to Upgrades.')

    def devices(self, devices):
        logging.debug("In devices() for Upgrades class.")
        for device in devices:
            device1 = Device(fmc=self.fmc)
            device1.get(name=device)
            if 'id' in device1.__dict__ and 'targets' in self.__dict__:
                self.targets.append({"id": device1.id, "type": device1.type, "name": device1.name})
            elif 'id' in device1.__dict__:
                self.targets = [{"id": device1.id, "type": device1.type, "name": device1.name}]
            else:
                logging.warning(f'Device "{device}" not found.  Cannot prepare devices for Upgrades.')

    def get(self):
        logging.info('GET method for API for Upgrades not supported.')
        pass

    def post(self, **kwargs):
        # returns a task status object
        logging.debug("In post() for Upgrades class.")
        self.fmc.autodeploy = False
        return super().post(**kwargs)

    def put(self):
        logging.info('PUT method for API for Upgrades not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for Upgrades not supported.')
        pass
