"""Auto NAT Rules class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .ftdnatpolicies import FTDNatPolicies
from fmcapi.api_objects.object_services.networkaddresses import NetworkAddresses
from fmcapi.api_objects.object_services.interfaceobjects import InterfaceObjects
from fmcapi.api_objects.object_services.networkgroups import NetworkGroups
import logging


class AutoNatRules(APIClassTemplate):
    """The AutoNatRules Object in the FMC."""

    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
        "originalNetwork",
        "translatedNetwork",
        "interfaceInTranslatedNetwork",
        "natType",
        "interfaceIpv6",
        "fallThrough",
        "dns",
        "routeLookup",
        "noProxyArp",
        "netToNet",
        "sourceInterface",
        "destinationInterface",
        "originalPort",
        "translatedPort",
        "serviceProtocol",
        "patOptions",
        "description",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    PREFIX_URL = "/policy/ftdnatpolicies"
    REQUIRED_FOR_POST = ["nat_id"]

    def __init__(self, fmc, **kwargs):
        """
        Initialize AutoNatRules object.

        Set self.type to "FTDAutoNatRule" and parse the kwargs.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for AutoNatRules class.")
        self.parse_kwargs(**kwargs)
        self.type = "FTDAutoNatRule"

    def parse_kwargs(self, **kwargs):
        """
        Parse the kwargs and set self variables to match.

        :return: None
        """
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for AutoNatRules class.")
        if ("translatedNetwork" in kwargs) and ("interfaceInTranslatedNetwork" is True):
            logging.warning(
                "Cannot have both a translatedNetwork and interfaceInTranslatedNetwork"
            )
        elif "translatedNetwork" in kwargs:
            self.translatedNetwork = kwargs["translatedNetwork"]
        elif "interfaceInTranslatedNetwork" in kwargs:
            self.interfaceInTranslatedNetwork = kwargs["interfaceInTranslatedNetwork"]

    def nat_policy(self, name):
        """
        Associate NAT Policy with this rule.

        :param name: (str) Name of NAT Policy.
        :return: None
        """
        logging.debug("In nat_policy() for AutoNatRules class.")
        ftd_nat = FTDNatPolicies(fmc=self.fmc)
        ftd_nat.get(name=name)
        if "id" in ftd_nat.__dict__:
            self.nat_id = ftd_nat.id
            self.URL = f"{self.fmc.configuration_url}{self.PREFIX_URL}/{self.nat_id}/autonatrules"
            self.nat_added_to_url = True
        else:
            logging.warning(
                f"FTD NAT Policy {name} not found.  Cannot set up AutoNatRule for NAT Policy."
            )

    def original_network(self, name):
        """
        Associate Network with this rule.

        :param name: (str) Name of Network.
        :return: None
        """
        logging.debug("In original_network() for AutoNatRules class.")
        ipaddresses_json = NetworkAddresses(fmc=self.fmc).get()
        items = ipaddresses_json.get("items", [])
        new_net = None
        for item in items:
            if item["name"] == name:
                new_net = {"id": item["id"], "type": item["type"]}
                break
        if new_net is None:
            logging.warning(
                f'Network "{name}" is not found in FMC.  Cannot add to originalNetwork.'
            )
        else:
            self.originalNetwork = new_net
            logging.info(f'Adding "{name}" to sourceNetworks for this AutoNatRule.')

    def translated_network(self, name):
        """
        Associate Network to this rule.

        :param name: (str) Name of Network.
        :return: None
        """
        # Auto Nat rules can't use network group objects
        logging.debug("In translated_network() for AutoNatRules class.")
        ipaddresses_json = NetworkAddresses(fmc=self.fmc).get()
        items = ipaddresses_json.get("items", [])
        new_net = None
        for item in items:
            if item["name"] == name:
                new_net = {"id": item["id"], "type": item["type"]}
                break
        if new_net is None:
            logging.warning(
                f'Network "{name}" is not found in FMC.  Cannot add to translatedNetwork.'
            )
        else:
            self.translatedNetwork = new_net
            logging.info(
                f'Adding "{name}" to destinationNetworks for this AutoNatRule.'
            )

    def source_intf(self, name):
        """
        Associate interface to this rule.

        :param name: (str) Name of interface.
        :return: None
        """
        logging.debug("In source_intf() for AutoNatRules class.")
        intf_obj = InterfaceObjects(fmc=self.fmc).get()
        items = intf_obj.get("items", [])
        new_intf = None
        for item in items:
            if item["name"] == name:
                new_intf = {"id": item["id"], "type": item["type"]}
                break
        if new_intf is None:
            logging.warning(
                f'Interface Object "{name}" is not found in FMC.  Cannot add to sourceInterface.'
            )
        else:
            if new_intf["type"] == "InterfaceGroup" and len(new_intf.interfaces) > 1:
                logging.warning(
                    f'Interface Object "{name}" contains more than one physical interface. Cannot add to '
                    f"sourceInterface."
                )
            else:
                self.sourceInterface = new_intf
                logging.info(f'Interface Object "{name}" added to NAT Policy.')

    def destination_intf(self, name):
        """
        Associate interface to this rule.

        :param name: (str) Name of interface.
        :return: None
        """
        logging.debug("In destination_intf() for AutoNatRules class.")
        intf_obj = InterfaceObjects(fmc=self.fmc).get()
        items = intf_obj.get("items", [])
        new_intf = None
        for item in items:
            if item["name"] == name:
                new_intf = {"id": item["id"], "type": item["type"]}
                break
        if new_intf is None:
            logging.warning(
                f'Interface Object "{name}" is not found in FMC.  Cannot add to destinationInterface.'
            )
        else:
            if new_intf["type"] == "InterfaceGroup" and len(new_intf.interfaces) > 1:
                logging.warning(
                    f'Interface Object "{name}" contains more than one physical interface. Cannot add to '
                    f"destinationInterface."
                )
            else:
                self.destinationInterface = new_intf
                logging.info(f'Interface Object "{name}" added to NAT Policy.')

    def identity_nat(self, name):
        """
        Associate Network to this rule.

        :param name: (str) Name of Network.
        :return: None
        """
        logging.debug("In identity_nat() for AutoNatRules class.")
        ipaddresses_json = NetworkAddresses(fmc=self.fmc).get()
        items = ipaddresses_json.get("items", [])
        new_net = None
        for item in items:
            if item["name"] == name:
                new_net = {"id": item["id"], "type": item["type"]}
                break
        if new_net is None:
            logging.warning(
                f'Network "{name}" is not found in FMC.  Cannot add to this AutoNatRule.'
            )
        else:
            self.natType = "STATIC"
            self.originalNetwork = new_net
            self.translatedNetwork = new_net
            logging.info(f'Adding "{name}" to AutoNatRule.')

    def patPool(self, name, options={}):
        """
        Associate a PAT Pool with this rule.

        :param name: (str) Name of PAT Pool.
        :param options: (dict) Dictionary of options.
        :return: None
        """
        # Network Group Object permitted for patPool
        ipaddresses_json = NetworkAddresses(fmc=self.fmc).get()
        networkgroup_json = NetworkGroups(fmc=self.fmc).get()
        items = ipaddresses_json.get("items", []) + networkgroup_json.get("items", [])
        new_net = None
        for item in items:
            if item["name"] == name:
                new_net = {"name": item["name"], "id": item["id"], "type": item["type"]}
                break
        if new_net is None:
            logging.warning(
                f'Network "{name}" is not found in FMC.  Cannot add to patPool.'
            )
        else:
            self.natType = "DYNAMIC"
            self.patOptions = {"patPoolAddress": new_net}
            self.patOptions["interfacePat"] = (
                options.interfacePat if "interfacePat" in options.keys() else False
            )
            self.patOptions["includeReserve"] = (
                options.includeReserve if "includeReserve" in options.keys() else False
            )
            self.patOptions["roundRobin"] = (
                options.roundRobin if "roundRobin" in options.keys() else True
            )
            self.patOptions["extendedPat"] = (
                options.extendedPat if "extendedPat" in options.keys() else False
            )
            self.patOptions["flatPortRange"] = (
                options.flatPortRange if "flatPortRange" in options.keys() else False
            )
            logging.info(f'Adding "{name}" to patPool for this AutoNatRule.')
