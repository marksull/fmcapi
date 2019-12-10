"""Device Group Services Classes."""

import logging
from .devicegrouprecords import DeviceGroupRecords
from .devicegrouprecords import DeviceGroups

logging.debug("In the device_group_services __init__.py file.")

__all__: ["DeviceGroupRecords", "DeviceGroups"]
