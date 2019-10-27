import logging
import fmcapi
import time


def test__hitcounts(fmc, device_name="", prefilter_id=""):
    if not device_name and not prefilter_id:
        return f"Name of an actual device or prefilter ID is required for the HitCounts test to work... skipping test."

    logging.info(
        "In preparation for testing HitCounts method, set up some known objects in the FMC."
    )
    starttime = str(int(time.time()))
    namer = f"test__hitcounts_{starttime}"

    # Get the device
    device1 = fmcapi.DeviceRecords(fmc=fmc, name=device_name)
    device1.get()

    # In case there is no ACP Rule build a temp one.
    acprule1 = fmcapi.AccessRules(fmc=fmc, acp_id=device1.accessPolicy["id"])
    # acprule1 = fmcapi.AccessRules(fmc=fmc, acp_name=device1.accessPolicy['name'])
    acprule1.name = namer
    acprule1.action = "ALLOW"
    acprule1.post()
    time.sleep(1)
    acprule1.get()

    hitcounter1 = None
    if prefilter_id:
        hitcounter1 = fmcapi.HitCounts(
            fmc=fmc, prefilter_id=prefilter_id, device_name=device_name
        )
    else:
        hitcounter1 = fmcapi.HitCounts(
            fmc=fmc, acp_id=device1.accessPolicy["id"], device_name=device_name
        )
        """ 
        Searching for AccessRule by name returns the "correct" ID for the rule but HitCount shows a completely
        different ID so it doesn't match.
        # hitcounter1.acp_rules(action="add", name="Permit HQ LAN")

        If you know the ID that HitCount is looking for a specific rule:
        # hitcounter1.acp_rules(action="add", acp_rule_id="005056B5-44E6-0ed3-0000-000268434433")
        """
    for result in hitcounter1.get():
        print(result)

    logging.info("Test HitCount done.")

    logging.info("Cleanup of testing HitCount methods.")
    acprule1.delete()
    time.sleep(1)
    logging.info("Cleanup of objects for HitCount test done.\n\n")
