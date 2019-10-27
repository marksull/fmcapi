from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .accesspolicies import AccessPolicies
from fmcapi.api_objects.device_services.devicerecords import DeviceRecords
from .prefilterpolicies import PreFilterPolicies
import logging
import warnings


class HitCounts(APIClassTemplate):
    """
    The HitCounts Object in the FMC.
    """

    VALID_JSON_DATA = []
    VALID_FOR_KWARGS = VALID_JSON_DATA + [
        "acp_id",
        "acp_name",
        "device_id",
        "device_name",
        "prefilter_id",
        "fetchZeroHitcount",
        "limit",
    ]
    PREFIX_URL = "/policy/accesspolicies"
    REQUIRED_FOR_PUT = ["acp_id", "device_id"]
    REQUIRED_FOR_DELETE = ["acp_id", "device_id"]
    REQUIRED_FOR_GET = ["acp_id", "device_id"]
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""
    FIRST_SUPPORTED_FMC_VERSION = "6.4"

    @property
    def URL_SUFFIX(self):
        """
        Add the URL suffixes for filter.
        """
        filter_init = '?filter="'
        filter_string = filter_init

        self.URL = self.URL.split("?")[0]

        if self.device_id:
            filter_string += f"deviceId:{self.device_id};"
        if self.prefilter_ids:
            filter_string += f"ids:{self.prefilter_ids};"
        if self.fetchZeroHitCount:
            filter_string += f"fetchZeroHitCount:{self._fetchZeroHitCount};"

        if filter_string == filter_init:
            filter_string += '"'
        filter_string = f'{filter_string[:-1]}"&expanded=true'

        if "limit" in self.__dict__:
            filter_string += f"&limit={self.limit}"
        return filter_string

    @property
    def fetchZeroHitCount(self):
        return self._fetchZeroHitCount

    @fetchZeroHitCount.setter
    def fetchZeroHitCount(self, value=False):
        self._fetchZeroHitCount = value
        # Rebuild the URL with possible new information
        self.URL = self.URL.split("?")[0]
        self.URL = f"{self.URL}{self.URL_SUFFIX}"

    def __init__(self, fmc, **kwargs):
        logging.debug("In __init__() for HitCounts class.")
        self.device_id = None
        self.prefilter_ids = []
        self.fetchZeroHitCount = False
        super().__init__(fmc, **kwargs)
        self.parse_kwargs(**kwargs)
        self.type = "HitCount"
        self.URL = f"{self.URL}{self.URL_SUFFIX}"

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for HitCounts class.")
        if "acp_id" in kwargs:
            self.acp(acp_id=kwargs["acp_id"])
        if "acp_name" in kwargs:
            self.acp(name=kwargs["acp_name"])
        if "device_id" in kwargs:
            self.device(id=kwargs["device_id"])
        if "device_name" in kwargs:
            self.device(name=kwargs["device_name"])

    def acp(self, name="", acp_id=""):
        # either name or id of the ACP should be given
        logging.debug("In acp() for HitCounts class.")
        if acp_id != "":
            self.acp_id = acp_id
            self.URL = f"{self.fmc.configuration_url}{self.PREFIX_URL}/{self.acp_id}/operational/hitcounts"
            self.acp_added_to_url = True
        elif name != "":
            acp1 = AccessPolicies(fmc=self.fmc)
            acp1.get(name=name)
            if "id" in acp1.__dict__:
                self.acp_id = acp1.id
                self.URL = f"{self.fmc.configuration_url}{self.PREFIX_URL}/{self.acp_id}/operational/hitcounts"
                self.acp_added_to_url = True
            else:
                logging.warning(
                    f'Access Control Policy "{name}" not found.  Cannot configure acp for HitCounts.'
                )
        else:
            logging.error("No accessPolicy name or id was provided.")
        # Rebuild the URL with possible new information
        self.URL = self.URL.split("?")[0]
        self.URL = f"{self.URL}{self.URL_SUFFIX}"

    def device(self, name="", id=""):
        logging.debug("In device() for HitCounts class")
        if id != "":
            self.device_id = id
        elif name != "":
            device1 = DeviceRecords(fmc=self.fmc)
            device1.get(name=name)
            if "id" in device1.__dict__:
                self.device_id = device1.id
            else:
                logging.warning(
                    f'Device "{name}" not found.  Cannot configure device for HitCounts.'
                )
        else:
            logging.error("No device name or id was provided.")
        # Rebuild the URL with possible new information
        self.URL = self.URL.split("?")[0]
        self.URL = f"{self.URL}{self.URL_SUFFIX}"

    def prefilter_policies(self, action, name="", prefilter_id=""):
        logging.debug("In prefilter_policies_tags() for HitCounts class.")
        if action == "add":
            ppolicy = PreFilterPolicies(fmc=self.fmc)
            if prefilter_id:
                ppolicy.get(id=prefilter_id)
            elif name:
                ppolicy.get(name=name)
            if "id" in ppolicy.__dict__:
                if self.prefilter_ids:
                    duplicate = False
                    for obj in self.prefilter_ids.split(","):
                        if obj == ppolicy.id:
                            duplicate = True
                            logging.warning(
                                f"Id, {ppolicy.id}, already in prefilter_ids not duplicating."
                            )
                            break
                    if not duplicate:
                        self.prefilter_ids.append(ppolicy.id)
                        logging.info(
                            f'Adding "{ppolicy.id}" to prefilter_ids for this HitCounts.'
                        )
                else:
                    self.prefilter_ids.append(ppolicy.id)
                    logging.info(
                        f'Adding "{ppolicy.id}" to prefilter_ids for this HitCounts.'
                    )
            else:
                if name:
                    logging.warning(
                        f'Prefilter, "{name}", not found.  Cannot add to HitCounts.'
                    )
                elif prefilter_id:
                    logging.warning(
                        f"Prefilter, {prefilter_id}, not found.  Cannot add to HitCounts."
                    )
        elif action == "remove":
            ppolicy = PreFilterPolicies(fmc=self.fmc)
            if prefilter_id:
                ppolicy.get(id=prefilter_id)
            elif name:
                ppolicy.get(name=name)
            if "id" in ppolicy.__dict__:
                if self.prefilter_ids:
                    objects = []
                    for obj in self.prefilter_ids:
                        if obj != ppolicy.id:
                            objects.append(obj)
                    self.prefilter_ids = objects
                    logging.info(
                        f'Removed "{ppolicy.id}" from prefilter_ids for this HitCounts.'
                    )
                else:
                    logging.info(
                        "prefilter_ids is empty for this HitCounts.  Nothing to remove."
                    )
            else:
                logging.warning(
                    f"Prefilter Policy, {ppolicy.id}, not found.  Cannot remove from HitCounts."
                )
        elif action == "clear":
            if self.prefilter_ids:
                self.prefilter_ids = []
                logging.info("All prefilter_ids removed from this HitCounts object.")

        # Rebuild the URL with possible new information
        self.URL = self.URL.split("?")[0]
        self.URL = f"{self.URL}{self.URL_SUFFIX}"

    def get(self, **kwargs):
        """
        Get HitCounts based on filter criteria
        :return:
        """
        logging.debug("In get() for HitCount class.")
        self.parse_kwargs(**kwargs)
        if self.fmc.serverVersion < self.FIRST_SUPPORTED_FMC_VERSION:
            logging.error(
                f"Your FMC version, {self.fmc.serverVersion} does not support GET of this feature."
            )
            return {"items": []}
        if self.valid_for_get() and (self.device_id or self.prefilter_ids):
            if self.dry_run:
                logging.info(
                    "Dry Run enabled.  Not actually sending to FMC.  Here is what would have been sent:"
                )
                logging.info("\tMethod = GET")
                logging.info(f"\tURL = {self.URL}")
                return False
            response = self.fmc.send_to_api(method="get", url=self.URL)
            self.parse_kwargs(**response)
            if "items" not in response:
                response["items"] = []
            return response
        else:
            logging.warning(
                "get() method failed due to failure to pass valid_for_get() test."
            )
            return False

    def put(self, **kwargs):
        logging.info(
            "Though supported by FMC, API PUT method is not yet working for HitCounts in fmcapi."
        )
        pass

    def delete(self, **kwargs):
        logging.info(
            "Though supported by FMC, API DELETE method is not yet working for HitCounts in fmcapi."
        )
        pass

    def post(self):
        logging.info("APIhit_count POST method for HitCounts not supported.")
        pass


class HitCount(HitCounts):
    """Dispose of this Class after 20210101."""

    def __init__(self, fmc, **kwargs):
        warnings.resetwarnings()
        warnings.warn("Deprecated: HitCount() should be called via HitCount().")
        super().__init__(fmc, **kwargs)
