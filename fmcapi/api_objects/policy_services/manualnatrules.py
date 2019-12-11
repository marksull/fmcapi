"""Manual NAT Rules Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .ftdnatpolicies import FTDNatPolicies
from fmcapi.api_objects.object_services.networkaddresses import NetworkAddresses
from fmcapi.api_objects.object_services.networkgroups import NetworkGroups
from fmcapi.api_objects.object_services.portobjectgroups import PortObjectGroups
from fmcapi.api_objects.object_services.protocolportobjects import ProtocolPortObjects
from fmcapi.api_objects.object_services.interfaceobjects import InterfaceObjects
import logging


class ManualNatRules(APIClassTemplate):
    # Host,Network,NetworkGroup objects
    """The ManualNatRules Object in the FMC."""

    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
        "originalSource",
        "originalDestination",
        "translatedSource",
        "translatedDestination",
        "interfaceInTranslatedSource",
        "interfaceInOriginalDestination",
        "natType",
        "interfaceIpv6",
        "fallThrough",
        "dns",
        "routeLookup",
        "noProxyArp",
        "netToNet",
        "sourceInterface",
        "destinationInterface",
        "originalSourcePort",
        "translatedSourcePort",
        "originalDestinationPort",
        "translatedDestinationPort",
        "patOptions",
        "unidirectional",
        "enabled",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    PREFIX_URL = "/policy/ftdnatpolicies"
    REQUIRED_FOR_POST = ["nat_id"]

    def __init__(self, fmc, **kwargs):
        """
        Initialize ManualNatRules object.

        Set self.type to "ManualNatRules" and parse the kwargs.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ManualNatRules class.")
        self.parse_kwargs(**kwargs)
        self.type = "FTDManualNatRule"

    def parse_kwargs(self, **kwargs):
        """
        Parse the kwargs and set self variables to match.

        :return: None
        """
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for ManualNatRules class.")
        if "translatedSource" in kwargs and "interfaceInTranslatedSource" is True:
            logging.warning(
                "Cannot have both a translatedSource and interfaceInTranslatedSource"
            )
        elif "translatedSource" in kwargs:
            self.translatedSource = kwargs["translatedSource"]
        elif "interfaceInTranslatedSource" in kwargs:
            self.interfaceInTranslatedSource = kwargs["interfaceInTranslatedSource"]

    def nat_policy(self, name):
        """
        Associate NAT Policy.

        :param name: (str) Name of NAT Policy.
        :return: None
        """
        logging.debug("In nat_policy() for ManualNatRules class.")
        ftd_nat = FTDNatPolicies(fmc=self.fmc)
        ftd_nat.get(name=name)
        if "id" in ftd_nat.__dict__:
            self.nat_id = ftd_nat.id
            self.URL = f"{self.fmc.configuration_url}{self.PREFIX_URL}/{self.nat_id}/manualnatrules"
            self.nat_added_to_url = True
        else:
            logging.warning(
                f'FTD NAT Policy "{name}" not found.  Cannot set up ManualNatRule for NAT Policy.'
            )

    def original_source(self, name):
        """
        Associate Network to be used as Original Source.

        :param name: (str) Name of Network.
        :return: None
        """
        logging.debug("In original_source() for ManualNatRules class.")
        ipaddresses_json = NetworkAddresses(fmc=self.fmc).get()
        networkgroup_json = NetworkGroups(
            fmc=self.fmc
        ).get()  # FIXME, shouldn't this be a part of items?
        items = ipaddresses_json.get("items", [])
        new_net = None
        for item in items:
            if item["name"] == name:
                new_net = {"id": item["id"], "type": item["type"]}
                break
        if new_net is None:
            logging.warning(
                f'Network "{name}" is not found in FMC.  Cannot add to original_source.'
            )
        else:
            self.originalSource = new_net
            logging.info(f'Adding "{name}" to original_source for this ManualNatRule.')

    def translated_source(self, name):
        """
        Associate Network to be used as Translated Source.

        :param name: (str) Name of Network.
        :return: None
        """
        logging.debug("In translated_source() for ManualNatRules class.")
        ipaddresses_json = NetworkAddresses(fmc=self.fmc).get()
        networkgroup_json = NetworkGroups(
            fmc=self.fmc
        ).get()  # FIXME, shouldn't this be a part of items?
        items = ipaddresses_json.get("items", [])
        new_net = None
        for item in items:
            if item["name"] == name:
                new_net = {"id": item["id"], "type": item["type"]}
                break
        if new_net is None:
            logging.warning(
                f'Network "{name}" is not found in FMC.  Cannot add to translated_source.'
            )
        else:
            self.translatedSource = new_net
            logging.info(
                f'Adding "{name}" to translated_source for this ManualNatRule.'
            )

    def original_destination(self, name):
        """
        Associate Network to be used as Original Destination.

        :param name: (str) Name of Network.
        :return: None
        """
        logging.debug("In original_destination() for ManualNatRules class.")
        ipaddresses_json = NetworkAddresses(fmc=self.fmc).get()
        networkgroup_json = NetworkGroups(
            fmc=self.fmc
        ).get()  # FIXME, shouldn't this be a part of items?
        items = ipaddresses_json.get("items", [])
        new_net = None
        for item in items:
            if item["name"] == name:
                new_net = {"id": item["id"], "type": item["type"]}
                break
        if new_net is None:
            logging.warning(
                f'Network "{name}" is not found in FMC.  Cannot add to original_destination.'
            )
        else:
            self.originalDestination = new_net
            logging.info(
                f'Adding "{name}" to original_destination for this ManualNatRule.'
            )

    def translated_destination(self, name):
        """
        Associate Network to be used as Translated Destination.

        :param name: (str) Name of Network.
        :return: None
        """
        logging.debug("In translated_destination() for ManualNatRules class.")
        ipaddresses_json = NetworkAddresses(fmc=self.fmc).get()
        networkgroup_json = NetworkGroups(
            fmc=self.fmc
        ).get()  # FIXME, shouldn't this be a part of items?
        items = ipaddresses_json.get("items", [])
        new_net = None
        for item in items:
            if item["name"] == name:
                new_net = {"id": item["id"], "type": item["type"]}
                break
        if new_net is None:
            logging.warning(
                f'Network "{name}" is not found in FMC.  Cannot add to translated_destination.'
            )
        else:
            self.translatedDestination = new_net
            logging.info(
                f'Adding "{name}" to translated_destination for this ManualNatRule.'
            )

    def original_source_port(self, name):
        """
        Associate Port to be used as Origin Source port.

        :param name: (str) Name of Port.
        :return: None
        """
        logging.debug("In original_source_port() for ManualNatRules class.")
        ports_json = ProtocolPortObjects(fmc=self.fmc).get()
        portgroup_json = PortObjectGroups(fmc=self.fmc).get()
        items = ports_json.get("items", []) + portgroup_json.get("items", [])
        new_port = None
        for item in items:
            if item["name"] == name:
                new_port = {"id": item["id"], "type": item["type"]}
                break
        if new_port is None:
            logging.warning(
                f'Port "{name}" is not found in FMC.  Cannot add to original_source_port.'
            )
        else:
            self.originalSourcePort = new_port
            logging.info(
                f'Adding "{name}" to original_source_port for this ManualNatRule.'
            )

    def translated_source_port(self, name):
        """
        Associate Port to be used as Translated Source port.

        :param name: (str) Name of Port.
        :return: None
        """
        logging.debug("In translated_source_port() for ManualNatRules class.")
        ports_json = ProtocolPortObjects(fmc=self.fmc).get()
        portgroup_json = PortObjectGroups(fmc=self.fmc).get()
        items = ports_json.get("items", []) + portgroup_json.get("items", [])
        new_port = None
        for item in items:
            if item["name"] == name:
                new_port = {"id": item["id"], "type": item["type"]}
                break
        if new_port is None:
            logging.warning(
                f'Port "{name}" is not found in FMC.  Cannot add to translated_source_port.'
            )
        else:
            self.translatedSourcePort = new_port
            logging.info(
                f'Adding "{name}" to translated_source_port for this ManualNatRule.'
            )

    def original_destination_port(self, name):
        """
        Associate Port to be used as Origin Destination port.

        :param name: (str) Name of Port.
        :return: None
        """
        logging.debug("In original_destination_port() for ManualNatRules class.")
        ports_json = ProtocolPortObjects(fmc=self.fmc).get()
        portgroup_json = PortObjectGroups(fmc=self.fmc).get()
        items = ports_json.get("items", []) + portgroup_json.get("items", [])
        new_port = None
        for item in items:
            if item["name"] == name:
                new_port = {"id": item["id"], "type": item["type"]}
                break
        if new_port is None:
            logging.warning(
                f'Port "{name}" is not found in FMC.  Cannot add to original_destination_port.'
            )
        else:
            self.originalDestinationPort = new_port
            logging.info(
                f'Adding "{name}" to original_destination_port for this ManualNatRule.'
            )

    def translated_destination_port(self, name):
        """
        Associate Port to be used as Destination port.

        :param name: (str) Name of Port.
        :return: None
        """
        logging.debug("In translated_destination_port() for ManualNatRules class.")
        ports_json = ProtocolPortObjects(fmc=self.fmc).get()
        portgroup_json = PortObjectGroups(fmc=self.fmc).get()
        items = ports_json.get("items", []) + portgroup_json.get("items", [])
        new_port = None
        for item in items:
            if item["name"] == name:
                new_port = {"id": item["id"], "type": item["type"]}
                break
        if new_port is None:
            logging.warning(
                f'Port "{name}" is not found in FMC.  Cannot add to translated_destination_port.'
            )
        else:
            self.translatedDestinationPort = new_port
            logging.info(
                f'Adding "{name}" to translated_destination_port for this ManualNatRule.'
            )

    def source_intf(self, name):
        """
        Associate source interface.

        :param name: (str) Name of interface.
        :return: None
        """
        logging.debug("In source_intf() for ManualNatRules class.")
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
            self.sourceInterface = new_intf
            logging.info(f'Interface Object "{name}" added to NAT Policy.')

    def destination_intf(self, name):
        """
        Associate destination interface.

        :param name: (str) Name of interface.
        :return: None
        """
        logging.debug("In destination_intf() for ManualNatRules class.")
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
            self.destinationInterface = new_intf
            logging.info(f'Interface Object "{name}" added to NAT Policy.')

    def identity_nat(self, name):
        """
        Associate an Identity Network.

        :param name: (str) Name of Network.
        :return: None
        """
        logging.debug("In identity_nat() for ManualNatRules class.")
        ipaddresses_json = NetworkAddresses(fmc=self.fmc).get()
        networkgroup_json = NetworkGroups(fmc=self.fmc).get()
        items = ipaddresses_json.get("items", []) + networkgroup_json.get("items", [])
        new_net = None
        for item in items:
            if item["name"] == name:
                new_net = {"id": item["id"], "type": item["type"]}
                break
        if new_net is None:
            logging.warning(
                f'Network "{name}" is not found in FMC.  Cannot add to this ManualNatRules.'
            )
        else:
            self.natType = "STATIC"
            self.originalSource = new_net
            self.translatedSource = new_net
            logging.info(f'Adding "{name}" to ManualNatRules.')

    def patPool(self, name, options={}):
        """
        Associate a PAT Pool.

        :param name: (str) Name of PAT Pool.
        :param options: (dict) key/value of options.
        :return: None
        """
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
            self.unidirectional = True
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
            logging.info(f'Adding "{name}" to patPool for this ManualNatRule.')
