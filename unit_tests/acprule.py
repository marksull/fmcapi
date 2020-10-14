import logging
import fmcapi
import time


def test__acp_rule(fmc):
    logging.info(
        "In preparation for testing ACPRule methods, set up some known objects in the FMC."
    )

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    # Build an IP host object
    iphost1 = fmcapi.Hosts(fmc=fmc, name="_iphost1", value="7.7.7.7")
    iphost1.post()
    # Build an IP Network object
    ipnet1 = fmcapi.Networks(fmc=fmc, name="_ipnet1", value="1.2.3.0/24")
    ipnet1.post()
    # Build an IP range object
    iprange1 = fmcapi.Ranges(fmc=fmc, name="_iprange1", value="6.6.6.6-7.7.7.7")
    iprange1.post()
    # Build a Network Group object
    ipnet2 = fmcapi.Networks(fmc=fmc, name="_ipnet2", value="5.5.5.0/24")
    ipnet2.post()
    time.sleep(1)
    # Build an FQDNS object
    fqdns1 = fmcapi.FQDNS(fmc=fmc, name="_fqdns1", value="www.cisco.com")
    fqdns1.post()

    obj1 = fmcapi.NetworkGroups(fmc=fmc, name="_fmcapi_test_networkgroup")
    obj1.named_networks(action="add", name=ipnet2.name)
    obj1.unnamed_networks(action="add", value="4.4.4.4/32")
    obj1.post()
    # Build a URL object
    url1 = fmcapi.URLs(fmc=fmc, name="_url1", url="asdf.org")
    url1.post()
    url1.get()
    # lists = [{"type": url1.type, "id": url1.id, "name": url1.name}]
    # Build a VLAN Tag object
    vlantag1 = fmcapi.VlanTags(
        fmc=fmc, name="_vlantag1", data={"startTag": "888", "endTag": "999"}
    )
    vlantag1.post()
    # Build a Port object
    pport1 = fmcapi.ProtocolPortObjects(
        fmc=fmc, name="_pport1", port="9090", protocol="UDP"
    )
    pport1.post()
    # Build a Port Group Object
    obj10 = fmcapi.ProtocolPortObjects(
        fmc=fmc, name="_porttcp1", port="8443", protocol="TCP"
    )
    obj10.post()
    obj11 = fmcapi.ProtocolPortObjects(
        fmc=fmc, name="_portudp1", port="161", protocol="UDP"
    )
    obj11.post()
    obj12 = fmcapi.ProtocolPortObjects(
        fmc=fmc, name="_portrangetcp1", port="0-1023", protocol="TCP"
    )
    obj12.post()
    obj2 = fmcapi.PortObjectGroups(fmc=fmc, name="_fmcapi_test_portobjectgroup")
    obj2.named_ports(action="add", name=obj10.name)
    obj2.named_ports(action="add", name=obj11.name)
    obj2.named_ports(action="add", name=obj12.name)
    obj2.post()
    # Build a Security Zone object
    sz1 = fmcapi.SecurityZones(fmc=fmc, name="_sz1", interfaceMode="ROUTED")
    sz1.post()
    # Build an ACP Object
    acp1 = fmcapi.AccessPolicies(fmc=fmc, name=namer)
    acp1.post()
    # Get a file_policy
    # fp = fmcapi.FilePolicies(fmc=fmc1, name='daxm_test')
    time.sleep(1)
    logging.info("Setup of objects for ACPRule test done.\n")

    logging.info(
        "Test ACPRule.  Try to test all features of all methods of the ACPRule class."
    )
    acprule1 = fmcapi.AccessRules(fmc=fmc, acp_name=acp1.name)
    acprule1.name = namer
    acprule1.action = "ALLOW"
    acprule1.enabled = False
    acprule1.sendEventsToFMC = True
    acprule1.logFiles = False
    acprule1.logBegin = True
    acprule1.logEnd = True
    acprule1.variable_set(action="set", name="Default-Set")
    acprule1.source_zone(action="add", name=sz1.name)
    acprule1.destination_zone(action="add", name=sz1.name)
    acprule1.intrusion_policy(action="set", name="Security Over Connectivity")
    acprule1.vlan_tags(action="add", name=vlantag1.name)
    acprule1.source_port(action="add", name=pport1.name)
    acprule1.destination_port(action="add", name=pport1.name)
    acprule1.destination_port(action="add", name=obj2.name)
    acprule1.source_network(action="add", name=iphost1.name)
    acprule1.source_network(action="add", name=obj1.name)
    acprule1.source_network(action="add", name=iprange1.name)
    acprule1.destination_network(action="add", name=ipnet1.name)
    acprule1.destination_network(action="add", name=iprange1.name)
    acprule1.destination_network(action="add", name=fqdns1.name)
    acprule1.urls_info(action="add", name=url1.name)

    # To set a comment on an ACP rule, you use the new_comments function which sets "newComments" in the API POST call
    # To read comments, you read the "commentHistoryList" from the API GET call
    # Just another one of those strange quirks of the FMC API
    acprule1.new_comments(action="add", value="comment-1")
    acprule1.post()

    logging.info("Test ACPRule done.\n")

    logging.info("Cleanup of testing ACPRule methods.")
    acprule1.delete()
    time.sleep(1)
    acp1.delete()
    iphost1.delete()
    ipnet1.delete()
    iprange1.delete()
    fqdns1.delete()
    obj1.delete()
    ipnet2.delete()
    url1.delete()
    vlantag1.delete()
    pport1.delete()
    sz1.delete()
    obj2.delete()
    obj10.delete()
    obj11.delete()
    obj12.delete()
    logging.info("Cleanup of objects for ACPRule test done.\n")
