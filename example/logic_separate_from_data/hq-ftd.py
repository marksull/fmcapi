#! /usr/bin/env python
"""
Program FMC and FTD using YAML file for user data.
"""
import fmcapi
import logging
from ruamel.yaml import YAML
from pathlib import Path
import argparse


def main(datafile):
    """Grab the data from the yaml file and send it to program_fmc()."""
    yaml = YAML(typ="safe")
    path = Path(datafile)
    with open(path, "r") as stream:
        try:
            my_data = yaml.load(stream)
            logging.info(f"Loading {path} file.")
            program_fmc(data_vars=my_data, path=path)
        except OSError:
            logging.error(f"An error has occurred trying to open {path}.")
            exit(1)


def program_fmc(data_vars, path):
    """Use values from YAML file to program the FMC. """
    if "fmc" in data_vars:
        # noinspection PyBroadException
        try:
            with fmcapi.FMC(**data_vars["fmc"]) as fmc1:
                if "security_zones" in data_vars:
                    create_security_zones(fmc=fmc1, sz_list=data_vars["security_zones"])
                else:
                    logging.info(
                        "'security_zones' section not in YAML file.  Skipping."
                    )
                if "hosts" in data_vars:
                    create_hosts(fmc=fmc1, na_list=data_vars["hosts"])
                else:
                    logging.info("'hosts' section not in YAML file.  Skipping.")
                if "networks" in data_vars:
                    create_networks(fmc=fmc1, network_list=data_vars["networks"])
                else:
                    logging.info("'networks' section not in YAML file.  Skipping.")
                if "access_policies" in data_vars:
                    create_access_policies(
                        fmc=fmc1, acp_list=data_vars["access_policies"]
                    )
                else:
                    logging.info(
                        "'access_policies' section not in YAML file.  Skipping."
                    )
                if "nat_policies" in data_vars:
                    create_nat_policies(fmc=fmc1, nat_list=data_vars["nat_policies"])
                else:
                    logging.info("'nat_policies' section not in YAML file.  Skipping.")
                if "device_records" in data_vars:
                    create_device_records(
                        fmc=fmc1, device_list=data_vars["device_records"]
                    )
                else:
                    logging.info(
                        "'device_records' section not in YAML file.  Skipping."
                    )
        except Exception as e:
            logging.error(
                f"Section 'fmc' does not have the right information (bad password?)"
                f" to establish a connection to FMC:"
            )
            logging.error(f"Error is '{e}'")
    else:
        logging.warning(f"No 'fmc' section found in {path}")


def create_security_zones(fmc, sz_list):
    """Create Security Zones"""
    for sz in sz_list:
        if "name" in sz:
            sz1 = fmcapi.SecurityZones(fmc=fmc, name=sz["name"])
            sz1.post()


def create_hosts(fmc, na_list):
    """Create Hosts Objects"""
    for na in na_list:
        if "name" in na and "value" in na:
            netaddr = fmcapi.Hosts(fmc=fmc, name=na["name"], value=na["value"])
            netaddr.post()


def create_networks(fmc, network_list):
    """Create Networks Objects"""
    for net in network_list:
        if "name" in net and "value" in net:
            netaddr = fmcapi.Networks(fmc=fmc, name=net["name"], value=net["value"])
            netaddr.post()


