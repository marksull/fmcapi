import logging
import fmcapi
import time


def test__ftds2svpns(fmc):
    logging.info("Testing FTDS2SVPNs class.  Requires at least one registered device.")

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    # Create a Site2Site VPN Policy

    vpnpol1 = fmcapi.FTDS2SVPNs(fmc=fmc, name=namer)
    vpnpol1.topologyType = "POINT_TO_POINT"
    vpnpol1.ikeV1Enabled = True
    vpnpol1.ikeV2Enabled = False
    vpnpol1.post()
    vpnpol1.get()

    # Create some network objects for the encryption domains
    obj1 = fmcapi.Networks(fmc=fmc)
    obj1.name = "_net1_site1"
    obj1.value = "10.255.0.0/24"
    obj1.post()
    time.sleep(1)

    obj2 = fmcapi.Networks(fmc=fmc)
    obj2.name = "_net2_site1"
    obj2.value = "10.255.1.0/24"
    obj2.post()
    time.sleep(1)

    obj3 = fmcapi.Networks(fmc=fmc)
    obj3.name = "_net1_site2"
    obj3.value = "10.255.2.0/24"
    obj3.post()
    time.sleep(1)

    # Create Phase 1 settings
    # There is no way to search by name, so we just find the iksettings object inside the vpn policy
    ike1_json = fmcapi.IKESettings(fmc=fmc)
    ike1_json.vpn_policy(pol_name=namer)
    items = ike1_json.get()["items"][0]

    ike1 = fmcapi.IKESettings(fmc=fmc)
    ike1.vpn_policy(pol_name=namer)
    ike1.id = items["id"]
    ike1.get()
    ike1.ike_policy(pol_name="preshared_sha_aes192_dh5_10")

    ike1.put()

    # Create Phase 2 settings
    # There is no way to search by name, so we just find the ipsecsettings object inside the vpn policy
    ipsec1_json = fmcapi.IPSecSettings(fmc=fmc)
    ipsec1_json.vpn_policy(pol_name=namer)
    items = ipsec1_json.get()["items"][0]

    ipsec1 = fmcapi.IPSecSettings(fmc=fmc)
    ipsec1.vpn_policy(pol_name=namer)
    ipsec1.id = items["id"]
    ipsec1.get()
    ipsec1.ipsec_policy(pol_name="tunnel_aes256_sha")

    ipsec1.put()

    # Add vpn peers
    # FTD in HA mode should use the name of logical HA device
    endp1 = fmcapi.Endpoints(fmc=fmc)
    endp1.peerType = "PEER"
    endp1.connectionType = "BIDIRECTIONAL"
    endp1.vpn_policy(pol_name=namer)
    endp1.endpoint(action="add", device_name="_ha_name")
    endp1.vpn_interface(device_name="_ha_name", ifname="OUTSIDE1")
    endp1.encryption_domain(action="add", names=["_net1_site1", "_net2_site1"])

    endp2 = fmcapi.Endpoints(fmc=fmc)
    endp2.peerType = "PEER"
    endp2.connectionType = "BIDIRECTIONAL"
    endp2.vpn_policy(pol_name=namer)
    endp2.endpoint(action="add", device_name="_device_name")
    endp2.vpn_interface(device_name="device_name", ifname="OUTSIDE1")
    endp2.encryption_domain(action="add", names=["_net1_site2"])

    endp1.post()
    endp2.post()

    time.sleep(30)

    vpnpol1.delete()
    obj1.delete()
    obj2.delete()
    obj3.delete()
