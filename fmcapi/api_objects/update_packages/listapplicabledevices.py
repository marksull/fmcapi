from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .upgradepackages import UpgradePackages
import logging
import warnings


class ListApplicableDevices(APIClassTemplate):
    """
    The ListApplicableDevices Object in the FMC.
    """

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
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ListApplicableDevices class.")
        self.type = "UpgradePackage"
        self.parse_kwargs(**kwargs)

    def upgrade_package(self, package_name):
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
        logging.info("POST method for API for ListApplicableDevices not supported.")
        pass

    def put(self):
        logging.info("PUT method for API for ListApplicableDevices not supported.")
        pass

    def delete(self):
        logging.info("DELETE method for API for ListApplicableDevices not supported.")
        pass


class ApplicableDevices(ListApplicableDevices):
    """Dispose of this Class after 20210101."""

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn(
            "Deprecated: ApplicableDevices() should be called via ListApplicableDevices()."
        )
        super().__init__(fmc, **kwargs)
