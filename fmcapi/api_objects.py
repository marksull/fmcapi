"""
This module contains the class objects that represent the various objects in the FMC.
"""

import logging
import datetime
import requests
from .helper_functions import *


class Token(object):
    """
    The token is the validation object used with the FMC.

    """

    MAX_REFRESHES = 3
    TOKEN_LIFETIME = 60 * 30
    API_PLATFORM_VERSION = 'api/fmc_platform/v1'

    def __init__(self, host='192.168.45.45', username='admin', password='Admin123', verify_cert=False):
        """
        Initialize variables used in the Token class.
        :param host:
        :param username:
        :param password:
        :param verify_cert:
        """
        logging.debug("In the Token __init__() class method.")

        self.__host=host
        self.__username=username
        self.__password=password
        self.verify_cert=verify_cert
        self.token_expiry = None
        self.token_refreshes = 0
        self.access_token = None
        self.uuid = None
        self.generate_tokens()

    def generate_tokens(self):
        """
        Create new and refresh expired tokens.
        :return:
        """
        logging.debug("In the Token generate_tokens() class method.")

        if self.token_refreshes <= self.MAX_REFRESHES and self.access_token is not None:
            headers = {'Content-Type': 'application/json', 'X-auth-access-token': self.access_token,
                       'X-auth-refresh-token': self.refresh_token}
            url = 'https://{}/{}/auth/refreshtoken'.format(self.__host, self.API_PLATFORM_VERSION)
            logging.info("Refreshing tokens, {} out of {} refreshes, from {}.".format(self.token_refreshes,
                                                                                      self.MAX_REFRESHES, url))
            response = requests.post(url, headers=headers, verify=self.verify_cert)
            self.token_refreshes += 1
        else:
            headers = {'Content-Type': 'application/json'}
            url = 'https://{}/{}/auth/generatetoken'.format(self.__host, self.API_PLATFORM_VERSION)
            logging.info("Requesting new tokens from {}.".format(url))
            response = requests.post(url, headers=headers,
                                     auth=requests.auth.HTTPBasicAuth(self.__username, self.__password),
                                     verify=self.verify_cert)
            self.token_refreshes = 0
        self.access_token = response.headers.get('X-auth-access-token')
        self.refresh_token = response.headers.get('X-authrefresh-token')
        self.token_expiry = datetime.datetime.now() + datetime.timedelta(seconds=self.TOKEN_LIFETIME)
        self.uuid = response.headers.get('DOMAIN_UUID')

    def get_token(self):
        """
        Check validity of current token.  If needed make a new or resfresh.  Then return access_token.
        :return:
        """
        logging.debug("In the Token get_token() class method.")

        if datetime.datetime.now() > self.token_expiry:
            logging.info("Token Expired.")
            self.generate_tokens()
        return self.access_token
