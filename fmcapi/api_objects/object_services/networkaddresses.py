"""Network Addresses Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging
import warnings


class NetworkAddresses(APIClassTemplate):
    """The NetworkAddresses Object in the FMC."""

    URL_SUFFIX = "/object/networkaddresses"

    def __init__(self, fmc, **kwargs):
        """
        Initialize NetworkAddresses object.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for NetworkAddresses class.")
        self.parse_kwargs(**kwargs)

    def post(self):
        """POST method for API for NetworkAddresses not supported."""
        logging.info("POST method for API for NetworkAddresses not supported.")
        pass

    def put(self):
        """PUT method for API for NetworkAddresses not supported."""
        logging.info("PUT method for API for NetworkAddresses not supported.")
        pass

    def delete(self):
        """DELETE method for API for NetworkAddresses not supported."""
        logging.info("DELETE method for API for NetworkAddresses not supported.")
        pass


class IPAddresses(NetworkAddresses):
    """
    Dispose of this Class after 20210101.

    Use NetworkAddresses() instead.
    """

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn(
            "Deprecated: IPAddresses() should be called via NetworkAddresses()."
        )
        super().__init__(fmc, **kwargs)
