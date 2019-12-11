"""Access Control Policy Classes."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging
import warnings


class AccessPolicies(APIClassTemplate):
    """The AccessPolicies Object in the FMC."""

    VALID_JSON_DATA = ["id", "name", "type", "description", "defaultAction"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/policy/accesspolicies"
    REQUIRED_FOR_POST = ["name"]
    REQUIRED_FOR_PUT = ["id", "defaultAction"]
    DEFAULT_ACTION_OPTIONS = [
        "BLOCK",
        "TRUST",
        "PERMIT",
        "NETWORK_DISCOVERY",
        "INHERIT_FROM_PARENT",
    ]
    FILTER_BY_NAME = True

    @property
    def defaultAction(self):
        """
        Getter for defaultAction.

        :return: {"action": self._defaultAction}
        """
        return {"action": self._defaultAction}

    @defaultAction.setter
    def defaultAction(self, action):
        """
        Setter for defaultAction.

        :return: None
        """
        if action in self.DEFAULT_ACTION_OPTIONS:
            self._defaultAction = action
        else:
            logging.error(
                f"action, {action}, is not a valid option.  Choose from {self.DEFAULT_ACTION_OPTIONS}."
            )

    def __init__(self, fmc, **kwargs):
        """
        Initialize AccessPolicies object.

        :param fmc: (object) FMC object
        :param **kwargs: Set initial variables during instantiation of AccessPolicies object.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for AccessPolicies class.")
        self.parse_kwargs(**kwargs)
        self._defaultAction = None
        self.defaultAction = "BLOCK"

    def format_data(self, filter_query=""):
        """
        Gather all the data in preparation for sending to API in JSON format.

        :param filter_query: (str) 'all' or 'kwargs'
        :return: (dict) json_data
        """
        json_data = super().format_data()
        logging.debug("In format_data() for AccessPolicies class.")
        json_data["defaultAction"] = self.defaultAction
        return json_data

    def put(self):
        """PUT method for API for AccessPolicies not supported."""
        logging.info("PUT method for API for AccessPolicies not supported.")
        pass

    def delete(self):
        """DELETE method for API for AccessPolicies not supported."""
        logging.info("DELETE method for API for AccessPolicies not supported.")
        pass


class AccessControlPolicy(AccessPolicies):
    """
    Dispose of this Class after 20210101.

    Use AccessPolicies() instead.
    """

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn(
            "Deprecated: AccessControlPolicy() should be called via AccessPolicies()."
        )
        super().__init__(fmc, **kwargs)
