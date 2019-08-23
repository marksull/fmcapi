from .apiclasstemplate import APIClassTemplate
import logging


class DNSServerGroups(APIClassTemplate):
    """
    The DNSServerGroups Object in the FMC.
    """

    URL_SUFFIX = '/object/dnsservergroups'
    REQUIRED_FOR_POST = ['name', 'timeout']
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for DNSServerGroups class.")
        self.parse_kwargs(**kwargs)
        self.type = 'DNSServerGroupObject'

    def format_data(self):
        logging.debug("In format_data() for DNSServerGroups class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'retries' in self.__dict__:
            json_data['retries'] = self.retries
        if 'timeout' in self.__dict__:
            json_data['timeout'] = self.timeout
        if 'dnsservers' in self.__dict__:
            json_data['dnsservers'] = self.dnsservers
        if 'defaultdomain' in self.__dict__:
            json_data['defaultdomain'] = self.defaultdomain
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for DNSServerGroups class.")
        if 'retries' in kwargs:
            self.retries = kwargs['retries']
        if 'timeout' in kwargs:
            self.timeout = kwargs['timeout']
        if 'dnsservers' in kwargs:
            self.dnsservers = kwargs['dnsservers']
        if 'defaultdomain' in kwargs:
            self.defaultdomain = kwargs['defaultdomain']

    def servers(self, action, name_servers):
        logging.debug("In servers() for DNSServerGroups class.")
        if action == 'add':
            for name_server in name_servers:
                if 'dnsservers' in self.__dict__:
                    self.dnsservers.append({"name-server":name_server})
                else:
                    self.dnsservers = [{"name-server":name_server}]
                logging.info('Name-server "{}" added to this DNSServerGroups object.'.format(name_server))
        elif action == 'remove':
            if 'dnsservers' in self.__dict__:
                for name_server in name_servers:
                    self.dnsservers = list(filter(lambda i: i['name-server'] != name_server, self.dnsservers))
            else:
                logging.warning('DNSServerGroups has no members.  Cannot remove name-server.')
        elif action == 'clear':
            if 'dnsservers' in self.__dict__:
                del self.dnsservers
                logging.info('All name-servers removed from this DNSServerGroups object.')
