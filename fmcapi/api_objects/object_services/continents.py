from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging
import warnings


class Continents(APIClassTemplate):
    """
    The Continents Object in the FMC.
    """

    URL_SUFFIX = '/object/continents'
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Continents class.")
        self.parse_kwargs(**kwargs)
        self.type = 'Continent'

    def format_data(self):
        logging.debug("In format_data() for Continents class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'countries' in self.__dict__:
            json_data['countries'] = self.countries
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for Continents class.")
        if 'countries' in kwargs:
            self.countries = kwargs['countries']

    def post(self):
        logging.info('POST method for API for Continents not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for Continents not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for Continents not supported.')
        pass


class Continent(Continents):
    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn("Deprecated: Continent() should be called via Continents().")
        super().__init__(fmc, **kwargs)
