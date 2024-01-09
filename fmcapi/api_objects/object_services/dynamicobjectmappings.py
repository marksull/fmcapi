from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .dynamicobjects import DynamicObject
import logging


class DynamicObjectMappings(APIClassTemplate):
    """The Dynamic Object in the FMC."""

    VALID_JSON_DATA = ["add", "remove", "mappings", "type", "id","name"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/dynamicobjectmappings"
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    REQUIRED_FOR_POST = []
    obj_id = ""

    def __init__(self, fmc, **kwargs):
        """
        Initialize Dynamic Object.

        Set self.type to "DynamicObject" and parse the kwargs.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Dynamic Object class.")
        self.parse_kwargs(**kwargs)
        if "id" in kwargs:
            self.obj_id = kwargs["id"]

    def handle_mappings(self, action, value, name):
        """
        Associate mappings to dynamic object.

        :param action: (str) 'add', 'remove', or 'clear'
        :param dynamic_objects: (DynamicObject) Dynamic object to be mapped.
        """
        logging.debug("In mappings for dynamic object")

        dynamic_object = DynamicObject(fmc=self.fmc, name=name)
        response = dynamic_object.get()
        if response:
            new_obj = {
                "dynamicObject": {
                    "name": response["name"],
                    "id": response["id"],
                    "type": response["type"],
                },
                "mappings": value,
            }
            if action == "add":
                if "add" in self.__dict__:
                    self.add.append(new_obj)

                else:
                    self.add = [new_obj]

                logging.info(f"Adding mappings to Dynamic Object.")

            elif action == "remove":
                if "remove" in self.__dict__:
                    self.remove.append(new_obj)

                else:
                    self.remove = [new_obj]

                logging.info(f"Remove mappings to Dynamic Object.")

        else:
            logging.warning(
                f'Dynamic Object "{name}" is not found in FMC.  Cannot add mappings.'
            )

    def get(self):
        self.URL_SUFFIX = f"/object/dynamicobjects/{str(self.obj_id)}/mappings"
        self.__init__(self.fmc)
        return self._get()

    def put(self):
        self.URL_SUFFIX = f"/object/dynamicobjects/{str(self.obj_id)}/mappings"
        super().__init__(self.fmc)
        return super().put()

    def delete(self):
        self.URL_SUFFIX = f"/object/dynamicobjects/{str(self.obj_id)}/mappings"
        super().__init__(self.fmc)
        return super().delete()


    def _get(self, **kwargs):
        """
            To get mappings url is GET /api/fmc_config/v1/domain/{domainUUID}/object/dynamicobjects/{objectId}/mappings
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
                    url = f"{self.URL}"
                    if "backupVersion" in self.__dict__:
                        url += f"?backupVersion={self.backupVersion}"
                else:
                    url = f"{self.URL}"
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



