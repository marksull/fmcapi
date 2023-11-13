from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class Backup(APIClassTemplate):
    """The Backup Object in the FMC."""

    FIRST_SUPPORTED_FMC_VERSION = "7.3"
    VALID_JSON_DATA = []
    VALID_FOR_KWARGS = VALID_JSON_DATA + [
        "targetId",
        "backupVersion",
    ]
    REQUIRED_FOR_DELETE = [
        "targetId",
        "backupVersion",
    ]

    URL_SUFFIX = "/backup/files"

    def __init__(self, fmc, **kwargs):
        """
        Initialize Backup object.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: requests response
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Backup class.")
        self.parse_kwargs(**kwargs)

    def get(self, **kwargs):
        """
        Prepare to send GET call to FMC Backup Files API.

        If no self.targetId exists then return a full listing of all
        backups. Self.targetId must be set to 'manager' to target an FMC backup, otherwise,
        set self.targetId to device UUID to target backups for a particular FTD device.
        Set self.backupVersion(optional) with self.targetId to a specific backup version ID
        otherwise the latest backup version of self.targetId will be used.
        Set "expanded=true" results for specific object
        to gather additional detail.

        :return: requests response
        """
        response = super().get(**kwargs)
        return response

    def delete(self, **kwargs):
        """
        Prepare to send DELETE call to FMC Backup Files API.

        Self.targetId is required.
        Set self.targetId must be set to 'manager' to target an FMC backup, otherwise,
        set self.targetId to device UUID to target backups for a particular FTD device.
        Set self.backupVersion is technically optional, but is being enforced as required for extra safety.
        Otherwise, the latest backup could be deleted unintentionally.
        Set "expanded=true" results for specific object
        to gather additional detail.

        :return: requests response
        """
        response = super().delete(**kwargs)
        return response

    def post(self):
        """POST method for API for Backup not supported."""
        logging.info("POST method for API for Backup not supported.")
        pass

    def put(self):
        """PUT method for API for Backup not supported."""
        logging.info("PUT method for API for Backup not supported.")
        pass
