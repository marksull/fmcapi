from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class Geolocation(APIClassTemplate):
    """
    The Geolocation Object in the FMC.
    """

    URL_SUFFIX = '/object/geolocations'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Geolocation class.")
        self.parse_kwargs(**kwargs)

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for Geolocation class.")

    def post(self):
        logging.info('POST method for API for Geolocation not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for Geolocation not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for Geolocation not supported.')
        pass
