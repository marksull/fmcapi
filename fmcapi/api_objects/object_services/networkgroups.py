"""Network Groups Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from fmcapi.api_objects.helper_functions import *
from .networkaddresses import NetworkAddresses
import logging


class NetworkGroups(APIClassTemplate):
    """The NetworkGroups Object in the FMC."""

    VALID_JSON_DATA = ["id", "name", "type", "objects", "literals", "description"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/networkgroups"

    # Technically you can have objects OR literals but I'm not set up for "OR" logic, yet.
    REQUIRED_FOR_POST = ["name"]

    def __init__(self, fmc, **kwargs):
        """
        Initialize NetworkGroups object.

        Set self.type to "NetworkGroup" and parse the kwargs.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for NetworkGroups class.")
        self.parse_kwargs(**kwargs)
        self.type = "NetworkGroup"

    def named_networks(self, action, name=""):
        """
        Associate Named Networks.

        :param action: (str) 'add', 'addgroup', 'remove', or 'clear'
        :param name: (str) Name of network.
        """
        logging.debug("In named_networks() for NetworkGroups class.")
        if action == "add":
            net1 = NetworkAddresses(fmc=self.fmc)
            response = net1.get()
            if "items" in response:
                new_net = None
                for item in response["items"]:
                    if item["name"] == name:
                        new_net = {
                            "name": item["name"],
                            "id": item["id"],
                            "type": item["type"],
                        }
                        break
                if new_net is None:
                    logging.warning(
                        f'Network "{name}" is not found in FMC.  Cannot add to NetworkGroups.'
                    )
                else:
                    if "objects" in self.__dict__:
                        duplicate = False
                        for obj in self.objects:
                            if obj["name"] == new_net["name"]:
                                duplicate = True
                                break
                        if not duplicate:
                            self.objects.append(new_net)
                            logging.info(f'Adding "{name}" to NetworkGroups.')
                    else:
                        self.objects = [new_net]
                        logging.info(f'Adding "{name}" to NetworkGroups.')
        if action == "addgroup":
            netg1 = NetworkGroups(fmc=self.fmc)
            response = netg1.get()
            if "items" in response:
                new_net = None
                for item in response["items"]:
                    if item["name"] == name:
                        new_net = {
                            "name": item["name"],
                            "id": item["id"],
                            "type": item["type"],
                        }
                        break
                if new_net is None:
                    logging.warning(
                        f'Network "{name}" is not found in FMC.  Cannot add to NetworkGroups.'
                    )
                else:
                    if "objects" in self.__dict__:
                        duplicate = False
                        for obj in self.objects:
                            if obj["name"] == new_net["name"]:
                                duplicate = True
                                break
                        if not duplicate:
                            self.objects.append(new_net)
                            logging.info(f'Adding "{name}" to NetworkGroups.')
                    else:
                        self.objects = [new_net]
                        logging.info(f'Adding "{name}" to NetworkGroups.')
        elif action == "remove":
            if "objects" in self.__dict__:
                objects_list = []
                for obj in self.objects:
                    if obj["name"] != name:
                        objects_list.append(obj)
                self.objects = objects_list
                logging.info(f'Removed "{name}" from NetworkGroups.')
            else:
                logging.info(
                    "This NetworkGroups has no named_networks.  Nothing to remove."
                )
        elif action == "clear":
            if "objects" in self.__dict__:
                del self.objects
                logging.info("All named_networks removed from this NetworkGroups.")

    def unnamed_networks(self, action, value=""):
        """
        Associate Unnamed Networks.

        :param action: (str) 'add', 'remove', or 'clear'
        :param value: (str) Network x.x.x.x/xx
        """
        logging.debug("In unnamed_networks() for NetworkGroups class.")
        new_literal = []
        if action == "add":
            if value == "":
                logging.error(
                    "Value assignment required to add unamed_network to NetworkGroups."
                )
                return
            literal_type = get_networkaddress_type(value=value)
            if literal_type == "host" or literal_type == "network":
                new_literal = {"value": value, "type": literal_type}
            elif literal_type == "range":
                logging.error(
                    "Ranges are not supported as unnamed_networks in a NetworkGroups."
                )
            else:
                logging.error(
                    f'Value "{value}" provided is not in a recognizable format.'
                )
                return
            if "literals" in self.__dict__:
                duplicate = False
                for obj in self.literals:
                    if obj["value"] == new_literal["value"]:
                        duplicate = True
                        break
                if not duplicate:
                    self.literals.append(new_literal)
                    logging.info(f'Adding "{value}" to NetworkGroup.')
            else:
                self.literals = [new_literal]
                logging.info(f'Adding "{value}" to NetworkGroup.')
        elif action == "remove":
            if "literals" in self.__dict__:
                literals_list = []
                for obj in self.literals:
                    if obj["value"] != value:
                        literals_list.append(obj)
                self.literals = literals_list
                logging.info(f'Removed "{value}" from NetworkGroup.')
            else:
                logging.info(
                    "This NetworkGroups has no unnamed_networks.  Nothing to remove."
                )
        elif action == "clear":
            if "literals" in self.__dict__:
                del self.literals
                logging.info("All unnamed_networks removed from this NetworkGroups.")
