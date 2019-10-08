import logging
import fmcapi
import time


def test__autonat(fmc):
    logging.info("Testing AutoNatPolicy class.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    # Create a container policy for FTD NAT rules
    natpol1 = fmcapi.FTDNatPolicies(fmc=fmc, name=namer)
    natpol1.post()
    natpol1.get()

    # Create original and translate objects
    obj1 = fmcapi.Networks(fmc=fmc)
    obj1.name = "_net_original"
    obj1.value = "10.0.0.0/8"
    obj1.post()
    time.sleep(1)

    obj2 = fmcapi.Hosts(fmc=fmc)
    obj2.name = "_net_xlate"
    obj2.value = "192.0.2.1"
    obj2.post()
    time.sleep(1)

    # Create identity nat object
    obj3 = fmcapi.Networks(fmc=fmc)
    obj3.name = "_net_identity"
    obj3.value = "192.168.0.0/24"
    obj3.post()
    time.sleep(1)

    # Create nat pool objects
    obj4 = fmcapi.Networks(fmc=fmc)
    obj4.name = "_net_original_pool"
    obj4.value = "172.16.0.0/24"
    obj4.post()
    time.sleep(1)

    # PAT Pool must be a range, not a subnet
    obj5 = fmcapi.Ranges(fmc=fmc)
    obj5.name = "_net_xlate_pool"
    obj5.value = "192.0.2.128-192.0.2.254"
    obj5.post()
    time.sleep(1)

    # Create interface PAT object
    obj6 = fmcapi.Networks(fmc=fmc)
    obj6.name = "_net_original_intf"
    obj6.value = "192.168.1.0/24"
    obj6.post()
    time.sleep(1)

    # Create Security Zones
    sz1 = fmcapi.SecurityZones(fmc=fmc, name="IG-INSIDE")
    sz1.post()
    sz2 = fmcapi.SecurityZones(fmc=fmc, name="SZ-OUTSIDE1")
    sz2.post()

    # Autonat a network object to a host
    autonat1 = fmcapi.AutoNatRules(fmc=fmc)
    autonat1.original_network(name="_net_original")
    autonat1.translated_network(name="_net_xlate")
    autonat1.natType = "STATIC"
    # Source and destination interface can be either an interface group or security zone
    autonat1.source_intf(name="IG-INSIDE")
    autonat1.destination_intf(name="SZ-OUTSIDE1")
    autonat1.nat_policy(name=namer)

    # Autonat identity nat
    autonat2 = fmcapi.AutoNatRules(fmc=fmc)
    autonat2.identity_nat(name="_net_identity")
    autonat2.source_intf(name="IG-INSIDE")
    autonat2.destination_intf(name="SZ-OUTSIDE1")
    autonat2.nat_policy(name=namer)

    # Autonat nat pool
    autonat3 = fmcapi.AutoNatRules(fmc=fmc)
    autonat3.original_network(name="_net_original_pool")
    autonat3.patPool(name="_net_xlate_pool")
    autonat3.source_intf(name="IG-INSIDE")
    autonat3.destination_intf(name="SZ-OUTSIDE1")
    autonat3.nat_policy(name=namer)

    # Autonat interface PAT
    autonat4 = fmcapi.AutoNatRules(fmc=fmc)
    autonat4.original_network(name="_net_original_intf")
    autonat4.natType = "DYNAMIC"
    autonat4.source_intf(name="IG-INSIDE")
    autonat4.destination_intf(name="SZ-OUTSIDE1")
    autonat4.nat_policy(name=namer)
    autonat4.interfaceInTranslatedNetwork = True

    autonat1.post()
    autonat2.post()
    autonat3.post()
    autonat4.post()

    """
    # Associate a nat policy to a device
    # Do not uncomment if you do not have a device registered to FMC
    # Use name of device or deviceHAPair as applicable
    pol_devices = [{"name": "deviceHAName", "type": "deviceHAPair"}]
    assign1 = fmcapi.PolicyAssignments(fmc=fmc)
    assign1.ftd_natpolicy(name=namer, devices=pol_devices)
    assign1.post()
    assign1.ftd_natpolicy(name=namer, devices=[])
    assign1.put()
    """

    natpol1.delete()
    obj1.delete()
    obj2.delete()
    obj3.delete()
    obj4.delete()
    obj5.delete()
    obj6.delete()
    sz1.delete()
    sz2.delete()
