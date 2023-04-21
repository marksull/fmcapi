"""AccessPolicy Category Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from fmcapi.api_objects.policy_services.accesspolicies import AccessPolicies
import logging


class Categories(APIClassTemplate):
    """
    The AccessPolicy Categories Object in the FMC.
    """

    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + [
        "acp_id",
        "acp_name",
        "aboveCategory",
        "insertBefore",
        "insertAfter",
        "section",
    ]
    FIRST_SUPPORTED_FMC_VERSION = "6.5"
    PREFIX_URL = "/policy/accesspolicies"
    REQUIRED_FOR_POST = ["name", "acp_id"]
    REQUIRED_FOR_GET = ["acp_id"]
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\-<>, ]"""

    @property
    def URL_SUFFIX(self):
        """
        Add the URL suffixes for aboveCategory, insertBefore and insertAfter
        NOTE: You must specify these at the time the object is initialized (created) for this feature
        to work correctly. Example:
            This works:
                new_category = Categories(fmc=fmc, acp_name='acp1', insertBefore=2)

            This does not:
                new_category = Categories(fmc=fmc, acp_name='acp1')
                new_category.insertBefore = 2
        """
        url = "?"

        if "aboveCategory" in self.__dict__:
            url = f"{url}aboveCategory={self.aboveCategory}&"
        if "insertBefore" in self.__dict__:
            url = f"{url}insertBefore={self.insertBefore}&"
        if "insertAfter" in self.__dict__:
            url = f"{url}insertAfter={self.insertAfter}&"
        if "insertBefore" in self.__dict__ and "insertAfter" in self.__dict__:
            logging.warning("ACP category has both insertBefore and insertAfter params")
        if "section" in self.__dict__:
            url = f"{url}section={self.section}&"

        return url[:-1]

    def __init__(self, fmc, **kwargs):
        """
        Initialize Categories object.

        Set self.type to "Category", parse the kwargs, and set up the self.URL.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Categories class.")
        self.type = "Category"
        self.parse_kwargs(**kwargs)
        self.URL = f"{self.URL}{self.URL_SUFFIX}"

    def parse_kwargs(self, **kwargs):
        """
        Parse the kwargs and set self variables to match.

        :return: None
        """
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for Categories class.")
        if "acp_id" in kwargs:
            self.acp(id=kwargs["acp_id"])
        if "acp_name" in kwargs:
            self.acp(name=kwargs["acp_name"])

    def acp(self, name="", id=""):
        """
        Associate an AccessPolicies object with this Categories object.

        :param name: (str)  Name of ACP.
        :param id: (str) ID of ACP.
        :return: None
        """
        # either name or id of the ACP should be given
        logging.debug("In acp() for Categories class.")
        if id != "":
            self.acp_id = id
            self.URL = f"{self.fmc.configuration_url}{self.PREFIX_URL}/{id}/categories"
        elif name != "":
            acp1 = AccessPolicies(fmc=self.fmc)
            acp1.get(name=name)
            if "id" in acp1.__dict__:
                self.acp_id = acp1.id
                self.URL = f"{self.fmc.configuration_url}{self.PREFIX_URL}/{acp1.id}/categories"
            else:
                logging.warning(
                    f"Access Control Policy {name} not found.  Cannot set up accessPolicy for Categories."
                )
        else:
            logging.error("No accessPolicy name or ID was provided.")
