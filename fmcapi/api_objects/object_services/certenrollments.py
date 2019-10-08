from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging
import warnings


class CertEnrollments(APIClassTemplate):
    """
    The CertEnrollments Object in the FMC.
    """

    VALID_JSON_DATA = ["id", "name", "type"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/certenrollments"

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for CertEnrollments class.")
        self.parse_kwargs(**kwargs)

    def post(self):
        logging.info("POST method for API for CertEnrollments not supported.")
        pass

    def put(self):
        logging.info("PUT method for API for CertEnrollments not supported.")
        pass

    def delete(self):
        logging.info("DELETE method for API for CertEnrollments not supported.")
        pass


class CertEnrollment(CertEnrollments):
    """Dispose of this Class after 20210101."""

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn(
            "Deprecated: CertEnrollment() should be called via CertEnrollments()."
        )
        super().__init__(fmc, **kwargs)
