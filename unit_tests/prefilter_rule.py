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
    prefilter_rule_1.post()
    time.sleep(1)

    prefilter.delete()
    ip_host_1.delete()
    ip_net_1.delete()
    ip_range_1.delete()
    fqdn_1.delete()
    net_group_1.delete()
    sec_zone_1.delete()
    sec_zone_2.delete()
