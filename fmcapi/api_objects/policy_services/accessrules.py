"""Access Rules Classes."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from fmcapi.api_objects.policy_services.accesspolicies import AccessPolicies
from fmcapi.api_objects.policy_services.intrusionpolicies import IntrusionPolicies
from fmcapi.api_objects.object_services.variablesets import VariableSets
from fmcapi.api_objects.object_services.securityzones import SecurityZones
from fmcapi.api_objects.object_services.vlantags import VlanTags
from fmcapi.api_objects.object_services.portobjectgroups import PortObjectGroups
from fmcapi.api_objects.object_services.protocolportobjects import ProtocolPortObjects
from fmcapi.api_objects.object_services.icmpv4objects import ICMPv4Objects
from fmcapi.api_objects.object_services.fqdns import FQDNS
from fmcapi.api_objects.object_services.networkgroups import NetworkGroups
from fmcapi.api_objects.object_services.networkaddresses import NetworkAddresses
from fmcapi.api_objects.policy_services.filepolicies import FilePolicies
from fmcapi.api_objects.object_services.isesecuritygrouptags import ISESecurityGroupTags
from fmcapi.api_objects.helper_functions import (
    get_networkaddress_type,
    true_false_checker,
)
from fmcapi.api_objects.object_services.applications import Applications
from fmcapi.api_objects.object_services.applicationfilters import ApplicationFilters
from fmcapi.api_objects.object_services.urlgroups import URLGroups
from fmcapi.api_objects.object_services.urls import URLs
from fmcapi.api_objects.object_services.realmusergroups import RealmUserGroups
from fmcapi.api_objects.object_services.realmusers import RealmUsers
import logging
import sys


class AccessRules(APIClassTemplate):
    """
    The AccessRules Object in the FMC.
    """

    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
        "action",
        "enabled",
        "sendEventsToFMC",
        "logFiles",
        "logBegin",
        "logEnd",
        "variableSet",
        "originalSourceNetworks",
        "vlanTags",
        "users",
        "sourceNetworks",
        "destinationNetworks",
        "sourcePorts",
        "destinationPorts",
        "ipsPolicy",
        "urls",
        "sourceZones",
        "destinationZones",
        "applications",
        "filePolicy",
        "sourceSecurityGroupTags",
        "destinationSecurityGroupTags",
        "enableSyslog",
        "newComments",
        "commentHistoryList",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + [
        "acp_id",
        "acp_name",
        "insertBefore",
        "insertAfter",
        "section",
        "category",
    ]
    PREFIX_URL = "/policy/accesspolicies"
    REQUIRED_FOR_POST = ["name", "acp_id"]
    REQUIRED_FOR_GET = ["acp_id"]
    VALID_FOR_ACTION = [
        "ALLOW",
        "TRUST",
        "BLOCK",
        "MONITOR",
        "BLOCK_RESET",
        "BLOCK_INTERACTIVE",
        "BLOCK_RESET_INTERACTIVE",
    ]
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\-<>, ]"""

    @property
    def URL_SUFFIX(self):
        """
        Add the URL suffixes for categories, insertBefore and insertAfter
        NOTE: You must specify these at the time the object is initialized (created) for this feature
        to work correctly. Example:
            This works:
                new_rule = AccessRules(fmc=fmc, acp_name='acp1', insertBefore=2)

            This does not:
                new_rule = AccessRules(fmc=fmc, acp_name='acp1')
                new_rule.insertBefore = 2
        """
        url = "?"

        if "category" in self.__dict__:
            url = f"{url}category={self.category}&"
        if "insertBefore" in self.__dict__:
            url = f"{url}insertBefore={self.insertBefore}&"
        if "insertAfter" in self.__dict__:
            url = f"{url}insertAfter={self.insertAfter}&"
        if "insertBefore" in self.__dict__ and "insertAfter" in self.__dict__:
            logging.warning("ACP rule has both insertBefore and insertAfter params")
        if "section" in self.__dict__:
            url = f"{url}section={self.section}&"

        return url[:-1]

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value=False):
        self._enabled = true_false_checker(value)

    @property
    def logBegin(self):
        return self._logBegin

    @logBegin.setter
    def logBegin(self, value=False):
        self._logBegin = true_false_checker(value)

    @property
    def logEnd(self):
        return self._logEnd

    @logEnd.setter
    def logEnd(self, value=False):
        self._logEnd = true_false_checker(value)

    @property
    def sendEventsToFMC(self):
        return self._sendEventsToFMC

    @sendEventsToFMC.setter
    def sendEventsToFMC(self, value=False):
        self._sendEventsToFMC = true_false_checker(value)

    @property
    def enableSyslog(self):
        return self._enableSyslog

    @enableSyslog.setter
    def enableSyslog(self, value=False):
        self._enableSyslog = true_false_checker(value)

    @property
    def newComments(self):
        return self._newComments

    @property
    def commentHistoryList(self):
        return self._commentHistoryList

    def __init__(self, fmc, **kwargs):
        """
        Initialize AccessRules object.

        Set self.type to "AccessRule", parse the kwargs, and set up the self.URL.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for AccessRules class.")
        self.type = "AccessRule"
        self._enabled = False
        self._logBegin = False
        self._logEnd = False
        self._sendEventsToFMC = False
        self._enableSyslog = False
        self._newComments = []
        self._commentHistoryList = []
        self.parse_kwargs(**kwargs)
        self.URL = f"{self.URL}{self.URL_SUFFIX}"

    def format_data(self, filter_query=""):
        """
        Gather all the data in preparation for sending to API in JSON format.

        :param filter_query: (str) 'all' or 'kwargs'
        :return: (dict) json_data
        """
        json_data = super().format_data(filter_query=filter_query)
        logging.debug("In format_data() for AccessRules class.")
        if "sourceNetworks" in self.__dict__:
            json_data["sourceNetworks"] = {"objects": self.sourceNetworks["objects"]}
            json_data["sourceNetworks"]["literals"] = [
                {"type": v, "value": k}
                for k, v in self.sourceNetworks["literals"].items()
            ]
        if "destinationNetworks" in self.__dict__:
            json_data["destinationNetworks"] = {
                "objects": self.destinationNetworks["objects"]
            }
            json_data["destinationNetworks"]["literals"] = [
                {"type": v, "value": k}
                for k, v in self.destinationNetworks["literals"].items()
            ]
        if "action" in self.__dict__:
            if self.action not in self.VALID_FOR_ACTION:
                logging.warning(f"Action {self.action} is not a valid action.")
                logging.warning(f"\tValid actions are: {self.VALID_FOR_ACTION}.")
        return json_data

    def parse_kwargs(self, **kwargs):
        """
        Parse the kwargs and set self variables to match.

        :return: None
        """
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for AccessRules class.")
        if "acp_id" in kwargs:
            self.acp(id=kwargs["acp_id"])
        if "acp_name" in kwargs:
            self.acp(name=kwargs["acp_name"])
        if "action" in kwargs:
            if kwargs["action"] in self.VALID_FOR_ACTION:
                self.action = kwargs["action"]
            else:
                logging.warning(f"Action {kwargs['action']} is not a valid action.")
                logging.warning(f"\tValid actions are: {self.VALID_FOR_ACTION}.")
        if "sourceNetworks" in kwargs:
            self.sourceNetworks = {"objects": [], "literals": {}}
            if kwargs["sourceNetworks"].get("objects"):
                self.sourceNetworks["objects"] = kwargs["sourceNetworks"]["objects"]
            if kwargs["sourceNetworks"].get("literals"):
                for literal in kwargs["sourceNetworks"]["literals"]:
                    self.sourceNetworks["literals"][literal["value"]] = literal["type"]
        if "destinationNetworks" in kwargs:
            self.destinationNetworks = {"objects": [], "literals": {}}
            if kwargs["destinationNetworks"].get("objects"):
                self.destinationNetworks["objects"] = kwargs["destinationNetworks"][
                    "objects"
                ]
            if kwargs["destinationNetworks"].get("literals"):
                for literal in kwargs["destinationNetworks"]["literals"]:
                    self.destinationNetworks["literals"][literal["value"]] = literal[
                        "type"
                    ]
        if "enableSyslog" in kwargs:
            self.enableSyslog = kwargs["enableSyslog"]
        if "logBegin" in kwargs:
            self.logBegin = kwargs["logBegin"]
        if "logEnd" in kwargs:
            self.logEnd = kwargs["logEnd"]
        if "enabled" in kwargs:
            self.enabled = kwargs["enabled"]
        if "sendEventsToFMC" in kwargs:
            self.sendEventsToFMC = kwargs["sendEventsToFMC"]
        if "newComments" in kwargs:
            self._newComments = kwargs["newComments"]
        if "commentHistoryList" in kwargs:
            self._commentHistoryList = kwargs["commentHistoryList"]
        if "users" in kwargs:
            self.users = {"objects": []}
            if kwargs["users"].get("objects"):
                self.users["objects"] = kwargs["users"]["objects"]

    def acp(self, name="", id=""):
        """
        Associate an AccessPolicies object with this AccessRule object.

        :param name: (str)  Name of ACP.
        :param id: (str) ID of ACP.
        :return: None
        """
        # either name or id of the ACP should be given
        logging.debug("In acp() for AccessRules class.")
        if id != "":
            self.acp_id = id
            self.URL = f"{self.fmc.configuration_url}{self.PREFIX_URL}/{id}/accessrules"
        elif name != "":
            acp1 = AccessPolicies(fmc=self.fmc)
            acp1.get(name=name)
            if "id" in acp1.__dict__:
                self.acp_id = acp1.id
                self.URL = f"{self.fmc.configuration_url}{self.PREFIX_URL}/{acp1.id}/accessrules"
            else:
                logging.warning(
                    f"Access Control Policy {name} not found.  Cannot set up accessPolicy for AccessRules."
                )
        else:
            logging.error("No accessPolicy name or ID was provided.")

    def intrusion_policy(self, action, name=""):
        """
        Add/remove name of ipsPolicy field of AccessRules object.

        :param action: (str) 'set', or 'clear'
        :param name: (str) Name of intrusion policy in FMC.
        :return: None
        """
        logging.debug("In intrusion_policy() for AccessRules class.")
        if action == "clear":
            if "ipsPolicy" in self.__dict__:
                del self.ipsPolicy
                logging.info("Intrusion Policy removed from this AccessRules object.")
        elif action == "set":
            ips = IntrusionPolicies(fmc=self.fmc, name=name)
            ips.get()
            self.ipsPolicy = {"name": ips.name, "id": ips.id, "type": ips.type}
            logging.info(
                f'Intrusion Policy set to "{name}" for this AccessRules object.'
            )

    def variable_set(self, action, name="Default-Set"):
        """
        Add/remove name of variableSet field of AccessRules object.

        :param action: (str) 'set', or 'clear'
        :param name: (str) Name of variable set in FMC.
        :return: None
        """
        logging.debug("In variable_set() for AccessRules class.")
        if action == "clear":
            if "variableSet" in self.__dict__:
                del self.variableSet
                logging.info("Variable Set removed from this AccessRules object.")
        elif action == "set":
            vs = VariableSets(fmc=self.fmc)
            vs.get(name=name)
            self.variableSet = {"name": vs.name, "id": vs.id, "type": vs.type}
            logging.info(f'VariableSet set to "{name}" for this AccessRules object.')

    def file_policy(self, action, name="None"):
        """
        Add/remove name of filePolicy field of AccessRules object.

        :param action: (str) 'set', or 'clear'
        :param name: (str) Name of file policy in FMC.
        :return: None
        """
        logging.debug("In file_policy() for ACPRule class.")
        if action == "clear":
            if "filePolicy" in self.__dict__:
                del self.filePolicy
                logging.info("file_policy removed from this AccessRules object.")
        elif action == "set":
            fp = FilePolicies(fmc=self.fmc)
            fp.get(name=name)
            self.filePolicy = {"name": fp.name, "id": fp.id, "type": fp.type}
            logging.info(f'file_policy set to "{name}" for this AccessRules object.')

    def vlan_tags(self, action, name=""):
        """
        Add/modify name to vlanTags field of AccessRules object.

        :param action: (str) 'add', 'remove', or 'clear'
        :param name: (str) Name of VLAN tag in FMC.
        :return: None
        """
        logging.debug("In vlan_tags() for AccessRules class.")
        if action == "add":
            vlantag = VlanTags(fmc=self.fmc)
            vlantag.get(name=name)
            if "id" in vlantag.__dict__:
                if "vlanTags" in self.__dict__:
                    new_vlan = {
                        "name": vlantag.name,
                        "id": vlantag.id,
                        "type": vlantag.type,
                    }
                    duplicate = False
                    for obj in self.vlanTags["objects"]:
                        if obj["name"] == new_vlan["name"]:
                            duplicate = True
                            break
                    if not duplicate:
                        self.vlanTags["objects"].append(new_vlan)
                        logging.info(
                            f'Adding "{name}" to vlanTags for this AccessRules.'
                        )
                else:
                    self.vlanTags = {
                        "objects": [
                            {
                                "name": vlantag.name,
                                "id": vlantag.id,
                                "type": vlantag.type,
                            }
                        ]
                    }
                    logging.info(f'Adding "{name}" to vlanTags for this AccessRules.')
            else:
                logging.warning(
                    f'VLAN Tag, "{name}", not found.  Cannot add to AccessRules.'
                )
        elif action == "remove":
            vlantag = VlanTags(fmc=self.fmc)
            vlantag.get(name=name)
            if "id" in vlantag.__dict__:
                if "vlanTags" in self.__dict__:
                    objects = []
                    for obj in self.vlanTags["objects"]:
                        if obj["name"] != name:
                            objects.append(obj)
                    self.vlanTags["objects"] = objects
                    logging.info(
                        f'Removed "{name}" from vlanTags for this AccessRules.'
                    )
                else:
                    logging.info(
                        "vlanTags doesn't exist for this AccessRules.  Nothing to remove."
                    )
            else:
                logging.warning(
                    f"VLAN Tag, {name}, not found.  Cannot remove from AccessRules."
                )
        elif action == "clear":
            if "vlanTags" in self.__dict__:
                del self.vlanTags
                logging.info("All VLAN Tags removed from this AccessRules object.")

    def source_zone(self, action, name=""):
        """
        Add/modify name to sourceZones field of AccessRules object.

        :param action: (str) 'add', 'remove', or 'clear'
        :param name: (str) Name of Security Zone in FMC.
        :return: None
        """
        logging.debug("In source_zone() for AccessRules class.")
        if action == "add":
            sz = SecurityZones(fmc=self.fmc)
            sz.get(name=name)
            if "id" in sz.__dict__:
                if "sourceZones" in self.__dict__:
                    new_zone = {"name": sz.name, "id": sz.id, "type": sz.type}
                    duplicate = False
                    for obj in self.sourceZones["objects"]:
                        if obj["name"] == new_zone["name"]:
                            duplicate = True
                            break
                    if not duplicate:
                        self.sourceZones["objects"].append(new_zone)
                        logging.info(
                            f'Adding "{name}" to sourceZones for this AccessRules.'
                        )
                else:
                    self.sourceZones = {
                        "objects": [{"name": sz.name, "id": sz.id, "type": sz.type}]
                    }
                    logging.info(
                        f'Adding "{name}" to sourceZones for this AccessRules.'
                    )
            else:
                logging.warning(
                    'Security Zone, "{name}", not found.  Cannot add to AccessRules.'
                )
        elif action == "remove":
            sz = SecurityZones(fmc=self.fmc)
            sz.get(name=name)
            if "id" in sz.__dict__:
                if "sourceZones" in self.__dict__:
                    objects = []
                    for obj in self.sourceZones["objects"]:
                        if obj["name"] != name:
                            objects.append(obj)
                    self.sourceZones["objects"] = objects
                    logging.info(
                        f'Removed "{name}" from sourceZones for this AccessRules.'
                    )
                else:
                    logging.info(
                        "sourceZones doesn't exist for this AccessRules.  Nothing to remove."
                    )
            else:
                logging.warning(
                    f'Security Zone, "{name}", not found.  Cannot remove from AccessRules.'
                )
        elif action == "clear":
            if "sourceZones" in self.__dict__:
                del self.sourceZones
                logging.info("All Source Zones removed from this AccessRules object.")

    def destination_zone(self, action, name=""):
        """
        Add/modify name to destinationZones field of AccessRules object.

        :param action: (str) 'add', 'remove', or 'clear'
        :param name: (str) Name of Security Zone in FMC.
        :return: None
        """
        logging.debug("In destination_zone() for AccessRules class.")
        if action == "add":
            sz = SecurityZones(fmc=self.fmc)
            sz.get(name=name)
            if "id" in sz.__dict__:
                if "destinationZones" in self.__dict__:
                    new_zone = {"name": sz.name, "id": sz.id, "type": sz.type}
                    duplicate = False
                    for obj in self.destinationZones["objects"]:
                        if obj["name"] == new_zone["name"]:
                            duplicate = True
                            break
                    if not duplicate:
                        self.destinationZones["objects"].append(new_zone)
                        logging.info(
                            f'Adding "{name}" to destinationZones for this AccessRules.'
                        )
                else:
                    self.destinationZones = {
                        "objects": [{"name": sz.name, "id": sz.id, "type": sz.type}]
                    }
                    logging.info(
                        f'Adding "{name}" to destinationZones for this AccessRules.'
                    )
            else:
                logging.warning(
                    f'Security Zone, "{name}", not found.  Cannot add to AccessRules.'
                )
        elif action == "remove":
            sz = SecurityZones(fmc=self.fmc)
            sz.get(name=name)
            if "id" in sz.__dict__:
                if "destinationZones" in self.__dict__:
                    objects = []
                    for obj in self.destinationZones["objects"]:
                        if obj["name"] != name:
                            objects.append(obj)
                    self.destinationZones["objects"] = objects
                    logging.info(
                        'Removed "{name}" from destinationZones for this AccessRules.'
                    )
                else:
                    logging.info(
                        "destinationZones doesn't exist for this AccessRules.  Nothing to remove."
                    )
            else:
                logging.warning(
                    f"Security Zone, {name}, not found.  Cannot remove from AccessRules."
                )
        elif action == "clear":
            if "destinationZones" in self.__dict__:
                del self.destinationZones
                logging.info(
                    "All Destination Zones removed from this AccessRules object."
                )

    def source_port(self, action, name=""):
        """
        Add/modify name to sourcePorts field of AccessRules object.

        :param action: (str) 'add', 'addgroup', 'remove', or 'clear'
        :param name: (str) Name of Port in FMC.
        :return: None
        """
        logging.debug("In source_port() for AccessRules class.")
        if action == "add":
            pport_json = ProtocolPortObjects(fmc=self.fmc)
            pport_json.get(name=name)
            icmpv4_json = ICMPv4Objects(fmc=self.fmc)
            icmpv4_json.get(name=name)
            if "id" in pport_json.__dict__:
                item = pport_json
            elif "id" in icmpv4_json.__dict__:
                item = icmpv4_json
            else:
                item = PortObjectGroups(fmc=self.fmc)
                item.get(name=name)
            if "id" in item.__dict__:
                if "sourcePorts" in self.__dict__:
                    new_port = {"name": item.name, "id": item.id, "type": item.type}
                    duplicate = False
                    if "objects" not in self.sourcePorts:
                        self.__dict__["sourcePorts"]["objects"] = []
                    for obj in self.sourcePorts["objects"]:
                        if obj["name"] == new_port["name"]:
                            duplicate = True
                            break
                    if not duplicate:
                        self.sourcePorts["objects"].append(new_port)
                        logging.info(
                            f'Adding "{name}" to sourcePorts for this AccessRules.'
                        )
                else:
                    self.sourcePorts = {
                        "objects": [
                            {"name": item.name, "id": item.id, "type": item.type}
                        ]
                    }
                    logging.info(
                        f'Adding "{name}" to sourcePorts for this AccessRules.'
                    )
            else:
                logging.warning(
                    f'Protocol Port or Protocol Port Group: "{name}", '
                    f"not found.  Cannot add to AccessRules."
                )
        elif action == "addgroup":
            item = PortObjectGroups(fmc=self.fmc)
            item.get(name=name)
            if "id" in item.__dict__:
                if "sourcePorts" in self.__dict__:
                    new_port = {"name": item.name, "id": item.id, "type": item.type}
                    duplicate = False
                    if "objects" not in self.sourcePorts:
                        self.__dict__["sourcePorts"]["objects"] = []
                    for obj in self.sourcePorts["objects"]:
                        if obj["name"] == new_port["name"]:
                            duplicate = True
                            break
                    if not duplicate:
                        self.sourcePorts["objects"].append(new_port)
                        logging.info(
                            f'Adding "{name}" to sourcePorts for this AccessRules.'
                        )
                else:
                    self.sourcePorts = {
                        "objects": [
                            {"name": item.name, "id": item.id, "type": item.type}
                        ]
                    }
                    logging.info(
                        f'Adding "{name}" to sourcePorts for this AccessRules.'
                    )
            else:
                logging.warning(
                    f'Protocol Port Port Group: "{name}", '
                    f"not found.  Cannot add to AccessRules."
                )
        elif action == "remove":
            pport_json = ProtocolPortObjects(fmc=self.fmc)
            pport_json.get(name=name)
            icmpv4_json = ICMPv4Objects(fmc=self.fmc)
            icmpv4_json.get(name=name)
            if "id" in pport_json.__dict__:
                item = pport_json
            elif "id" in icmpv4_json.__dict__:
                item = icmpv4_json
            else:
                item = PortObjectGroups(fmc=self.fmc)
                item.get(name=name)
            if "id" in item.__dict__:
                if "sourcePorts" in self.__dict__:
                    objects = []
                    for obj in self.sourcePorts["objects"]:
                        if obj["name"] != name:
                            objects.append(obj)
                    self.sourcePorts["objects"] = objects
                    logging.info(
                        f'Removed "{name}" from sourcePorts for this AccessRules.'
                    )
                else:
                    logging.info(
                        "sourcePorts doesn't exist for this AccessRules.  Nothing to remove."
                    )
            else:
                logging.warning(
                    f'Protocol Port or Protocol Port Group: "{name}", '
                    f"not found.  Cannot add to AccessRules."
                )
        elif action == "clear":
            if "sourcePorts" in self.__dict__:
                del self.sourcePorts
                logging.info("All Source Ports removed from this AccessRules object.")

    def destination_port(self, action, name=""):
        """
        Add/modify name to destinationPorts field of AccessRules object.

        :param action: (str) 'add', 'addgroup', 'remove', or 'clear'
        :param name: (str) Name of Port in FMC.
        :return: None
        """
        logging.debug("In destination_port() for AccessRules class.")
        if action == "add":
            pport_json = ProtocolPortObjects(fmc=self.fmc)
            pport_json.get(name=name)
            icmpv4_json = ICMPv4Objects(fmc=self.fmc)
            icmpv4_json.get(name=name)
            if "id" in pport_json.__dict__:
                item = pport_json
            elif "id" in icmpv4_json.__dict__:
                item = icmpv4_json
            else:
                item = PortObjectGroups(fmc=self.fmc)
                item.get(name=name)
            if "id" in item.__dict__:
                if "destinationPorts" in self.__dict__:
                    new_port = {"name": item.name, "id": item.id, "type": item.type}
                    duplicate = False
                    if "objects" not in self.destinationPorts:
                        self.__dict__["destinationPorts"]["objects"] = []
                    for obj in self.destinationPorts["objects"]:
                        if obj["name"] == new_port["name"]:
                            duplicate = True
                            break
                    if not duplicate:
                        self.destinationPorts["objects"].append(new_port)
                        logging.info(
                            f'Adding "{name}" to destinationPorts for this AccessRules.'
                        )
                else:
                    self.destinationPorts = {
                        "objects": [
                            {"name": item.name, "id": item.id, "type": item.type}
                        ]
                    }
                    logging.info(
                        f'Adding "{name}" to destinationPorts for this AccessRules.'
                    )
            else:
                logging.warning(
                    f'Protocol Port or Protocol Port Group: "{name}", '
                    f"not found.  Cannot add to AccessRules."
                )
        if action == "addgroup":
            item = PortObjectGroups(fmc=self.fmc)
            item.get(name=name)
            if "id" in item.__dict__:
                if "destinationPorts" in self.__dict__:
                    new_port = {"name": item.name, "id": item.id, "type": item.type}
                    duplicate = False
                    if "objects" not in self.destinationPorts:
                        self.__dict__["destinationPorts"]["objects"] = []
                    for obj in self.destinationPorts["objects"]:
                        if obj["name"] == new_port["name"]:
                            duplicate = True
                            break
                    if not duplicate:
                        self.destinationPorts["objects"].append(new_port)
                        logging.info(
                            f'Adding "{name}" to destinationPorts for this AccessRules.'
                        )
                else:
                    self.destinationPorts = {
                        "objects": [
                            {"name": item.name, "id": item.id, "type": item.type}
                        ]
                    }
                    logging.info(
                        f'Adding "{name}" to destinationPorts for this AccessRules.'
                    )
            else:
                logging.warning(
                    f'Protocol Port Port Group: "{name}", '
                    f"not found.  Cannot add to AccessRules."
                )
        elif action == "remove":
            pport_json = ProtocolPortObjects(fmc=self.fmc)
            pport_json.get(name=name)
            icmpv4_json = ICMPv4Objects(fmc=self.fmc)
            icmpv4_json.get(name=name)
            if "id" in pport_json.__dict__:
                item = pport_json
            elif "id" in icmpv4_json.__dict__:
                item = icmpv4_json
            else:
                item = PortObjectGroups(fmc=self.fmc)
                item.get(name=name)
            if "id" in item.__dict__:
                if "destinationPorts" in self.__dict__:
                    objects = []
                    for obj in self.destinationPorts["objects"]:
                        if obj["name"] != name:
                            objects.append(obj)
                    self.destinationPorts["objects"] = objects
                    logging.info(
                        f'Removed "{name}" from destinationPorts for this AccessRules.'
                    )
                else:
                    logging.info(
                        "destinationPorts doesn't exist for this AccessRules.  Nothing to remove."
                    )
            else:
                logging.warning(
                    f'Protocol Port or Protocol Port Group: "{name}", '
                    f"not found.  Cannot add to AccessRules."
                )
        elif action == "clear":
            if "destinationPorts" in self.__dict__:
                del self.destinationPorts
                logging.info(
                    "All Destination Ports removed from this AccessRules object."
                )

    def source_network(self, action, name="", literal=None):
        """
        Add/modify name/literal to sourceNetworks field of AccessRules object.

        :param action: (str) the action to be done 'add', 'remove', 'clear'
        :param name: (str) name of the object in question
        :param literal: (dict) the literal in question {value:<>, type:<>}
        :return: None
        """
        # using dict() as default value is dangerous here, any thoughts/workarounds on this?
        logging.debug("In source_network() for AccessRules class.")
        if literal and name != "":
            raise ValueError(
                "Only one of literals or name (object name) should be set while creating a source network"
            )

        if not hasattr(self, "sourceNetworks"):
            self.sourceNetworks = {"objects": [], "literals": {}}

        if action == "add":
            if literal:
                type_ = get_networkaddress_type(literal)
                self.sourceNetworks["literals"][literal] = type_
                logging.info(
                    f'Adding literal "{literal}" of type "{type_}" to sourceNetworks for this AccessRules.'
                )
            else:
                ipaddresses_json = NetworkAddresses(fmc=self.fmc).get()
                networkgroup_json = NetworkGroups(fmc=self.fmc).get()
                fqdns_json = FQDNS(fmc=self.fmc).get()
                items = (
                    ipaddresses_json.get("items", [])
                    + networkgroup_json.get("items", [])
                    + fqdns_json.get("items", [])
                )
                new_net = None
                for item in items:
                    if item["name"] == name:
                        new_net = {
                            "name": item["name"],
                            "id": item["id"],
                            "type": item["type"],
                        }
                        break
                if new_net is None:
                    logging.warning(
                        f'Network "{name}" is not found in FMC.  Cannot add to sourceNetworks.'
                    )
                else:
                    if "sourceNetworks" in self.__dict__:
                        # thus either some objects are already present in sourceNetworks,
                        # or only literals are present in sourceNetworks
                        if "objects" in self.__dict__["sourceNetworks"]:
                            # some objects are already present
                            duplicate = False
                            # see if its a duplicate or not. If not, append to the list of
                            # existing objects in sourceNetworks
                            for obj in self.sourceNetworks["objects"]:
                                if obj["name"] == new_net["name"]:
                                    duplicate = True
                                    break
                            if not duplicate:
                                self.sourceNetworks["objects"].append(new_net)
                                logging.info(
                                    f'Adding "{name}" to sourceNetworks for this AccessRules.'
                                )
                        else:
                            # this means no objects were present in sourceNetworks,
                            # and sourceNetworks contains literals only
                            self.sourceNetworks.update({"objects": [new_net]})
                            # So update the sourceNetworks dict which contained 'literals' key initially
                            # to have a 'objects' key as well
                            logging.info(
                                f'Adding "{name}" to sourceNetworks for this AccessRules.'
                            )
                    else:
                        # None of literals or objects are present in sourceNetworks,
                        # so initialize it with objects and update the provided object
                        self.sourceNetworks = {"objects": [new_net]}
                        logging.info(
                            f'Adding "{name}" to sourceNetworks for this AccessRules.'
                        )
        elif action == "remove":
            if "sourceNetworks" in self.__dict__:
                if name != "":
                    # an object's name has been provided to be removed
                    objects = []
                    for obj in self.sourceNetworks["objects"]:
                        if obj["name"] != name:
                            objects.append(obj)
                    if len(objects) == 0:
                        # it was the last object which was deleted now
                        del self.sourceNetworks
                        logging.info(
                            f'Removed "{name}" from sourceNetworks for this AccessRules'
                        )
                        logging.info(
                            "All Source Networks removed from this AccessRules object."
                        )
                    else:
                        self.sourceNetworks["objects"] = objects
                        logging.info(
                            f'Removed "{name}" from sourceNetworks for this AccessRules.'
                        )
                else:
                    # a literal value has been provided to be removed
                    type_ = self.sourceNetworks["literals"].get(literal)
                    if type_:
                        self.sourceNetworks["literals"].pop(literal)
                        logging.info(
                            f'Removed literal "{literal}" of type '
                            f'"{type_}" from sourceNetworks for this AccessRules.'
                        )
                    else:
                        logging.info(
                            f'Unable to removed literal "{literal}" from sourceNetworks as it was not found'
                        )
            else:
                logging.info(
                    "sourceNetworks doesn't exist for this AccessRules.  Nothing to remove."
                )
        elif action == "clear":
            if "sourceNetworks" in self.__dict__:
                del self.sourceNetworks
                logging.info(
                    "All Source Networks removed from this AccessRules object."
                )

    def destination_network(self, action, name="", literal=None):
        """
        Add/modify name/literal to destinationNetworks field of AccessRules object.

        :param action: (str) the action to be done 'add', 'remove', 'clear'
        :param name: (str) name of the object in question
        :param literal: (dict) the literal in question {value:<>, type:<>}
        :return: None
        """
        # using dict() as default value is dangerous here, any thoughts/workarounds on this?

        logging.debug("In destination_network() for ACPRule class.")
        if literal and name != "":
            raise ValueError(
                "Only one of literals or name (object name) should be set while creating a source network"
            )

        if not hasattr(self, "destinationNetworks"):
            self.destinationNetworks = {"objects": [], "literals": {}}

        if action == "add":
            if literal:
                type_ = get_networkaddress_type(literal)
                self.destinationNetworks["literals"][literal] = type_
                logging.info(
                    f'Adding literal "{literal}" of type "{type_}" '
                    f"to destinationNetworks for this AccessRules."
                )
            else:
                ipaddresses_json = NetworkAddresses(fmc=self.fmc).get()
                networkgroup_json = NetworkGroups(fmc=self.fmc).get()
                if self.fmc.serverVersion >= "6.4":
                    fqdns_json = FQDNS(fmc=self.fmc).get()
                else:
                    fqdns_json = {"items": []}
                items = (
                    ipaddresses_json.get("items", [])
                    + networkgroup_json.get("items", [])
                    + fqdns_json.get("items", [])
                )
                new_net = None
                for item in items:
                    if item["name"] == name:
                        new_net = {
                            "name": item["name"],
                            "id": item["id"],
                            "type": item["type"],
                        }
                        break
                if new_net is None:
                    logging.warning(
                        f'Network "{name}" is not found in FMC.  Cannot add to destinationNetworks.'
                    )
                else:
                    if "destinationNetworks" in self.__dict__:
                        # thus either some objects are already present in destinationNetworks,
                        # or only literals are present in destinationNetworks
                        if "objects" in self.__dict__["destinationNetworks"]:
                            # some objects are already present
                            duplicate = False
                            for obj in self.destinationNetworks["objects"]:
                                if obj["name"] == new_net["name"]:
                                    duplicate = True
                                    break
                            if not duplicate:
                                self.destinationNetworks["objects"].append(new_net)
                                logging.info(
                                    f'Adding "{name}" to destinationNetworks for this AccessRules.'
                                )
                        else:
                            # this means no objects were present in destinationNetworks,
                            # and destinationNetworks contains literals only
                            self.destinationNetworks.update({"objects": [new_net]})
                            # So update the destinationNetworks dict which contained 'literals' key initially
                            # to have a 'objects' key as well
                            logging.info(
                                f'Adding "{name}" to destinationNetworks for this AccessRules.'
                            )
                    else:
                        # None of literals or objects are present in destinationNetworks,
                        # so initialize it with objects and update the provided object
                        self.destinationNetworks = {"objects": [new_net]}
                        logging.info(
                            f'Adding "{name}" to destinationNetworks for this AccessRules.'
                        )
        elif action == "remove":
            if "destinationNetworks" in self.__dict__:
                if name != "":
                    # an object's name has been provided to be removed
                    objects = []
                    for obj in self.destinationNetworks["objects"]:
                        if obj["name"] != name:
                            objects.append(obj)
                    if len(objects) == 0:
                        # it was the last object which was deleted now
                        del self.destinationNetworks
                        logging.info(
                            f'Removed "{name}" from destinationNetworks for this AccessRules'
                        )
                        logging.info(
                            "All Destination Networks removed from this AccessRules object."
                        )
                    else:
                        self.destinationNetworks["objects"] = objects
                        logging.info(
                            f'Removed "{name}" from destinationNetworks for this AccessRules.'
                        )
                else:
                    # a literal value has been provided to be removed
                    type_ = self.destinationNetworks["literals"].get(literal)
                    if type_:
                        self.destinationNetworks["literals"].pop(literal)
                        logging.info(
                            f'Removed literal "{literal}" of '
                            f'type "{type_}" from destinationNetworks for this AccessRules.'
                        )
                    else:
                        logging.info(
                            f'Unable to removed literal "{literal}" '
                            f"from destinationNetworks as it was not found"
                        )
            else:
                logging.info(
                    "destinationNetworks doesn't exist for this AccessRules.  Nothing to remove."
                )
        elif action == "clear":
            if "destinationNetworks" in self.__dict__:
                del self.destinationNetworks
                logging.info(
                    "All Destination Networks removed from this AccessRules object."
                )

    def source_sgt(self, action, name="", literal=None):
        """
        Add/modify name/literal to the sourceSecurityGroupTags field of AccessRules object.

        :param action: (str) 'add', 'remove', or 'clear'
        :param name: (str) Name of SGT in FMC.
        :param literal: (dict) {value:<>, type:<>}
        :return: None
        """
        # using dict() as default value is dangerous here, any thoughts/workarounds on this?

        logging.debug("In source_sgt() for ACPRule class.")
        if literal and name != "":
            raise ValueError(
                "Only one of literals or name (object name) should be set while creating a source sgt"
            )

        if not hasattr(self, "sourceSecurityGroupTags"):
            self.sourceSecurityGroupTags = {"objects": [], "literals": {}}

        if action == "add":
            if literal:
                type_ = "ISESecurityGroupTag"
                self.sourceSecurityGroupTags["literals"][literal] = type_
                logging.info(
                    f'Adding literal "{literal}" of type "{type_}" '
                    f"to sourceSecurityGroupTags for this AccessRules."
                )
            else:
                # Query FMC for all SGTs and iterate through them to see if our name matches 1 of them.
                sgt = ISESecurityGroupTags(fmc=self.fmc)
                sgt.get(name=name)
                if "id" in sgt.__dict__:
                    item = sgt
                else:
                    item = {}
                new_sgt = None
                if item.name == name:
                    new_sgt = {"name": item.name, "tag": item.tag, "type": item.type}
                if new_sgt is None:
                    logging.warning(
                        f'SecurityGroupTag "{name}" is not found in FMC.  '
                        f"Cannot add to sourceSecurityGroupTags."
                    )
                else:
                    if "sourceSecurityGroupTags" in self.__dict__:
                        # thus either some objects are already present in sourceSecurityGroupTags,
                        # or only literals are present in sourceSecurityGroupTags
                        if "objects" in self.__dict__["sourceSecurityGroupTags"]:
                            # some objects are already present
                            duplicate = False
                            for obj in self.sourceSecurityGroupTags["objects"]:
                                if obj["name"] == new_sgt["name"]:
                                    duplicate = True
                                    break
                            if not duplicate:
                                self.sourceSecurityGroupTags["objects"].append(new_sgt)
                                logging.info(
                                    f'Adding "{name}" to sourceSecurityGroupTags for this AccessRules.'
                                )
                        else:
                            # this means no objects were present in sourceSecurityGroupTags,
                            # and sourceSecurityGroupTags contains literals only
                            self.sourceSecurityGroupTags.update({"objects": [new_sgt]})
                            # So update the sourceSecurityGroupTags dict which contained 'literals' key initially
                            # to have a 'objects' key as well
                            logging.info(
                                f'Adding "{name}" to sourceSecurityGroupTags for this AccessRules.'
                            )
                    else:
                        # None of literals or objects are present in sourceSecurityGroupTags,
                        # so initialize it with objects and update the provided object
                        self.sourceSecurityGroupTags = {"objects": [new_sgt]}
                        logging.info(
                            f'Adding "{name}" to sourceSecurityGroupTags for this AccessRules.'
                        )
        elif action == "remove":
            if "sourceSecurityGroupTags" in self.__dict__:
                if name != "":
                    # an object's name has been provided to be removed
                    objects = []
                    for obj in self.sourceSecurityGroupTags["objects"]:
                        if obj["name"] != name:
                            objects.append(obj)
                    if len(objects) == 0:
                        # it was the last object which was deleted now
                        del self.sourceSecurityGroupTags
                        logging.info(
                            f'Removed "{name}" from sourceSecurityGroupTags for this AccessRules'
                        )
                        logging.info(
                            "All source security group tags are removed from this AccessRules object."
                        )
                    else:
                        self.sourceSecurityGroupTags["objects"] = objects
                        logging.info(
                            f'Removed "{name}" from sourceSecurityGroupTags for this AccessRules.'
                        )
                else:
                    # a literal value has been provided to be removed
                    type_ = self.sourceSecurityGroupTags["literals"].get(literal)
                    if type_:
                        self.sourceSecurityGroupTags["literals"].pop(literal)
                        logging.info(
                            f'Removed literal "{literal}" of '
                            f'type "{type_}" from sourceSecurityGroupTags for this AccessRules.'
                        )
                    else:
                        logging.info(
                            f'Unable to removed literal "{literal}" '
                            f"from sourceSecurityGroupTags as it was not found"
                        )
            else:
                logging.info(
                    "No sourceSecurityGroupTags exist for this AccessRules.  Nothing to remove."
                )
        elif action == "clear":
            if "sourceSecurityGroupTags" in self.__dict__:
                del self.sourceSecurityGroupTags
                logging.info(
                    "All source security group tags are removed from this AccessRules object."
                )

    def destination_sgt(self, action, name="", literal=None):
        """
        Add/modify name/literal to the destinationSecurityGroupTags field of AccessRules object.

        :param action: (str) 'add', 'remove', or 'clear'
        :param name: (str) Name of SGT in FMC.
        :param literal: (dict) {value:<>, type:<>}
        :return: None
        """
        pass

    def realm_user(self, action, name="", realm_type="user"):
        """
        Add/modify realm users field of AccessRules object.
        :param action: (str) 'add', 'remove', or 'clear'
        :param name: (str) Name Realm user/usergroup in FMC.
        :param realm_type (str) 'user' or 'group' default to user - not used in 'clear'
        :return: None
        NOTE Only tested on single realm deployment
        """
        logging.debug("In realm_user() for AccessRules class.")
        if action == "add":
            if realm_type == "user":
                user = RealmUsers(fmc=self.fmc)
                logging.debug("Type user")
            elif realm_type == "group":
                user = RealmUserGroups(fmc=self.fmc)
                logging.debug("Type Group")
            else:
                logging.warning("not a valid realm_type - 'user'|'group'")
                return None
            user.get(name=name)
            if "id" in user.__dict__:
                if "users" in self.__dict__:
                    new_realm_user = {
                        "name": user.name,
                        "id": user.id,
                        "type": user.type,
                        "realm": user.realm,
                    }
                    duplicate = False
                    if "objects" not in self.users:
                        self.__dict__["users"]["objects"] = []

                    for obj in self.users["objects"]:
                        if obj["name"] == new_realm_user["name"]:
                            duplicate = True
                            break
                    if not duplicate:
                        self.users["objects"].append(new_realm_user)
                        logging.info(f'Adding "{name}" to users for this AccessRules.')
                else:
                    self.users = {
                        "objects": [
                            {
                                "name": user.name,
                                "id": user.id,
                                "type": user.type,
                                "realm": user.realm,
                            }
                        ]
                    }
                    logging.info(f'Adding "{name}" to users for this AccessRules.')
            else:
                logging.warning(
                    f'User: "{name}", ' f"not found.  Cannot add to AccessRules."
                )

        elif action == "remove":
            if realm_type == "user":
                user = RealmUsers(fmc=self.fmc)
            elif realm_type == "group":
                user = RealmUserGroups(fmc=self.fmc)
            user.get(name=name)
            if "id" in user.__dict__:
                if "users" in self.__dict__:
                    users = []
                    for obj in self.users["objects"]:
                        if obj["name"] != name:
                            users.append(obj)
                    self.users["objects"] = users
                    logging.info(f'Removed "{name}" from users for this AccessRules.')
                else:
                    logging.info(
                        "Users doesn't exist for this AccessRules.  Nothing to remove."
                    )
            else:
                logging.warning(
                    f"User, {name}, not found.  Cannot remove from AccessRules."
                )

        elif action == "clear":
            if "users" in self.__dict__:
                del self.users
                logging.info("All Users removed from this AccessRules object.")

    def application(self, action, name=""):
        """
        Add/modify name to applications field of AccessRules object.
        :param action: (str) 'add', 'remove', or 'clear'
        :param name: (str) Name of Application in FMC.
        :return: None
        """
        logging.debug("In application() for AccessRules class.")
        if action == "add":
            app = Applications(fmc=self.fmc)
            app.get(name=name)
            if "id" in app.__dict__:
                if "applications" in self.__dict__:
                    new_app = {"name": app.name, "id": app.id, "type": app.type}
                    duplicate = False
                    if "applications" not in self.applications:
                        self.__dict__["applications"]["applications"] = []
                    for obj in self.applications["applications"]:
                        if obj["name"] == new_app["name"]:
                            duplicate = True
                            break
                    if not duplicate:
                        self.applications["applications"].append(new_app)
                        logging.info(
                            f'Adding "{name}" to applications for this AccessRules.'
                        )
                else:
                    self.applications = {
                        "applications": [
                            {"name": app.name, "id": app.id, "type": app.type}
                        ]
                    }
                    logging.info(
                        f'Adding "{name}" to applications for this AccessRules.'
                    )
            else:
                logging.warning(
                    f'Application: "{name}", ' f"not found.  Cannot add to AccessRules."
                )
        elif action == "addappfilter":
            app = ApplicationFilters(fmc=self.fmc)
            app.get(name=name)
            if "id" in app.__dict__:
                if "applicationFilters" in self.__dict__:
                    new_app = {"name": app.name, "id": app.id, "type": app.type}
                    duplicate = False
                    if "applicationFilters" not in self.applications:
                        self.__dict__["applicationFilters"]["applicationFilters"] = []
                    for obj in self.applications["applicationFilters"]:
                        if obj["name"] == new_app["name"]:
                            duplicate = True
                            break
                    if not duplicate:
                        self.applications["applicationFilters"].append(new_app)
                        logging.info(
                            f'Adding "{name}" to applications for this AccessRules.'
                        )
                else:
                    self.applications = {
                        "applicationFilters": [
                            {"name": app.name, "id": app.id, "type": app.type}
                        ]
                    }
                    logging.info(
                        f'Adding "{name}" application filter to applications for this AccessRules.'
                    )
            else:
                logging.warning(
                    f'Application Filter: "{name}", '
                    f"not found.  Cannot add to AccessRules."
                )
        elif action == "remove":
            app = Applications(fmc=self.fmc)
            app.get(name=name)
            if "id" in app.__dict__:
                if "applicationFilters" in self.__dict__:
                    applications = []
                    for obj in self.applications["applications"]:
                        if obj["name"] != name:
                            applications.append(obj)
                    self.applications["applicationFilters"] = applications
                    logging.info(
                        f'Removed "{name}" from applications for this AccessRules.'
                    )
                else:
                    logging.info(
                        "Application doesn't exist for this AccessRules.  Nothing to remove."
                    )
            else:
                logging.warning(
                    f"Application, {name}, not found.  Cannot remove from AccessRules."
                )
        elif action == "removeappfilter":
            app = ApplicationFilters(fmc=self.fmc)
            app.get(name=name)
            if "id" in app.__dict__:
                if "applications" in self.__dict__:
                    applications = []
                    for obj in self.applications["applicationFilters"]:
                        if obj["name"] != name:
                            applications.append(obj)
                    self.applications["applicationFilters"] = applications
                    logging.info(
                        f'Removed "{name}" application filter from applications for this AccessRules.'
                    )
                else:
                    logging.info(
                        "Application filter doesn't exist for this AccessRules.  Nothing to remove."
                    )
            else:
                logging.warning(
                    f"Application filter, {name}, not found.  Cannot remove from AccessRules."
                )

        elif action == "clear":
            if "applications" in self.__dict__:
                del self.applications
                logging.info("All Applications removed from this AccessRules object.")

    def urls_info(self, action, name=""):
        """
        Add/modify name to URLs field of AccessRules object.
        :param action: (str) 'add', 'remove', or 'clear'
        :param name: (str) Name of URLs in FMC.
        :return: None
        """
        logging.debug("In urls() for AccessRules class.")
        if action == "add":
            urlobj_json = URLs(fmc=self.fmc)
            urlobj_json.get(name=name)
            if "id" in urlobj_json.__dict__:
                item = urlobj_json
            else:
                item = URLGroups(fmc=self.fmc)
                item.get(name=name)
            if "id" in item.__dict__:
                if "urls" in self.__dict__:
                    new_url = {"name": item.name, "id": item.id}
                    duplicate = False
                    if "objects" not in self.urls:
                        self.__dict__["urls"]["objects"] = []
                    for obj in self.urls["objects"]:
                        if obj["name"] == new_url["name"]:
                            duplicate = True
                            break
                    if not duplicate:
                        self.urls["objects"].append(new_url)
                        logging.info(
                            f'Adding URLs "{name}" to URLs for this AccessRules.'
                        )
                else:
                    self.urls = {"objects": [{"name": item.name, "id": item.id}]}
                    logging.info(f'Adding URLs "{name}" to URLs for this AccessRules.')
            else:
                logging.warning(
                    f'URL Object or URL Object Group: "{name}", '
                    f"not found.  Cannot add to AccessRules."
                )
        elif action == "remove":
            urlobj_json = URLs(fmc=self.fmc)
            urlobj_json.get(name=name)
            if "id" in urlobj_json.__dict__:
                item = urlobj_json
            else:
                item = URLGroups(fmc=self.fmc)
                item.get(name=name)
            if "id" in item.__dict__:
                if "urls" in self.__dict__:
                    objects = []
                for obj in self.urls["objects"]:
                    if obj["name"] != name:
                        objects.append(obj)
                    self.urls["objects"] = objects
                    logging.info(
                        f'Removed URLs "{name}" from URLs for this AccessRules.'
                    )
                else:
                    logging.info(
                        "URLs doesn't exist for this AccessRules.  Nothing to remove."
                    )
            else:
                logging.warning(
                    f'URL Object or URL Object Group: "{name}", '
                    f"not found.  Cannot add to AccessRules."
                )
        elif action == "clear":
            if "urls" in self.__dict__:
                del self.urls
                logging.info("All URLs removed from this AccessRules object.")

    def new_comments(self, action, value):
        """
        Add a comment to the comment list
        Args:
            action (str): Add, remove or clear
            value (str): Comment value to add
        """
        if action == "add":
            self._newComments.append(value)
        if action == "remove":
            self._newComments.remove(value)
        if action == "clear":
            self._newComments = []


class Bulk(object):
    """
    Send many JSON objects in one API call.

    This is specific to the AccessRules() method.
    """

    MAX_SIZE_QTY = 1000
    MAX_SIZE_IN_BYTES = 2048000
    REQUIRED_FOR_POST = []

    @property
    def URL_SUFFIX(self):
        """
        Add the URL suffixes for section, categories, insertBefore and insertAfter.

        :return (str): url
        """
        url = "?"

        if "category" in self.__dict__:
            url = f"{url}category={self.category}&"
        if "insertBefore" in self.__dict__:
            url = f"{url}insertBefore={self.insertBefore}&"
        if "insertAfter" in self.__dict__:
            url = f"{url}insertAfter={self.insertAfter}&"
        if "insertBefore" in self.__dict__ and "insertAfter" in self.__dict__:
            logging.warning("ACP rule has both insertBefore and insertAfter params")
        if "section" in self.__dict__:
            url = f"{url}section={self.section}&"

        return url[:-1]

    def __init__(self, fmc, url="", **kwargs):
        """
        Initialize Bulk object.

        :param fmc (object):  FMC object
        :param url (str): Base URL used for API action.
        :param **kwargs: Pass any/all variables for self.
        :return: None
        """
        logging.debug("In __init__() for Bulk class.")
        self.fmc = fmc
        self.items = []
        self.URL = url
        self.parse_kwargs(**kwargs)

    def parse_kwargs(self, **kwargs):
        """
        Add/modify variables in self.

        :return: None
        """
        logging.debug("In parse_kwargs() for Bulk class.")
        if "category" in kwargs:
            self.category = kwargs["category"]
        if "insertBefore" in kwargs:
            self.insertBefore = kwargs["insertBefore"]
        if "insertAfter" in kwargs:
            self.insertAfter = kwargs["insertAfter"]
        if "section" in kwargs:
            self.section = kwargs["section"]

    def add(self, item):
        """
        :param item: (str) Add JSON string to list of items to send to FMC.

        :return: None
        """
        self.items.append(item)
        logging.info(f"Adding {item} to bulk items list.")

    def clear(self):
        """
        Clear self.items -- Empty out list of JSON strings to send to FMC.

        :return: None
        """
        logging.info(f"Clearing bulk items list.")
        self.items = []

    def post(self):
        """
        Send list of self.items to FMC as a bulk import.

        :return: (str) requests response from FMC
        """
        # Build URL
        self.URL = f"{self.URL}{self.URL_SUFFIX}&bulk=true"

        # Break up the items into MAX_BULK_POST_SIZE chunks.
        chunks = [
            self.items[i * self.MAX_SIZE_QTY : (i + 1) * self.MAX_SIZE_QTY]
            for i in range(
                (len(self.items) + self.MAX_SIZE_QTY - 1) // self.MAX_SIZE_QTY
            )
        ]

        # Post the chunks
        for item in chunks:
            # I'm not sure what to do about the max bytes right now so I'll just throw a warning message.
            if sys.getsizeof(item, 0) > self.MAX_SIZE_IN_BYTES:
                logging.warning(
                    f"This chunk of the post is too large.  Please submit less items to be bulk posted."
                )
            response = self.fmc.send_to_api(method="post", url=self.URL, json_data=item)
            logging.info(f"Posting to bulk items.")
            return response
