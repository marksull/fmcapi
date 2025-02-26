"""Super class(es) that is inherited by all API objects."""
from .helper_functions import syntax_correcter, bulk_list_splitter, check_uuid
import logging
import json

logging.debug(f"In the {__name__} module.")


class APIClassTemplate(object):
    """The base framework for all/(most of) the objects in the FMC."""

    REQUIRED_FOR_POST = ["name"]
    REQUIRED_FOR_PUT = ["id"]
    REQUIRED_FOR_DELETE = ["id"]
    REQUIRED_FOR_GET = [""]
    REQUIRED_GET_FILTERS = []
    REQUIRED_FOR_BULK_POST = ["bulk"]
    REQUIRED_FOR_BULK_DELETE = ["bulk"]
    FILTER_BY_NAME = False
    URL = ""
    URL_SUFFIX = ""
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\-]"""
    FIRST_SUPPORTED_FMC_VERSION = "6.1"
    VALID_JSON_DATA = []
    VALID_GET_FILTERS = []
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
        self.expanded = False
        self.get_filters = {}
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
                if key_value in self.VALID_GET_FILTERS:
                    self.get_filters[key_value] = kwargs[key_value]
                else:
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
        if len(self.REQUIRED_GET_FILTERS) > 0:
            for item in self.REQUIRED_GET_FILTERS:
                if item not in self.get_filters:
                    logging.error(
                        f'Missing REQUIRED_GET_FILTERS "{item}" for GET request.'
                    )
                    return False
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
        to gather additional detail. Set "unusedOnly=True" to query for unused objects only for certain object types. Set
        "nameOrValue=String" to filter for a particular name or value of an object. This includes partial matches and is
        available for some objects.

        :param: expanded=Bool
        :param: unusedOnly=Bool
        :param: nameOrValue=String
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
            if "id" in self.__dict__ or "targetId" in self.__dict__:
                if "targetId" in self.__dict__:
                    url = f"{self.URL}/{self.targetId}"
                    if "backupVersion" in self.__dict__:
                        url += f"?backupVersion={self.backupVersion}"
                else:
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
                elif "targetId" in self.__dict__:
                    if "backupVersion" in self.__dict__:
                        logging.info(
                            f'GET success. Object with targetId: "{self.targetId}" backupVersion: "{self.backupVersion}" fetched from FMC.'
                        )
                    logging.info(
                        f'GET success. Object with targetId: "{self.targetId}" fetched from FMC.'
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
            elif len(self.get_filters) > 0:
                url_filter = ""
                for key, value in self.get_filters.items():
                    # Filter value must not be empty otherwise will result in a 400 response
                    if value != "":
                        url_filter += f"{key}%3A{value};"
                    else:
                        logging.warning(
                            f"Terminating GET - {self.URL}?expanded={self.expanded}&filter={url_filter}"
                        )
                        logging.warning(f"{key} MUST have a non empty value")
                        return False
                url = f"{self.URL}?expanded={self.expanded}&filter={url_filter}"
                if self.dry_run:
                    logging.info(
                        "Dry Run enabled.  Not actually sending to FMC.  Here is what would have been sent:"
                    )
                    logging.info("\tMethod = GET")
                    logging.info(f"\tURL = {url}")
                    return False
                response = self.fmc.send_to_api(method="get", url=url)
                if "items" not in response:
                    logging.info(
                        f"GET success. No Objects were found with query filter: {self.get_filters}"
                    )
                    return response
                else:
                    response_count = response.get("paging").get("count")
                    logging.info(
                        f"GET success. {response_count} items found that match query filter: {self.get_filters}"
                    )
                    return response
            else:
                logging.debug(
                    "GET query for object with no name or id set.  "
                    "Returning full list of these object types instead."
                )
                url_suffix_start = "?"
                if url_suffix_start in self.URL:
                    url_suffix_start = "&"
                url = f"{self.URL}{url_suffix_start}expanded=true&limit={self.limit}"
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
        if "bulk_post_data" in self.__dict__:
            missing_required_item = False
            # Check within each payload to ensure required for post is handled
            for i in self.bulk_post_data:
                for item in self.REQUIRED_FOR_POST:
                    if item not in i:
                        logging.error(
                            f'BULK POST FAILED: Missing value "{item}" in {i}'
                        )
                        missing_required_item = True
            if missing_required_item:
                return False
            return True
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
                if "bulk_post_data" in self.__dict__:
                    url = f"{self.URL}?bulk=true"
                else:
                    url = f"{self.URL}"
                if self.dry_run:
                    logging.info(
                        "Dry Run enabled.  Not actually sending to FMC.  Here is what would have been sent:"
                    )
                    logging.info("\tMethod = POST")
                    logging.info(f"\tURL = {url}")
                    logging.info(f"\tJSON = {self.show_json}")
                    return False
                if "bulk_post_data" in self.__dict__:
                    response = self.fmc.send_to_api(
                        method="post", url=url, json_data=self.bulk_post_data
                    )
                else:
                    response = self.fmc.send_to_api(
                        method="post", url=url, json_data=self.format_data()
                    )
                if response:
                    self.parse_kwargs(**response)
                    if "name" in self.__dict__ and "id" in self.__dict__:
                        logging.info(
                            f'POST success. Object with name: "{self.name}" and id: "{self.id}" created in FMC.'
                        )
                    elif "bulk_post_data" in self.__dict__:
                        logging.info(
                            f'BULK POST success. Items bulk posted: {len(response["items"])}'
                        )
                        logging.debug(f'BULK POST: {response["items"]}')
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
        if "bulk_delete_data" in self.__dict__:
            # Validate bulk delete data is a list of valid ids
            valid = True
            for i in self.bulk_delete_data:
                if not check_uuid(i):
                    valid = False
            if not valid:
                return False
            return True
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
            if "targetId" in self.__dict__:
                url = f"{self.URL}/{self.targetId}"
                if "backupVersion" in self.__dict__:
                    url += f"?backupVersion={self.backupVersion}"
            elif "bulk_delete_data" in self.__dict__:
                # Convert bulk delete data to csv string to insert into url
                self.bulk_delete_str = ",".join(map(str, self.bulk_delete_data))
                url = f"{self.URL}?filter=ids:{self.bulk_delete_str}&bulk=true"
            else:
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
            if hasattr(self, "name"):
                logging.info(
                    f'DELETE success. Object with name: "{self.name}" and id: "{self.id}" deleted in FMC.'
                )
            elif "targetId" in self.__dict__:
                if "backupVersion" in self.__dict__:
                    logging.info(
                        f'DELETE success. Object with targetId: "{self.targetId}" backupVersion: "{self.backupVersion}" deleted from FMC.'
                    )
                else:
                    logging.info(
                        f'DELETE success. Object with targetId: "{self.targetId}" deleted from FMC.'
                    )
            elif "bulk_delete_data" in self.__dict__:
                logging.info(
                    f"Bulk DELETE success. Objects deleted in FMC: {len(self.bulk_delete_data)}"
                )
                logging.debug(f"Bulk DELETE: {self.bulk_delete_data}")
            else:
                logging.info(f'DELETE success. Object id: "{self.id}" deleted in FMC.')
            return response
        else:
            logging.warning(
                "delete() method failed due to failure to pass valid_for_delete() test."
            )
            return False

    def valid_for_bulk_delete(self):
        """
        Use REQUIRED_FOR_BULK_DELETE to ensure all necessary variables exist prior to submitting to API.

        :return: (boolean)
        """
        logging.debug("In valid_for_bulk_delete() for APIClassTemplate class.")

        for item in self.REQUIRED_FOR_BULK_DELETE:
            if item not in self.__dict__:
                logging.error(f'Missing value "{item}" for bulk DELETE request.')
                return False
        return True

    def bulk_delete(self, **kwargs):
        """
        This is a shim in front of the normal delete() to handle bulk deletes.

        """
        logging.debug("In bulk_delete() for APIClassTemplate class.")
        self.parse_kwargs(**kwargs)
        if self.fmc.serverVersion < self.FIRST_SUPPORTED_FMC_VERSION:
            logging.error(
                f"Your FMC version, {self.fmc.serverVersion} does not support bulk DELETE of this feature."
            )
            return False
        if self.valid_for_bulk_delete():
            if len(self.bulk) > 0:
                if len(self.bulk) > 49:
                    self.chunks = bulk_list_splitter(self.bulk)
                    for chunk in self.chunks:
                        self.bulk_delete_data = chunk
                        # self.ids_str = ','.join(map(str,self.ids))
                        APIClassTemplate.delete(self)
                else:
                    self.bulk_delete_data = self.bulk
                    # self.ids_str = ','.join(map(str,self.ids))
                    APIClassTemplate.delete(self)

    def valid_for_bulk_post(self):
        """
        Use REQUIRED_FOR_BULK_POST to ensure all necessary variables exist prior to submitting to API.

        :return: (boolean)
        """
        logging.debug("In valid_for_bulk_post() for APIClassTemplate class.")

        for item in self.REQUIRED_FOR_BULK_POST:
            if item not in self.__dict__:
                logging.error(f'Missing value "{item}" for bulk POST request.')
                return False
        return True

    def bulk_post(self, **kwargs):
        """
        This is a shim in front of the normal post() to handle bulk posts.

        """
        logging.debug("In bulk_post() for APIClassTemplate class.")
        self.parse_kwargs(**kwargs)
        if self.fmc.serverVersion < self.FIRST_SUPPORTED_FMC_VERSION:
            logging.error(
                f"Your FMC version, {self.fmc.serverVersion} does not support bulk POST of this feature."
            )
            return False
        if self.valid_for_bulk_post():
            self.bulk_ids = []
            if len(self.bulk) > 0:
                if len(self.bulk) > 49:
                    self.chunks = bulk_list_splitter(self.bulk)
                    for chunk in self.chunks:
                        self.bulk_post_data = chunk
                        response = APIClassTemplate.post(self)
                        if response is not None:
                            for i in response["items"]:
                                self.bulk_ids.append(i["id"])
                else:
                    self.bulk_post_data = self.bulk
                    response = APIClassTemplate.post(self)
                    if response is not None:
                        for i in response["items"]:
                            self.bulk_ids.append(i["id"])
