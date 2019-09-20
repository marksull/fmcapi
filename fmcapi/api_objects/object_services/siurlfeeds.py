from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class SIUrlFeeds(APIClassTemplate):
    """
    The SIUrlFeeds Object in the FMC.
    """

    URL_SUFFIX = '/object/siurlfeeds'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for SIUrlFeeds class.")
        self.parse_kwargs(**kwargs)

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for SIUrlFeeds class.")

    def post(self):
        logging.info('POST method for API for SIUrlFeeds not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for SIUrlFeeds not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for SIUrlFeeds not supported.')
        pass
