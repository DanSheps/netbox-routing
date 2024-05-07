from .static import StaticRoute
from .ospf import OSPFArea, OSPFInstance, OSPFInterface
from .objects import PrefixList, PrefixListEntry, RouteMap, RouteMapEntry
from .bgp import BGPRouter, BGPScope, BGPAddressFamily, BGPSetting

__all__ = (
    'StaticRoute',
    'OSPFArea',
    'OSPFInstance',
    'OSPFInterface',
    'PrefixList',
    'PrefixListEntry',
    'RouteMap',
    'RouteMapEntry',
    'BGPRouter',
    'BGPScope',
    'BGPAddressFamily',
    'BGPSetting'
)
