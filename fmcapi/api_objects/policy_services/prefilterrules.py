from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from fmcapi.api_objects.policy_services.prefilterpolicies import PreFilterPolicies
from fmcapi.api_objects.object_services.securityzones import SecurityZones
from fmcapi.api_objects.helper_functions import get_networkaddress_type
from fmcapi.api_objects.object_services.fqdns import FQDNS
from fmcapi.api_objects.object_services.networkgroups import NetworkGroups
from fmcapi.api_objects.object_services.networkaddresses import NetworkAddresses
from fmcapi.api_objects.object_services.protocolportobjects import ProtocolPortObjects
from fmcapi.api_objects.object_services.portobjectgroups import PortObjectGroups
from fmcapi.api_objects.object_services.vlangrouptags import VlanTags, VlanGroupTags
import logging


class PreFilterRules(APIClassTemplate):
    """
    The PreFilterRules object in the FMC
    """

    VALID_JSON_DATA = [
        "id",
        "name",
        "action",
        "sourceNetworks",
        "destinationNetworks",
        "sourceInterfaces",
        "destinationInterfaces",
        "sourcePorts",
        "destinationPorts",
        "vlanTags",
        "ruleType",
        "type",
        "enabled",
    ]
    PREFIX_URL = "/policy/prefilterpolicies"
    VALID_FOR_ACTION = ["FASTPATH", "ANALYZE", "BLOCK"]
    VALID_FOR_RULETYPE = ["TUNNEL", "PREFILTER"]
    REQUIRED_FOR_POST = ["prefilter_id"]
    REQUIRED_FOR_GET = ["prefilter_id"]

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for PreFilterRules class.")
        self.type = "PreFilterRules"
        self.prefilter_id = None
        self.prefilter_added_to_url = False
        self.action = "FASTPATH"
        self.parse_kwargs(**kwargs)
        self.URL = f"{self.URL}{self.URL_SUFFIX}"
        self.ruleType = "PREFILTER"
        self.type = "PrefilterRule"
        self.enabled = False

    @property
    def URL_SUFFIX(self):
        """
        Add the URL suffixes for insertBefore and insertAfter
        NOTE: You must specify these at the time of the object is initialized
        for this to work correctly. Example:
            This works:
                new_rule = PreFilterRules(fmc=fmc, prefilter_name='pre1', insertBefore=2)

            This does not:
                new_rule = PreFilterRules(fmc=fmc, prefilter_name='pre1')
                new_rule.insertBefore = 2
        """
        url = "?"
        if "insertBefore" in self.__dict__:
            url = f"{url}insertBefore={self.insertBefore}"
        elif "insertAfter" in self.__dict__:
            url = f"{url}insertAfter={self.insertAfter}"

        return url

    def parse_kwargs(self, **kwargs):
        """
        Parse the kwargs and load into object properties
        Args:
            kwargs (dict): Keyword arguments
        """
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for PreFilterRules class")

        if "prefilter_id" in kwargs:
            self.prefilter(prefilter_id=kwargs["prefilter_id"])
        if "prefilter_name" in kwargs:
            self.prefilter(name=kwargs["prefilter_name"])
        if "action" in kwargs:
            self.validate_action(kwargs["action"])

    def prefilter(self, name=None, prefilter_id=None):
        """
        If the name has been supplied, go and pull the prefilter ID. If ID has been specified, add it to self.
        Also create the URL for prefilter policy
        Args:
            name (str): Prefilter name
            prefilter_id (str): UUID of prefilter
        """
        logging.debug("In prefilter() for PreFilterRules")
        if not name and not prefilter_id:
            logging.warning(f"Unable to find prefilter as no name or ID was specified")

        elif name:
            logging.info(f'Searching ID for prefilter "{name}"')
            pre1 = PreFilterPolicies(fmc=self.fmc)
            pre1.get(name=name)

            if "id" in pre1.__dict__:
                prefilter_id = pre1.id
            else:
                logging.warning(
                    f"Prefilter policy {name} not found. Cannot setup perfilter policy for PreFilterRules"
                )

        self.prefilter_id = prefilter_id
        self.URL = f"{self.fmc.configuration_url}{self.PREFIX_URL}/{self.prefilter_id}/prefilterrules"
        self.prefilter_added_to_url = True

    def validate_action(self, action):
        """
        Checks the provided action is valid and sets property
        Args:
            action (str): Prefilter rule action
        """
        if action in self.VALID_FOR_ACTION:
            self.action = action
        else:
            logging.warning(
                f"Action {action} is not a valid option\nValid actions are: {self.VALID_FOR_ACTION}"
            )

    def source_interface(self, action, name=""):
        """
        Set the source interface (zone) information
        Args:
            action (str): "add" or "remove"
            name (str): Name of interface zone object
        """
        logging.debug("In source_zone() for PreFilterRules class.")
        if action == "clear":
            if "sourceInterfaces" in self.__dict__:
                del self.sourceInterfaces
                logging.info(f"Removed source zone from prefilter rule")

        elif action == "add":
            src_zone_id, src_zone_type = self.get_zone_id(name)
            if src_zone_id:
                self.add_zone("sourceInterfaces", name, src_zone_id, src_zone_type)
            else:
                logging.warning(f'Security zone object "{name}" not found on FMC')

    def destination_interface(self, action, name=""):
        """
        Set the destination interface (zone) information
        Args:
            action (str): "add" or "remove"
            name (str): Name of interface zone object
        """
        logging.debug("In source_zone() for PreFilterRules class.")
        if action == "clear":
            if "sourceZones" in self.__dict__:
                del self.destinationInterfaces
                logging.info(f"Removed source zone from prefilter rule")

        elif action == "add":
            dst_zone_id, dst_zone_type = self.get_zone_id(name)
            if dst_zone_id:
                self.add_zone("destinationInterfaces", name, dst_zone_id, dst_zone_type)
            else:
                logging.warning(f'Security zone object "{name}" not found on FMC')

    def get_zone_id(self, name):
        """
        Pull the ID for a security zone
        Args:
            name (str): Name of interface zone object

        Returns:
            UUID of zone object (str)
        """
        sec_zone = SecurityZones(fmc=self.fmc)
        sec_zone.get(name=name)
        if "id" in sec_zone.__dict__:
            return sec_zone.id, sec_zone.type
        else:
            return None, None

    def add_zone(self, target, name, id, zone_type):
        """
        Check if zone is already on object, skip if it is, add if it isn't and create sourceZone if that object
        attribute doesn't exist at all
        Args:
            target (str): "sourceZones" or "destinationZones"
            name (str): Name of zone object
            id (str): UUID of zone object
            zone_type (str): Security zone type
        """

        if target in self.__dict__:

            # Look through existing zones, if present, for the zone name. Skip if it's already there
            zone_name_duplicate = False
            zone_list = []
            for zone in getattr(self, target)["objects"]:
                zone_list.append(zone)
                if zone["name"] == name:
                    zone_name_duplicate = True

            if not zone_name_duplicate:
                zone_list.append({"name": name, "id": id, "type": zone_type})
                setattr(self, target, {"objects": zone_list})

        # Set the zone if it doesn't exist
        else:
            setattr(
                self, target, {"objects": [{"name": name, "id": id, "type": zone_type}]}
            )

    def source_network(self, action, name=None, literal=None):
        """
        Adds either an object (name) or a literal to sourceNetworks
        Args:
            action (str): Action to be done on this object
            name (str): Object name
            literal (str): Host, network or range

        """
        logging.debug("In source_network() for PreFilterRules class.")
        if literal and name:
            raise ValueError(
                "Adding source literal and object at the same time not supported"
            )
            return

        if not hasattr(self, "sourceNetworks"):
            self.sourceNetworks = {"objects": [], "literals": []}

        if action == "add" and literal:
            literal_type = get_networkaddress_type(literal)
            self.sourceNetworks["literals"].append(
                {"type": literal_type, "value": literal}
            )
            return

        if name:
            new_object = self.find_object(name)

        if not new_object:
            return

        if action == "add":
            # Check if object is already in the list and if not, then add it
            if new_object not in self.sourceNetworks["objects"]:
                logging.info(f'Adding "{name}" to sourceNetworks for prefilter rule')
                self.sourceNetworks["objects"].append(new_object)

        elif action == "remove":
            index = self.sourceNetworks["objects"].index(new_object)
            logging.info(f'Removing "{new_object}" from sourceNetworks')
            self.sourceNetworks["objects"].pop(index)

        elif action == "clear":
            logging.info("Clearing all destination networks")
            del self.destinationNetworks

    def destination_network(self, action, name=None, literal=None):
        """
        Adds either an object (name) or a literal to destinationNetworks
        Args:
            action (str): Action to be done on this object
            name (str): Object name
            literal (str): Host, network or range

        """
        logging.debug("In destination_network() for PreFilterRules class.")
        if literal and name:
            raise ValueError(
                "Adding source literal and object at the same time not supported"
            )
            return

        if not hasattr(self, "destinationNetworks"):
            self.destinationNetworks = {"objects": [], "literals": []}

        if action == "add" and literal:
            literal_type = get_networkaddress_type(literal)
            self.destinationNetworks["literals"].append(
                {"type": literal_type, "value": literal}
            )
            return

        if name:
            new_object = self.find_object(name)

        if not new_object:
            return

        if action == "add":
            # Check if object is already in the list and if not, then add it
            if new_object not in self.destinationNetworks["objects"]:
                logging.info(
                    f'Adding "{name}" to destinationNetworks for prefilter rule'
                )
                self.destinationNetworks["objects"].append(new_object)

        elif action == "remove":
            index = self.destinationNetworks["objects"].index(new_object)
            logging.info(f'Removing "{new_object}" from destinationNetworks')
            self.destinationNetworks["objects"].pop(index)

        elif action == "clear":
            logging.info("Clearing all destination networks")
            del self.destinationNetworks

    def find_object(self, name):
        """
        Search through IP net objects, network group objects and FQDN objects by name
        Args:
            name (str): Name of object
        Returns:
            Object details (dict) or None
        """
        object_id, object_type = self.find_network_object(name)
        if object_id:
            return {"name": name, "id": object_id, "type": object_type}

        object_id, object_type = self.find_group_object(name)
        if object_id:
            return {"name": name, "id": object_id, "type": object_type}

        object_id, object_type = self.find_fqdn_object(name)
        if object_id:
            return {"name": name, "id": object_id, "type": object_type}

        logging.warning(f'Unable to find network object "{name}"')
        return None

    def find_network_object(self, name):
        """
        Search for network object by name
        Args:
            name (str): Name of network object
        Returns:
            id (str), type (str) or None None
        """
        network_object = NetworkAddresses(fmc=self.fmc, name=name)
        resp = network_object.get()

        return self._return_id_type(resp)

    def find_group_object(self, name):
        """
        Search for group object by name
        Args:
            name (str): Name of group object
        Returns:
            id (str), type (str) or None None
        """
        group_object = NetworkGroups(fmc=self.fmc, name=name)
        resp = group_object.get()

        return self._return_id_type(resp)

    def find_fqdn_object(self, name):
        """
        Search for group object by name
        Args:
            name (str): Name of group object
        Returns:
            id (str), type (str) or None None
        """
        fqdn_object = FQDNS(fmc=self.fmc, name=name)
        resp = fqdn_object.get()

        return self._return_id_type(resp)

    @staticmethod
    def _return_id_type(resp):
        """
        Check dict for ID and return ID and type if present
        Args:
            resp (dict): Response from NetworkGroup, NetworkAddress or FQDNS GET
        Returns:
            Returns:
            id (str), type (str) or None None
        """
        if "id" in resp.keys():
            return resp["id"], resp["type"]
        else:
            return None, None

    def rule_type(self, rule_type):
        """
        Set the rule type attribute
        Args:
            rule_type (str): PREFITLER or TUNNEL
        """
        if rule_type in self.VALID_FOR_RULETYPE:
            self.ruleType = rule_type
        else:
            logging.warning(
                f'Rule type "{rule_type}" is not valid. Must be "PREFILTER" or "TUNNEL"'
            )

    def source_port(self, action, name=None, literal=None):
        """
        Create the source protocol and ports
        Args:
            action (str): Add, delete or clear
            name (str): Name of port object
            literal (dict): Dictionary of protocol and port expressed as integers
        """
        logging.debug("In source_port for PreFilterRules")

        if literal and name:
            raise ValueError(
                "Adding source literal and object at the same time not supported"
            )
            return

        if not hasattr(self, "sourcePorts"):
            self.sourcePorts = {"literals": [], "objects": []}

        if action == "add" and literal:
            if self._port_literal_verify(literal):
                literal["type"] = "PortLiteral"
                self.sourcePorts["literals"].append(literal)
            return

        if name:
            port_object = self._find_port_object(name)

        if not port_object:
            return

        if action == "add":
            if port_object not in self.sourcePorts["objects"]:
                logging.info(f'Adding "{port_object}" to sourcePorts')
                self.sourcePorts["objects"].append(port_object)

        elif action == "remove":
            index = self.sourcePorts["objects"].index(port_object)
            logging.info(f'Removing "{port_object}" from sourcePorts')
            self.sourcePorts["objects"].pop(index)

        elif action == "clear":
            del self.sourcePorts

    def destination_port(self, action, name=None, literal=None):
        """
        Create the destination protocol and ports
        Args:
            action (str): Add, delete or clear
            name (str): Name of port object
            literal (dict): Dictionary of protocol and port expressed as integers
        """
        logging.debug("In destination_port for PreFilterRules")

        if literal and name:
            raise ValueError(
                "Adding destination literal and object at the same time not supported"
            )
            return

        if not hasattr(self, "destinationPorts"):
            self.destinationPorts = {"literals": [], "objects": []}

        if action == "add" and literal:
            if self._port_literal_verify(literal):
                literal["type"] = "PortLiteral"
                self.destinationPorts["literals"].append(literal)
            return

        if name:
            port_object = self._find_port_object(name)

        if not port_object:
            return

        if action == "add":
            if port_object not in self.destinationPorts["objects"]:
                logging.info(f'Adding "{port_object}" to destinationPorts')
                self.destinationPorts["objects"].append(port_object)

        elif action == "remove":
            index = self.destinationPorts["objects"].index(port_object)
            logging.info(f'Removing "{port_object}" from destinationPorts')
            self.destinationPorts["objects"].pop(index)

        elif action == "clear":
            del self.destinationPorts

    def _find_port_object(self, name):
        """
        Find port object or port group object and return dictionary
        Args:
            name (str): Name of port object/port group object
        Returns:
            Dictionary of port object
        """
        protocol_port = ProtocolPortObjects(fmc=self.fmc, name=name)
        resp = protocol_port.get()
        if "id" in resp.keys():
            return {"name": name, "id": resp["id"], "type": resp["type"]}

        protocol_port_group = PortObjectGroups(fmc=self.fmc, name=name)
        resp = protocol_port_group.get()
        if "id" in resp.keys():
            return {"name": name, "id": resp["id"], "type": resp["type"]}

        logging.warning(f'Unable to find port object "{name}"')
        return None

    @staticmethod
    def _port_literal_verify(literal):
        """
        Ensure that the literal is expressed as integers. It's too hard dealing with named protocols/ports.
        Also check that protocol and ports keys are in the dictionary
        Args:
            literal (dict): Dictionary with protocol and ports
        Returns:
            Bool
        """
        if not isinstance(literal, dict):
            logging.warning(
                'Invalid port literal. Must be defined as a dictionary: "{"protocol": <protocol>, "port": <port}'
            )
            return False

        if "protocol" not in literal.keys() and "port" not in literal.keys():
            logging.warning(
                '"protocol" and/or "port" missing from literal. You must specify both'
            )
            return False

        return True

    def vlan_tags(self, action, name=None, literal=None):
        """
        Add, remove or clear VLAN tags
        Args:
            action (str): Add, remove or clear
            name (str): Name of VLAN tag object
            literal (str): VLAN tag or range
        """
        logging.debug("In vlan_tags() for PreFilterRules")
        if literal and name:
            raise ValueError(
                "Adding/Removing VLAN literal and object at the same time not supported"
            )
            return

        if not hasattr(self, "vlanTags"):
            self.vlanTags = {"literals": [], "objects": []}

        if action == "add" and literal:
            start_vlan, end_vlan = self._vlan_tag_check(literal)
            self.vlanTags["literals"].append(
                {"startTag": start_vlan, "endTag": end_vlan, "type": "VlanTagLiteral"}
            )
            return

        if name:
            vlan_object = self._find_vlan_object(name)

        if not vlan_object:
            return

        if action == "add":
            if vlan_object not in self.vlanTags["objects"]:
                self.vlanTags["objects"].append(vlan_object)

        if action == "remove":
            index = self.vlanTags["objects"].index(vlan_object)
            logging.info(f'Removing "{vlan_object}" from vlanTags')
            self.vlanTags["objects"].pop(index)

        elif action == "clear":
            del self.vlanTags

    @staticmethod
    def _vlan_tag_check(literal):
        """
        Check if the VLAN tag literal is a range or not and returns start and end tag number
        Args:
            literal (str): VLAN tag literal
        Returns:
            start_vlan (str), end_vlan (str)
        """
        if "-" in literal:
            vlans = literal.strip("-")
            return vlans[0], vlans[1]
        else:
            return literal, literal

    def _find_vlan_object(self, name):
        """
        Find the vlan or vlan group object by name
        Args:
            name (str): Object name
        """
        vlan_object = VlanTags(fmc=self.fmc, name=name)
        resp = vlan_object.get()
        if "id" in resp.keys():
            return {"name": name, "id": resp["id"], "type": resp["type"]}

        vlan_object = VlanGroupTags(fmc=self.fmc, name=name)
        resp = vlan_object.get()
        if "id" in resp.keys():
            return {"name": name, "id": resp["id"], "type": resp["type"]}

        logging.warning(f'Unable to find vlan object "{name}"')
        return None
