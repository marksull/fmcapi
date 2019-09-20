from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging
import warnings


class ICMPv4Objects(APIClassTemplate):
    """
    The ICMPv4Objects Object in the FMC.
    """

    URL_SUFFIX = '/object/icmpv4objects'
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ICMPv4Objects class.")
        self.parse_kwargs(**kwargs)
        self.type = 'ICMPV4Object'

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for ICMPv4Objects class.")
        if 'overrideTargetId' in kwargs:
            self.overrideTargetId = kwargs['overrideTargetId']
        if 'code' in kwargs:
            self.code = kwargs['code']
        if 'icmpType' in kwargs:
            self.icmpType = kwargs['icmpType']
        if 'overrides' in kwargs:
            self.overrides = kwargs['overrides']
        if 'overridable' in kwargs:
            self.overridable = kwargs['overridable']


class ICMPv4Object(ICMPv4Objects):
    """Dispose of this Class after 20210101."""

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn("Deprecated: ICMPv4Object() should be called via ICMPv4Objects().")
        super().__init__(fmc, **kwargs)
