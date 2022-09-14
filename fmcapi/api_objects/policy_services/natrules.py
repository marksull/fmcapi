"""NAT Rules Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .ftdnatpolicies import FTDNatPolicies
import logging


class NatRules(APIClassTemplate):
    """The NatRules Object in the FMC."""

    VALID_JSON_DATA = ["id", "name", "type"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    PREFIX_URL = "/policy/ftdnatpolicies"
    REQUIRED_FOR_GET = []
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        """
        Initialize NatRules object.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for NatRules class.")
        self.parse_kwargs(**kwargs)

    def nat_policy(self, name=None, id=None):
        """
        Associate NAT Policy.

        :param name: (str) Name of NAT Policy.
        :param id: (str) ID of NAT Policy.
        :return: None
        """
        logging.debug("In nat_policy() for NatRules class.")
        if id:
            self.URL = f"{self.fmc.configuration_url}{self.PREFIX_URL}/{id}/natrules"
            self.nat_added_to_url = True
        elif name:
            ftd_nat = FTDNatPolicies(fmc=self.fmc)
            ftd_nat.get(name=name)
            if "id" in ftd_nat.__dict__:
                self.URL = f"{self.fmc.configuration_url}{self.PREFIX_URL}/{ftd_nat.id}/natrules"
                self.nat_added_to_url = True
            else:
                logging.warning(
                    f"FTD NAT Policy {name} not found.  Cannot set up NatRules for NAT Policy."
                )
        else:
            logging.error("No NatRules name or ID was provided.")

    def parse_kwargs(self, **kwargs):
        """
        Parse the kwargs and set self variables to match.

        :return: None
        """
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for NatRules class.")
        if "nat_id" in kwargs:
            self.nat_policy(id=kwargs["nat_id"])
        elif "nat_name" in kwargs:
            self.nat_policy(name=kwargs["nat_name"])
        elif "name" in kwargs:
            self.nat_policy(name=kwargs["name"])

    def post(self):
        """POST method for API for NatRules not supported."""
        logging.info("POST method for API for NatRules not supported.")
        pass

    def put(self):
        """PUT method for API for NatRules not supported."""
        logging.info("PUT method for API for NatRules not supported.")
        pass

    def delete(self):
        """DELETE method for API for NatRules not supported."""
        logging.info("DELETE method for API for NatRules not supported.")
        pass
