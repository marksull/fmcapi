from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging
import warnings


class ApplicationCategories(APIClassTemplate):
    """
    The ApplicationCategories Object in the FMC.
    """

    URL_SUFFIX = '/object/applicationcategories'
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for ApplicationCategories class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for ApplicationCategories class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'type' in self.__dict__:
            json_data['type'] = self.type
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for ApplicationCategories class.")

    def post(self):
        logging.info('POST method for API for ApplicationCategories not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for ApplicationCategories not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for ApplicationCategories not supported.')
        pass


class ApplicationCategory(ApplicationCategories):
    warnings.warn("Deprecated: ApplicationCategory() should be called via ApplicationCategories().")
