"""
Program FMC and FTD using YAML file for user data.
"""
import fmcapi
import logging
from ruamel.yaml import YAML
from pathlib import Path
import time

# User Modifiable Data
YAML_CONFIGS_DIR = '.'
YAML_FILE = 'userdata.yml'


def main():
    """Grab the data from the yaml file and send it to program_fmc()."""
    yaml = YAML(typ='safe')
    path = Path(YAML_CONFIGS_DIR) / YAML_FILE
    with open(path, 'r') as stream:
        try:
            my_data = yaml.load(stream)
            logging.info(f"Loading {path} file.")
            program_fmc(my_data)
        except OSError:
            logging.error(f"An error has occurred trying to open {path}.")
            exit(1)


def create_security_zones(fmc, sz_list):
    """Create Security Zones"""
    for sz in sz_list:
        if 'name' in sz:
            sz1 = fmcapi.SecurityZones(fmc=fmc, name=sz['name'])
            sz1.post()


def create_hosts(fmc, na_list):
    """Create Hosts Objects"""
    for na in na_list:
        if 'name' in na and 'value' in na:
            netaddr = fmcapi.Hosts(fmc=fmc, name=na['name'], value=na['value'])
            netaddr.post()


def create_networks(fmc, network_list):
    """Create Networks Objects"""
    for net in network_list:
        if 'name' in net and 'value' in net:
            netaddr = fmcapi.Networks(fmc=fmc, name=net['name'], value=net['value'])
            netaddr.post()


def create_access_policies(fmc, acp_list):
    """Create Access Policies and their associated AccessRules"""
    for acp in acp_list:
        policy = fmcapi.AccessPolicies(fmc=fmc, name=acp['name'], defaultAction=acp['default_action'])
        policy.post()

        # Build access_rules associated with this acp.
        if 'rules' in acp:
            for rule in acp['rules']:
                acp_rule = fmcapi.AccessRules(fmc=fmc, acp_name=policy.name, name=rule['name'])
                """  This is broken at the moment.
                if 'log_begin' in rule:
                    acp_rule.logBegin = rule['log_begin']
                if 'log_end' in rule:
                    acp_rule.logBegin = rule['log_end']
                """
                if 'enabled' in rule:
                    acp_rule.enabled = rule['enabled']
                if 'action' in rule:
                    acp_rule.action = rule['action']
                if 'source_networks' in rule:
                    for sn in rule['source_networks']:
                        acp_rule.source_network(action='add', name=sn['name'])
                if 'destination_networks' in rule:
                    for dn in rule['destination_networks']:
                        acp_rule.destination_network(action='add', name=dn['name'])
                if 'source_ports' in rule:
                    for sp in rule['source_ports']:
                        acp_rule.source_port(action='add', name=sp['name'])
                if 'destination_ports' in rule:
                    for dp in rule['destination_ports']:
                        acp_rule.destination_port(action='add', name=dp['name'])
                if 'intrusion_policy' in rule:
                    acp_rule.intrusion_policy(action='add', name=rule['intrusion_policy'])
                """
                # Using SGTs isn't implemented in fmcapi yet.
                if 'source_ise_sgts' in rule:
                    for sgt in rule['source_ise_sgts']:
                        acp_rule.source_ise_sgt(action='add', name=sgt['name'])
                if 'destination_ise_sgts' in rule:
                    for sgt in rule['destination_ise_sgts']:
                        acp_rule.destination_ise_sgt(action='add', name=sgt['name'])
                """
                acp_rule.post()


def create_nat_policies(fmc, nat_list):
    """Create Nat Policies and their rules"""
    for natp in nat_list:
        policy = fmcapi.FTDNatPolicies(fmc=fmc, name=natp['name'])
        policy.post()
        print("Sleeping for 10 seconds to see if this solves my problem.")
        time.sleep(10)

        # Build nat_rules associated with this nat policy.
        if 'rules' in natp:
            print("Am I here?")  # FIXME:  We don't ger here.  I don't know why yet.
            for rule_type in natp['rules']:
                if 'auto' in rule_type:
                    autorule = rule_type['auto']
                    autonat = fmcapi.AutoNatRules(fmc=fmc)
                    if 'nat_type' in autorule:
                        autonat.natType = autorule['nat_type']
                    if 'interface_in_translated_network' in autorule:
                        autonat.interfaceInTranslatedNetwork = autorule['interface_in_translated_network']
                    if 'original_network' in autorule:
                        autonat.original_network(autorule['original_network'])
                    if 'source_interface' in autorule:
                        autonat.source_intf(name=autorule['source_interface'])
                    if 'destination_interface' in autorule:
                        autonat.destination_intf(name=autorule['destination_interface'])
                    autonat.nat_policy(name=natp['name'])
                    autonat.post()
                elif 'manual' in rule_type:
                    manualrule = rule_type['manual']
                    manualnat = fmcapi.ManualNatRules(fmc=fmc)
                    if 'nat_type' in manualrule:
                        manualnat.natType = manualrule['nat_type']
                    if 'original_source' in manualrule:
                        manualnat.original_source(manualrule['original_source'])
                    if 'translated_source' in manualrule:
                        manualnat.translated_source(manualrule['translated_source'])
                    if 'source_interface' in manualrule:
                        manualnat.source_intf(name=manualrule['source_interface'])
                    if 'destination_interface' in manualrule:
                        manualnat.destination_intf(name=manualrule['destination_interface'])
                    if 'enabled' in manualrule:
                        manualnat.enabled = manualrule['enabled']
                    manualnat.nat_policy(name=natp['name'])
                    manualnat.post()


