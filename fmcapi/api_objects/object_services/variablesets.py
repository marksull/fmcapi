from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging
import warnings


class VariableSets(APIClassTemplate):
    """
    The VariableSets Object in the FMC.
    """

    URL_SUFFIX = '/object/variablesets'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for VariableSets class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for VariableSets class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'description' in self.__dict__:
            json_data['description'] = self.description
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for VariableSets class.")

    def post(self):
        logging.info('POST method for API for VariableSets not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for VariableSets not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for VariableSets not supported.')
        pass


class VariableSet(VariableSets):
    warnings.warn("Deprecated: VariableSet() should be called via VariableSets().")
