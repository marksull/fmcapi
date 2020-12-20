"""
Establish and manage connection to FMC.

This module (fmc.py) is designed to provide a "toolbox" of tools for interacting with the Cisco FMC API.
The "toolbox" is the FMC class and the "tools" are its methods.  Note: There exists a "Quick Start Guide" for the Cisco
FMC API too.  Just Google for it as it gets updated with each release of code.
"""

import datetime
import requests
import time
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import logging
from logging.handlers import RotatingFileHandler
from .api_objects import ServerVersion
from .api_objects import DeploymentRequests
from sys import exit

# Disable annoying HTTP warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

""""
The 'requests' package is very chatty on the INFO logging level.  Change its logging threshold sent to logger to
something greater than INFO (i.e. not INFO or DEBUG) will cause it to not log its INFO and DEBUG messages to the
default logger.  This reduces the size of our log files.
"""
logging.getLogger("requests").setLevel(logging.WARNING)


class FMC(object):
    """Establish and maintain connection to Firepower Management Center."""

    logging.debug("In the FMC() class.")

    API_CONFIG_VERSION = "api/fmc_config/v1"
    API_PLATFORM_VERSION = "api/fmc_platform/v1"
    VERIFY_CERT = False
    MAX_PAGING_REQUESTS = 2000
    TOO_MANY_CONNECTIONS_TIMEOUT = 30
    FMC_MAX_PAYLOAD = 2048000

    def __init__(
        self,
        host="192.168.45.45",
        username="admin",
        password="Admin123",
        domain=None,
        autodeploy=True,
        file_logging=None,
        logging_level="INFO",
        debug=False,
        limit=1000,
    ):
        """
        Instantiate some variables prior to calling the __enter__() method.

        :param host (str): Hostname/IP of FMC (Default is 192.168.45.45)
        :param username (str): Admin for FMC (Default is admin)
        :param password (str): Admin Password (Default is Admin123)
        :param domain (str): UUID of domain (Default is None which implies the Global domain)
        :param autodeploy (bool): Deploy changes to affected FMC manage devices. (Default is True)
        :param file_logging (str): The filename (and optional path) of the output file if a file logger is required,
        None if no file logger is required. (Default is None)
        :param logging_level (str): The desired logging level. (Default is INFO)
        :param debug (bool): True to enable debug logging. (Default is False)
        :param limit (int): Sets up max data to gather per "page". (Default is 1000)
        :return: None
        """
        self.debug = debug
        if self.debug:
            logging_level = "DEBUG"
        root_logger = logging.getLogger("")
        if logging_level.upper() == "DEBUG":
            root_logger.setLevel(logging.DEBUG)
        if logging_level.upper() == "INFO":
            root_logger.setLevel(logging.INFO)
        if logging_level.upper() == "WARNING":
            root_logger.setLevel(logging.WARNING)
        if logging_level.upper() == "ERROR":
            root_logger.setLevel(logging.ERROR)
        if logging_level.upper() == "CRITICAL":
            root_logger.setLevel(logging.CRITICAL)

        if file_logging:
            print(
                f'Logging is enabled and set to {logging_level}.  Look for file "{file_logging}" for output.'
            )
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s:%(filename)s:%(lineno)s - %(message)s",
                "%Y/%m/%d-%H:%M:%S",
            )
            file_logger = RotatingFileHandler(
                file_logging, maxBytes=1024000, backupCount=10, mode="w"
            )
            file_logger.setFormatter(formatter)
            root_logger.addHandler(file_logger)

        logging.debug("In the FMC __init__() class method.")

        self.host = host
        self.username = username
        self.password = password
        self.domain = domain
        self.autodeploy = autodeploy
        self.limit = limit
        self.vdbVersion = None
        self.sruVersion = None
        self.serverVersion = None
        self.geoVersion = None
        self.configuration_url = None
        self.platform_url = None
        self.page_counter = None
        self.more_items = []

    def __enter__(self):
        """
        Get a token from the FMC as well as the Global UUID.  With this information set up the base_url variable.

        :return: self
        """
        logging.debug("In the FMC __enter__() class method.")
        self.mytoken = Token(
            host=self.host,
            username=self.username,
            password=self.password,
            domain=self.domain,
            verify_cert=self.VERIFY_CERT,
        )
        self.uuid = self.mytoken.uuid
        if self.mytoken.access_token:
            self.build_urls()

            version = ServerVersion(fmc=self)
            version.get()
            self.serverVersion = version.serverVersion
            logging.info(f"This FMC's version is {self.serverVersion}")

            return self
        else:
            logging.info("User authentication failed.")
            exit(1)

    def __exit__(self, *args):
        """
        If autodeploy == True, push changes to FMC upon exit of "with" contract.

        :param args:
        :return: None
        """
        logging.debug("In the FMC __exit__() class method.")

        if self.autodeploy:
            tmp = DeploymentRequests(fmc=self)
            tmp.post()
        else:
            logging.info(
                "Auto deploy changes set to False.  Use the Deploy button in FMC to push changes to FTDs."
            )

    def build_urls(self):
        """
        Build configuration_url and platform_url variables.

        :return: None
        """
        logging.debug("In the FMC build_urls() class method.")
        logging.info("Building base to URLs.")
        self.configuration_url = (
            f"https://{self.host}/{self.API_CONFIG_VERSION}/domain/{self.uuid}"
        )
        self.platform_url = f"https://{self.host}/{self.API_PLATFORM_VERSION}"

    def send_to_api(
        self, method="", url="", headers="", json_data=None, more_items=None
    ):
        """
        Send API call to FMC.

        :param method (str): GET, POST, PUT, or DELETE
        :param url (str): URL for API call.
        :param headers (str):  String of header variables.
        :param json_data (str):  JSON formatted string as payload. (Default is None)
        :param more_items (str):  Used for paging in query.
        :return: JSON response from FMC
        """
        logging.debug("In the FMC send_to_api() class method.")

        if not more_items:
            self.more_items = []
            self.page_counter = 0
        if headers == "":
            # These values for headers works for most API requests.
            headers = {
                "Content-Type": "application/json",
                "X-auth-access-token": self.mytoken.get_token(),
            }
        status_code = 429
        response = None
        json_response = None
        logging.debug(
            f"Being sent to FMC's API:\n\tHEADERS={headers}\n\tURL={url}\n\tMETHOD={method}\n\t"
            f"MORE_ITEMS={more_items}\n\tJSON_DATA={json_data}"
        )
        try:
            while status_code == 429:
                if method == "get":
                    response = requests.get(
                        url, headers=headers, verify=self.VERIFY_CERT
                    )
                elif method == "post":
                    response = requests.post(
                        url, json=json_data, headers=headers, verify=self.VERIFY_CERT
                    )
                elif method == "put":
                    response = requests.put(
                        url, json=json_data, headers=headers, verify=self.VERIFY_CERT
                    )
                elif method == "delete":
                    response = requests.delete(
                        url, headers=headers, verify=self.VERIFY_CERT
                    )
                else:
                    logging.error("No request method given.  Returning nothing.")
                    return
                if self.debug:
                    debug_msg = ["Response from FMC's API:"]
                    for response_var in dir(response):
                        if "__" not in response_var:
                            tmp_var = getattr(response, response_var)
                            debug_msg.append(f"\n\t{response_var}={tmp_var}")
                    logging.debug("".join(debug_msg))

                status_code = response.status_code
                if status_code == 429:
                    logging.warning(
                        f"Too many connections to the FMC.  Waiting {self.TOO_MANY_CONNECTIONS_TIMEOUT} "
                        f"seconds and trying again."
                    )
                    time.sleep(self.TOO_MANY_CONNECTIONS_TIMEOUT)
                if status_code == 401:
                    logging.warning("Token has expired. Trying to refresh.")
                    self.mytoken.access_token = None
                    self.mytoken.access_token = self.mytoken.get_token()
                    headers = {
                        "Content-Type": "application/json",
                        "X-auth-access-token": self.mytoken.access_token,
                    }
                    status_code = 429
                if status_code == 422:
                    logging.warning(
                        "Either:\n\t1. Payload too large.  FMC can only handle a payload of "
                        f"{self.FMC_MAX_PAYLOAD} bytes.\n\t2.The payload contains an unprocessable or "
                        f"unreadable entity such as a invalid attribut name or incorrect JSON syntax "
                    )
            json_response = json.loads(response.text)
            if status_code > 301 or "error" in json_response:
                response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logging.error(f"Error in POST operation --> {str(err)}")
            logging.error(f"json_response -->\t{json_response}")
            if response:
                response.close()
            return None
        if response:
            response.close()
        try:
            if (
                "next" in json_response["paging"]
                and self.page_counter <= self.MAX_PAGING_REQUESTS
            ):
                self.more_items += json_response["items"]
                logging.debug(
                    f"Paging:  Offset:{json_response['paging']['offset']}, "
                    f"Limit:{json_response['paging']['limit']}, "
                    f"Count:{json_response['paging']['count']}, "
                    f"Gathered_Items:{len(self.more_items)}."
                )
                self.page_counter += 1
                return self.send_to_api(
                    method=method,
                    url=json_response["paging"]["next"][0],
                    json_data=json_data,
                    more_items=self.more_items,
                )
            else:
                json_response["items"] = self.more_items + json_response["items"]
                self.more_items = []
                return json_response
        except KeyError:
            # Used only when the response only has "one page" of results.
            return json_response


