from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .ftdnatpolicies import FTDNatPolicies
import logging


class NatRules(APIClassTemplate):
    """
    The NatRules Object in the FMC.
    """

    PREFIX_URL = '/policy/ftdnatpolicies'
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for NatRules class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for NatRules class.")
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
        logging.debug("In parse_kwargs() for NatRules class.")

    def nat_policy(self,name):
        logging.debug("In nat_policy() for NatRules class.")
        ftd_nat = FTDNatPolicies(fmc=self.fmc)
        ftd_nat.get(name=name)
        if 'id' in ftd_nat.__dict__:
            self.nat_id = ftd_nat.id
            self.URL = f'{self.fmc.configuration_url}{self.PREFIX_URL}/{self.nat_id}/natrules'
            self.nat_added_to_url = True
        else:
            logging.warning(f'FTD NAT Policy {name} not found.  Cannot set up NatRules for NAT Policy.')

    def post(self):
        logging.info('POST method for API for NatRules not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for NatRules not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for NatRules not supported.')
        pass
