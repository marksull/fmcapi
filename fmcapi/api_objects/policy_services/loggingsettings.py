"""
Access Control Policy logging settings

A few things to note:
- Each ACP has it's own unique LoggingSettings. You can't create a LoggingSettings object and then associate to ACPs

- The LoggingSettings object for an ACP is created automatically when the ACP itself is created.

- Only PUT method is support for changing an existing LoggingSettings for an ACP

- Not all values are present by default. For example severityForPlatformSettingSyslogConfig is only valid if you have
syslogConfigFromPlatformSetting enabled

Not yet supported
- Custom syslog setting for ACP
"""
from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
from fmcapi.api_objects import AccessPolicies
from fmcapi.api_objects.helper_functions import true_false_checker
import logging


class LoggingSettings(APIClassTemplate):
    """
    The LoggingSettings object in the FMC
    """

    VALID_JSON_DATA = [
        "enableFileAndMalwareSyslog",
        "fileAndMalwareSyslogSeverity",
        "syslogConfigFromPlatformSetting",
        "severityForPlatformSettingSyslogConfig",
        "type",
        "id",
    ]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    VALID_SEVERITY = [
        "ALERT",
        "CRIT",
        "DEBUG",
        "EMERG",
        "ERR",
        "INFO",
        "NOTICE",
        "WARNING",
    ]
    REQUIRED_FOR_PUT = ["id", "type"]
    REQUIRED_FOR_GET = ["acp_id"]

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for LoggingSettings class.")
        self.fmc = fmc
        self.acp_id = None
        self.type = "LoggingSetting"
        self._syslogConfigFromPlatformSetting = False
        self._severityForPlatformSettingSyslogConfig = "ALERT"
        self._enableFileAndMalwareSyslog = False
        self._fileAndMalwareSyslogSeverity = "ALERT"
        self.parse_kwargs(**kwargs)

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for AccessRules class.")
        self.get_acp_id(**kwargs)

    def get_acp_id(self, **kwargs):
        if "acp_id" in kwargs:
            self.acp_id = kwargs["acp_id"]
        elif "acp_name" in kwargs:
            acp = AccessPolicies(fmc=self.fmc)
            acp.get(name=kwargs["acp_name"])
            if hasattr(acp, "id"):
                self.acp_id = acp.id
            else:
                logging.warning(
                    f"Access Control Policy {kwargs['name']} not found.  Cannot set up logging for ACP."
                )
        else:
            logging.error("No accessPolicy name or ID was provided.")

    def set_url(self):
        if hasattr(self, "id"):
            self.URL = f"{self.fmc.configuration_url}/policy/accesspolicies/{self.acp_id}/loggingsettings"
        else:
            self.URL = f"{self.fmc.configuration_url}/policy/accesspolicies/{self.acp_id}/loggingsettings?expanded=true"

    def get(self):
        for item in self.REQUIRED_FOR_GET:
            if not hasattr(self, item):
                logging.warning(
                    f"Unable to perform operation due to missing attribute: {item}"
                )
                return
        self.set_url()
        response = self.fmc.send_to_api(method="get", url=self.URL)
        if "items" in response:
            self.set_logging_attributes(response["items"][0])
        self.set_url()

    def set_logging_attributes(self, items):
        for attribute in items:
            if attribute == "metadata":
                continue
            setattr(self, attribute, items[attribute])

    @property
    def enableFileAndMalwareSyslog(self):
        return self._enableFileAndMalwareSyslog

    @enableFileAndMalwareSyslog.setter
    def enableFileAndMalwareSyslog(self, value=False):
        self._enableFileAndMalwareSyslog = true_false_checker(value)

    @property
    def fileAndMalwareSyslogSeverity(self):
        return self._severityForPlatformSettingSyslogConfig

    @fileAndMalwareSyslogSeverity.setter
    def fileAndMalwareSyslogSeverity(self, value="ALERT"):
        if value in self.VALID_SEVERITY:
            self._severityForPlatformSettingSyslogConfig = value
        else:
            self._severityForPlatformSettingSyslogConfig = "ALERT"

    @property
    def syslogConfigFromPlatformSetting(self):
        return self._syslogConfigFromPlatformSetting

    @syslogConfigFromPlatformSetting.setter
    def syslogConfigFromPlatformSetting(self, value=False):
        self._syslogConfigFromPlatformSetting = true_false_checker(value)

    @property
    def severityForPlatformSettingSyslogConfig(self):
        return self._severityForPlatformSettingSyslogConfig

    @severityForPlatformSettingSyslogConfig.setter
    def severityForPlatformSettingSyslogConfig(self, value="ALERT"):
        if value in self.VALID_SEVERITY:
            self._severityForPlatformSettingSyslogConfig = value
        else:
            self._severityForPlatformSettingSyslogConfig = "ALERT"
