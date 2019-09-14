from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class RealmUsers(APIClassTemplate):
    """
    The RealmUsers Object in the FMC.
    """

    URL_SUFFIX = '/object/realmusers'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for RealmUsers class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for RealmUsers class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'realmUuid' in self.__dict__:
            json_data['realmUuid'] = self.realmUuid
        if 'realm' in self.__dict__:
            json_data['realm'] = self.realm
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for RealmUsers class.")

    def post(self):
        logging.info('POST method for API for RealmUsers not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for RealmUsers not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for RealmUsers not supported.')
        pass
