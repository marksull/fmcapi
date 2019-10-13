from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class IKEv1Policies(APIClassTemplate):
    """
    The IKEv1Policies Object in the FMC.
    """

    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
        "encryption",
        "hash",
        "priority",
        "diffieHellmanGroup",
        "authenticationMethod",
        "lifetimeInSeconds",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/ikev1policies"
    REQUIRED_FOR_POST = [
        "name",
        "encryption",
        "hash",
        "diffieHellmanGroup",
        "lifetimeInSeconds",
        "authenticationMethod",
    ]
    VALID_FOR_ENCRYPTION = ["DES", "3DES", "AES-128", "AES-192", "AES-256"]
    VALID_FOR_HASH = ["MD5", "SHA"]
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""
    FIRST_SUPPORTED_FMC_VERSION = "6.3"

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for IKEv1Policies class.")
        self.parse_kwargs(**kwargs)
        self.type = "Ikev1PolicyObject"

    def format_data(self):
        json_data = super().format_data()
        logging.debug("In format_data() for IKEv1Policies class.")
        if "encryption" in self.__dict__:
            if self.encryption in self.VALID_FOR_ENCRYPTION:
                json_data["encryption"] = self.encryption
            else:
                logging.warning(f'encryption "{self.encryption}" not a valid type.')
        if "hash" in self.__dict__:
            if self.hash in self.VALID_FOR_HASH:
                json_data["hash"] = self.hash
            else:
                logging.warning(f'hash "{self.hash}" not a valid type.')
        return json_data
