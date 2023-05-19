from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class AccessPolicies(APIClassTemplate):
    """
    The AccessPolicies Object in the FMC.
    """

    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
        "description",
        "defaultAction",
        "prefilterPolicySetting",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    VALID_CHARACTERS_FOR_NAME = """[ .\w\d_\-]"""
    URL_SUFFIX = "/policy/accesspolicies"
    REQUIRED_FOR_POST = ["name"]
    REQUIRED_FOR_PUT = ["id", "defaultAction", "defaultActionId"]
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
        self._defaultAction = None
        self.prefilter_id = None
        self.prefilter_name = None
        self.defaultAction = "BLOCK"
        self.defaultActionId = None
        self.parse_kwargs(**kwargs)

    def format_data(self):
        json_data = super().format_data()
        logging.debug("In format_data() for AccessPolicies class.")

        json_data["defaultAction"] = self.defaultAction

        if self.defaultActionId:
            json_data["defaultAction"]["id"] = self.defaultActionId

        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for AccessPolicies class.")

        default_action = kwargs.get("defaultAction", {}).get("action")
        if default_action:
            self.defaultAction = default_action

        default_action_id = kwargs.get("defaultAction", {}).get("id")
        if default_action_id:
            self.defaultActionId = default_action_id
