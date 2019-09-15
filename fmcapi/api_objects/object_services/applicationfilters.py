from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging
import warnings


class ApplicationFilters(APIClassTemplate):
    """
    The ApplicationFilters Object in the FMC.
    """

    URL_SUFFIX = '/object/applicationfilters'
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ApplicationFilters class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for ApplicationFilters class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        if 'appConditions' in self.__dict__:
            json_data['appConditions'] = self.appConditions
        if 'applications' in self.__dict__:
            json_data['applications'] = self.applications
        if 'conditions' in self.__dict__:
            json_data['conditions'] = self.conditions
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for ApplicationFilters class.")

    def post(self):
        logging.info('POST method for API for ApplicationFilters not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for ApplicationFilters not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for ApplicationFilters not supported.')
        pass


class ApplicationFilter(ApplicationFilters):
    """Dispose of this Class after 20210101."""

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn("Deprecated: ApplicationFilter() should be called via ApplicationFilters().")
        super().__init__(fmc, **kwargs)
