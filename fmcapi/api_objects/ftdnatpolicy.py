from .apiclasstemplate import APIClassTemplate
import logging


class FTDNatPolicy(APIClassTemplate):
    """
    The FTDNATPolicy Object in the FMC.
    """

    URL_SUFFIX = '/policy/ftdnatpolicies'
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for FTDNatPolicy class.")
        self.parse_kwargs(**kwargs)
        self.type = "FTDNatPolicy"

    def format_data(self):
        logging.debug("In format_data() for FTDNatPolicy class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for FTDNatPolicy class.")
