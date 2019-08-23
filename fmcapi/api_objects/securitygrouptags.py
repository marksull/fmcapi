from .apiclasstemplate import APIClassTemplate
import logging


class SecurityGroupTags(APIClassTemplate):
    """
    The SecurityGroupTags Object in the FMC.
    """

    URL_SUFFIX = '/object/securitygrouptags'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for SecurityGroupTags class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for SecurityGroupTags class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'tag' in self.__dict__:
            json_data['tag'] = self.tag
        if 'overrides' in self.__dict__:
            json_data['overrides'] = self.overrides
        if 'overridable' in self.__dict__:
            json_data['overridable'] = self.overridable
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for SecurityGroupTags class.")

    def post(self):
        logging.info('POST method for API for SecurityGroupTags not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for SecurityGroupTags not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for SecurityGroupTags not supported.')
        pass
