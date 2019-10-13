from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging
import warnings


class SecurityZones(APIClassTemplate):
    """
    The SecurityZones Object in the FMC.
    """

    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
        "description",
        "interfaceMode",
        "interfaces",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/securityzones"
    REQUIRED_FOR_POST = ["name", "interfaceMode"]
    FILTER_BY_NAME = True

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for SecurityZones class.")
        self.parse_kwargs(**kwargs)

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for SecurityZones class.")
        if "interfaceMode" in kwargs:
            self.interfaceMode = kwargs["interfaceMode"]
        else:
            self.interfaceMode = "ROUTED"


class SecurityZone(SecurityZones):
    """Dispose of this Class after 20210101."""

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn(
            "Deprecated: SecurityZone() should be called via SecurityZones()."
        )
        super().__init__(fmc, **kwargs)
