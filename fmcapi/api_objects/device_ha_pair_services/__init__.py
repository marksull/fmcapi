"""Device HA Pair Services Classes."""

import logging
from .ftddevicehapairs import FTDDeviceHAPairs
from .ftddevicehapairs import DeviceHAPairs
from .failoverinterfacemacaddressconfigs import FailoverInterfaceMACAddressConfigs
from .failoverinterfacemacaddressconfigs import DeviceHAFailoverMAC
from .monitoredinterfaces import DeviceHAMonitoredInterfaces
from .monitoredinterfaces import MonitoredInterfaces

logging.debug("In the device_ha_pair_services __init__.py file.")

__all__ = [
    "FTDDeviceHAPairs",
    "DeviceHAPairs",
    "FailoverInterfaceMACAddressConfigs",
    "DeviceHAFailoverMAC",
    "DeviceHAMonitoredInterfaces",
    "MonitoredInterfaces",
]
