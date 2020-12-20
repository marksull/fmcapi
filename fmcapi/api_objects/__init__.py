"""Update Packages Classes."""

import logging
from .policy_services.accesspolicies import AccessPolicies  # Needs loaded before Device
from .device_services.devicerecords import DeviceRecords  # Needs loaded early.

from .audit_services.audit_records import AuditRecords

from .deployment_services import DeployableDevices
from .deployment_services import DeploymentRequests

from .device_ha_pair_services import FTDDeviceHAPairs

from .device_group_services import DeviceGroupRecords

from .device_clusters import FTDDeviceCluster

from .device_ha_pair_services.failoverinterfacemacaddressconfigs import (
    FailoverInterfaceMACAddressConfigs,
)
from .device_ha_pair_services.monitoredinterfaces import MonitoredInterfaces

from .device_services.bridgegroupinterfaces import BridgeGroupInterfaces
from .device_services.etherchannelinterfaces import EtherchannelInterfaces
from .device_services.ipv4staticroutes import IPv4StaticRoutes
from .device_services.ipv6staticroutes import IPv6StaticRoutes
from .device_services.physicalinterfaces import PhysicalInterfaces
from .device_services.redundantinterfaces import RedundantInterfaces
from .device_services.staticroutes import StaticRoutes
from .device_services.subinterfaces import SubInterfaces

from .object_services.anyprotocolportobjects import AnyProtocolPortObjects
from .object_services.applications import Applications
from .object_services.applicationcategories import ApplicationCategories
from .object_services.applicationfilters import ApplicationFilters
from .object_services.applicationproductivities import ApplicationProductivities
from .object_services.applicationrisks import ApplicationRisks
from .object_services.applicationtags import ApplicationTags
from .object_services.applicationtypes import ApplicationTypes
from .object_services.certenrollments import CertEnrollments
from .object_services.continents import Continents
from .object_services.countries import Countries
from .object_services.dnsservergroups import DNSServerGroups
from .object_services.endpointdevicetypes import EndPointDeviceTypes
from .object_services.extendedaccesslist import ExtendedAccessList
from .object_services.fqdns import FQDNS
from .object_services.geolocation import Geolocation
from .object_services.icmpv4objects import ICMPv4Objects
from .object_services.icmpv6objects import ICMPv6Objects
from .object_services.ikev1ipsecproposals import IKEv1IpsecProposals
from .object_services.ikev1policies import IKEv1Policies
from .object_services.ikev2ipsecproposals import IKEv2IpsecProposals
from .object_services.ikev2policies import IKEv2Policies
from .object_services.interfacegroups import InterfaceGroups
from .object_services.interfaceobjects import InterfaceObjects
from .object_services.networkaddresses import NetworkAddresses
from .object_services.hosts import Hosts
from .object_services.networks import Networks
from .object_services.ranges import Ranges
from .object_services.isesecuritygrouptags import ISESecurityGroupTags
from .object_services.networkgroups import NetworkGroups
from .object_services.portobjectgroups import PortObjectGroups
from .object_services.ports import Ports
from .object_services.protocolportobjects import ProtocolPortObjects
from .object_services.realms import Realms
from .object_services.realmusergroups import RealmUserGroups
from .object_services.realmusers import RealmUsers
from .object_services.securitygrouptags import SecurityGroupTags
from .object_services.securityzones import SecurityZones
from .object_services.siurlfeeds import SIUrlFeeds
from .object_services.siurllists import SIUrlLists
from .object_services.slamonitors import SLAMonitors
from .object_services.tunneltags import TunnelTags
from .object_services.urls import URLs
from .object_services.urlcategories import URLCategories
from .object_services.urlgroups import URLGroups
from .object_services.variablesets import VariableSets
from .object_services.vlangrouptags import VlanGroupTags
from .object_services.vlantags import VlanTags

