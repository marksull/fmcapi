import logging
from .url_category import test__url_category
from .ports import test__ports
from .upgrades import test__upgrades
from .manualnat import test__manualnat
from .autonat import test__autonat
from .port_object_group import test__port_object_group
from .audit import test__audit
from .acprule import test__acp_rule
from .acp import test__access_control_policy
from .intrusion_policy import test__intrusion_policy
from .device_ha_failover_mac import test__device_ha_failover_mac
from .device_ha_monitored_interface import test__device_ha_monitored_interfaces
from .device_ha_pair import test__device_ha_pair
from .device_group import test__device_group
from .static_routes_ipv4 import test__ipv4_static_routes
from .static_routes import test__static_routes
from .interfaces_subinterfaces import test__subinterfaces
from .interfaces_etherchannel import test__etherchannel_interfaces
from .interfaces_redundant import test__redundant_interfaces
from .interfaces_bridge_group import test__bridge_group_interfaces
from .interfaces_physical import test__phys_interfaces
from .wait_for_task import wait_for_task
from .device_with_task import test__device_with_task
from .device import test__device
from .sla_monitor import test__slamonitor
from .interface_group import test__interface_group
from .security_zone import test__security_zone
from .protocol_port import test__protocol_port

logging.debug("In the unit-tests __init__.py file.")

__all__ = ['test__url_category',
           'test__protocol_port',
           'test__security_zone',
           'test__interface_group',
           'test__slamonitor',
           'test__device',
           'test__device_with_task',
           'wait_for_task',
           'test__phys_interfaces',
           'test__bridge_group_interfaces',
           'test__redundant_interfaces',
           'test__etherchannel_interfaces',
           'test__subinterfaces',
           'test__static_routes',
           'test__ipv4_static_routes',
           'test__device_group',
           'test__device_ha_pair',
           'test__device_ha_monitored_interfaces',
           'test__ports',
           'test__upgrades',
           'test__manualnat',
           'test__autonat',
           'test__port_object_group',
           'test__audit',
           'test__acp_rule',
           'test__access_control_policy',
           'test__intrusion_policy',
           'test__device_ha_failover_mac',
           ]
