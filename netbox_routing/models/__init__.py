from .static import StaticRoute
from .ospf import OSPFArea, OSPFInstance, OSPFInterface
from .objects import PrefixList, PrefixListEntry, RouteMap, RouteMapEntry
from .bgp import *
from .eigrp import *
from .communities import *

__all__ = (
    'StaticRoute',

    'OSPFArea',
    'OSPFInstance',
    'OSPFInterface',

    'EIGRPRouter',
    'EIGRPAddressFamily',
    'EIGRPNetwork',
    'EIGRPInterface',

    'PrefixList',
    'PrefixListEntry',
    'RouteMap',
    'RouteMapEntry',

    # Not fully implemented
    'BGPRouter',
    'BGPScope',
    'BGPAddressFamily',
    'BGPSessionTemplate',
    'BGPPolicyTemplate',
    'BGPPeerTemplate',
    'BGPPeer',
    'BGPPeerAddressFamily',
    'BGPSetting',

    'CommunityList',
    'Community',
)
