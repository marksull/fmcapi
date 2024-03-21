import logging
import fmcapi
import time
import json

def test__connectionprofiles(fmc):
    logging.info("Testing ConnectionProfiles class.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    connection_profiles = fmcapi.ConnectionProfiles(fmc=fmc, container_uuid="40A6B737-FDDC-0ed3-0000-227633610030")
    conn_profs = connection_profiles.get(expanded=True)
    logging.info(conn_profs)
    for item in conn_profs.get('items'):
        conn_profile_id = item.get('id')
        profile = fmcapi.ConnectionProfiles(fmc=fmc, container_uuid="40A6B737-FDDC-0ed3-0000-227633610030")
        profile.id = conn_profile_id
        conn_prof = profile.get(expanded=True)
        logging.info(f"current groupPolicy: {conn_prof.get('groupPolicy')}")
        lock_out_grp_pol = {
            'name': 'LOCKOUT_GRP_POL',
            'id': '40A6B737-FDDC-0ed3-0000-227637209390',
            'type': 'GroupPolicy'
        }
        profile.groupPolicy = lock_out_grp_pol
        profile.put()

    logging.info(json.dumps(conn_prof, indent=2))


    # ravpn_policies = fmcapi.RAVpn(fmc=fmc)
    # logging.info(f'Looking for all RAVPN Policies')
    # all_ravpn_policies = ravpn_policies.get()
    # logging.info(f'Found {len(all_ravpn_policies.get("items"))} RAVPN Policies')

    # for policy in all_ravpn_policies.get('items'):
    #     ravpn_policy = fmcapi.RAVpn(fmc=fmc)
    #     ravpn_policy.id = policy.get('id')
    #     ravpn_policy.get(expanded=True)
    #     logging.info(f'Found {ravpn_policy.name} with ID of {ravpn_policy.id}')

    # POST, PUT and DELETE are valid endpoints in the api >7.2, however ravpn POST has a cycical dependency
    # with serveral other api endpoints - connectionprofiles, addressassignments, etc.
    # This is due to needing a container uuid of the RAVPN policy but also needing those objects to
    # create the RAVPN policy in the first place.

    logging.info("Testing ConnectionProfiles class done.\n")