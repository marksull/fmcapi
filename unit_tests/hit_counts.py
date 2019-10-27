import logging
import fmcapi
import time

# Set your device's name for this test to work:
device_name = ""
prefilter_id = ""

def test__hitcounts(fmc):
    if not device_name and not prefilter_id:
        return f"Name of an actual device or prefilter ID is required for the HitCounts test to work... skipping test."

    logging.info(
        "In preparation for testing HitCounts method, set up some known objects in the FMC."
    )
    starttime = str(int(time.time()))
    namer = f"test__hitcounts_{starttime}"

    # Build an ACP Object
    acp1 = fmcapi.AccessPolicies(fmc=fmc, name=namer)
    acp1.post()
    time.sleep(1)

    # Build an ACP Rule Object
    acprule1 = fmcapi.AccessRules(fmc=fmc, acp_name=acp1.name)
    acprule1.name = namer
    acprule1.action = "ALLOW"
    acprule1.enabled = True
    acprule1.variable_set(action="set", name="Default-Set")
    acprule1.intrusion_policy(action="set", name="Security Over Connectivity")
    acprule1.post()

    # Device
    device1 = fmcapi.DeviceRecords(fmc=fmc, device_name=device_name)
    device1.get()

    if device_name:
        hitcounter1 = fmcapi.HitCounts(fmc=fmc, acp_name=acp1.name, device_name=device1.name)
    elif prefilter_id:
        hitcounter1 = fmcapi.HitCounts(fmc=fmc, acp_name=acp1.name, prefilter_id=prefilter_id)
    print(hitcounter1)

    logging.info("Test Hitcount done.")

    logging.info("Cleanup of testing HitCount methods.")
    acprule1.delete()
    time.sleep(1)
    acp1.delete()
    logging.info("Cleanup of objects for HitCount test done.\n")
