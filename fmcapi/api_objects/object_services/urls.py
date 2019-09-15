from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging
import warnings


class URLs(APIClassTemplate):
    """
    The URLs Object in the FMC.
    """

    URL_SUFFIX = '/object/urls'
    REQUIRED_FOR_POST = ['name', 'url']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for URLs class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for URLs class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'url' in self.__dict__:
            json_data['url'] = self.url
        if 'description' in self.__dict__:
            json_data['description'] = self.description
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for URLs class.")
        if 'url' in kwargs:
            self.url = kwargs['url']


class URL(URLs):
    """Dispose of this Class after 20210101."""

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn("Deprecated: URL() should be called via URLs().")
        super().__init__(fmc, **kwargs)
