from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging
import warnings


class PreFilterPolicies(APIClassTemplate):
    """
    The PreFilterPolicies Object in the FMC.
    """

    VALID_JSON_DATA = ["id", "name", "type", "description", "defaultAction"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/policy/prefilterpolicies"
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""
    REQUIRED_FOR_POST = ["name"]
    DEFAULT_ACTION_OPTIONS = ["ANALYZE_TUNNELS", "BOCK_TUNNELS"]
    FIRST_SUPPORTED_FMC_VERSION = "6.5"

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for PreFilterPolicies class.")
        self.parse_kwargs(**kwargs)
        self.type = "PreFilterPolicy"
        self._defaultAction = None
        self.defaultAction = "ANALYZE_TUNNELS"

    @property
    def defaultAction(self):
        return {"type": "PrefilterPolicyDefaultAction", "action": self._defaultAction}

    @defaultAction.setter
    def defaultAction(self, action):
        if action in self.DEFAULT_ACTION_OPTIONS:
            self._defaultAction = action
        else:
            logging.error(
                f"action, {action}, is not a valid option.  Choose from {self.DEFAULT_ACTION_OPTIONS}."
            )

    def format_data(self):
        json_data = super().format_data()
        logging.debug("In format_data() for AccessPolicies class.")
        json_data["defaultAction"] = self.defaultAction
        return json_data

    def put(self):
        logging.info("PUT method for API for PreFilterPolicies not supported.")
        pass


class PreFilterPolicy(PreFilterPolicies):
    """Dispose of this Class after 20210101."""

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn(
            "Deprecated: PreFilterPolicy() should be called via PreFilterPolicies()."
        )
        super().__init__(fmc, **kwargs)
