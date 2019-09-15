from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging
import warnings


class UpgradePackages(APIClassTemplate):
    """
    The UpgradePackages Object in the FMC.
    """

    URL_SUFFIX = '/updates/upgradepackages'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for UpgradePackages class.")
        self.type = 'UpgradePackage'
        self.URL = f'{self.fmc.platform_url}{self.URL_SUFFIX}'
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for UpgradePackages class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for UpgradePackages class.")

    def post(self):
        logging.info('POST method for API for UpgradePackages not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for UpgradePackages not supported.')
        pass


class UpgradePackage(UpgradePackages):
    """Dispose of this Class after 20210101."""

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn("Deprecated: UpgradePackage() should be called via UpgradePackages().")
        super().__init__(fmc, **kwargs)
