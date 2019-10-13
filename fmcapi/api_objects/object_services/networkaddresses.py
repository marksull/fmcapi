from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging
import warnings


class NetworkAddresses(APIClassTemplate):
    """
    The NetworkAddresses Object in the FMC.
    """

    URL_SUFFIX = "/object/networkaddresses"

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for NetworkAddresses class.")
        self.parse_kwargs(**kwargs)

    def post(self):
        logging.info("POST method for API for NetworkAddresses not supported.")
        pass

    def put(self):
        logging.info("PUT method for API for NetworkAddresses not supported.")
        pass

    def delete(self):
        logging.info("DELETE method for API for NetworkAddresses not supported.")
        pass


class IPAddresses(NetworkAddresses):
    """Dispose of this Class after 20210101."""

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn(
            "Deprecated: IPAddresses() should be called via NetworkAddresses()."
        )
        super().__init__(fmc, **kwargs)
