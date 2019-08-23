from .apiclasstemplate import APIClassTemplate
import logging


class ICMPv4Object(APIClassTemplate):
    """
    The ICMPv4Object Object in the FMC.
    """

    URL_SUFFIX = '/object/icmpv4objects'
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ICMPv4Object class.")
        self.parse_kwargs(**kwargs)
        self.type = 'ICMPV4Object'

    def format_data(self):
        logging.debug("In format_data() for ICMPv4Object class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'overrideTargetId' in self.__dict__:
            json_data['overrideTargetId'] = self.overrideTargetId
        if 'code' in self.__dict__:
            json_data['code'] = self.code
        if 'icmpType' in self.__dict__:
            json_data['icmpType'] = self.icmpType
        if 'overrides' in self.__dict__:
            json_data['overrides'] = self.overrides
        if 'overridable' in self.__dict__:
            json_data['overridable'] = self.overridable
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for ICMPv4Object class.")
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
