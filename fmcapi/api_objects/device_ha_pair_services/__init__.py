"""Device HA Pair Services Classes."""

import logging
from .ftddevicehapairs import FTDDeviceHAPairs
from .failoverinterfacemacaddressconfigs import FailoverInterfaceMACAddressConfigs
from .monitoredinterfaces import MonitoredInterfaces

logging.debug("In the device_ha_pair_services __init__.py file.")

__all__ = [
    "FTDDeviceHAPairs",
    "FailoverInterfaceMACAddressConfigs",
    "MonitoredInterfaces",
]
