"""Interface Groups Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from fmcapi.api_objects.device_services.physicalinterfaces import PhysicalInterfaces
import logging


class InterfaceGroups(APIClassTemplate):
    """The InterfaceGroups Object in the FMC."""

    VALID_JSON_DATA = ["id", "name", "description", "interfaceMode", "interfaces"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/interfacegroups"
    REQUIRED_FOR_POST = ["name", "interfaceMode"]
    REQUIRED_FOR_PUT = ["id"]
    FILTER_BY_NAME = True

    def __init__(self, fmc, **kwargs):
        """
        Initialize InterfaceGroups object.

        Set self.type to "InterfaceGroup" and parse the kwargs.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for InterfaceGroups class.")
        self.parse_kwargs(**kwargs)
        self.type = "InterfaceGroup"

    def parse_kwargs(self, **kwargs):
        """
        Parse the kwargs and set self variables to match.

        :return: None
        """
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for InterfaceGroups class.")
        if "interfaceMode" in kwargs:
            self.interfaceMode = kwargs["interfaceMode"]
        else:
            self.interfaceMode = "ROUTED"

    def p_interface(self, device_name="", action="add", names=[]):
        """
        Associate Physical Interface.

        :param device_name: (str) Name of device.
        :param action: (str) 'add', 'remove', or 'clear'
        :param names: (list) List of interface names
        """
        logging.debug("In interfaces() for InterfaceGroups class.")
        if action == "add":
            intfs = []
            for name in names:
                intf = PhysicalInterfaces(fmc=self.fmc)
                intf.get(name=name, device_name=device_name)
                if "id" in intf.__dict__ and "ifname" in intf.__dict__:
                    intfs.append({"name": intf.name, "id": intf.id, "type": intf.type})
                elif "id" in intf.__dict__:
                    logging.warning(
                        f'PhysicalInterface, "{name}", found without logical ifname.  '
                        f"Cannot add to InterfaceGroups."
                    )
                else:
                    logging.warning(
                        f'PhysicalInterface, "{name}", not found.  Cannot add to InterfaceGroups.'
                    )
            if len(intfs) != 0:
                # Make sure we found at least one intf
                self.interfaces = intfs
            else:
                logging.warning(
                    f'No valid PhysicalInterface found: "{names}".  Cannot remove from InterfaceGroups.'
                )
        elif action == "remove":
            if "interfaces" in self.__dict__:
                intfs = []
                for interface in self.interfaces:
                    if interface["name"] not in names:
                        intfs.append(interface)
                    else:
                        logging.info(
                            f"""Removed "{interface['name']}" from InterfaceGroups."""
                        )
                self.interfaces = intfs
            else:
                logging.warning(
                    "This InterfaceObject has no interfaces.  Nothing to remove."
                )
        elif action == "clear" or action == "clear-all":
            if "interfaces" in self.__dict__:
                del self.interfaces
                logging.info(
                    "All PhysicalInterfaces removed from this InterfaceGroups."
                )
