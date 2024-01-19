import logging
import fmcapi
import time

def test__grouppolicies(fmc):
    logging.info("Testing GroupPolicies class.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    group_policy = fmcapi.GroupPolicies(fmc=fmc)
    group_policy.name = namer
    # Posting a group policy with just a name will create a blank group policy with whatever defaults the GUI uses at the moment
    group_policy.post()

    group_policy.get()

    # Change number of simultaneous ravpn sessions per user as PUT example
    sessionSettings = group_policy.advancedSettings.get('sessionSettings')
    sessionSettings['simultaneousLoginPerUser'] = 0
    group_policy.advancedSettings['sessionSettings'] = sessionSettings
    group_policy.put()

    group_policy.get()
    if group_policy.advancedSettings.get('sessionSettings').get('simultaneousLoginPerUser') == 0:
        group_policy.delete()

    logging.info("Testing GroupPolicies class done.\n")