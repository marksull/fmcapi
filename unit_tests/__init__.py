import logging
from .hit_counts import test__hitcounts
from .url_category import test__url_category
from .ports import test__ports
from .upgrades import test__upgrades
from .manualnat import test__manualnat
from .autonat import test__autonat
from .port_object_group import test__port_object_group
from .acprule import test__acp_rule
from .acp import test__access_control_policy
from .intrusion_policy import test__intrusion_policy
from .interfaces_subinterfaces import test__subinterfaces
from .interfaces_etherchannel import test__etherchannel_interfaces
from .interfaces_redundant import test__redundant_interfaces
from .interfaces_bridge_group import test__bridge_group_interfaces
from .interfaces_physical import test__phys_interfaces
from .wait_for_task import wait_for_task
from .device_with_task import test__device_with_task
from .sla_monitor import test__slamonitor
from .interface_group import test__interface_group
from .security_zone import test__security_zone
from .protocol_port import test__protocol_port
from .vlan_tag import test__vlan_tag
from .url import test__url
from .ikev2 import test__ikev2
from .ikev1 import test__ikev1
from .icmpv6 import test__icmpv6
from .icmpv4 import test__icmpv4
from .geolocations import test__geolocations
from .acls_extended import test__extended_acls
from .ip_range import test__ip_range
from .ip_network import test__ip_network
from .ip_host import test__ip_host
from .variable_set import test__variable_set
from .server_version import test__fmc_version
from .ip_addresses import test__ip_addresses
from .network_group import test__network_group
from .url_group import test__url_group
from .vlan_group_tag import test__vlan_group_tag
from .dns_servers_group import test__dns_servers_group
from .continent import test__continent
from .file_policies import test__filepolicies
from .country import test__country
from .certificate_enrollment import test__cert_enrollment
from .application_category import test__application_category
from .application_productivity import test__application_productivity
from .application_filter import test__application_filter
from .application_risk import test__application_risk
from .application import test__application
from .application_tag import test__application_tag
from .application_type import test__application_type

from .audit_records import test__audit_records
from .deployable_devices import test__deployable_devices
from .deployment_requests import test__deployment_requests
from .devicegrouprecords import test__devicegrouprecords
from .ftddevicehapairs import test__ftddevicehapairs
from .failoverinterfacemacaddressconfigs import test__failoverinterfacemacaddressconfigs
from .monitored_interface import test__monitoredinterfaces
from .devicerecords import test__devicerecords
from .staticroutes import test__staticroutes
from .ipv4staticroutes import test__ipv4staticroutes
from .ipv6staticroutes import test__ipv6staticroutes
from .prefilter import test__prefilter_policy
from .prefilter_rule import test__prefiler_rule
from .s2s_vpn import test__ftds2svpns

logging.debug("In the unit-tests __init__.py file.")

__all__ = [
    "test__audit_records",
    "test__deployment_requests",
    "test__deployable_devices",
    "test__devicegrouprecords",
    "test__ftddevicehapairs",
    "test__failoverinterfacemacaddressconfigs",
    "test__monitoredinterfaces",
    "test__devicerecords",
    "test__staticroutes",
    "test__ipv4staticroutes",
    "test__ipv6staticroutes",
    "test__bridge_group_interfaces",
    "test__url_category",
    "test__application_type",
    "test__application_tag",
    "test__application",
    "test__application_risk",
    "test__application_filter",
    "test__application_productivity",
    "test__application_category",
    "test__cert_enrollment",
    "test__country",
    "test__filepolicies",
    "test__continent",
    "test__dns_servers_group",
    "test__vlan_group_tag",
    "test__url_group",
    "test__network_group",
    "test__ip_addresses",
    "test__fmc_version",
    "test__variable_set",
    "test__ip_host",
    "test__ip_network",
    "test__ip_range",
    "test__extended_acls",
    "test__geolocations",
    "test__icmpv6",
    "test__icmpv4",
    "test__ikev2",
    "test__ikev1",
    "test__vlan_tag",
    "test__url",
    "test__protocol_port",
    "test__security_zone",
    "test__interface_group",
    "test__slamonitor",
    "test__device_with_task",
    "wait_for_task",
    "test__phys_interfaces",
    "test__redundant_interfaces",
    "test__etherchannel_interfaces",
    "test__subinterfaces",
    "test__ports",
    "test__upgrades",
    "test__manualnat",
    "test__autonat",
    "test__port_object_group",
    "test__acp_rule",
    "test__access_control_policy",
    "test__intrusion_policy",
    "test__prefilter_policy",
]
