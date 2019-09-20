from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class IKEv1IpsecProposals(APIClassTemplate):
    """
    The IKEv1IpsecProposals Object in the FMC.
    """

    URL_SUFFIX = '/object/ikev1ipsecproposals'
    REQUIRED_FOR_POST = ['name', 'espEncryption', 'espHash']
    VALID_FOR_ENCRYPTION = ['DES', '3DES', 'AES-128', 'AES-192', 'AES-256', 'ESP-NULL']
    VALID_FOR_HASH = ['NONE', 'MD5', 'SHA']
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""
    FIRST_SUPPORTED_FMC_VERSION = '6.3'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for IKEv1IpsecProposals class.")
        self.parse_kwargs(**kwargs)
        self.type = 'IKEv1IPsecProposal'

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for IKEv1IpsecProposals class.")
        if 'espEncryption' in kwargs:
            self.espEncryption = kwargs['espEncryption']
        if 'espHash' in kwargs:
            self.espHash = kwargs['espHash']
