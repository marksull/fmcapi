import logging
import fmcapi
import time
import json

def test__connectionprofiles(fmc):
    logging.info("Testing ConnectionProfiles class.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    connection_profiles = fmcapi.ConnectionProfiles(fmc=fmc, container_uuid="40A6B737-FDDC-0ed3-0000-227633610030")
    connection_profiles.get(expanded=True)

    # Example to change group policy in an existing connection profile
    # for item in conn_profs.get('items'):
    #     conn_profile_id = item.get('id')
    #     profile = fmcapi.ConnectionProfiles(fmc=fmc, container_uuid="40A6B737-FDDC-0ed3-0000-227633610030")
    #     profile.id = conn_profile_id
    #     conn_prof = profile.get(expanded=True)
    #     logging.info(f"current groupPolicy: {conn_prof.get('groupPolicy')}")
    #     lock_out_grp_pol = {
    #         'name': 'LOCKOUT_GRP_POL',
    #         'id': '40A6B737-FDDC-0ed3-0000-227637209390',
    #         'type': 'GroupPolicy'
    #     }
    #     profile.groupPolicy = lock_out_grp_pol
    #     profile.put()

    logging.info("Testing ConnectionProfiles class done.\n")