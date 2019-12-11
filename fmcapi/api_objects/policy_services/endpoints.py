"""Endpoints Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .ftds2svpns import FTDS2SVPNs
from fmcapi.api_objects.object_services.fqdns import FQDNS
from fmcapi.api_objects.object_services.hosts import Hosts
from fmcapi.api_objects.object_services.networks import Networks
from fmcapi.api_objects.object_services.networkgroups import NetworkGroups
from fmcapi.api_objects.device_ha_pair_services.ftddevicehapairs import FTDDeviceHAPairs
from fmcapi.api_objects.device_services.devicerecords import DeviceRecords
from fmcapi.api_objects.device_services.etherchannelinterfaces import (
    EtherchannelInterfaces,
)
from fmcapi.api_objects.device_services.physicalinterfaces import PhysicalInterfaces
from fmcapi.api_objects.device_services.redundantinterfaces import RedundantInterfaces
from fmcapi.api_objects.device_services.subinterfaces import SubInterfaces
import logging


class Endpoints(APIClassTemplate):
    """The Endpoints Object in the FMC."""

    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
        "device",
        "interface",
        "nattedInterfaceAddress",
        "protectedNetworks",
        "ipv6InterfaceAddress",
        "connectionType",
        "peerType",
        "extranet",
        "extranetInfo",
        "description",
        "version",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    FIRST_SUPPORTED_FMC_VERSION = "6.3"
    VALID_FOR_POINT_TO_POINT = ["PEER"]
    VALID_FOR_HUB_AND_SPOKE = ["HUB", "SPOKE"]
    PREFIX_URL = "/policy/ftds2svpns"
    REQUIRED_FOR_POST = ["vpn_id"]

    def __init__(self, fmc, **kwargs):
        """
        Initialize Endpoints object.

        Set self.type to "Endpoint" and parse the kwargs.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Endpoints class.")
        self.parse_kwargs(**kwargs)
        self.type = "EndPoint"

    def vpn_policy(self, pol_name):
        """
        Associate a VPN Policy.

        :param pol_name: (str) Name of VPN Policy.
        :return: None
        """
        logging.debug("In vpn_policy() for Endpoints class.")
        ftd_s2s = FTDS2SVPNs(fmc=self.fmc)
        ftd_s2s.get(name=pol_name)
        if "id" in ftd_s2s.__dict__:
            self.vpn_id = ftd_s2s.id
            self.URL = (
                f"{self.fmc.configuration_url}{self.PREFIX_URL}/{self.vpn_id}/endpoints"
            )
            self.vpn_added_to_url = True
            self.topology_type = ftd_s2s.topologyType
        else:
            logging.warning(
                f'FTD S2S VPN Policy "{pol_name}" not found.  '
                f"Cannot set up Endpoints for FTDS2SVPNs Policy."
            )

    def endpoint(self, action, device_name):
        """
        Associate an endpoint.

        :param action: (str) 'add', 'remove', or 'clear'
        :param device_name: (str) Name of device.
        """
        logging.debug("In endpoint() for Endpoints class.")
        device_json = DeviceRecords(fmc=self.fmc).get()
        device_ha_json = FTDDeviceHAPairs(fmc=self.fmc).get()
        items = device_json.get("items", []) + device_ha_json.get("items", [])
        new_device = None

        if action == "add":
            for item in items:
                if item["name"] == device_name:
                    new_device = {
                        "name": item["name"],
                        "id": item["id"],
                        "type": item["type"],
                    }
                    break
            if new_device is None:
                logging.warning(
                    f'Device/DeviceHA "{device_name}" is not found in FMC.  Cannot add to Endpoints.'
                )
            else:
                if "device" in self.__dict__:
                    self.device.append(new_device)
                    logging.info(f'Adding "{device_name}" to Endpoints.')
                else:
                    self.device = new_device
        elif action == "remove":
            if "device" in self.__dict__:
                self.device = list(
                    filter(lambda i: i["name"] != device_name, self.device)
                )
            else:
                logging.warning("Endpoints has no members.  Cannot remove device.")
        elif action == "clear":
            if "device" in self.__dict__:
                del self.device

    def vpn_interface(self, device_name, ifname):
        """
        Associate an interface.

        :param device_name: (str) Name of device.
        :param ifname: (str) Name of interface.
        """
        logging.debug("In vpn_interface() for Endpoints class.")
        ether_json = EtherchannelInterfaces(fmc=self.fmc, device_name=device_name).get()
        phys_json = PhysicalInterfaces(fmc=self.fmc, device_name=device_name).get()
        redund_json = RedundantInterfaces(fmc=self.fmc, device_name=device_name).get()
        subintf_json = SubInterfaces(fmc=self.fmc, device_name=device_name).get()
        items = (
            ether_json.get("items", [])
            + phys_json.get("items", [])
            + redund_json.get("items", [])
            + subintf_json.get("items", [])
        )
        new_intf = None
        for item in items:
            if item["ifname"] == ifname:
                new_intf = {"id": item["id"], "type": item["type"]}
                break
        if new_intf is None:
            logging.warning(
                f'Interface "{ifname}" is not found in FMC.  Cannot add to interface.'
            )
        else:
            self.interface = new_intf
            logging.info(f'Interface "{ifname}" added.')

    def encryption_domain(self, action, names=[]):
        """
        Associate Encryption.

        :param action: (str) 'add', 'remove', or 'clear'.
        :param names: (list) List of Encryption names.
        """
        logging.debug("In endpoint() for Endpoints class.")
        fqdns_json = FQDNS(fmc=self.fmc).get()
        host_json = Hosts(fmc=self.fmc).get()
        net_json = Networks(fmc=self.fmc).get()
        netg_json = NetworkGroups(fmc=self.fmc).get()
        items = (
            fqdns_json.get("items", [])
            + host_json.get("items", [])
            + net_json.get("items", [])
            + netg_json.get("items", [])
        )
        new_network = None

        if action == "add":
            for name in names:
                for item in items:
                    if item["name"] == name:
                        new_network = {"id": item["id"], "type": item["type"]}
                        break
                if new_network is None:
                    logging.warning(
                        f'FQDNS/Host/Network/Network Group"{name}" is not found in FMC.'
                        f"  Cannot add to protectedNetworks."
                    )
                else:
                    if "protectedNetworks" in self.__dict__:
                        self.protectedNetworks["networks"].append(new_network)
                        logging.info(f'Appending "{name}" to protectedNetworks.')
                    else:
                        self.protectedNetworks = {"networks": [new_network]}
                        logging.info(f'Adding "{name}" to protectedNetworks.')
        elif action == "remove":
            if "protectedNetworks" in self.__dict__:
                for name in names:
                    self.protectedNetworks = list(
                        filter(lambda i: i["name"] != name, self.protectedNetworks)
                    )
            else:
                logging.warning(
                    "protectedNetworks has no members.  Cannot remove network."
                )
        elif action == "clear":
            if "protectedNetworks" in self.__dict__:
                del self.protectedNetworks
