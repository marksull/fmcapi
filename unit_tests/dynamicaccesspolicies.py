import logging
import fmcapi
import time
import json

def test__dynamicaccesspolicies(fmc):
    logging.info("Testing DynamicAccessPolicies class.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    dap = fmcapi.DynamicAccessPolicies(fmc=fmc)
    dap.name = namer
    dap.post()
    dap.get()

    dap.authorizationAttributes = [
        {
        "dapRecordName": "TEST_DAP_RECORD",
        "action": "CONTINUE",
        "message": "TEST_MESSAGE",
        "priority": 0
        },
        {
        "dapRecordName": "DfltAccessPolicy",
        "action": "CONTINUE",
        "priority": -1
        }
    ]

    dapXmlConfig_json = '{"dapRecordList":{"dapRecord":{"dapName":{"value":"TEST_DAP_RECORD"},"dapViewsRelation":{"value":"and"},"dapBasicView":{"dapSelection":{"dapPolicy":{"value":"match-any"},"attr":{"name":"aaa.ldap.memberOf","operation":"EQ","value":"test_ad_group"}}}}}}'
    dap.dapXmlConfig_dict = json.loads(dapXmlConfig_json)

    hostscanXmlConfig_json = '{"data":{"config":{"field":{"_type":"dropdown","_name":"logging","_value":"error"}},"multilocation":{"sequence":{"start":{"location":{"_name":"Default"}}}},"location":{"field":[{"_type":"text","_name":"tWindowsCleanerLogoutTitle","_value":"(WebVPN Logout)"},{"_type":"checkbox","_name":"cWindowsCleanerLogoutTitle","_value":"ON"},{"_type":"dropdown","_name":"dWindowsCleanerTimeout","_value":"5"},{"_type":"dropdown","_name":"dCleanerSecureDeletePass","_value":"3"},{"_type":"dropdown","_name":"dTimeout","_value":"5"},{"_type":"dropdown","_name":"dSDSecureDeletePass","_value":"3"},{"_type":"text","_name":"tRestrictedModeUnRestricted","_value":""},{"_type":"text","_name":"tInternetExplorerHomePage","_value":"about:blank"}],"favorite":{"_type":"folder","_value":"Favorites"},"_name":"Default"},"customization":"","hostscan":"","_version":"3.2.1"}}'
    dap.hostscanXmlConfig_dict = json.loads(hostscanXmlConfig_json)

    dap.put()
    dap.delete()

    logging.info("Testing DynamicAccessPolicies class done.\n")