"""
Program SDA Security PoV's FMC and FTD for this PoV.
"""
import fmcapi
import logging
from ruamel.yaml import YAML
from pathlib import Path

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
        sz1 = fmcapi.SecurityZones(fmc=fmc)
        sz1.name = sz['name']
        sz1.post()
        del sz1


def create_network_addresses(fmc, na_list):
    """Create NetworkAddresses Objects"""
    for na in na_list:
        netaddr = fmcapi.NetworkAddresses(fmc=fmc, name=na['name'], value=na['value'])
        netaddr.post()
        del netaddr


def create_networks(fmc, network_list):
    """Create Networks Objects"""
    for net in network_list:
        netaddr = fmcapi.Networks(fmc=fmc, name=net['name'], value=net['value'])
        netaddr.post()
        del netaddr


def create_access_policies(fmc, acp_list):
    """Create Access Policies and their associated AccessRules"""
    for acp in acp_list:
        policy = fmcapi.AccessPolicies(fmc=fmc, name=acp['name'], defaultAction=acp['default_action'])
        policy.post()
        # Build access_rules associated with this acp.
        for rule in acp['access_rules']:
            acp_rule = fmcapi.AccessRules(fmc=fmc, acp_name=policy.name, name=rule['name'])
            """  This is broken at the moment.
            if 'log_begin' in rule:
                acp_rule.logBegin = rule['log_begin']
            if 'log_end' in rule:
                acp_rule.logBegin = rule['log_end']
            """
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
                    acp_rule.destiantion_ise_sgt(action='add', name=sgt['name'])
            """
            acp_rule.post()
            del acp_rule
        del policy


def create_device_records(fmc, device_list):
    """DeviceRecords (Registration and Interfaces)"""
    for dr in device_list:
        ftd = fmcapi.DeviceRecords(fmc=fmc)
        ftd.hostName = dr['hostname']
        ftd.regKey = dr['registration_key']
        ftd.acp(name=dr['access_policy'])
        ftd.name = dr['name']
        for license1 in dr['licenses']:
            ftd.licensing(action='add', name=license1['name'])
        # Push to FMC to start device registration.
        ftd.post(post_wait_time=dr['wait_for_post'])
        # Registration done.  Time to configure it's interfaces.
        for interface_types in dr['interfaces']:
            if 'physical' in interface_types:
                for interface in interface_types['physical']:
                    int1 = fmcapi.PhysicalInterfaces(fmc=fmc, device_name=ftd.name)
                    int1.get(name=interface['name'])
                    int1.enabled = interface['enabled']
                    int1.ifname = interface['interface_name']
                    int1.sz(name=interface['security_zone'])
                    if 'static' in interface['addresses']['ipv4']:
                        v4 = interface['addresses']['ipv4']['static']
                        int1.static(ipv4addr=v4['ip'], ipv4mask=v4['bitmask'])
                    elif 'dhcp' in interface['addresses']['ipv4']:
                        v4 = interface['addresses']['ipv4']['dhcp']
                        int1.dhcp(enableDefault=v4['enable_default'], routeMetric=v4['route_metric'])
                    int1.put()
                    del int1
        for route_types in dr['routing']:
            if 'static' in route_types:
                for route in route_types['static']:
                    rt = fmcapi.IPv4StaticRoutes(fmc=fmc,
                                                 name=route['name'],
                                                 gw=route['gateway'],
                                                 interfaceName=route['interface'],
                                                 metric=route['metric']
                                                 )
                    rt.networks(action='add', networks=route['networks'])
                    rt.post()
                    del rt
        if 'nat_policy' in dr:
            natp = fmcapi.PolicyAssignments(fmc=fmc)
            natp.ftd_natpolicy(name=dr['nat_policy'], devices=[{'name': dr['name'], 'type': 'device'}])
            natp.post()
        del ftd


def program_fmc(data_vars):
    """Use values from YAML file to program the FMC. """
    if 'fmc' in data_vars:
        # noinspection PyBroadException
        try:
            with fmcapi.FMC(**data_vars['fmc']) as fmc1:
                if 'security_zones' in data_vars:
                    create_security_zones(fmc=fmc1, sz_list=data_vars['security_zones'])
                if 'network_addresses' in data_vars:
                    create_network_addresses(fmc=fmc1, na_list=data_vars['network_addresses'])
                if 'networks' in data_vars:
                    create_networks(fmc=fmc1, network_list=data_vars['networks'])
                if 'access_policies' in data_vars:
                    create_access_policies(fmc=fmc1, acp_list=data_vars['access_policies'])
                if 'device_records' in data_vars:
                    create_device_records(fmc=fmc1, device_list=data_vars['device_records'])
        except:
            logging.error(f"Section 'fmc' does not have enough/right information to establish a connection to FMC:")
    else:
        logging.warning(f"No 'fmc' section found in {YAML_FILE}")


if __name__ == "__main__":
    main()
