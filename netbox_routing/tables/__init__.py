from .bgp import *
from .eigrp import *
from .objects import *
from .static import *
from .ospf import *

__all__ = (

    'BGPRouterTable',
    'BGPScopeTable',
    'BGPSessionTemplateTable',
    'BGPPolicyTemplateTable',
    'BGPPeerTemplateTable',
    'BGPAddressFamilyTable',
    'BGPPeerTable',
    'BGPPeerAddressFamilyTable',
    'BGPSettingTable',

    'EIGRPAddressFamilyTable',
    'EIGRPRouterTable',
    'EIGRPNetworkTable',
    'EIGRPInterfaceTable',

    'OSPFAreaTable',
    'OSPFInstanceTable',
    'OSPFInterfaceTable',

    'PrefixListTable',
    'PrefixListEntryTable',
    'RouteMapTable',
    'RouteMapEntryTable',

    'StaticRouteTable',
)