class Token(object):
    """The token is the validation object used with the FMC."""

    logging.debug("In the Token class.")

    MAX_REFRESHES = 3
    TOKEN_LIFETIME = 60 * 30
    TOKEN_REFRESH_TIME = int(
        TOKEN_LIFETIME * 0.95
    )  # Refresh token at 95% refresh time.
    API_PLATFORM_VERSION = "api/fmc_platform/v1"

    def __init__(
        self,
        host="192.168.45.45",
        username="admin",
        password="Admin123",
        domain=None,
        verify_cert=False,
    ):
        """
        Initialize variables used in the Token class.

        :param host (str):  FMC hostname/IP (Default is 192.168.45.45)
        :param username (str): FMC Admin user (Default is admin)
        :param password (str): FMC user's password (Default is Admin123)
        :param domain (str):  UUID of domain.  Default is None which implies Global domain.
        :param verify_cert (bool):  Validate cert  (Default is False)
        :return: None
        """
        logging.debug("In the Token __init__() class method.")

        self.__host = host
        self.__username = username
        self.__password = password
        self.__domain = domain
        self.uuid = None
        self.verify_cert = verify_cert
        self.token_refreshes = 0
        self.access_token = None
        self.refresh_token = None
        self.token_creation_time = None
        self.generate_tokens()

    def generate_tokens(self):
        """
        Create new or refresh expired tokens.

        :return: None
        """
        logging.debug("In the Token generate_tokens() class method.")

        if self.token_refreshes <= self.MAX_REFRESHES and self.access_token is not None:
            headers = {
                "Content-Type": "application/json",
                "X-auth-access-token": self.access_token,
                "X-auth-refresh-token": self.refresh_token,
            }
            url = f"https://{self.__host}/{self.API_PLATFORM_VERSION}/auth/refreshtoken"
            logging.info(
                f"Refreshing tokens, {self.token_refreshes} out of {self.MAX_REFRESHES} refreshes, "
                f"from {url}."
            )
            response = requests.post(url, headers=headers, verify=self.verify_cert)
            logging.debug(
                "Response from refreshtoken() post:\n"
                f"\turl: {url}\n"
                f"\theaders: {headers}\n"
                f"\tresponse: {response}"
            )
            self.token_refreshes += 1
        else:
            self.token_refreshes = 0
            self.token_creation_time = (
                datetime.datetime.now()
            )  # Can't trust that your clock is in sync with FMC's.
            headers = {"Content-Type": "application/json"}
            url = (
                f"https://{self.__host}/{self.API_PLATFORM_VERSION}/auth/generatetoken"
            )
            logging.info(f"Requesting new tokens from {url}.")
            response = requests.post(
                url,
                headers=headers,
                auth=requests.auth.HTTPBasicAuth(self.__username, self.__password),
                verify=self.verify_cert,
            )
            logging.debug(
                "Response from generatetoken() post:\n"
                f"\turl: {url}\n"
                f"\theaders: {headers}\n"
                f"\tresponse: {response}"
            )
        self.access_token = response.headers.get("X-auth-access-token")
        self.refresh_token = response.headers.get("X-auth-refresh-token")
        self.uuid = response.headers.get("DOMAIN_UUID")
        if self.access_token:
            all_domain = json.loads(response.headers.get("DOMAINS"))
            if self.__domain is not None:
                for domain in all_domain:
                    if "global/" + self.__domain.lower() == domain["name"].lower():
                        logging.info(f"Domain set to {domain['name']}")
                        self.uuid = domain["uuid"]
                    else:
                        logging.info(
                            "Domain name entered not found in FMC, falling back to Global"
                        )

    def get_token(self):
        """
        Check validity of current token.  If needed make a new or refresh.  Then return access_token.

        :return self.access_token
        """
        logging.debug("In the Token get_token() class method.")
        if (
            datetime.datetime.now()
            > (
                self.token_creation_time
                + datetime.timedelta(seconds=self.TOKEN_REFRESH_TIME)
            )
            or self.access_token == None
        ):
            logging.info("Token expired.  Generating a new token.")
            self.token_refreshes = 0
            self.access_token = None
            self.refresh_token = None
            self.generate_tokens()

        return self.access_token
