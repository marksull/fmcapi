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

from .accesscontrolpolicy import AccessControlPolicy
from .acprule import ACPRule
from .anyprotocolportobjects import AnyProtocolPortObjects
from .applicabledevices import ApplicableDevices
from .application import Application
from .applicationcategory import ApplicationCategory
from .applicationfilter import ApplicationFilter
from .applicationproductivity import ApplicationProductivity
from .applicationrisk import ApplicationRisk
from .applicationtag import ApplicationTag
from .applicationtype import ApplicationType
from .autonatrules import AutoNatRules
from .bulk import Bulk
from .certenrollment import CertEnrollment
from .continent import Continent
from .country import Country
from .dnsservergroups import DNSServerGroups
from .endpointdevicetypes import EndPointDeviceTypes
from .extendedaccesslist import ExtendedAccessList
from .filepolicies import FilePolicies
from .fqdns import FQDNS
from .ftdnatpolicy import FTDNatPolicy
from .geolocation import Geolocation
from .icmpv4object import ICMPv4Object
from .icmpv6object import ICMPv6Object
from .ikev1ipsecproposals import IKEv1IpsecProposals
from .ikev1policies import IKEv1Policies
from .ikev2ipsecproposals import IKEv2IpsecProposals
from .ikev2policies import IKEv2Policies
from .interfacegroup import InterfaceGroup
from .interfaceobject import InterfaceObject
from .intrusionpolicy import IntrusionPolicy
from .ipaddresses import IPAddresses
from .iphost import IPHost
from .ipnetwork import IPNetwork
from .iprange import IPRange
from .isesecuritygrouptags import ISESecurityGroupTags
from .manualnatrules import ManualNatRules
from .natrules import NatRules
from .networkgroup import NetworkGroup
from .policyassignments import PolicyAssignments
from .portobjectgroup import PortObjectGroup
from .ports import Ports
from .protocolport import ProtocolPort
from .realms import Realms
from .realmusergroups import RealmUserGroups
from .realmusers import RealmUsers
from .securitygrouptags import SecurityGroupTags
from .securityzone import SecurityZone
from .siurlfeeds import SIUrlFeeds
from .siurllists import SIUrlLists
from .slamonitor import SLAMonitor
from .taskstatuses import TaskStatuses
from .tunneltags import TunnelTags
from .upgradepackage import UpgradePackage
from .upgrades import Upgrades
from .url import URL
from .urlcategory import URLCategory
from .urlgroup import URLGroup
from .variableset import VariableSet
from .vlantag import VlanTag
from .vlangrouptag import VlanGroupTag
from .hitcounts import HitCount
from .prefilterpolicies import PreFilterPolicy

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

    'AccessControlPolicy',
    'PreFilterPolicy',
    'HitCount',
    'ACPRule',
    'AnyProtocolPortObjects',
    'ApplicableDevices',
    'ApplicationCategory',
    'ApplicationFilter',
    'ApplicationProductivity',
    'Application',
    'ApplicationRisk',
    'ApplicationTag',
    'ApplicationType',
    'AutoNatRules',
    'Bulk',
    'CertEnrollment',
    'Continent',
    'Country',
    'DNSServerGroups',
    'EndPointDeviceTypes',
    'ExtendedAccessList',
    'FilePolicies',
    'FQDNS',
    'FTDNatPolicy',
    'Geolocation',
    'ICMPv4Object',
    'ICMPv6Object',
    'IKEv1IpsecProposals',
    'IKEv1Policies',
    'IKEv2IpsecProposals',
    'IKEv2Policies',
    'InterfaceObject',
    'InterfaceGroup',
    'IntrusionPolicy',
    'IPAddresses',
    'IPHost',
    'IPNetwork',
    'IPRange',
    'ISESecurityGroupTags',
    'ManualNatRules',
    'NetworkGroup',
    'NatRules',
    'PortObjectGroup',
    'ProtocolPort',
    'PolicyAssignments',
    'Ports',
    'Realms',
    'RealmUserGroups',
    'RealmUsers',
    'SecurityGroupTags',
    'SecurityZone',
    'SLAMonitor',
    'SIUrlFeeds',
    'SIUrlLists',
    'TaskStatuses',
    'TunnelTags',
    'UpgradePackage',
    'Upgrades',
    'URLCategory',
    'URLGroup',
    'URL',
    'VlanTag',
    'VariableSet',
    'VlanGroupTag',
]
