from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging
import warnings


class Applications(APIClassTemplate):
    """
    The Applications Object in the FMC.
    """

    URL_SUFFIX = '/object/applications'
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\-\/\. ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Applications class.")
        self.parse_kwargs(**kwargs)

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for Applications class.")
        if 'appProductivity' in kwargs:
            self.appProductivity = kwargs['appProductivity']
        if 'appCategories' in kwargs:
            self.appCategories = kwargs['appCategories']
        if 'appTags' in kwargs:
            self.appTags = kwargs['appTags']
        if 'appId' in kwargs:
            self.appId = kwargs['appId']
        if 'risk' in kwargs:
            self.risk = kwargs['risk']
        if 'applicationTypes' in kwargs:
            self.applicationTypes = kwargs['applicationTypes']

    def post(self):
        logging.info('POST method for API for Applications not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for Applications not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for Applications not supported.')
        pass


class Application(Applications):
    """Dispose of this Class after 20210101."""

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn("Deprecated: Application() should be called via Applications().")
        super().__init__(fmc, **kwargs)
