"""IKE v1 IPSec Proposals Object Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class IKEv1IpsecProposals(APIClassTemplate):
    """The IKEv1IpsecProposals Object in the FMC."""

    VALID_JSON_DATA = ["id", "name", "type", "espEncryption", "espHash"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/ikev1ipsecproposals"
    REQUIRED_FOR_POST = ["name", "espEncryption", "espHash"]
    VALID_FOR_ENCRYPTION = ["DES", "3DES", "AES-128", "AES-192", "AES-256", "ESP-NULL"]
    VALID_FOR_HASH = ["NONE", "MD5", "SHA"]
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""
    FIRST_SUPPORTED_FMC_VERSION = "6.3"

    def __init__(self, fmc, **kwargs):
        """
        Initialize IKEv1IpsecProposals object.

        Set self.type to "IKEv1IpsecProposal" and  parse the kwargs.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for IKEv1IpsecProposals class.")
        self.parse_kwargs(**kwargs)
        self.type = "IKEv1IPsecProposal"