def create_device_records(fmc, device_list):
    """DeviceRecords (Registration and Interfaces)"""
    for dr in device_list:
        # Register this device with the FMC.  Assume the device is pre-programmed to listen for the FTD registration.
        ftd = fmcapi.DeviceRecords(fmc=fmc)
        if 'hostname' in dr:
            ftd.hostName = dr['hostname']
        if 'registration_key' in dr:
            ftd.regKey = dr['registration_key']
        if 'access_policy' in dr:
            ftd.acp(name=dr['access_policy'])
        if 'name' in dr:
            ftd.name = dr['name']
        if 'licenses' in dr:
            for lice in dr['licenses']:
                ftd.licensing(action='add', name=lice['name'])
        # Push to FMC to start device registration.
        ftd.post(post_wait_time=dr['wait_for_post'])

        # Time to configure interfaces.
        if 'interfaces' in dr:
            for interface_types in dr['interfaces']:
                if 'physical' in interface_types:
                    for interface in interface_types['physical']:
                        int1 = fmcapi.PhysicalInterfaces(fmc=fmc, device_name=dr['name'])
                        if 'name ' in interface:
                            int1.get(name=interface['name'])
                        if 'enabled' in interface:
                            int1.enabled = interface['enabled']
                        if 'interface_name' in interface:
                            int1.ifname = interface['interface_name']
                        if 'security_zone' in interface:
                            int1.sz(name=interface['security_zone'])
                        if 'ipv4' in interface:
                            if 'static' in interface['addresses']['ipv4']:
                                int1.static(ipv4addr=interface['addresses']['ipv4']['static']['ip'],
                                            ipv4mask=interface['addresses']['ipv4']['static']['bitmask'])
                            elif 'dhcp' in interface['addresses']['ipv4']:
                                int1.dhcp(enableDefault=interface['addresses']['ipv4']['dhcp']['enable_default'],
                                          routeMetric=interface['addresses']['ipv4']['dhcp']['route_metric'])
                        if 'ipv6' in interface:
                            pass
                        int1.put()
                elif 'blah' in interface_types:
                    pass

        # Any routing related to this device.
        if 'routing' in dr:
            for route_types in dr['routing']:
                if 'static' in route_types:
                    if 'ipv4' in route_types['static']:
                        for route in route_types['static']['ipv4']:
                            rt = fmcapi.IPv4StaticRoutes(fmc=fmc)
                            if 'name' in route:
                                rt.name = route['name']
                            if 'device_name' in route:
                                rt.device(device_name=route['device_name'])
                            if 'networks' in route:
                                for network in route['networks']:
                                    if 'name' in network:
                                        rt.networks(action='add', networks=network['name'])
                            if 'gateway' in route:
                                rt.gw(name=route['gateway'])
                            if 'interface' in route:
                                rt.interfaceName = route['interface']
                            if 'metric' in route:
                                rt.metricValue = route['metric']
                            rt.post()
                    if 'ipv6' in route_types['static']:
                        pass
                elif 'blah' in route_types:
                    pass

        # Any NAT Policy assigned to this device.
        if 'nat_policy' in dr:
            natp = fmcapi.PolicyAssignments(fmc=fmc)
            natp.ftd_natpolicy(name=dr['nat_policy'], devices=[{'name': dr['name'], 'type': 'device'}])
            natp.post()


def program_fmc(data_vars):
    """Use values from YAML file to program the FMC. """
    if 'fmc' in data_vars:
        # noinspection PyBroadException
        try:
            with fmcapi.FMC(**data_vars['fmc']) as fmc1:
                if 'security_zones' in data_vars:
                    create_security_zones(fmc=fmc1, sz_list=data_vars['security_zones'])
                else:
                    logging.info("'security_zones' section not in YAML file.  Skipping.")
                if 'hosts' in data_vars:
                    create_hosts(fmc=fmc1, na_list=data_vars['hosts'])
                else:
                    logging.info("'hosts' section not in YAML file.  Skipping.")
                if 'networks' in data_vars:
                    create_networks(fmc=fmc1, network_list=data_vars['networks'])
                else:
                    logging.info("'networks' section not in YAML file.  Skipping.")
                if 'access_policies' in data_vars:
                    create_access_policies(fmc=fmc1, acp_list=data_vars['access_policies'])
                else:
                    logging.info("'access_policies' section not in YAML file.  Skipping.")
                if 'nat_policies' in data_vars:
                    create_nat_policies(fmc=fmc1, nat_list=data_vars['nat_policies'])
                else:
                    logging.info("'nat_policies' section not in YAML file.  Skipping.")
                if 'device_records' in data_vars:
                    create_device_records(fmc=fmc1, device_list=data_vars['device_records'])
                else:
                    logging.info("'device_records' section not in YAML file.  Skipping.")
        except:
            logging.error(f"Section 'fmc' does not have the right information (bad password?)"
                          f" to establish a connection to FMC:")
    else:
        logging.warning(f"No 'fmc' section found in {YAML_FILE}")


if __name__ == "__main__":
    main()
