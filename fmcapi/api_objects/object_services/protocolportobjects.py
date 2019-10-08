from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging
import warnings


class ProtocolPortObjects(APIClassTemplate):
    """
    The ProtocolPortObjects in the FMC.
    """

    VALID_JSON_DATA = ["id", "name", "description", "port", "protocol", "type"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/protocolportobjects"
    REQUIRED_FOR_POST = ["name", "port", "protocol"]

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ProtocolPortObjects class.")
        self.parse_kwargs(**kwargs)


class ProtocolPort(ProtocolPortObjects):
    """Dispose of this Class after 20210101."""

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn(
            "Deprecated: ProtocolPort() should be called via ProtocolPortObjects()."
        )
        super().__init__(fmc, **kwargs)
