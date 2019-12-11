"""Realm Users Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class RealmUsers(APIClassTemplate):
    """The RealmUsers Object in the FMC."""

    VALID_JSON_DATA = ["id", "name", "type", "realmUuid", "realm"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/realmusers"

    def __init__(self, fmc, **kwargs):
        """
        Initialize RealmUsers object.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for RealmUsers class.")
        self.parse_kwargs(**kwargs)

    def post(self):
        """POST method for API for RealmUsers not supported."""
        logging.info("POST method for API for RealmUsers not supported.")
        pass

    def put(self):
        """PUT method for API for RealmUsers not supported."""
        logging.info("PUT method for API for RealmUsers not supported.")
        pass

    def delete(self):
        """DELETE method for API for RealmUsers not supported."""
        logging.info("DELETE method for API for RealmUsers not supported.")
        pass
