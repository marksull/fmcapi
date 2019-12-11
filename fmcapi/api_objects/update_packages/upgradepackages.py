"""Upgrade Packages Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging
import warnings


class UpgradePackages(APIClassTemplate):
    """The UpgradePackages Object in the FMC."""

    VALID_JSON_DATA = ["id", "name", "type"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/updates/upgradepackages"

    def __init__(self, fmc, **kwargs):
        """
        Initialize UpgradePackages object.

        Set self.type to "UpgradePackage", parse the kwargs, and set up the self.URL.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for UpgradePackages class.")
        self.type = "UpgradePackage"
        self.URL = f"{self.fmc.platform_url}{self.URL_SUFFIX}"
        self.parse_kwargs(**kwargs)

    def post(self):
        """POST method for API for UpgradePackages not supported."""
        logging.info("POST method for API for UpgradePackages not supported.")
        pass

    def put(self):
        """PUT method for API for UpgradePackages not supported."""
        logging.info("PUT method for API for UpgradePackages not supported.")
        pass


class UpgradePackage(UpgradePackages):
    """
    Dispose of this Class after 20210101.

    Use UpgradePackages() instead.
    """

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn(
            "Deprecated: UpgradePackage() should be called via UpgradePackages()."
        )
        super().__init__(fmc, **kwargs)
