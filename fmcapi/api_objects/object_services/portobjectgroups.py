"""Port Object Groups Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .ports import Ports
import logging


class PortObjectGroups(APIClassTemplate):
    """The PortObjectGroups Object in the FMC."""

    VALID_JSON_DATA = ["id", "name", "type", "objects", "literals", "description"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/portobjectgroups"

    # Technically you can have objects OR literals but I'm not set up for "OR" logic, yet.
    REQUIRED_FOR_POST = ["name", "objects"]

    def __init__(self, fmc, **kwargs):
        """
        Initialize PortObjectGroups object.

        Set self.type to "PortObjectGroup" and parse the kwargs.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for PortObjectGroups class.")
        self.parse_kwargs(**kwargs)
        self.type = "NetworkGroup"

    def named_ports(self, action, name=""):
        """
        Associate Named Ports.

        :param action: (str) 'add', 'remove', or 'clear'
        :param name: (str) Name of port.
        """
        logging.debug("In named_ports() for PortObjectGroups class.")
        if action == "add":
            port1 = Ports(fmc=self.fmc)
            response = port1.get()
            if "items" in response:
                new_port = None
                for item in response["items"]:
                    if item["name"] == name:
                        new_port = {
                            "name": item["name"],
                            "id": item["id"],
                            "type": item["type"],
                        }
                        break
                if new_port is None:
                    logging.warning(
                        f'Port "{name}" is not found in FMC.  Cannot add to PortObjectGroups.'
                    )
                else:
                    if "objects" in self.__dict__:
                        duplicate = False
                        for obj in self.objects:
                            if obj["name"] == new_port["name"]:
                                duplicate = True
                                break
                        if not duplicate:
                            self.objects.append(new_port)
                            logging.info(f'Adding "{name}" to PortObjectGroups.')
                    else:
                        self.objects = [new_port]
                        logging.info(f'Adding "{name}" to PortObjectGroups.')
        elif action == "remove":
            if "objects" in self.__dict__:
                objects_list = []
                for obj in self.objects:
                    if obj["name"] != name:
                        objects_list.append(obj)
                self.objects = objects_list
                logging.info(f'Removed "{name}" from PortObjectGroups.')
            else:
                logging.info(
                    "This PortObjectGroups has no named_ports.  Nothing to remove."
                )
        elif action == "clear":
            if "objects" in self.__dict__:
                del self.objects
                logging.info("All named_ports removed from this PortObjectGroups.")
