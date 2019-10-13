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
    VALID_FOR_KWARGS = VALID_JSON_DATA + [
        "id",
        "username",
        "subsystem",
        "source",
        "starttime",
        "endtime",
        "limit",
    ]
    URL_SUFFIX = "/audit/auditrecords"

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for AuditRecords class.")
        self.url_parameters = ""
        self.URL = f"{self.fmc.platform_url}/domain/{self.fmc.uuid}{self.URL_SUFFIX}"
        self.parse_kwargs(**kwargs)

    def parse_kwargs(self, **kwargs):
        logging.debug("In parse_kwargs() for AuditRecords class.")
        tmp = self.url_parameters
        if "username" in kwargs:
            self.url_parameters += f"username={kwargs['username']}&"
        if "subsystem" in kwargs:
            self.url_parameters += f"subsystem={kwargs['subsystem']}&"
        if "source" in kwargs:
            self.url_parameters += f"source={kwargs['source']}&"
        if "starttime" in kwargs:
            self.url_parameters += f"starttime={kwargs['starttime']}&"
        if "endtime" in kwargs:
            self.url_parameters += f"endtime={kwargs['endtime']}&"
        if "limit" in kwargs:
            self.url_parameters += f"limit={kwargs['limit']}&"
        if tmp is not self.url_parameters:
            self.url_parameters = self.url_parameters[:-1]
        self.URL += self.url_parameters

    def get(self):
        logging.debug("GET method for API for AuditRecords.")
        return self.fmc.send_to_api(method="get", url=self.URL)

    def post(self):
        logging.info("POST method for API for AuditRecords not supported.")
        pass

    def put(self):
        logging.info("PUT method for API for AuditRecords not supported.")
        pass

    def delete(self):
        logging.info("DELETE method for API for AuditRecords not supported.")
        pass
