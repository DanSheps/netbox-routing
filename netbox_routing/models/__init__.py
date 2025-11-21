from .static import StaticRoute
from .ospf import OSPFArea, OSPFInstance, OSPFInterface
from .objects import RoutingPrefixList, PrefixListEntry, RouteMap, RouteMapEntry
from .bgp import BGPRouter, BGPScope, BGPAddressFamily, BGPSetting
from .eigrp import *

__all__ = (
    'StaticRoute',
    'OSPFArea',
    'OSPFInstance',
    'OSPFInterface',
    'EIGRPRouter',
    'EIGRPAddressFamily',
    'EIGRPNetwork',
    'EIGRPInterface',
    'RoutingPrefixList',
    'PrefixListEntry',
    'RouteMap',
    'RouteMapEntry',
    # Not fully implemented
    'BGPRouter',
    'BGPScope',
    'BGPAddressFamily',
    'BGPSetting',
)
