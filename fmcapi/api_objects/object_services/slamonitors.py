"""SLA Monitors Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .securityzones import SecurityZones
import logging


class SLAMonitors(APIClassTemplate):
    """The SLAMonitors Object in the FMC."""

    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
        "timeout",
        "threshold",
        "frequency",
        "slaId",
        "dataSize",
        "tos",
        "noOfPackets",
        "monitorAddress",
        "interfaceObjects",
        "description",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/slamonitors"
    REQUIRED_FOR_POST = ["name", "slaId", "monitorAddress", "interfaceObjects", "type"]
    REQUIRED_FOR_PUT = ["id", "type"]

    def __init__(self, fmc, **kwargs):
        """
        Initialize SLAMonitors object.

        Set self.type to "SLAMonitor" and parse the kwargs.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for SLAMonitors class.")
        self.parse_kwargs(**kwargs)
        self.type = "SLAMonitor"

    def interfaces(self, names):
        """
        Associate interfaces (AKA Security Zones).

        :param names: (list) List of Security Zone names.
        """
        logging.debug("In interfaces() for SLAMonitors class.")
        zones = []
        for name in names:
            # Supports passing list of str
            sz = SecurityZones(fmc=self.fmc)
            sz.get(name=name)
            if "id" in sz.__dict__:
                zones.append({"name": sz.name, "id": sz.id, "type": sz.type})
            else:
                logging.warning(
                    f'Security Zone, "{name}", not found.  Cannot add to SLAMonitors.'
                )
        if len(zones) != 0:
            # Make sure we found at least one zone
            self.interfaceObjects = zones
        else:
            logging.warning(
                f'No valid Security Zones found: "{names}".  Cannot add to SLAMonitosr.'
            )
