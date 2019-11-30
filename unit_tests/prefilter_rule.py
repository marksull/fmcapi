import logging
import time
from fmcapi import (
    Hosts,
    Networks,
    Ranges,
    FQDNS,
    NetworkGroups,
    PreFilterPolicies,
    PreFilterRules,
    SecurityZones,
    PortObjectGroups,
    ProtocolPortObjects,
    VlanGroupTags,
    VlanTags,
)


def test__prefiler_rule(fmc):
    logging.info("Testing prefilter rules on FMC")
    logging.info("Creating objects for testing on FMC")

    namer = f"fmcapi_test_{str(int(time.time()))}"
    ip_host_1 = Hosts(fmc=fmc, name=f"test_host_1_{namer}", value="7.7.7.7")
    ip_host_1.post()
    ip_net_1 = Networks(fmc=fmc, name=f"test_net_1_{namer}", value="10.0.0.0/8")
    ip_net_1.post()
    ip_range_1 = Ranges(
        fmc=fmc, name=f"test_range_1_{namer}", value="10.1.1.1-10.1.1.10"
    )
    ip_range_1.post()
    fqdn_1 = FQDNS(fmc=fmc, name=f"test_fqdn_1_{namer}", value="www.cisco.com")
    fqdn_1.post()
    net_group_1 = NetworkGroups(fmc=fmc, name=f"net_group_1_{namer}")
    net_group_1.named_networks(action="add", name=f"test_net_1_{namer}")
    net_group_1.post()
    sec_zone_1 = SecurityZones(
        fmc=fmc, name=f"test_zone_1_{namer}", interfaceMode="ROUTED"
    )
    sec_zone_1.post()
    sec_zone_2 = SecurityZones(
        fmc=fmc, name=f"test_zone_2_{namer}", interfaceMode="ROUTED"
    )
    sec_zone_2.post()
    port_1 = ProtocolPortObjects(
        fmc=fmc, name=f"test_port_1_{namer}", port="8443", protocol="TCP"
    )
    port_1.post()
    port_2 = ProtocolPortObjects(
        fmc=fmc, name=f"test_port_2_{namer}", port="161", protocol="UDP"
    )
    port_2.post()
    port_3 = ProtocolPortObjects(
        fmc=fmc, name=f"test_port_3_{namer}", port="0-1023", protocol="TCP"
    )
    port_3.post()
    time.sleep(1)
    port_group_1 = PortObjectGroups(fmc=fmc, name=f"port_group_1_{namer}")
    port_group_1.named_ports(action="add", name=port_1.name)
    port_group_1.named_ports(action="add", name=port_2.name)
    port_group_1.named_ports(action="add", name=port_3.name)
    port_group_1.post()

    vlan_tag_1 = VlanTags(fmc=fmc, name=f"vlan_tag_1_{namer}")
    vlan_tag_1.vlans(start_vlan="1", end_vlan="9")
    vlan_tag_1.post()
    vlan_tag_2 = VlanTags(fmc=fmc, name=f"vlan_tag_2_{namer}")
    vlan_tag_2.vlans(start_vlan="10", end_vlan="19")
    vlan_tag_2.post()
    vlan_tag_3 = VlanTags(fmc=fmc, name=f"vlan_tag_3_{namer}")
    vlan_tag_3.vlans(start_vlan="20", end_vlan="29")
    vlan_tag_3.post()
    vlan_group_1 = VlanGroupTags(fmc=fmc, name=f"vlan_group_1_{namer}")
    vlan_group_1.named_vlantags(action="add", name=f"vlan_tag_3_{namer}")
    vlan_group_1.post()

    logging.info(f'Creating test prefiler "{namer}"')
    prefilter = PreFilterPolicies(fmc=fmc, name=namer)
    prefilter.post()
    time.sleep(1)

    logging.info(f'Creating test prefiler "{namer}"')
    prefilter = PreFilterPolicies(fmc=fmc, name=namer)
    prefilter.post()
    time.sleep(1)

    logging.info(f'Creating test prefiler rule "test_1"')
    prefilter_rule_1 = PreFilterRules(fmc=fmc, prefilter_name=namer)
    prefilter_rule_1.name = "test_1"
    prefilter_rule_1.enabled = True
    prefilter_rule_1.source_interface(action="add", name=f"test_zone_1_{namer}")
    prefilter_rule_1.destination_interface(action="add", name=f"test_zone_2_{namer}")
    prefilter_rule_1.source_network(action="add", literal="10.1.1.1")
    prefilter_rule_1.destination_network(action="add", name=f"test_host_1_{namer}")
    prefilter_rule_1.destination_network(action="add", name=f"test_net_1_{namer}")
    prefilter_rule_1.destination_network(action="add", name=f"test_range_1_{namer}")
    prefilter_rule_1.destination_network(action="add", name=f"test_fqdn_1_{namer}")
    prefilter_rule_1.destination_network(action="remove", name=f"test_fqdn_1_{namer}")
    prefilter_rule_1.post()
    time.sleep(1)

    logging.info(f'Creating test prefiler rule "test_2"')
    prefilter_rule_2 = PreFilterRules(fmc=fmc, prefilter_name=namer)
    prefilter_rule_2.name = "test_2"
    prefilter_rule_2.enabled = True
    prefilter_rule_2.action = "FASTPATH"
    prefilter_rule_2.source_port(action="add", literal={"protocol": "6", "port": "22"})
    prefilter_rule_2.source_port(action="add", literal={"protocol": "6", "port": "443"})
    prefilter_rule_2.source_port(action="add", literal={"protocol": "17", "port": "53"})
    prefilter_rule_2.destination_port(action="add", name=f"test_port_1_{namer}")
    prefilter_rule_2.destination_port(action="add", name=f"test_port_2_{namer}")
    prefilter_rule_2.destination_port(action="add", name=f"test_port_3_{namer}")
    prefilter_rule_2.destination_port(action="remove", name=f"test_port_3{namer}")
    prefilter_rule_2.destination_port(action="add", name=f"port_group_1_{namer}")
    prefilter_rule_2.vlan_tags(action="add", literal="100-110")
    prefilter_rule_2.vlan_tags(action="add", name=f"vlan_tag_1_{namer}")
    prefilter_rule_2.vlan_tags(action="add", name=f"vlan_tag_2_{namer}")
    prefilter_rule_2.vlan_tags(action="add", name=f"vlan_tag_3_{namer}")
    prefilter_rule_2.vlan_tags(action="remove", name=f"vlan_tag_2_{namer}")
    prefilter_rule_2.vlan_tags(action="add", name=f"vlan_group_1_{namer}")
    prefilter_rule_2.post()
    time.sleep(1)

    prefilter.delete()
    ip_host_1.delete()
    ip_net_1.delete()
    ip_range_1.delete()
    fqdn_1.delete()
    net_group_1.delete()
    sec_zone_1.delete()
    sec_zone_2.delete()
    port_group_1.delete()
    port_1.delete()
    port_2.delete()
    port_3.delete()
    vlan_group_1.delete()
    vlan_tag_1.delete()
    vlan_tag_2.delete()
    vlan_tag_3.delete()
