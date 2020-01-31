from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging
import warnings


class AccessPolicies(APIClassTemplate):
    """
    The AccessPolicies Object in the FMC.
    """

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
        return {"action": self._defaultAction}

    @defaultAction.setter
    def defaultAction(self, action):
        if action in self.DEFAULT_ACTION_OPTIONS:
            self._defaultAction = action
        else:
            logging.error(
                f"action, {action}, is not a valid option.  Choose from {self.DEFAULT_ACTION_OPTIONS}."
            )

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for AccessPolicies class.")
        self.parse_kwargs(**kwargs)
        self._defaultAction = None
        self.defaultAction = "BLOCK"

    def format_data(self):
        json_data = super().format_data()
        logging.debug("In format_data() for AccessPolicies class.")
        json_data["defaultAction"] = self.defaultAction
        return json_data


class AccessControlPolicy(AccessPolicies):
    """Dispose of this Class after 20210101."""

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn(
            "Deprecated: AccessControlPolicy() should be called via AccessPolicies()."
        )
        super().__init__(fmc, **kwargs)
