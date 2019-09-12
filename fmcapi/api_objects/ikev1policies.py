from .apiclasstemplate import APIClassTemplate
import logging


class IKEv1Policies(APIClassTemplate):
    """
    The IKEv1Policies Object in the FMC.
    """

    URL_SUFFIX = '/object/ikev1policies'
    REQUIRED_FOR_POST = ['name',
                         'encryption',
                         'hash',
                         'diffieHellmanGroup',
                         'lifetimeInSeconds',
                         'authenticationMethod']
    VALID_FOR_ENCRYPTION = ['DES', '3DES', 'AES-128', 'AES-192', 'AES-256']
    VALID_FOR_HASH = ['MD5', 'SHA']
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""
    FIRST_SUPPORTED_FMC_VERSION = '6.3'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for IKEv1Policies class.")
        self.parse_kwargs(**kwargs)
        self.type = 'Ikev1PolicyObject'

    def format_data(self):
        logging.debug("In format_data() for IKEv1Policies class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'encryption' in self.__dict__:
            if self.encryption in self.VALID_FOR_ENCRYPTION:
                json_data['encryption'] = self.encryption
            else:
                logging.warning(f'encryption "{self.encryption}" not a valid type.')
        if 'hash' in self.__dict__:
            if self.hash in self.VALID_FOR_HASH:
                json_data['hash'] = self.hash
            else:
                logging.warning(f'hash "{self.hash}" not a valid type.')
        if 'priority' in self.__dict__:
            json_data['priority'] = self.priority
        if 'diffieHellmanGroup' in self.__dict__:
            json_data['diffieHellmanGroup'] = self.diffieHellmanGroup
        if 'authenticationMethod' in self.__dict__:
            json_data['authenticationMethod'] = self.authenticationMethod
        if 'lifetimeInSeconds' in self.__dict__:
            json_data['lifetimeInSeconds'] = self.lifetimeInSeconds
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for IKEv1Policies class.")
        if 'encryption' in kwargs:
            self.encryption = kwargs['encryption']
        if 'hash' in kwargs:
            self.hash = kwargs['hash']
        if 'priority' in kwargs:
            self.priority = kwargs['priority']
        if 'diffieHellmanGroup' in kwargs:
            self.diffieHellmanGroup = kwargs['diffieHellmanGroup']
        if 'authenticationMethod' in kwargs:
            self.authenticationMethod = kwargs['authenticationMethod']
        if 'lifetimeInSeconds' in kwargs:
            self.lifetimeInSeconds = kwargs['lifetimeInSeconds']
