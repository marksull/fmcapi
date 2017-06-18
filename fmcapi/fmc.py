"""
This module (fmc.py) is designed to provide a "toolbox" of tools for interacting with the Cisco FMC API.
The "toolbox" is the FMC class and the "tools" are its methods.

Note: There exists a "Quick Start Guide" for the Cisco FMC API too.  Just Google for it as it gets updated with each
 release of code.
"""

import logging
import datetime
import json
import requests
import time
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from .helper_functions import *
from .api_objects import *
from . import export

# Disable annoying HTTP warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

""""
The 'requests' package is very chatty on the INFO logging level.  Change its logging threshold sent to logger to 
something greater than INFO (i.e. not INFO or DEBUG) will cause it to not log its INFO and DEBUG messages to the 
default logger.  This reduces the size of our log files.
"""
logging.getLogger("requests").setLevel(logging.WARNING)


@export
class FMC(object):
    """
The FMC class has a series of methods, lines that start with "def", that are used to interact with the Cisco FMC
via its API.  Each method has its own DOCSTRING (like this triple quoted text here) describing its functionality.
    """
    logging.debug("In the FMC() class.")

    API_CONFIG_VERSION = 'api/fmc_config/v1'
    API_PLATFORM_VERSION = 'api/fmc_platform/v1'
    VERIFY_CERT = False
    MAX_PAGING_REQUESTS = 100

    def __init__(self, host='192.168.45.45', username='admin', password='Admin123', autodeploy=True):
        """
        Instantiate some variables prior to calling the __enter__() method.
        :param host:
        :param username:
        :param password:
        :param autodeploy:
        """
        logging.debug("In the FMC __init__() class method.")

        self.host = host
        self.username = username
        self.password = password
        self.autodeploy = autodeploy

    def __enter__(self):
        """
        Get a token from the FMC as well as the Global UUID.  With this information set up the base_url variable.
        :return:
        """
        logging.debug("In the FMC __enter__() class method.")
        self.mytoken = Token(host=self.host, username=self.username, password=self.password, verify_cert=self.VERIFY_CERT)
        self.uuid = self.mytoken.uuid
        self.build_urls()
        self.version()
        return self

    def __exit__(self, *args):
        """
        If autodeploy == True push changes to FMC upon exit of "with" contract.
        :param args:
        :return:
        """
        logging.debug("In the FMC __exit__() class method.")

        if self.autodeploy:
            self.deploy_changes()
        else:
            logging.info("Auto deploy changes set to False.  "
                         "Use the Deploy button in FMC to push changes to FTDs.\n\n")

    def build_urls(self):
        """
        The FMC APIs appear to use 2 base URLs, depending on what that API is for.  One for "configuration" and the
        other for FMC "platform" things.
        """
        logging.debug("In the FMC build_urls() class method.")
        logging.info('Building base to URLs.')
        self.configuration_url = "https://{}/{}/domain/{}".format(self.host, self.API_CONFIG_VERSION, self.uuid)
        self.platform_url = "https://{}/{}".format(self.host, self.API_PLATFORM_VERSION)

    def send_to_api(self, method='', url='', headers='', json_data=None, more_items=[]):
        """
        Using the "method" type, send a request to the "url" with the "json_data" as the payload.
        :param method:
        :param url:
        :param json_data:
        :return:
        """
        logging.debug("In the FMC send_to_api() class method.")

        if not more_items:
            self.more_items = []
            self.page_counter = 0
        if headers == '':
            # These values for headers works for most API requests.
            headers = {'Content-Type': 'application/json', 'X-auth-access-token': self.mytoken.get_token()}
        status_code = 429
        response = None
        json_response = None
        try:
            while status_code == 429:
                if method == 'get':
                    response = requests.get(url, headers=headers, verify=self.VERIFY_CERT)
                elif method == 'post':
                    response = requests.post(url, json=json_data, headers=headers, verify=self.VERIFY_CERT)
                elif method == 'put':
                    response = requests.put(url, json=json_data, headers=headers, verify=self.VERIFY_CERT)
                elif method == 'delete':
                    response = requests.delete(url, headers=headers, verify=self.VERIFY_CERT)
                else:
                    logging.error("No request method given.  Returning nothing.")
                    return
                status_code = response.status_code
                if status_code == 429:
                    logging.warning("Too many connections to the FMC.  Waiting 30 seconds and trying again.")
                    time.sleep(30)
            json_response = json.loads(response.text)
            if status_code > 301 or 'error' in json_response:
                response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logging.error("Error in POST operation --> {}".format(str(err)))
            logging.error("json_response -->\t{}".format(json_response))
        if response:
            response.close()
        try:
            if 'next' in json_response['paging'] and self.page_counter <= self.MAX_PAGING_REQUESTS:
                self.more_items += json_response['items']
                logging.info('Paging:  Offset:{}, Limit:{}, Count:{}, Gathered_Items:{}'.
                             format(json_response['paging']['offset'],
                                    json_response['paging']['limit'],
                                    json_response['paging']['count'],
                                    len(self.more_items)))
                self.page_counter += 1
                return self.send_to_api(method=method,
                                 url=json_response['paging']['next'][0],
                                 json_data=json_data,
                                 more_items=self.more_items)
            else:
                json_response['items'] += self.more_items
                self.more_items = []
                return json_response
        except KeyError:
            return json_response

    def version(self):
        """
        Get the FMC's version information.  Set instance variables for each version info returned as well as return
        the whole response text.
        :return:
        """
        logging.debug("In the FMC version() class method.")
        logging.info('Collecting version information from FMC.')

        url_suffix = '/info/serverversion'
        url = '{}{}'.format(self.platform_url, url_suffix)

        response = self.send_to_api(method='get', url=url)
        if 'items' in response:
            logging.info('Populating vdbVersion, sruVersion, serverVersion, and geoVersion FMC instance variables.')
            self.vdbVersion = response['items'][0]['vdbVersion']
            self.sruVersion = response['items'][0]['sruVersion']
            self.serverVersion = response['items'][0]['serverVersion']
            self.geoVersion = response['items'][0]['geoVersion']
        return response

    def audit(self, **kwargs):
        '''
        This API function supports filtering the GET query URL with: username, subsystem, source, starttime, and
        endtime parameters.
        :return: response
        '''
        url_parameters = '?'
        if 'username' in kwargs:
            url_parameters = '{}&username={}'.format(url_parameters, kwargs['username'])
        if 'subsystem' in kwargs:
            url_parameters = '{}&subsystem={}'.format(url_parameters, kwargs['subsystem'])
        if 'source' in kwargs:
            url_parameters = '{}&source={}'.format(url_parameters, kwargs['source'])
        if 'starttime' in kwargs:
            url_parameters = '{}&starttime={}'.format(url_parameters, kwargs['starttime'])
        if 'endtime' in kwargs:
            url_parameters = '{}&endtime={}'.format(url_parameters, kwargs['endtime'])

        url_suffix = '/audit/auditrecords'
        url = '{}/domain/{}{}{}'.format(self.platform_url, self.uuid, url_suffix, url_parameters)

        response = self.send_to_api(method='get', url=url)
        return  response

    def get_deployable_devices(self):
        """
        Collect a list of FMC managed devices who's configuration is not up-to-date.
        :return: List of devices needing updates.
        """
        logging.debug("In the FMC get_deployable_devices() class method.")

        waittime = 15
        logging.info("Waiting {} seconds to allow the FMC to update the list of deployable devices.".format(waittime))
        time.sleep(waittime)
        logging.info("Getting a list of deployable devices.")
        url = "/deployment/deployabledevices?expanded=true"
        response = self.send_to_api(method='get', url=url)
        # Now to parse the response list to get the UUIDs of each device.
        if 'items' not in response:
            return
        uuids = []
        for item in response['items']:
            if not item['canBeDeployed']:
                pass
            else:
                uuids.append(item['device']['id'])
        return uuids

    def deploy_changes(self):
        """
        Iterate through the list of devices needing deployed and submit a request to the FMC to deploy changes to them.
        :return:
        """
        logging.debug("In the deploy_changes() class method.")

        url = "/deployment/deploymentrequests"
        devices = self.get_deployable_devices()
        if not devices:
            logging.info("No devices need deployed.\n\n")
            return
        nowtime = int(1000000 * datetime.datetime.now().timestamp())
        json_data = {
            'type': 'DeploymentRequest',
            'forceDeploy': True,
            'ignoreWarning': True,
            'version': nowtime,
            'deviceList': []
        }
        for device in devices:
            logging.info("Adding device {} to deployment queue.".format(device))
            json_data['deviceList'].append(device)
        logging.info("Deploying changes to devices.")
        response = self.send_to_api(method='post', url=url, json_data=json_data)
        return response['deviceList']


class Token(object):
    """
    The token is the validation object used with the FMC.

    """
    logging.debug("In the Token class.")

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

        self.__host = host
        self.__username = username
        self.__password = password
        self.verify_cert = verify_cert
        self.token_expiry = None
        self.token_refreshes = 0
        self.access_token = None
        self.uuid = None
        self.refresh_token = None
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
