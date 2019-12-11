"""Upgrades Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from fmcapi.api_objects.device_services.devicerecords import DeviceRecords
from .upgradepackages import UpgradePackages
import logging


class Upgrades(APIClassTemplate):
    """
    The Upgrades Object in the FMC.

    NOTE:  This should be called UpgradePackage but that collides with a Deprecated name for UpgradePackages.
    We can rename this after we remove that deprecation... which will be a while from now.
    """

    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
        "upgradePackage",
        "targets",
        "pushUpgradeFileOnly",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/updates/upgrades"

    def __init__(self, fmc, **kwargs):
        """
        Initialize Upgrades object.

        Set self.type to "Upgrade", parse the kwargs, and set up the self.URL.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Upgrades class.")
        self.type = "Upgrade"
        self.URL = f"{self.fmc.platform_url}{self.URL_SUFFIX}"
        self.parse_kwargs(**kwargs)

    def upgrade_package(self, package_name):
        """
        Upgrade named package.

        :param package_name: (str) Name of package to upgrade
        :return: None
        """
        logging.debug("In upgrade_package() for Upgrades class.")
        package1 = UpgradePackages(fmc=self.fmc)
        package1.get(name=package_name)
        if "id" in package1.__dict__:
            self.upgradePackage = {"id": package1.id, "type": package1.type}
        else:
            logging.warning(
                f'UpgradePackage "{package_name}" not found.  Cannot add package to Upgrades.'
            )

    def devices(self, devices):
        """
        List of devices.

        :param devices: (list) List of device names.
        :return: None
        """
        logging.debug("In devices() for Upgrades class.")
        for device in devices:
            device1 = DeviceRecords(fmc=self.fmc)
            device1.get(name=device)
            if "id" in device1.__dict__ and "targets" in self.__dict__:
                self.targets.append(
                    {"id": device1.id, "type": device1.type, "name": device1.name}
                )
            elif "id" in device1.__dict__:
                self.targets = [
                    {"id": device1.id, "type": device1.type, "name": device1.name}
                ]
            else:
                logging.warning(
                    f'Device "{device}" not found.  Cannot prepare devices for Upgrades.'
                )

    def get(self):
        """GET method for API for Upgrades not supported."""
        logging.info("GET method for API for Upgrades not supported.")
        pass

    def post(self, **kwargs):
        """Run POST call on FMC."""
        # returns a task status object
        logging.debug("In post() for Upgrades class.")
        self.fmc.autodeploy = False
        return super().post(**kwargs)

    def put(self):
        """PUT method for API for Upgrades not supported."""
        logging.info("PUT method for API for Upgrades not supported.")
        pass

    def delete(self):
        """DELETE method for API for Upgrades not supported."""
        logging.info("DELETE method for API for Upgrades not supported.")
        pass
