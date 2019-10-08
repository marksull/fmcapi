from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class DNSServerGroups(APIClassTemplate):
    """
    The DNSServerGroups Object in the FMC.
    """

    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
        "retries",
        "timeout",
        "dnsservers",
        "defaultdomain",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/dnsservergroups"
    REQUIRED_FOR_POST = ["name", "timeout"]
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for DNSServerGroups class.")
        self.parse_kwargs(**kwargs)
        self.type = "DNSServerGroupObject"

    def servers(self, action, name_servers):
        logging.debug("In servers() for DNSServerGroups class.")
        if action == "add":
            for name_server in name_servers:
                if "dnsservers" in self.__dict__:
                    self.dnsservers.append({"name-server": name_server})
                else:
                    self.dnsservers = [{"name-server": name_server}]
                logging.info(
                    f'Name-server "{name_server}" added to this DNSServerGroups object.'
                )
        elif action == "remove":
            if "dnsservers" in self.__dict__:
                for name_server in name_servers:
                    self.dnsservers = list(
                        filter(
                            lambda i: i["name-server"] != name_server, self.dnsservers
                        )
                    )
            else:
                logging.warning(
                    "DNSServerGroups has no members.  Cannot remove name-server."
                )
        elif action == "clear":
            if "dnsservers" in self.__dict__:
                del self.dnsservers
                logging.info(
                    "All name-servers removed from this DNSServerGroups object."
                )
