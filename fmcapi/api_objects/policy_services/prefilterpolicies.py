from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class PreFilterPolicy(APIClassTemplate):
    """
    The PreFilterPolicy Object in the FMC.
    """

    URL_SUFFIX = '/policy/prefilterpolicies'
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for PreFilterPolicy class.")
        self.parse_kwargs(**kwargs)
        self.type = 'PreFilterPolicy'

    def format_data(self):
        logging.debug("In format_data() for PreFilterPolicy class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for PreFilterPolicy class.")

    def post(self):
        logging.info('POST method for API for PreFilterPolicy not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for PreFilterPolicy not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for PreFilterPolicy not supported.')
        pass
