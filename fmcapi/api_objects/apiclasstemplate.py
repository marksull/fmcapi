"""Super class(es) that is inherited by all API objects."""
from .helper_functions import syntax_correcter
import logging
import json

logging.debug(f"In the {__name__} module.")


class APIClassTemplate(object):
    """The base framework for all/(most of) the objects in the FMC."""

    REQUIRED_FOR_POST = ["name"]
    REQUIRED_FOR_PUT = ["id"]
    REQUIRED_FOR_DELETE = ["id"]
    REQUIRED_FOR_GET = [""]
    FILTER_BY_NAME = False
    URL = ""
    URL_SUFFIX = ""
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\-]"""
    FIRST_SUPPORTED_FMC_VERSION = "6.1"
    VALID_JSON_DATA = []
    GLOBAL_VALID_FOR_KWARGS = ["dry_run"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []

    @property
    def show_json(self):
        """
        json.dumps of format_data() info.

        :return (str)
        """
        return json.dumps(self.format_data())

    def __init__(self, fmc, **kwargs):
        """
        Initialize an instances of object being created.

        :param fmc: (object) FMC object
        :param **kwargs: Passed variables that will be added to object being instantiated.
        :return: None
        """
        logging.debug("In __init__() for APIClassTemplate class.")
        self.VALID_FOR_KWARGS = self.VALID_FOR_KWARGS + self.GLOBAL_VALID_FOR_KWARGS
        self.fmc = fmc
        self.limit = self.fmc.limit
        self.description = "Created by fmcapi."
        self.overridable = False
        self.dry_run = False
        self.URL = f"{self.fmc.configuration_url}{self.URL_SUFFIX}"
        if self.fmc.serverVersion < self.FIRST_SUPPORTED_FMC_VERSION:
            logging.warning(
                f"This API feature was released in version {self.FIRST_SUPPORTED_FMC_VERSION}.  "
                f"Your FMC version is {self.fmc.serverVersion}.  Upgrade to use this feature."
            )

    def format_data(self, filter_query=""):
        """
        Gather all the data in preparation for sending to API in JSON format.

        :param filter_query: (str) 'all' or 'kwargs'
        :return: (dict) json_data
        """
        logging.debug("In format_data() for APIClassTemplate class.")
        json_data = {}
        filter_list = self.VALID_JSON_DATA
        if filter_query == "all":
            filter_list = self.__dict__
        elif filter_query == "kwargs":
            filter_list = self.VALID_FOR_KWARGS
        for key_value in filter_list:
            if hasattr(self, key_value):
                json_data[key_value] = getattr(self, key_value)
        return json_data

    def parse_kwargs(self, **kwargs):
        """
        Parse the kwargs and set self variables to match.

        :return: None
        """
        logging.debug("In parse_kwargs() for APIClassTemplate class.")
        for key_value in self.VALID_FOR_KWARGS:
            if key_value in kwargs:
                self.__dict__[key_value] = kwargs[key_value]
        if "name" in kwargs:
            self.name = syntax_correcter(
                kwargs["name"], permitted_syntax=self.VALID_CHARACTERS_FOR_NAME
            )
            if self.name != kwargs["name"]:
                logging.info(
                    f"Adjusting name '{kwargs['name']}' to '{self.name}' due to invalid characters."
                )

    def valid_for_get(self):
        """
        Use REQUIRED_FOR_GET to ensure all necessary variables exist prior to submitting to API.

        :return: (boolean)
        """
        logging.debug("In valid_for_get() for APIClassTemplate class.")
        if self.REQUIRED_FOR_GET == [""]:
            return True
        for item in self.REQUIRED_FOR_GET:
            if item not in self.__dict__:
                logging.error(f'Missing value "{item}" for GET request.')
                return False
        return True

    def get(self, **kwargs):
        """
        Prepare to send GET call to FMC API.

        If no self.name or self.id exists then return a full listing of all
        objects of this type otherwise return requested name/id values.  Set "expanded=true" results for specific object
        to gather additional detail.

        :return: requests response
        """
        logging.debug("In get() for APIClassTemplate class.")
        self.parse_kwargs(**kwargs)
        if self.fmc.serverVersion < self.FIRST_SUPPORTED_FMC_VERSION:
            logging.error(
                f"Your FMC version, {self.fmc.serverVersion} does not support GET of this feature."
            )
            return {"items": []}
        if self.valid_for_get():
            if "id" in self.__dict__:
                url = f"{self.URL}/{self.id}"
                if self.dry_run:
                    logging.info(
                        "Dry Run enabled.  Not actually sending to FMC.  Here is what would have been sent:"
                    )
                    logging.info("\tMethod = GET")
                    logging.info(f"\tURL = {self.URL}")
                    return False
                response = self.fmc.send_to_api(method="get", url=url)
                try:
                    self.parse_kwargs(**response)
                except TypeError as e:
                    logging.error(
                        f"Response from FMC GET with 'id', {self.id}, returned none."
                        f"That 'id' probably was deleted.  Error: {e}."
                    )
                if "name" in self.__dict__:
                    logging.info(
                        f'GET success. Object with name: "{self.name}" and id: "{self.id}" fetched from FMC.'
                    )
                else:
                    logging.info(
                        f'GET success. Object with id: "{self.id}" fetched from FMC.'
                    )
            elif "name" in self.__dict__:
                if self.FILTER_BY_NAME:
                    url = f"{self.URL}?name={self.name}&expanded=true"
                else:
                    url = f"{self.URL}?expanded=true"
                    if "limit" in self.__dict__:
                        url = f"{url}&limit={self.limit}"
                    if "offset" in self.__dict__:
                        url = f"{url}&offset={self.offset}"
                response = self.fmc.send_to_api(method="get", url=url)
                if "items" not in response:
                    response["items"] = []
                for item in response["items"]:
                    if "name" in item:
                        if item["name"] == self.name:
                            self.id = item["id"]
                            self.parse_kwargs(**item)
                            logging.info(
                                f'GET success. Object with name: "{self.name}" and id: "{self.id}" '
                                f"fetched from FMC."
                            )
                            return item
                    else:
                        logging.warning(
                            f'No "name" attribute associated with this item to check against {self.name}.'
                        )
                if "id" not in self.__dict__:
                    logging.warning(f"\tGET query for {self.name} is not found.")
                    logging.debug(
                        f"\tGET query for {self.name} is not found.\n\t\tResponse: {json.dumps(response)}"
                    )
            else:
                logging.debug(
                    "GET query for object with no name or id set.  "
                    "Returning full list of these object types instead."
                )
                url = f"{self.URL}?expanded=true&limit={self.limit}"
                if self.dry_run:
                    logging.info(
                        "Dry Run enabled.  Not actually sending to FMC.  Here is what would have been sent:"
                    )
                    logging.info("\tMethod = GET")
                    logging.info(f"\tURL = {self.URL}")
                    return False
                response = self.fmc.send_to_api(method="get", url=url)
            if "items" not in response:
                response["items"] = []
            return response
        else:
            logging.warning(
                "get() method failed due to failure to pass valid_for_get() test."
            )
            return False

    def valid_for_post(self):
        """
        Use REQUIRED_FOR_POST to ensure all necessary variables exist prior to submitting to API.

        :return: (boolean)
        """
        logging.debug("In valid_for_post() for APIClassTemplate class.")
        for item in self.REQUIRED_FOR_POST:
            if item not in self.__dict__:
                logging.error(f'Missing value "{item}" for POST request.')
                return False
        return True

    def post(self, **kwargs):
        """
        Prepare to send POST call to FMC API.

        :return: requests response
        """
        logging.debug("In post() for APIClassTemplate class.")
        self.parse_kwargs(**kwargs)
        if self.fmc.serverVersion < self.FIRST_SUPPORTED_FMC_VERSION:
            logging.error(
                f"Your FMC version, {self.fmc.serverVersion} does not support POST of this feature."
            )
            return False
        if "id" in self.__dict__:
            logging.info(
                "ID value exists for this object.  Redirecting to put() method."
            )
            self.put()
        else:
            if self.valid_for_post():
                if self.dry_run:
                    logging.info(
                        "Dry Run enabled.  Not actually sending to FMC.  Here is what would have been sent:"
                    )
                    logging.info("\tMethod = POST")
                    logging.info(f"\tURL = {self.URL}")
                    logging.info(f"\tJSON = {self.show_json}")
                    return False
                response = self.fmc.send_to_api(
                    method="post", url=self.URL, json_data=self.format_data()
                )
                if response:
                    self.parse_kwargs(**response)
                    if "name" in self.__dict__ and "id" in self.__dict__:
                        logging.info(
                            f'POST success. Object with name: "{self.name}" and id: "{id}" created in FMC.'
                        )
                    else:
                        logging.debug(
                            'POST success but no "id" or "name" values in API response.'
                        )
                else:
                    logging.warning("POST failure.  No data in API response.")
                return response
            else:
                logging.warning(
                    "post() method failed due to failure to pass valid_for_post() test."
                )
                return False

    def valid_for_put(self):
        """
        Use REQUIRED_FOR_PUT to ensure all necessary variables exist prior to submitting to API.

        :return: (boolean)
        """
        logging.debug("In valid_for_put() for APIClassTemplate class.")
        for item in self.REQUIRED_FOR_PUT:
            if item not in self.__dict__:
                logging.error(f'Missing value "{item}" for PUT request.')
                return False
        return True

    def put(self, **kwargs):
        """
        Prepare to send PUT call to FMC API.

        :return: requests response
        """
        logging.debug("In put() for APIClassTemplate class.")
        self.parse_kwargs(**kwargs)
        if self.fmc.serverVersion < self.FIRST_SUPPORTED_FMC_VERSION:
            logging.error(
                f"Your FMC version, {self.fmc.serverVersion} does not support PUT of this feature."
            )
            return False
        if self.valid_for_put():
            url = f"{self.URL}/{self.id}"
            if self.dry_run:
                logging.info(
                    "Dry Run enabled.  Not actually sending to FMC.  Here is what would have been sent:"
                )
                logging.info("\tMethod = PUT")
                logging.info(f"\tURL = {self.URL}")
                logging.info(f"\tJSON = {self.show_json}")
                return False
            response = self.fmc.send_to_api(
                method="put", url=url, json_data=self.format_data()
            )
            self.parse_kwargs(**response)
            if "name" in self.__dict__:
                logging.info(
                    f'PUT success. Object with name: "{self.name}" and id: "{self.id}" updated in FMC.'
                )
            else:
                logging.info(
                    f'PUT success. Object with id: "{self.id}" updated in FMC.'
                )
            return response
        else:
            logging.warning(
                "put() method failed due to failure to pass valid_for_put() test."
            )
            return False

    def valid_for_delete(self):
        """
        Use REQUIRED_FOR_DELETE to ensure all necessary variables exist prior to submitting to API.

        :return: (boolean)
        """
        logging.debug("In valid_for_delete() for APIClassTemplate class.")
        for item in self.REQUIRED_FOR_DELETE:
            if item not in self.__dict__:
                logging.error(f'Missing value "{item}" for DELETE request.')
                return False
        return True

    def delete(self, **kwargs):
        """
        Prepare to send DELETE call to FMC API.

        :return: requests response
        """
        logging.debug("In delete() for APIClassTemplate class.")
        self.parse_kwargs(**kwargs)
        if self.fmc.serverVersion < self.FIRST_SUPPORTED_FMC_VERSION:
            logging.error(
                f"Your FMC version, {self.fmc.serverVersion} does not support DELETE of this feature."
            )
            return False
        if self.valid_for_delete():
            url = f"{self.URL}/{self.id}"
            if self.dry_run:
                logging.info(
                    "Dry Run enabled.  Not actually sending to FMC.  Here is what would have been sent:"
                )
                logging.info("\tMethod = DELETE")
                logging.info(f"\tURL = {self.URL}")
                logging.info(f"\tJSON = {self.show_json}")
                return False
            response = self.fmc.send_to_api(
                method="delete", url=url, json_data=self.format_data()
            )
            if not response:
                return None
            self.parse_kwargs(**response)
            if "name" in self.name:
                logging.info(
                    f'DELETE success. Object with name: "{self.name}" and id: "{self.id}" deleted in FMC.'
                )
            else:
                logging.info(f'DELETE success. Object id: "{self.id}" deleted in FMC.')
            return response
        else:
            logging.warning(
                "delete() method failed due to failure to pass valid_for_delete() test."
            )
            return False