def create_access_policies(fmc, acp_list):
    """Create Access Policies and their associated AccessRules"""
    for acp in acp_list:
        policy = fmcapi.AccessPolicies(
            fmc=fmc, name=acp["name"], defaultAction=acp["default_action"]
        )
        policy.post()

        # Build access_rules associated with this acp.
        if "rules" in acp:
            for rule in acp["rules"]:
                acp_rule = fmcapi.AccessRules(
                    fmc=fmc, acp_name=policy.name, name=rule["name"]
                )
                if "log_begin" in rule:
                    acp_rule.logBegin = rule["log_begin"]
                if "log_end" in rule:
                    acp_rule.logEnd = rule["log_end"]
                if "send_events_to_fmc" in rule:
                    acp_rule.sendEventsToFMC = rule["send_events_to_fmc"]
                if "enabled" in rule:
                    acp_rule.enabled = rule["enabled"]
                if "action" in rule:
                    acp_rule.action = rule["action"]
                if "source_networks" in rule:
                    for sn in rule["source_networks"]:
                        acp_rule.source_network(action="add", name=sn["name"])
                if "destination_networks" in rule:
                    for dn in rule["destination_networks"]:
                        acp_rule.destination_network(action="add", name=dn["name"])
                if "source_ports" in rule:
                    for sp in rule["source_ports"]:
                        acp_rule.source_port(action="add", name=sp["name"])
                if "destination_ports" in rule:
                    for dp in rule["destination_ports"]:
                        acp_rule.destination_port(action="add", name=dp["name"])
                if "intrusion_policy" in rule:
                    acp_rule.intrusion_policy(
                        action="add", name=rule["intrusion_policy"]
                    )
                """ Using SGTs isn't implemented in fmcapi yet.
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
        policy = fmcapi.FTDNatPolicies(fmc=fmc, name=natp["name"])
        policy.post()

        # Build nat_rules associated with this nat policy.
        if "rules" in natp:
            if "auto" in natp["rules"]:
                for this_rule in natp["rules"]["auto"]:
                    autonat = fmcapi.AutoNatRules(fmc=fmc)
                    if "nat_type" in this_rule:
                        autonat.natType = this_rule["nat_type"]
                    if "interface_in_translated_network" in this_rule:
                        autonat.interfaceInTranslatedNetwork = this_rule[
                            "interface_in_translated_network"
                        ]
                    if "original_network" in this_rule:
                        autonat.original_network(this_rule["original_network"])
                    if "source_interface" in this_rule:
                        autonat.source_intf(name=this_rule["source_interface"])
                    if "destination_interface" in this_rule:
                        autonat.destination_intf(
                            name=this_rule["destination_interface"]
                        )
                    autonat.nat_policy(name=natp["name"])
                    autonat.post()
            if "manual" in natp["rules"]:
                for this_rule in natp["rules"]["manual"]:
                    manualnat = fmcapi.ManualNatRules(fmc=fmc)
                    if "nat_type" in this_rule:
                        manualnat.natType = this_rule["nat_type"]
                    if "original_source" in this_rule:
                        manualnat.original_source(this_rule["original_source"])
                    if "translated_source" in this_rule:
                        manualnat.translated_source(this_rule["translated_source"])
                    if "source_interface" in this_rule:
                        manualnat.source_intf(name=this_rule["source_interface"])
                    if "destination_interface" in this_rule:
                        manualnat.destination_intf(
                            name=this_rule["destination_interface"]
                        )
                    if "enabled" in this_rule:
                        manualnat.enabled = this_rule["enabled"]
                    manualnat.nat_policy(name=natp["name"])
                    manualnat.post()


def create_device_records(fmc, device_list):
    """DeviceRecords (Registration and Interfaces)"""
    for dr in device_list:
        # Register this device with the FMC.  Assume the device is pre-programmed to listen for the FTD registration.
        ftd = fmcapi.DeviceRecords(fmc=fmc)
        if "hostname" in dr:
            ftd.hostName = dr["hostname"]
        if "registration_key" in dr:
            ftd.regKey = dr["registration_key"]
        if "access_policy" in dr:
            ftd.acp(name=dr["access_policy"])
        if "name" in dr:
            ftd.name = dr["name"]
        if "licenses" in dr:
            for lice in dr["licenses"]:
                ftd.licensing(action="add", name=lice["name"])
        # Push to FMC to start device registration.
        ftd.post(post_wait_time=dr["wait_for_post"])

        # Time to configure interfaces.
        if "interfaces" in dr:
            if "physical" in dr["interfaces"]:
                for interface in dr["interfaces"]["physical"]:
                    int1 = fmcapi.PhysicalInterfaces(fmc=fmc, device_name=dr["name"])
                    if "name" in interface:
                        int1.get(name=interface["name"])
                    if "enabled" in interface:
                        int1.enabled = interface["enabled"]
                    if "interface_name" in interface:
                        int1.ifname = interface["interface_name"]
                    if "security_zone" in interface:
                        int1.sz(name=interface["security_zone"])
                    if "addresses" in interface:
                        if "ipv4" in interface["addresses"]:
                            if "static" in interface["addresses"]["ipv4"]:
                                int1.static(
                                    ipv4addr=interface["addresses"]["ipv4"]["static"][
                                        "ip"
                                    ],
                                    ipv4mask=interface["addresses"]["ipv4"]["static"][
                                        "bitmask"
                                    ],
                                )
                            elif "dhcp" in interface["addresses"]["ipv4"]:
                                int1.dhcp(
                                    enableDefault=interface["addresses"]["ipv4"][
                                        "dhcp"
                                    ]["enable_default"],
                                    routeMetric=interface["addresses"]["ipv4"]["dhcp"][
                                        "route_metric"
                                    ],
                                )
                        if "ipv6" in interface["addresses"]:
                            pass
                    int1.put()

        # Any routing related to this device.
        if "routing" in dr:
            if "static" in dr["routing"]:
                if "ipv4" in dr["routing"]["static"]:
                    for route in dr["routing"]["static"]["ipv4"]:
                        rt = fmcapi.IPv4StaticRoutes(fmc=fmc, device_name=dr["name"])
                        if "name" in route:
                            rt.name = route["name"]
                        if "networks" in route:
                            for network in route["networks"]:
                                if "name" in network:
                                    rt.networks(
                                        action="add", networks=[network["name"]]
                                    )
                        if "gateway" in route:
                            rt.gw(name=route["gateway"])
                        if "interface_name" in route:
                            rt.interfaceName = route["interface_name"]
                        if "metric" in route:
                            rt.metricValue = route["metric"]
                        rt.post()
                if "ipv6" in dr["routing"]["static"]:
                    pass

        # Any NAT Policy assigned to this device.
        if "nat_policy" in dr:
            natp = fmcapi.PolicyAssignments(fmc=fmc)
            natp.ftd_natpolicy(
                name=dr["nat_policy"],
                devices=[{"name": dr["name"], "type": dr["type"]}],
            )
            natp.post()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Specify arguments to modify program.")
    parser.add_argument(
        "-d",
        "--datafile",
        action="store",
        dest="datafile",
        type=str,
        help="Path and filename to YAML file containing data.",
        default="datafile.yml",
    )
    args = parser.parse_args()
    main(datafile=args.datafile)
