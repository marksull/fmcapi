"""
Moving the fmc.auditrecords to an actual api_object.
"""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class AuditRecords(APIClassTemplate):
    """
    This API function supports filtering the GET query URL with: username, subsystem, source, starttime, and
    endtime parameters.
    :return: response
    """

    VALID_JSON_DATA = []
    VALID_FOR_KWARGS = VALID_JSON_DATA + ['id', 'name']
    URL_SUFFIX = '/deviceclusters/auditrecords'

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for AuditRecords class.")
        self.parse_kwargs(**kwargs)
        self.url_parameters = 'expanded=true'
        self.URL = f'{self.fmc.platform_url}/domain/{self.uuid}{self.URL_SUFFIX}?{self.url_parameters}'

    def post(self):
        logging.info('POST method for API for AuditRecords not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for AuditRecords not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for AuditRecords not supported.')
        pass
