import logging
import fmcapi
import time


def test__manualnat(fmc):
    logging.info("Testing ManualNatRules class.")

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

    # Create NAT divert objects
    obj7 = fmcapi.Hosts(fmc=fmc)
    obj7.name = "_net_source_divert"
    obj7.value = "172.30.1.1"
    obj7.post()
    time.sleep(1)

    obj8 = fmcapi.Hosts(fmc=fmc)
    obj8.name = "_net_destination_divert"
    obj8.value = "4.2.2.2"
    obj8.post()
    time.sleep(1)

    # Create port-based NAT objects
    obj9 = fmcapi.Hosts(fmc=fmc)
    obj9.name = "_net_source_portbased"
    obj9.value = "172.30.1.2"
    obj9.post()
    time.sleep(1)

    obj10 = fmcapi.Hosts(fmc=fmc)
    obj10.name = "_net_xlate_portbased"
    obj10.value = "192.0.2.254"
    obj10.post()
    time.sleep(1)

    obj11 = fmcapi.ProtocolPortObjects(fmc=fmc)
    obj11.name = "_port_original"
    obj11.protocol = "TCP"
    obj11.port = "443"
    obj11.post()
    time.sleep(1)

    obj12 = fmcapi.ProtocolPortObjects(fmc=fmc)
    obj12.name = "_port_xlate"
    obj12.protocol = "TCP"
    obj12.port = "8443"
    obj12.post()
    time.sleep(1)

    # Create Security Zones
    sz1 = fmcapi.SecurityZones(fmc=fmc, name="IG-INSIDE")
    sz1.post()
    sz2 = fmcapi.SecurityZones(fmc=fmc, name="SZ-OUTSIDE1")
    sz2.post()

    # Manualnat a network object to a host
    manualnat1 = fmcapi.ManualNatRules(fmc=fmc)
    manualnat1.original_source(name="_net_original")
    manualnat1.translated_source(name="_net_xlate")
    manualnat1.natType = "STATIC"
    # Source and destination interface can be either an interface group or security zone
    manualnat1.source_intf(name="IG-INSIDE")
    manualnat1.destination_intf(name="SZ-OUTSIDE1")
    manualnat1.enabled = True
    manualnat1.nat_policy(name=namer)

    # Manualnat identity nat
    manualnat2 = fmcapi.ManualNatRules(fmc=fmc)
    manualnat2.identity_nat(name="_net_identity")
    manualnat2.source_intf(name="IG-INSIDE")
    manualnat2.destination_intf(name="SZ-OUTSIDE1")
    manualnat2.enabled = True
    manualnat2.nat_policy(name=namer)

    # Manualnat nat pool
    manualnat3 = fmcapi.ManualNatRules(fmc=fmc)
    manualnat3.original_source(name="_net_original_pool")
    manualnat3.patPool(name="_net_xlate_pool")
    manualnat3.source_intf(name="IG-INSIDE")
    manualnat3.destination_intf(name="SZ-OUTSIDE1")
    manualnat3.enabled = True
    manualnat3.nat_policy(name=namer)

    # Manualnat interface PAT
    manualnat4 = fmcapi.ManualNatRules(fmc=fmc)
    manualnat4.original_source(name="_net_original_intf")
    manualnat4.natType = "DYNAMIC"
    manualnat4.unidirectional = True
    manualnat4.source_intf(name="IG-INSIDE")
    manualnat4.destination_intf(name="SZ-OUTSIDE1")
    manualnat4.nat_policy(name=namer)
    manualnat4.enabled = True
    manualnat4.interfaceInTranslatedSource = True

    # Manualnat divert
    manualnat5 = fmcapi.ManualNatRules(fmc=fmc)
    manualnat5.identity_nat(name="_net_source_divert")
    manualnat5.original_destination(name="_net_destination_divert")
    manualnat5.source_intf(name="IG-INSIDE")
    manualnat5.destination_intf(name="SZ-OUTSIDE1")
    manualnat5.enabled = True
    manualnat5.nat_policy(name=namer)

    # Manualnat port-based
    manualnat6 = fmcapi.ManualNatRules(fmc=fmc)
    manualnat6.original_source(name="_net_source_portbased")
    manualnat6.original_source_port(name="_port_original")
    manualnat6.translated_source(name="_net_xlate_portbased")
    manualnat6.translated_source_port(name="_port_xlate")
    manualnat6.natType = "STATIC"
    manualnat6.source_intf(name="IG-INSIDE")
    manualnat6.destination_intf(name="SZ-OUTSIDE1")
    manualnat6.enabled = True
    manualnat6.nat_policy(name=namer)

    manualnat1.post()
    manualnat2.post()
    manualnat3.post()
    manualnat4.post()
    manualnat5.post()
    manualnat6.post()

    """
    # Associate a nat policy to a device
    # Do not uncomment if you do not have a device registered to FPMC
    # Use name of device or deviceHAPair as applicable
    pol_devices = [{"name": "ftdv-HA", "type": "deviceHAPair"}]
    assign1 = PolicyAssignments(fmc=fmc)
    assign1.ftd_natpolicy(name=namer, devices=pol_devices)
    assign1.post()

    assign1.ftd_natpolicy(name=namer, devices=[])
    assign1.put()
    """

    logging.info("Cleanup of testing ManualNatRule methods.")

    natpol1.delete()
    obj1.delete()
    obj2.delete()
    obj3.delete()
    obj4.delete()
    obj5.delete()
    obj6.delete()
    obj7.delete()
    obj8.delete()
    obj9.delete()
    obj10.delete()
    obj11.delete()
    obj12.delete()
    sz1.delete()
    sz2.delete()
