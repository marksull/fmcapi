from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class InterfaceObject(APIClassTemplate):
    """
    The Interface Object Object in the FMC.
    """

    URL_SUFFIX = '/object/interfaceobjects'
    REQUIRED_FOR_POST = ['name', 'interfaceMode']
    FILTER_BY_NAME = True

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for InterfaceObject class.")
        self.parse_kwargs(**kwargs)

    def post(self):
        logging.info('POST method for API for InterfaceObject not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for InterfaceObject not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for InterfaceObject not supported.')
        pass
