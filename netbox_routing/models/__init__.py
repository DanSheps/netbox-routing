from .bgp import *
from .communities import *
from .eigrp import *
from .objects import PrefixList, PrefixListEntry, RouteMap, RouteMapEntry
from .ospf import OSPFArea, OSPFInstance, OSPFInterface
from .static import StaticRoute

__all__ = (
    # BGP
    'BGPRouter',
    'BGPScope',
    'BGPAddressFamily',
    'BGPPeerTemplate',
    'BGPPolicyTemplate',
    'BGPSessionTemplate',
    'BGPSetting',
    'BGPPeer',
    'BGPPeerAddressFamily',
    # Communities
    'Community',
    'CommunityList',
    # EIGRP
    'EIGRPRouter',
    'EIGRPAddressFamily',
    'EIGRPNetwork',
    'EIGRPInterface',
    # OSPF
    'OSPFArea',
    'OSPFInstance',
    'OSPFInterface',
    # Objects -> Prefix Lists
    'PrefixList',
    'PrefixListEntry',
    # Objects -> Route Maps
    'RouteMap',
    'RouteMapEntry',
    # Static Routing
    'StaticRoute',
)
