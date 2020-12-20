"""List Applicable Devices Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .upgradepackages import UpgradePackages
import logging


class ListApplicableDevices(APIClassTemplate):
    """The ListApplicableDevices Object in the FMC."""

    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
        "upgradePackage",
        "model",
        "modelId",
        "modelNumber",
        "modelType",
        "healthStatus",
        "sw_version",
        "isPartofContainer",
        "containerType",
        "healthPolicy",
        "accessPolicy",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/updates/upgradepackages"

    def __init__(self, fmc, **kwargs):
        """
        Initialize ListApplicableDevices object.

        Set self.type to "UpgradePackage", and parse the kwargs.
        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ListApplicableDevices class.")
        self.type = "UpgradePackage"
        self.parse_kwargs(**kwargs)

    def upgrade_package(self, package_name):
        """
        Upgrade named package.

        :param package_name: (str) Name of package to upgrade
        :return: None
        """
        logging.debug("In upgrade_package() for ListApplicableDevices class.")
        package1 = UpgradePackages(fmc=self.fmc)
        package1.get(name=package_name)
        if "id" in package1.__dict__:
            self.package_id = package1.id
            self.URL = f"{self.fmc.platform_url}{self.URL_SUFFIX}/{self.package_id}/applicabledevices"
            self.package_added_to_url = True
        else:
            logging.warning(
                f"UpgradePackage {package_name} not found.  Cannot get list of ListApplicableDevices."
            )

    def post(self):
        """POST method for API for ListApplicableDevices not supported."""
        logging.info("POST method for API for ListApplicableDevices not supported.")
        pass

    def put(self):
        """PUT method for API for ListApplicableDevices not supported."""
        logging.info("PUT method for API for ListApplicableDevices not supported.")
        pass

    def delete(self):
        """DELETE method for API for ListApplicableDevices not supported."""
        logging.info("DELETE method for API for ListApplicableDevices not supported.")
        pass