from .policy_services.accessrules import AccessRules
from .policy_services.accessrules import Bulk
from .policy_services.autonatrules import AutoNatRules
from .policy_services.advancedsettings import AdvancedSettings
from .policy_services.defaultactions import DefaultActions
from .policy_services.endpoints import Endpoints
from .policy_services.filepolicies import FilePolicies
from .policy_services.ftdnatpolicies import FTDNatPolicies
from .policy_services.ftds2svpns import FTDS2SVPNs
from .policy_services.hitcounts import HitCounts
from .policy_services.ikesettings import IKESettings
from .policy_services.intrusionpolicies import IntrusionPolicies
from .policy_services.ipsecsettings import IPSecSettings
from .policy_services.manualnatrules import ManualNatRules
from .policy_services.natrules import NatRules
from .policy_services.prefilterpolicies import PreFilterPolicies
from .policy_services.prefilterrules import PreFilterRules

from .policy_assignment_services.policyassignments import PolicyAssignments

from .status_services.taskstatuses import TaskStatuses

from .system_information import ServerVersion

from .update_packages.listapplicabledevices import ListApplicableDevices
from .update_packages.upgradepackages import UpgradePackages
from .update_packages.upgradepackage import Upgrades

from .policy_services.loggingsettings import LoggingSettings

logging.debug("In the api_objects __init__.py file.")

__all__ = [
    "AdvancedSettings",
    "IPSecSettings",
    "Endpoints",
    "FTDS2SVPNs",
    "IKESettings",
    "DeploymentRequests",
    "DeployableDevices",
    "ServerVersion",
    "AuditRecords",
    "DefaultActions",
    "DeviceGroupRecords",
    "FTDDeviceCluster",
    "FTDDeviceHAPairs",
    "FailoverInterfaceMACAddressConfigs",
    "MonitoredInterfaces",
    "DeviceRecords",
    "StaticRoutes",
    "IPv4StaticRoutes",
    "IPv6StaticRoutes",
    "PhysicalInterfaces",
    "BridgeGroupInterfaces",
    "RedundantInterfaces",
    "EtherchannelInterfaces",
    "SubInterfaces",
    "AnyProtocolPortObjects",
    "ApplicationCategories",
    "ApplicationFilters",
    "ApplicationProductivities",
    "ApplicationRisks",
    "Applications",
    "ApplicationTags",
    "ApplicationTypes",
    "CertEnrollments",
    "Continents",
    "Countries",
    "DNSServerGroups",
    "EndPointDeviceTypes",
    "ExtendedAccessList",
    "FQDNS",
    "Geolocation",
    "Hosts",
    "ICMPv4Objects",
    "ICMPv6Objects",
    "IKEv1IpsecProposals",
    "IKEv1Policies",
    "IKEv2IpsecProposals",
    "IKEv2Policies",
    "InterfaceGroups",
    "InterfaceObjects",
    "ISESecurityGroupTags",
    "NetworkAddresses",
    "NetworkGroups",
    "Networks",
    "PortObjectGroups",
    "Ports",
    "ProtocolPortObjects",
    "Ranges",
    "Realms",
    "RealmUserGroups",
    "RealmUsers",
    "SecurityGroupTags",
    "SecurityZones",
    "SIUrlFeeds",
    "SIUrlLists",
    "SLAMonitors",
    "TunnelTags",
    "URLCategories",
    "URLGroups",
    "URLs",
    "VariableSets",
    "VlanGroupTags",
    "VlanTags",
    "PolicyAssignments",
    "AccessPolicies",
    "AccessRules",
    "Bulk",
    "FilePolicies",
    "FTDNatPolicies",
    "AutoNatRules",
    "ManualNatRules",
    "NatRules",
    "IntrusionPolicies",
    "PreFilterPolicies",
    "PreFilterRules",
    "HitCounts",
    "TaskStatuses",
    "ListApplicableDevices",
    "UpgradePackages",
    "Upgrades",
    "LoggingSettings",
]
