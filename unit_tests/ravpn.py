import logging
import fmcapi
import time

def test__ravpn(fmc):
    logging.info("Testing RAVpn class.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    ravpn_policies = fmcapi.RAVpn(fmc=fmc)
    logging.info(f'Looking for all RAVPN Policies')
    all_ravpn_policies = ravpn_policies.get()
    logging.info(f'Found {len(all_ravpn_policies.get("items"))} RAVPN Policies')

    for policy in all_ravpn_policies.get('items'):
        ravpn_policy = fmcapi.RAVpn(fmc=fmc)
        ravpn_policy.id = policy.get('id')
        ravpn_policy.get(expanded=True)
        logging.info(f'Found {ravpn_policy.name} with ID of {ravpn_policy.id}')

    # POST, PUT and DELETE are valid endpoints in the api >7.2, however ravpn POST has a cycical dependency
    # with serveral other api endpoints - connectionprofiles, addressassignments, etc.
    # This is due to needing a container uuid of the RAVPN policy but also needing those objects to
    # create the RAVPN policy in the first place.

    logging.info("Testing RAVpn class done.\n")