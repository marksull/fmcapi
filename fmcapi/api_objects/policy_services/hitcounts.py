"""Hit Counts Class."""

from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from .accesspolicies import AccessPolicies
from .accessrules import AccessRules
from fmcapi.api_objects.device_services.devicerecords import DeviceRecords
from .prefilterpolicies import PreFilterPolicies
import logging


class HitCounts(APIClassTemplate):
    """The HitCounts Object in the FMC."""

    VALID_JSON_DATA = []
    VALID_FOR_KWARGS = VALID_JSON_DATA + [
        "acp_id",
        "acp_name",
        "device_id",
        "device_name",
        "prefilter_id",
        "prefilter_name",
        "fetchZeroHitcount",
        "limit",
        "lastFetchTimeStamp",
        "hitCount",
        "firstHitTimeStamp",
        "lastHitTimeStamp",
        "version",
        "policy",
    ]
    ACP_PREFIX_URL = "/policy/accesspolicies"
    PREFILTER_PREFIX_URL = "/policy/prefilterpolicies"
    REQUIRED_FOR_PUT = ["acp_id", "device_id"]
    REQUIRED_FOR_DELETE = ["acp_id", "device_id"]
    REQUIRED_FOR_GET = ["device_id"]
    FIRST_SUPPORTED_FMC_VERSION = "6.4"

    @property
    def URL_SUFFIX(self):
        """Add the URL suffixes for filter."""
        filter_init = '?filter="'
        filter_string = filter_init

        self.URL = self.URL.split("?")[0]

        if self.device_id:
            filter_string += f"deviceId:{self.device_id};"
        if self.acp_rule_ids:
            filter_string += f"ids:{','.join(self.acp_rule_ids)};"
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
        """Getter for fetchZeroHitCount."""
        return self._fetchZeroHitCount

    @fetchZeroHitCount.setter
    def fetchZeroHitCount(self, value=False):
        """Setter for fetchZeroHitCount."""
        self._fetchZeroHitCount = value
        # Rebuild the URL with possible new information
        self.URL = self.URL.split("?")[0]
        self.URL = f"{self.URL}{self.URL_SUFFIX}"

    def __init__(self, fmc, **kwargs):
        """
        Initialize HitCounts object.

        :param fmc (object): FMC object
        :param **kwargs: Any other values passed during instantiation.
        :return: None
        """
        logging.debug("In __init__() for HitCounts class.")
        self.device_id = None
        self.prefilter_id = None
        self.acp_id = None
        self.acp_rule_ids = []
        self.fetchZeroHitCount = False
        super().__init__(fmc, **kwargs)
        self.parse_kwargs(**kwargs)
        self.type = "HitCount"
        self.URL = f"{self.URL}"

    def parse_kwargs(self, **kwargs):
        """
        Parse the kwargs and set self variables to match.

        :return: None
        """
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for HitCounts class.")
        if "acp_id" in kwargs:
            self.acp(acp_id=kwargs["acp_id"])
        if "acp_name" in kwargs:
            self.acp(name=kwargs["acp_name"])
        if "device_id" in kwargs:
            self.device(device_id=kwargs["device_id"])
        if "device_name" in kwargs:
            self.device(name=kwargs["device_name"])
        if "prefilter_id" in kwargs:
            self.prefilter_policy(prefilter_policy_id=kwargs["prefilter_id"])
        if "prefilter_name" in kwargs:
            self.prefilter_policy(name=kwargs["prefilter_name"])

    def device(self, name="", device_id=""):
        """
        Associate a device with this HitCount.

        Either the 'name' or the 'device_id' is required, not both.
        :param name: (str) Name of device.
        :param device_id: (str) UUID of device.
        :return: None
        """
        logging.debug("In device() for HitCounts class")
        if device_id != "":
            self.device_id = device_id
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

    def acp(self, name="", acp_id=""):
        """
        Associate Access Control Policy with this HitCounts.

        Either the 'name' or the 'acp_id' is required, not both.
        :param name: (str) Name of ACP.
        :param acp_id: (str) UUID of ACP.
        """
        # either name or id of the ACP should be given
        logging.debug("In acp() for HitCounts class.")
        if acp_id != "":
            self.acp_id = acp_id
            self.URL = f"{self.fmc.configuration_url}{self.ACP_PREFIX_URL}/{self.acp_id}/operational/hitcounts"
        elif name != "":
            acp1 = AccessPolicies(fmc=self.fmc)
            acp1.get(name=name)
            if "id" in acp1.__dict__:
                self.URL = f"{self.fmc.configuration_url}{self.ACP_PREFIX_URL}/{acp1.id}/operational/hitcounts"
            else:
                logging.warning(
                    f'Access Control Policy "{name}" not found.  Cannot configure acp for HitCounts.'
                )
        else:
            logging.error("No accessPolicy name or id was provided.")

        # Rebuild the URL with possible new information
        self.URL = self.URL.split("?")[0]
        self.URL = f"{self.URL}{self.URL_SUFFIX}"

    def acp_rules(self, action=None, acp_rule_id=None, name=None):
        """
        Associate Access Rules to this HitCounts.

        Either the ID or the Name is required, not both.
        :param action: (str) 'add', 'remove', or 'clear'
        :param acp_rule_id: (str) UUID for Access Rule.
        :param name: (str) Name of Access Rule.
        """
        logging.debug("In acp_rules() for HitCounts class.")
        if name:
            # Need the acp_id if searching for AccessRule by name.
            if not self.acp_id:
                logging.error(
                    "Set AccessPolicy (acp_id or acp_name) prior to referencing acp_rules()."
                )
                return
            acp_rule = AccessRules(fmc=self.fmc, acp_id=self.acp_id)
            acp_rule.get(name=name)
            print(acp_rule.id)
            if hasattr(acp_rule, "id"):
                acp_rule_id = acp_rule.id
            else:
                acp_rule_id = None
                logging.warning(
                    f'AccessRule, "{name}", not found.  Cannot add to HitCounts.'
                )

        # If id is sent directly (and not looked up via name) assuming that the id is a valid AccessRule ID
        if acp_rule_id:
            if action == "add":
                if acp_rule_id not in self.acp_rule_ids:
                    self.acp_rule_ids.append(acp_rule_id)
                    logging.info(
                        f'Adding "{acp_rule_id}" to acp_rule_ids for this HitCounts.'
                    )
            elif action == "remove":
                if acp_rule_id in self.acp_rule_ids:
                    self.acp_rule_ids.remove(acp_rule_id)
                    logging.info(
                        f'Removed "{acp_rule_id}" from acp_rule_ids for this HitCounts.'
                    )
            elif action == "clear":
                self.acp_rule_ids = None
                logging.info("All ids removed from acp_rule_ids.")

        else:
            logging.warning(f"AccessRule ID not found.  Cannot add to HitCounts.")

        # Rebuild the URL with possible new information
        self.URL = self.URL.split("?")[0]
        self.URL = f"{self.URL}{self.URL_SUFFIX}"

    def prefilter_policy(self, name="", prefilter_policy_id=""):
        """
        Associate Pre-filter Policy with HitCount.

        Either the Name or the ID is needed, not both.
        :param name: (str) Name of PreFilter Policy.
        :param prefilter_policy_id: (str) UUID of PreFilter Policy.
        """
        # either name or id of the Prefilter Policy should be given
        logging.debug("In prefilter_policy() for HitCounts class.")
        if prefilter_policy_id != "":
            self.prefilter_id = prefilter_policy_id
            self.URL = (
                f"{self.fmc.configuration_url}{self.PREFILTER_PREFIX_URL}/"
                f"{self.prefilter_id}/operational/hitcounts"
            )
        elif name != "":
            ppolicy1 = PreFilterPolicies(fmc=self.fmc)
            ppolicy1.get(name=name)
            if "id" in ppolicy1.__dict__:
                self.prefilter_id = ppolicy1.id
                self.URL = (
                    f"{self.fmc.configuration_url}{self.PREFILTER_PREFIX_URL}/"
                    f"{self.prefilter_id}/operational/hitcounts"
                )
            else:
                logging.warning(
                    f'Access Control Policy "{name}" not found.  Cannot configure acp for HitCounts.'
                )
        else:
            logging.error("No accessPolicy name or id was provided.")

        # Rebuild the URL with possible new information
        self.URL = self.URL.split("?")[0]
        self.URL = f"{self.URL}{self.URL_SUFFIX}"

    def get(self, **kwargs):
        """
        Get HitCounts based on filter criteria.

        :return:
        """
        logging.debug("In get() for HitCount class.")
        self.parse_kwargs(**kwargs)

        if self.fmc.serverVersion < self.FIRST_SUPPORTED_FMC_VERSION:
            logging.error(
                f"Your FMC version, {self.fmc.serverVersion} does not support GET of this feature."
            )
            return {"items": []}
        if self.valid_for_get():
            if self.dry_run:
                logging.info(
                    "Dry Run enabled.  Not actually sending to FMC.  Here is what would have been sent:"
                )
                logging.info("\tMethod = GET")
                logging.info(f"\tURL = {self.URL}")
                return False
            response = self.fmc.send_to_api(method="get", url=self.URL)
            if "items" not in response:
                response["items"] = []
            return response["items"]
        else:
            logging.warning(
                "get() method failed due to failure to pass valid_for_get() test."
            )
            return False

    def put(self, **kwargs):
        """Though supported by FMC, API PUT method is not yet working for HitCounts in fmcapi."""
        logging.info(
            "Though supported by FMC, API PUT method is not yet working for HitCounts in fmcapi."
        )
        pass

    def delete(self, **kwargs):
        """Though supported by FMC, API DELETE method is not yet working for HitCounts in fmcapi."""
        logging.info(
            "Though supported by FMC, API DELETE method is not yet working for HitCounts in fmcapi."
        )
        pass

    def post(self):
        """POST method for HitCounts not supported."""
        logging.info("POST method for HitCounts not supported.")
        pass
