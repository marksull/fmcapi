"""
Unit testing, of a sort, all the created methods/classes.
"""

import fmcapi
import time

# ### Set these variables to match your environment. ### #
host = '10.0.0.10'
username = 'apiadmin'
password = 'Admin123'
autodeploy = True

DEVICE_REGISTRATION_PSK = 'cisco123'


def main():
    """
    The hq-ftd device already has 10.0.0.254 on its manage interface and the command 'configure network manager
    10.0.0.10 cisco123' has already been manually typed on the FTD's CLI.
    """
    with fmcapi.FMC(host=host, username=username, password=password, autodeploy=autodeploy) as fmc1:
        # Create Security Zones
        sz_inside = fmcapi.SecurityZone(fmc=fmc1, name='inside', interfaceMode='ROUTED')
        sz_inside.post()
        sz_inside.get()
        sz_outside = fmcapi.SecurityZone(fmc=fmc1, name='outside', interfaceMode='ROUTED')
        sz_outside.post()
        sz_outside.get()
        sz_dmz = fmcapi.SecurityZone(fmc=fmc1, name='dmz', interfaceMode='ROUTED')
        sz_dmz.post()
        sz_dmz.get()

        # Create Network Objects for HQ uses
        hq_dfgw_gateway = fmcapi.IPHost(fmc=fmc1, name='hq-default-gateway', value='100.64.0.1')
        hq_dfgw_gateway.post()
        hq_dfgw_gateway.get()
        hq_lan = fmcapi.IPNetwork(fmc=fmc1, name='hq-lan', value='10.0.0.0/24')
        hq_lan.post()
        all_lans = fmcapi.IPNetwork(fmc=fmc1, name='all-lans', value='10.0.0.0/8')
        all_lans.post()

        # Create an ACP for HQ device.
        acp = fmcapi.AccessControlPolicy(fmc=fmc1, name='HQ')
        acp.post()

        # Create ACP Rule for HQ ACP to permit hq_lan traffic.
        hq_acprule = fmcapi.ACPRule(fmc=fmc1,
                                    acp_name=acp.name,
                                    name='Permit HQ LAN',
                                    action='ALLOW',
                                    enabled=True,
                                    )
        hq_acprule.source_zone(action='add', name=sz_inside.name)
        hq_acprule.destination_zone(action='add', name=sz_outside.name)
        hq_acprule.source_network(action='add', name=hq_lan.name)
        hq_acprule.destination_network(action='add', name='any-ipv4')
        hq_acprule.post()

        # Build NAT Policy
        nat = fmcapi.FTDNatPolicy(fmc=fmc1, name='NAT Policy')
        nat.post()

        # Build NAT Rule
        autonat = fmcapi.AutoNatRules(fmc=fmc1,
                               natType="DYNAMIC",
                               interfaceInTranslatedNetwork=True,
                               )
        autonat.original_network(all_lans.name)
        autonat.source_intf(name=sz_inside.name)
        autonat.destination_intf(name=sz_outside.name)
        autonat.nat_policy(name=nat.name)
        autonat.post()

        # Add hq-ftd device to FMC
        hq_ftd = fmcapi.Device(fmc=fmc1)
        # Minimum things set.
        hq_ftd.hostName = '10.0.0.254'
        hq_ftd.regKey = DEVICE_REGISTRATION_PSK
        hq_ftd.acp(name=acp.name)
        # Other stuff I want set.
        hq_ftd.name = 'hq-ftd'
        hq_ftd.licensing(action='add', name='MALWARE')
        hq_ftd.licensing(action='add', name='VPN')
        hq_ftd.licensing(action='add', name='BASE')
        # Push to FMC to start device registration.
        hq_ftd.post()
        # At the moment fmcapi doesn't have good support for waiting for the device registration process to complete.
        wait_time = 300
        print(f'Waiting {wait_time} seconds for device discovery.')
        time.sleep(wait_time)
        # The Device Class disables the fmc.autodeploy.  We are waiting for the registration, we can re-enable.
        # hq_fmc.autodeploy = True

        # Once registration is complete configure the interfaces of hq-ftd.
        hq_ftd_g00 = fmcapi.PhysicalInterface(fmc=fmc1, device_name=hq_ftd.name)
        hq_ftd_g00.get(name="GigabitEthernet0/0")
        hq_ftd_g00.enabled = True  # This doesn't work yet for some reason.
        hq_ftd_g00.ifname = "IN"
        hq_ftd_g00.static(ipv4addr="10.0.0.1", ipv4mask=24)
        hq_ftd_g00.sz(name="inside")
        hq_ftd_g00.put()

        hq_ftd_g01 = fmcapi.PhysicalInterface(fmc=fmc1, device_name=hq_ftd.name)
        hq_ftd_g01.get(name="GigabitEthernet0/1")
        hq_ftd_g01.enabled = True  # This doesn't work yet for some reason.
        hq_ftd_g01.ifname = "OUT"
        hq_ftd_g01.static(ipv4addr="100.64.0.200", ipv4mask=24)
        hq_ftd_g01.sz(name="outside")
        hq_ftd_g01.put()

        # Build static default route.
        hq_default_route = fmcapi.IPv4StaticRoute(fmc=fmc1, name='hq_default_route')
        hq_default_route.device(device_name=hq_ftd.name)
        hq_default_route.networks(action='add', networks=['any-ipv4'])
        hq_default_route.gw(name=hq_dfgw_gateway.name)
        hq_default_route.interfaceName = hq_ftd_g01.ifname
        hq_default_route.metricValue = 1
        hq_default_route.post()

        # Associate NAT policy with device.
        devices = [{'name': hq_ftd.name, 'type': 'device'}]
        assign_nat_policy = fmcapi.PolicyAssignments(fmc=fmc1)
        assign_nat_policy.ftd_natpolicy(name=nat.name, devices=devices)
        assign_nat_policy.post()


if __name__ == "__main__":
    main()
