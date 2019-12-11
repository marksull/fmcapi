"""Device Services Classes."""

import logging
from .bridgegroupinterfaces import BridgeGroupInterfaces
from .devicerecords import Device
from .devicerecords import DeviceRecords
from .etherchannelinterfaces import EtherchannelInterfaces
from .ipv4staticroutes import IPv4StaticRoutes
from .ipv4staticroutes import IPv4StaticRoute
from .ipv6staticroutes import IPv6StaticRoutes
from .ipv6staticroutes import IPv6StaticRoute
from .physicalinterfaces import PhysicalInterfaces
from .physicalinterfaces import PhysicalInterface
from .redundantinterfaces import RedundantInterfaces
from .staticroutes import StaticRoutes
from .subinterfaces import SubInterfaces

logging.debug("In the device_services __init__.py file.")

__all__ = [
    "Device",
    "DeviceRecords",
    "StaticRoutes",
    "IPv4StaticRoutes",
    "IPv4StaticRoute",
    "IPv6StaticRoutes",
    "IPv6StaticRoute",
    "PhysicalInterfaces",
    "PhysicalInterface",
    "BridgeGroupInterfaces",
    "RedundantInterfaces",
    "EtherchannelInterfaces",
    "SubInterfaces",
]
