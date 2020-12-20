"""ICMPv6 Objects Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class ICMPv6Objects(APIClassTemplate):
    """The ICMPv6Objects Object in the FMC."""

    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
        "overrideTargetId",
        "code",
        "icmpType",
        "overrides",
        "overridable",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/icmpv6objects"
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        """
        Initialize ICMPv6Objects object.

        Set self.type to "ICMPv6Object" and parse the kwargs.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ICMPv6Objects class.")
        self.parse_kwargs(**kwargs)
        self.type = "ICMPV6Object"
