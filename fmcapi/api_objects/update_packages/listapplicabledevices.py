from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .upgradepackages import UpgradePackages
import logging
import warnings


class ListApplicableDevices(APIClassTemplate):
    """
    The ListApplicableDevices Object in the FMC.
    """

    URL_SUFFIX = '/updates/upgradepackages'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ListApplicableDevices class.")
        self.type = 'UpgradePackage'
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for ListApplicableDevices class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'upgadePackage' in self.__dict__:
            json_data['upgadePackage'] = self.upgadePackage
        if 'model' in self.__dict__:
            json_data['model'] = self.model
        if 'modelId' in self.__dict__:
            json_data['modelId'] = self.modelId
        if 'modelNumber' in self.__dict__:
            json_data['modelNumber'] = self.modelNumber
        if 'modelType' in self.__dict__:
            json_data['modelType'] = self.modelType
        if 'healthStatus' in self.__dict__:
            json_data['healthStatus'] = self.healthStatus
        if 'sw_version' in self.__dict__:
            json_data['sw_version'] = self.sw_version
        if 'isPartofContainer' in self.__dict__:
            json_data['isPartofContainer'] = self.isPartofContainer
        if 'containerType' in self.__dict__:
            json_data['containerType'] = self.containerType
        if 'healthPolicy' in self.__dict__:
            json_data['healthPolicy'] = self.healthPolicy
        if 'accessPolicy' in self.__dict__:
            json_data['accessPolicy'] = self.accessPolicy
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for ListApplicableDevices class.")

    def upgrade_package(self, package_name):
        logging.debug("In upgrade_package() for ListApplicableDevices class.")
        package1 = UpgradePackages(fmc=self.fmc)
        package1.get(name=package_name)
        if 'id' in package1.__dict__:
            self.package_id = package1.id
            self.URL = f'{self.fmc.platform_url}{self.URL_SUFFIX}/{self.package_id}/applicabledevices'
            self.package_added_to_url = True
        else:
            logging.warning(f'UpgradePackage {package_name} not found.  Cannot get list of ListApplicableDevices.')

    def post(self):
        logging.info('POST method for API for ListApplicableDevices not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for ListApplicableDevices not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for ListApplicableDevices not supported.')
        pass


class ApplicableDevices(ListApplicableDevices):
    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn("Deprecated: ApplicableDevices() should be called via ListApplicableDevices().")
        super().__init__(fmc, **kwargs)
