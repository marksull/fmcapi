from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import logging


class FQDNS(APIClassTemplate):
    """
    The FQDNS Object in the FMC.
    """

    VALID_JSON_DATA = [
        "id",
        "name",
        "type",
        "overridableTargetId",
        "value",
        "dnsResolution",
        "overrides",
        "overridable",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/fqdns"
    VALID_FOR_DNS_RESOLUTION = ["IPV4_ONLY", "IPV6_ONLY", "IPV4_AND_IPV6"]
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""
    FIRST_SUPPORTED_FMC_VERSION = "6.3.0"

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for FQDNS class.")
        self.parse_kwargs(**kwargs)
        self.type = "FQDN"
        if self.fmc.serverVersion < self.FIRST_SUPPORTED_FMC_VERSION:
            logging.warning(
                f"The FQDNS API feature was released in version {self.FIRST_SUPPORTED_FMC_VERSION}.  "
                f"Your FMC version is {self.fmc.serverVersion}.  Upgrade to use this feature."
            )

    def format_data(self):
        json_data = super().format_data()
        logging.debug("In format_data() for FQDNS class.")
        if "dnsResolution" in self.__dict__:
            if self.dnsResolution in self.VALID_FOR_DNS_RESOLUTION:
                json_data["dnsResolution"] = self.dnsResolution
            else:
                logging.warning(f"dnsResolution {self.dnsResolution} not a valid type.")
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for FQDNS class.")
        if "dnsResolution" in kwargs:
            if kwargs["dnsResolution"] in self.VALID_FOR_DNS_RESOLUTION:
                self.dnsResolution = kwargs["dnsResolution"]
            else:
                logging.warning(
                    f"dnsResolution {kwargs['dnsResolution']} not a valid type."
                )
