from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from fmcapi.api_objects.policy_services.prefilterpolicies import PreFilterPolicies
from fmcapi.api_objects.object_services.securityzones import SecurityZones
from fmcapi.api_objects.helper_functions import get_networkaddress_type
from fmcapi.api_objects.object_services.fqdns import FQDNS
from fmcapi.api_objects.object_services.networkgroups import NetworkGroups
from fmcapi.api_objects.object_services.networkaddresses import NetworkAddresses
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

        if not hasattr(self, "sourceNetworks"):
            self.sourceNetworks = {"objects": [], "literals": []}

        if action == "add" and literal:
            literal_type = get_networkaddress_type(literal)
            self.sourceNetworks["literals"].append(
                {"type": literal_type, "value": literal}
            )

        elif action == "add" and name:
            new_object = self.find_object(name)

            # Check if object is already in the list and if not, then add it
            if new_object and new_object not in self.sourceNetworks["objects"]:
                logging.info(f'Adding "{name}" to sourceNetworks for prefilter rule')
                self.sourceNetworks["objects"].append(new_object)

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

        if not hasattr(self, "destinationNetworks"):
            self.destinationNetworks = {"objects": [], "literals": []}

        if action == "add" and literal:
            literal_type = get_networkaddress_type(literal)
            self.destinationNetworks["literals"].append(
                {"type": literal_type, "value": literal}
            )

        elif action == "add" and name:
            new_object = self.find_object(name)

            # Check if object is already in the list and if not, then add it
            if new_object and new_object not in self.destinationNetworks["objects"]:
                logging.info(
                    f'Adding "{name}" to destinationNetworks for prefilter rule'
                )
                self.destinationNetworks["objects"].append(new_object)

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
