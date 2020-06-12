"""ACP Inheritance Settings Class"""
from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .accesspolicies import AccessPolicies
import logging


class InheritanceSettings(APIClassTemplate):
    """The InheritanceSettings Object in the FMC."""

    VALID_JSON_DATA = []
    VALID_FOR_KWARGS = VALID_JSON_DATA + [
        "id",
        "acp_id",
        "acp_name",
        "device_id",
        "device_name",
        "base_policy_id",
    ]
    PREFIX_URL = "/policy/accesspolicies"
    REQUIRED_FOR_PUT = ["acp_id", "id", "base_policy_id"]
    REQUIRED_FOR_GET = ["acp_id"]
    FIRST_SUPPORTED_FMC_VERSION = "6.5"

    def __init__(self, fmc, **kwargs):
        """
        Initialize InheritanceSettings object.

        Set self.type to "AccessPolicyInheritanceSettings", parse the kwargs, and set up the self.URL.

        Note: The InheritanceSettings API is a bit of a weird API. The construction of the API URI needs two IDs.
        According to the API documentation you need the ContainerID and the objectId where the later is defined as
        "Unique identifier of the Access Policy Inheritance Setting". These two values are actually the same value,
        specifically the ID of the ACP for which you are changing the inheritance.

        The third ID that is required for this API, which we have called the base_policy_id to align with the API
        documentation, is the ID of ACP that you want to be the parent.

        An example of use would be:

        fmc_integrate = InheritanceSettings(
            fmc=fmc_session,
            acp_id=child_policy["id"],
            id=child_policy["id"],
            base_policy_id=parent_policy["id"],
        )
        fmc_integrate.put()

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: None
        """
        logging.debug("In __init__() for InheritanceSettings class.")
        super().__init__(fmc, **kwargs)
        self.parse_kwargs(**kwargs)
        self.type = "AccessPolicyInheritanceSettings"
        self.URL = f"{self.URL}{self.URL_SUFFIX}"

    def parse_kwargs(self, **kwargs):
        """
        Parse the kwargs and set self variables to match.

        :return: None
        """
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for InheritanceSettings class.")
        if "acp_id" in kwargs:
            self.acp(acp_id=kwargs["acp_id"])
        if "acp_name" in kwargs:
            self.acp(name=kwargs["acp_name"])
        if "device_id" in kwargs:
            self.device(id=kwargs["device_id"])
        if "device_name" in kwargs:
            self.device(name=kwargs["device_name"])

    def acp(self, name="", acp_id=""):
        """
        Associate an AccessPolicies object with this InheritanceSettings object.

        :param name: (str)  Name of ACP.
        :param id: (str) ID of ACP.
        :return: None
        """
        # either name or id of the ACP should be given
        logging.debug("In acp() for InheritanceSettings class.")
        if acp_id != "":
            self.acp_id = acp_id
            self.URL = f"{self.fmc.configuration_url}{self.PREFIX_URL}/{self.acp_id}/inheritancesettings"
            self.acp_added_to_url = True
        elif name != "":
            acp1 = AccessPolicies(fmc=self.fmc)
            acp1.get(name=name)
            if "id" in acp1.__dict__:
                self.acp_id = acp1.id
                self.URL = f"{self.fmc.configuration_url}{self.PREFIX_URL}/{self.acp_id}/inheritancesettings"
                self.acp_added_to_url = True
            else:
                logging.warning(
                    f'Access Control Policy "{name}" not found.  Cannot configure acp for InheritanceSettings.'
                )
        else:
            logging.error("No accessPolicy name or id was provided.")

    def format_data(self, filter_query=""):
        """
        Gather all the data in preparation for sending to API in JSON format.

        :param filter_query: (str) 'all' or 'kwargs'
        :return: (dict) json_data
        """
        logging.debug("In format_data() for InheritanceSettings class.")
        return {
            "type": "AccessPolicyInheritanceSetting",
            "id": self.acp_id,
            "basePolicy": {"type": "AccessPolicy", "id": self.base_policy_id},
        }

    def post(self):
        """POST method for InheritanceSettings not supported."""
        logging.info("API POST method for InheritanceSettings not supported.")
        pass

    def delete(self, **kwargs):
        """DELETE method for InheritanceSettings not supported."""
        logging.info("API DELETE method for InheritanceSettings not supported.")
        pass
