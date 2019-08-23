"""
Unit testing, of a sort, all the created methods/classes.
"""

from fmcapi.fmc import *
from fmcapi.api_objects import *
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
    with FMC(host=host, username=username, password=password, autodeploy=autodeploy) as hq_fmc:
        # Create Security Zones
        sz_inside = SecurityZone(fmc=hq_fmc, name='inside', interfaceMode='ROUTED')
        sz_inside.post()
        sz_outside = SecurityZone(fmc=hq_fmc, name='outside', interfaceMode='ROUTED')
        sz_outside.post()
        sz_dmz = SecurityZone(fmc=hq_fmc, name='dmz', interfaceMode='ROUTED')
        sz_dmz.post()

        # Create Network Objects for HQ uses
        hq_dfgw_gateway = IPHost(fmc=hq_fmc, name='hq-default-gateway', value='100.64.0.1')
        hq_dfgw_gateway.post()
        hq_dfgw_gateway.get()
        hq_lan = IPNetwork(fmc=hq_fmc, name='hq-lan', value='10.0.0.0/24')
        hq_lan.post()
        all_lans = IPNetwork(fmc=hq_fmc, name='all-lans', value='10.0.0.0/8')
        all_lans.post()

        # Create an ACP for HQ device.
        acp = AccessControlPolicy(fmc=hq_fmc, name='HQ')
        acp.post()

        # Create ACP Rule for HQ ACP to permit hq_lan traffic.
        hq_acprule = ACPRule(fmc=hq_fmc,
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
        nat = FTDNatPolicy(fmc=hq_fmc, name='NAT Policy')
        nat.post()

        # Build NAT Rule
        '''
        autonat = AutoNatRules(fmc=hq_fmc,
                               natType="DYNAMIC",
                               interfaceInTranslatedNetwork=True,
                               )
        autonat.original_network(name=all_lans.name)
        autonat.source_intf(name=sz_inside.name)
        autonat.destination_intf(name=sz_outside.name)
        autonat.nat_policy(name=nat.name)
        autonat.post()
        '''

        # Add hq-ftd device to FMC
        hq_ftd = Device(fmc=hq_fmc)
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
        time.sleep(300)
        # The Device Class disables the fmc.autodeploy.  We are waiting for the registration, we can re-enable.
        hq_fmc.autodeploy = True

        # Once registration is complete configure the interfaces of hq-ftd.
        hq_ftd_g00 = PhysicalInterface(fmc=hq_fmc, device_name=hq_ftd.name)
        hq_ftd_g00.get(name="GigabitEthernet0/0")
        hq_ftd_g00.enabled = True
        hq_ftd_g00.ifname = "IN"
        hq_ftd_g00.static(ipv4addr="10.0.0.1", ipv4mask=24)
        hq_ftd_g00.sz(name="inside")
        hq_ftd_g00.put()

        hq_ftd_g01 = PhysicalInterface(fmc=hq_fmc, device_name=hq_ftd.name)
        hq_ftd_g01.get(name="GigabitEthernet0/1")
        hq_ftd_g01.enabled = True
        hq_ftd_g01.ifname = "OUT"
        hq_ftd_g01.static(ipv4addr="100.64.0.200", ipv4mask=24)
        hq_ftd_g01.sz(name="outside")
        hq_ftd_g01.put()

        # Build static default route.
        hq_default_route = IPv4StaticRoute(fmc=hq_fmc, name='hq_default_route')
        hq_default_route.device(device_name=hq_ftd.name)
        hq_default_route.networks(action='add', networks=['any-ipv4'])
        hq_default_route.gw(name=hq_dfgw_gateway.name)
        hq_default_route.interfaceName = hq_ftd_g01.ifname
        hq_default_route.metricValue = 1
        hq_default_route.post()


if __name__ == "__main__":
    main()
