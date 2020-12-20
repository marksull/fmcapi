"""URL Groups Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .urls import URLs
import logging


class URLGroups(APIClassTemplate):
    """The URLGroups Object in the FMC."""

    VALID_JSON_DATA = ["id", "name", "type", "objects", "literals"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/urlgroups"

    # Technically you can have objects OR literals but I'm not set up for "OR" logic, yet.
    REQUIRED_FOR_POST = ["name", "objects"]

    def __init__(self, fmc, **kwargs):
        """
        Initialize URLGroups object.

        Set self.type to "URLGroup" and parse the kwargs.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for URLGroups class.")
        self.parse_kwargs(**kwargs)
        self.type = "URLGroup"

    def named_urls(self, action, name=""):
        """
        Associate Named URLs.

        :param action: (str) 'add', 'remove', or 'clear'
        :param name: (str) Name of URL.
        """
        logging.debug("In named_urls() for URLGroups class.")
        if action == "add":
            url1 = URLs(fmc=self.fmc)
            response = url1.get()
            if "items" in response:
                new_url = None
                for item in response["items"]:
                    if item["name"] == name:
                        new_url = {
                            "name": item["name"],
                            "id": item["id"],
                            "type": item["type"],
                        }
                        break
                if new_url is None:
                    logging.warning(
                        f'URL "{name}" is not found in FMC.  Cannot add to URLGroups.'
                    )
                else:
                    if "objects" in self.__dict__:
                        duplicate = False
                        for obj in self.objects:
                            if obj["name"] == new_url["name"]:
                                duplicate = True
                                break
                        if not duplicate:
                            self.objects.append(new_url)
                            logging.info(f'Adding "{name}" to URLGroups.')
                    else:
                        self.objects = [new_url]
                        logging.info(f'Adding "{name}" to URLGroups.')
        elif action == "remove":
            if "objects" in self.__dict__:
                objects_list = []
                for obj in self.objects:
                    if obj["name"] != name:
                        objects_list.append(obj)
                self.objects = objects_list
                logging.info(f'Removed "{name}" from URLGroups.')
            else:
                logging.info("This URLGroups has no named_urls.  Nothing to remove.")
        elif action == "clear":
            if "objects" in self.__dict__:
                del self.objects
                logging.info("All named_urls removed from this URLGroups.")

    def unnamed_urls(self, action, value=""):
        """
        Associate Unnamed URLs.

        :param action: (str) 'add', 'remove', or 'clear'
        :param value: (str) URL.
        """
        logging.debug("In unnamed_urls() for URLGroups class.")
        if action == "add":
            if value == "":
                logging.error(
                    "Value assignment required to add unnamed_url to URLGroups."
                )
                return
            value_type = "Url"
            new_literal = {"type": value_type, "url": value}
            if "literals" in self.__dict__:
                duplicate = False
                for obj in self.literals:
                    if obj["url"] == new_literal["url"]:
                        duplicate = True
                        break
                if not duplicate:
                    self.literals.append(new_literal)
                    logging.info(f'Adding "{value}" to URLGroups.')
            else:
                self.literals = [new_literal]
                logging.info(f'Adding "{value}" to URLGroups.')
        elif action == "remove":
            if "literals" in self.__dict__:
                literals_list = []
                for obj in self.literals:
                    if obj["url"] != value:
                        literals_list.append(obj)
                self.literals = literals_list
                logging.info(f'Removed "{value}" from URLGroups.')
            else:
                logging.info("This URLGroups has no unnamed_urls.  Nothing to remove.")
        elif action == "clear":
            if "literals" in self.__dict__:
                del self.literals
                logging.info("All unnamed_urls removed from this URLGroups.")
