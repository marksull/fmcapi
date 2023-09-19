"""
Unit testing, of a sort, all the created methods/classes.
"""

import fmcapi
import logging
import unit_tests


# ### Set these variables to match your environment. ### #

host = "10.0.0.10"
username = "apiadmin"
password = "Admin123"
autodeploy = False
logname = "TestingUserScript.log"
pagelimit = 500
debug = False


def main():
    with fmcapi.FMC(
        host=host,
        username=username,
        password=password,
        autodeploy=autodeploy,
        limit=pagelimit,
        file_logging=logname,
        debug=debug,
    ) as fmc1:
        logging.info("# ### Mega Test Start!!! ### #\n\n")
        unit_tests.test__fmc_version(fmc=fmc1)

        """
        # Working Tests
        unit_tests.test__vlan_group_tag(fmc=fmc1)
        unit_tests.test__deployment_requests(fmc=fmc1)
        unit_tests.test__audit_records(fmc=fmc1)
        unit_tests.test__deployable_devices(fmc=fmc1)
        unit_tests.test__devicegrouprecords(fmc=fmc1)

        unit_tests.test__application_type(fmc=fmc1)
        unit_tests.test__application_tag(fmc=fmc1)
        unit_tests.test__application(fmc=fmc1)
        unit_tests.test__application_risk(fmc=fmc1)
        unit_tests.test__application_filter(fmc=fmc1)
        unit_tests.test__application_productivity(fmc=fmc1)
        unit_tests.test__application_category(fmc=fmc1)
        unit_tests.test__cert_enrollment(fmc=fmc1)
        unit_tests.test__country(fmc=fmc1)
        unit_tests.test__filepolicies(fmc=fmc1)
        unit_tests.test__continent(fmc=fmc1)
        unit_tests.test__dns_servers_group(fmc=fmc1)
        unit_tests.test__url_group(fmc=fmc1)
        unit_tests.test__network_group(fmc=fmc1)
        unit_tests.test__ip_addresses(fmc=fmc1)
        unit_tests.test__variable_set(fmc=fmc1)
        unit_tests.test__ip_host(fmc=fmc1)
        unit_tests.test__ip_network(fmc=fmc1)
        unit_tests.test__ip_range(fmc=fmc1)
        unit_tests.test__extended_acls(fmc=fmc1)
        unit_tests.test__geolocations(fmc=fmc1)
        unit_tests.test__icmpv4(fmc=fmc1)
        unit_tests.test__icmpv6(fmc=fmc1)
        unit_tests.test__ikev1(fmc=fmc1)
        unit_tests.test__ikev2(fmc=fmc1)
        unit_tests.test__url(fmc=fmc1)
        unit_tests.test__vlan_tag(fmc=fmc1)
        unit_tests.test__protocol_port(fmc=fmc1)
        unit_tests.test__security_zone(fmc=fmc1)
        unit_tests.test__slamonitor(fmc=fmc1)
        unit_tests.test__intrusion_policy(fmc=fmc1)
        unit_tests.test__access_control_policy(fmc=fmc1)
        unit_tests.test__acp_rule(fmc=fmc1)
        unit_tests.test__port_object_group(fmc=fmc1)
        unit_tests.test__url_category(fmc=fmc1)
        unit_tests.test__ports(fmc=fmc1)
        unit_tests.test__autonat(fmc=fmc1)
        unit_tests.test__manualnat(fmc=fmc1)
        unit_tests.test__backup(fmc=fmc1) # Delete needs existing backup and may need an increased fmc timeout for large backups
        """

        """
        # Need FTD device to test
        unit_tests.test__hitcounts(fmc=fmc1, device_name='hq-ftd')
        unit_tests.test__ftddevicehapairs(fmc=fmc1)
        unit_tests.test__failoverinterfacemacaddressconfigs(fmc=fmc1)
        unit_tests.test__monitoredinterfaces(fmc=fmc1)
        unit_tests.test__devicerecords(fmc=fmc1)
        unit_tests.test__staticroutes(fmc=fmc1)
        unit_tests.test__ipv4staticroutes(fmc=fmc1)
        unit_tests.test__ipv6staticroutes(fmc=fmc1)
        unit_tests.test__upgrades(fmc=fmc1)
        unit_tests.test__interface_group(fmc=fmc1)
        unit_tests.test__device_with_task(fmc=fmc1)
        unit_tests.test__phys_interfaces(fmc=fmc1)
        unit_tests.test__redundant_interfaces(fmc=fmc1)
        unit_tests.test__etherchannel_interfaces(fmc=fmc1)
        unit_tests.test__subinterfaces(fmc=fmc1)
        unit_tests.test__ftds2svpns(fms=fmc1)
        unit_tests.test__globalsearch(fms=fmc1)
        unit_tests.test__object(fms=fmc1)
        unit_tests.test__policy(fms=fmc1)
        """


if __name__ == "__main__":
    main()
