from .apiclasstemplate import APIClassTemplate
from .accesscontrolpolicy import AccessControlPolicy
import logging


class HitCount(APIClassTemplate):
    """
    The HitCount Object in the FMC.
    """

    PREFIX_URL = '/policy/accesspolicies/'
    REQUIRED_FOR_PUT = ['acp_id']
    REQUIRED_FOR_DELETE = ['acp_id']
    REQUIRED_FOR_GET = ['acp_id']
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for HitCount class.")
        self.parse_kwargs(**kwargs)
        self.type = 'HitCount'
        self.filter = {}

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for HitCount class.")

    def acp(self, name='', acp_id=''):
        # either name or id of the ACP should be given
        logging.debug("In acp() for HitCount class.")
        if acp_id != '':
            self.acp_id = acp_id
            self.URL = f'{self.fmc.configuration_url}{self.PREFIX_URL}/{self.acp_id}/operational/hitcounts'
            self.acp_added_to_url = True
        elif name != '':
            acp1 = AccessControlPolicy(fmc=self.fmc)
            acp1.get(name=name)
            if 'id' in acp1.__dict__:
                self.acp_id = acp1.id
                self.URL = f'{self.fmc.configuration_url}{self.PREFIX_URL}/{self.acp_id}/operational/hitcounts'
                self.acp_added_to_url = True
            else:
                logging.warning(f'Access Control Policy {name} not found.  Cannot set up accessPolicy for HitCount.')
        else:
            logging.error('No accessPolicy name or ID was provided.')

    def filter(self):
        logging.debug("In filter() for HitCount class")


    def post(self):
        logging.info('API POST method for HitCount not supported.')
        pass
