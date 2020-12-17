from fmcapi.api_objects import LoggingSettings, AccessPolicies
import random
import string


def test_logging_settings(fmc):

    suffix = "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(5)
    )

    acp_rule = AccessPolicies(fmc=fmc, name=f"acp-log-test-{suffix}")
    acp_rule.post()

    acp_logging = LoggingSettings(fmc=fmc, acp_name=f"acp-log-test-{suffix}")
    acp_logging.get()

    acp_logging.syslogConfigFromPlatformSetting = True
    acp_logging.severityForPlatformSettingSyslogConfig = "ERR"
    acp_logging.put()

    acp_logging_test = LoggingSettings(fmc=fmc, acp_name=f"acp-log-test-{suffix}")
    acp_logging_test.get()
    if not acp_logging_test.syslogConfigFromPlatformSetting:
        print(
            f"Test Failed: Expected syslogConfigFromPlatformSetting = true, Actual = false"
        )
    if not acp_logging_test.severityForPlatformSettingSyslogConfig == "ERR":
        print(
            f"Test Failed: Expected severityForPlatformSettingSyslogConfig = 'ERR', "
            f"Actual = '{acp_logging.severityForPlatformSettingSyslogConfig}'"
        )

    acp_logging.enableFileAndMalwareSyslog = True
    acp_logging.fileAndMalwareSyslogSeverity = "CRIT"
    acp_logging.put()

    acp_logging_test = LoggingSettings(fmc=fmc, acp_name=f"acp-log-test-{suffix}")
    acp_logging_test.get()
    if not acp_logging_test.enableFileAndMalwareSyslog:
        print(
            f"Test Failed: Expected enableFileAndMalwareSyslog = true, Actual = false"
        )
    if not acp_logging_test.fileAndMalwareSyslogSeverity == "CRIT":
        print(
            f"Test Failed: Expected fileAndMalwareSyslogSeverity = 'CRIT', "
            f"Actual = {acp_logging_test.fileAndMalwareSyslogSeverity}"
        )

    acp_rule.delete()
