from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class FTDS2SVPNs(APIClassTemplate):
    """
    The FTDS2SVPNs Object in the FMC.
    """

    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
        "ipsecSettings",
        "endpoints",
        "ikeSettings",
        "advancedSettings",
        "description",
        "ikeV2Enabled",
        "ikeV1Enabled",
        "topologyType",
        "version",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    FIRST_SUPPORTED_FMC_VERSION = "6.3"
    URL_SUFFIX = "/policy/ftds2svpns"
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for FTDNatPolicies class.")
        self.parse_kwargs(**kwargs)
        self.type = "FTDS2SVpn"
