"""VLAN Group Tags Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .vlantags import VlanTags
from fmcapi.api_objects.helper_functions import validate_vlans
import logging


class VlanGroupTags(APIClassTemplate):
    """The VlanGroupTags Object in the FMC."""

    VALID_JSON_DATA = ["id", "name", "type", "description", "objects", "literals"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/vlangrouptags"

    # Technically you can have objects OR literals but I'm not set up for "OR" logic, yet.
    REQUIRED_FOR_POST = ["name", "objects"]

    def __init__(self, fmc, **kwargs):
        """
        Initialize VlanGroupTags object.

        Set self.type to VlanGroupTag and parse kwargs.
        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for VlanGroupTags class.")
        self.parse_kwargs(**kwargs)
        self.type = "VlanGroupTag"

    def named_vlantags(self, action, name=""):
        """
        Associate Named VLAN Tags.

        :param action: (str) 'add', 'remove', or 'clear'.
        :param name: (str) Name of VLAN Tags.
        """
        logging.debug("In named_vlantags() for VlanGroupTags class.")
        if action == "add":
            vlan1 = VlanTags(fmc=self.fmc)
            response = vlan1.get()
            if "items" in response:
                new_vlan = None
                for item in response["items"]:
                    if item["name"] == name:
                        new_vlan = {
                            "name": item["name"],
                            "id": item["id"],
                            "type": item["type"],
                        }
                        break
                if new_vlan is None:
                    logging.warning(
                        f'VlanTag "{name}" is not found in FMC.  Cannot add to VlanGroupTags.'
                    )
                else:
                    if "objects" in self.__dict__:
                        duplicate = False
                        for obj in self.objects:
                            if obj["name"] == new_vlan["name"]:
                                duplicate = True
                                break
                        if not duplicate:
                            self.objects.append(new_vlan)
                            logging.info(f'Adding "{name}" to VlanGroupTags.')
                    else:
                        self.objects = [new_vlan]
                        logging.info(f'Adding "{name}" to VlanGroupTags.')
        elif action == "remove":
            if "objects" in self.__dict__:
                objects_list = []
                for obj in self.objects:
                    if obj["name"] != name:
                        objects_list.append(obj)
                self.objects = objects_list
                logging.info(f'Removed "{name}" from VlanGroupTags.')
            else:
                logging.info(
                    "This VlanGroupTags has no named_vlantags.  Nothing to remove."
                )
        elif action == "clear":
            if "objects" in self.__dict__:
                del self.objects
                logging.info("All named_vlantags removed from this VlanGroupTags.")

    def unnamed_vlantags(self, action, startvlan="", endvlan=""):
        """
        Associate Unnamed VLAN Tags.

        :param action: (str) 'add', 'remove', or 'clear'
        :param startvlan: (int) Lower VLAN.
        :param endvlan: (int) Upper VLAN.
        """
        logging.debug("In unnamed_vlantags() for VlanGroupTags class.")
        if action == "add":
            startvlan, endvlan = validate_vlans(start_vlan=startvlan, end_vlan=endvlan)
            new_literal = {"startTag": startvlan, "endTag": endvlan, "type": ""}
            if "literals" in self.__dict__:
                duplicate = False
                for obj in self.literals:
                    if (
                        obj["startTag"] == new_literal["startTag"]
                        and obj["endTag"] == new_literal["endTag"]
                    ):
                        duplicate = True
                        break
                if not duplicate:
                    self.literals.append(new_literal)
                    logging.info(f'Adding "{startvlan}/{endvlan}" to VlanGroupTags.')
            else:
                self.literals = [new_literal]
                logging.info(f'Adding "{startvlan}/{endvlan}" to VlanGroupTags.')
        elif action == "remove":
            startvlan, endvlan = validate_vlans(start_vlan=startvlan, end_vlan=endvlan)
            if "literals" in self.__dict__:
                literals_list = []
                for obj in self.literals:
                    if obj["startTag"] != startvlan and obj["endTag"] != endvlan:
                        literals_list.append(obj)
                self.literals = literals_list
                logging.info(f'Removed "{startvlan}/{endvlan}" from VlanGroupTags.')
            else:
                logging.info(
                    "This VlanGroupTag has no unnamed_vlantags.  Nothing to remove."
                )
        elif action == "clear":
            if "literals" in self.__dict__:
                del self.literals
                logging.info("All unnamed_vlantags removed from this VlanGroupTags.")
