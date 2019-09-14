import logging
from .device_group_services import DeviceGroups

from .device_clusters import FTDDeviceCluster

from .device_ha_pair_services import FTDDeviceHAPairs
from .device_ha_pair_services.devicehapairs import DeviceHAPairs
from .device_ha_pair_services.failoverinterfacemacaddressconfigs import FailoverInterfaceMACAddressConfigs
from .device_ha_pair_services.devicehafailovermac import DeviceHAFailoverMAC
from .device_ha_pair_services.devicehamonitoredinterfaces import DeviceHAMonitoredInterfaces
from .device_ha_pair_services.monitoredinterfaces import MonitoredInterfaces

from .device_services.bridgegroupinterfaces import BridgeGroupInterfaces
from .device_services.etherchannelinterfaces import EtherchannelInterfaces
from .device_services.device import Device
from .device_services.ipv4staticroute import IPv4StaticRoute
from .device_services.ipv6staticroute import IPv6StaticRoute
from .device_services.physicalinterface import PhysicalInterface
from .device_services.redundantinterfaces import RedundantInterfaces
from .device_services.staticroutes import StaticRoutes
from .device_services.subinterfaces import SubInterfaces

from .object_services.anyprotocolportobjects import AnyProtocolPortObjects
from .object_services.application import Application
from .object_services.applicationcategory import ApplicationCategory
from .object_services.applicationfilter import ApplicationFilter
from .object_services.applicationproductivity import ApplicationProductivity
from .object_services.applicationrisk import ApplicationRisk
from .object_services.applicationtag import ApplicationTag
from .object_services.applicationtype import ApplicationType
from .object_services.certenrollment import CertEnrollment
from .object_services.continent import Continent
from .object_services.country import Country
from .object_services.dnsservergroups import DNSServerGroups
from .object_services.endpointdevicetypes import EndPointDeviceTypes
from .object_services.extendedaccesslist import ExtendedAccessList
from .object_services.fqdns import FQDNS
from .object_services.geolocation import Geolocation
from .object_services.icmpv4object import ICMPv4Object
from .object_services.icmpv6object import ICMPv6Object
from .object_services.ikev1ipsecproposals import IKEv1IpsecProposals
from .object_services.ikev1policies import IKEv1Policies
from .object_services.ikev2ipsecproposals import IKEv2IpsecProposals
from .object_services.ikev2policies import IKEv2Policies
from .object_services.interfacegroup import InterfaceGroup
from .object_services.interfaceobject import InterfaceObject
from .object_services.ipaddresses import IPAddresses
from .object_services.iphost import IPHost
from .object_services.ipnetwork import IPNetwork
from .object_services.iprange import IPRange
from .object_services.isesecuritygrouptags import ISESecurityGroupTags
from .object_services.networkgroup import NetworkGroup
from .object_services.portobjectgroup import PortObjectGroup
from .object_services.ports import Ports
from .object_services.protocolport import ProtocolPort
from .object_services.realms import Realms
from .object_services.realmusergroups import RealmUserGroups
from .object_services.realmusers import RealmUsers
from .object_services.securitygrouptags import SecurityGroupTags
from .object_services.securityzone import SecurityZone
from .object_services.siurlfeeds import SIUrlFeeds
from .object_services.siurllists import SIUrlLists
from .object_services.slamonitor import SLAMonitor
from .object_services.tunneltags import TunnelTags
from .object_services.url import URL
from .object_services.urlcategory import URLCategory
from .object_services.urlgroup import URLGroup
from .object_services.variableset import VariableSet
from .object_services.vlangrouptag import VlanGroupTag
from .object_services.vlantag import VlanTag

from .policy_services.accesscontrolpolicy import AccessControlPolicy
from .policy_services.acprule import ACPRule
from .policy_services.autonatrules import AutoNatRules
from .policy_services.bulk import Bulk
from .policy_services.filepolicies import FilePolicies
from .policy_services.ftdnatpolicy import FTDNatPolicy
from .policy_services.hitcounts import HitCount
from .policy_services.intrusionpolicy import IntrusionPolicy
from .policy_services.manualnatrules import ManualNatRules
from .policy_services.natrules import NatRules
from .policy_services.prefilterpolicies import PreFilterPolicy

from .policy_assignment_services.policyassignments import PolicyAssignments

from .status_services.taskstatuses import TaskStatuses

from .applicabledevices import ApplicableDevices
from .upgradepackage import UpgradePackage
from .upgrades import Upgrades

logging.debug("In the api_objects __init__.py file.")

__all__ = [
    'DeviceGroups',
    'FTDDeviceCluster',
    'FTDDeviceHAPairs',
    'DeviceHAPairs',
    'FailoverInterfaceMACAddressConfigs',
    'DeviceHAFailoverMAC',
    'MonitoredInterfaces',
    'DeviceHAMonitoredInterfaces',
    'BridgeGroupInterfaces',
    'Device',
    'EtherchannelInterfaces',
    'IPv4StaticRoute',
    'IPv6StaticRoute',
    'PhysicalInterface',
    'RedundantInterfaces',
    'StaticRoutes',
    'SubInterfaces',
    'AnyProtocolPortObjects',
    'Application',
    'ApplicationCategory',
    'ApplicationFilter',
    'ApplicationProductivity',
    'ApplicationRisk',
    'ApplicationTag',
    'ApplicationType',
    'CertEnrollment',
    'Continent',
    'Country',
    'DNSServerGroups',
    'EndPointDeviceTypes',
    'ExtendedAccessList',
    'FQDNS',
    'Geolocation',
    'ICMPv4Object',
    'ICMPv6Object',
    'IKEv1IpsecProposals',
    'IKEv1Policies',
    'IKEv2IpsecProposals',
    'IKEv2Policies',
    'InterfaceGroup',
    'InterfaceObject',
    'IPAddresses',
    'IPHost',
    'IPNetwork',
    'IPRange',
    'ISESecurityGroupTags',
    'NetworkGroup',
    'PortObjectGroup',
    'Ports',
    'ProtocolPort',
    'Realms',
    'RealmUserGroups',
    'RealmUsers',
    'SecurityGroupTags',
    'SecurityZone',
    'SIUrlFeeds',
    'SIUrlLists',
    'SLAMonitor',
    'TunnelTags',
    'URL',
    'URLCategory',
    'URLGroup',
    'VariableSet',
    'VlanGroupTag',
    'VlanTag',
    'AccessControlPolicy',
    'ACPRule',
    'AutoNatRules',
    'Bulk',
    'FilePolicies',
    'FTDNatPolicy',
    'HitCount',
    'IntrusionPolicy',
    'ManualNatRules',
    'NatRules',
    'PreFilterPolicy',
    'PolicyAssignments',
    'TaskStatuses',

    'ApplicableDevices',
    'UpgradePackage',
    'Upgrades',
]
