"""Device Services Classes."""

import logging
from .bridgegroupinterfaces import BridgeGroupInterfaces
from .devicerecords import DeviceRecords
from .etherchannelinterfaces import EtherchannelInterfaces
from .ipv4staticroutes import IPv4StaticRoutes
from .ipv6staticroutes import IPv6StaticRoutes
from .physicalinterfaces import PhysicalInterfaces
from .redundantinterfaces import RedundantInterfaces
from .staticroutes import StaticRoutes
from .subinterfaces import SubInterfaces

logging.debug("In the device_services __init__.py file.")

__all__ = [
    "DeviceRecords",
    "StaticRoutes",
    "IPv4StaticRoutes",
    "IPv6StaticRoutes",
    "PhysicalInterfaces",
    "BridgeGroupInterfaces",
    "RedundantInterfaces",
    "EtherchannelInterfaces",
    "SubInterfaces",
]
