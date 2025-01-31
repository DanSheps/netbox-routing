from .static import StaticRouteFilterSet
from .communities import *
from .objects import PrefixListFilterSet, PrefixListEntryFilterSet, RouteMapFilterSet, RouteMapEntryFilterSet
from .ospf import *
from .bgp import *
from .eigrp import *


__all__ = (
    'StaticRouteFilterSet',

    'BGPSettingFilterSet',
    'BGPRouterFilterSet',
    'BGPScopeFilterSet',
    'BGPSessionTemplateFilterSet',
    'BGPPolicyTemplateFilterSet',
    'BGPPeerTemplateFilterSet',
    'BGPAddressFamilyFilterSet',
    'BGPPeerFilterSet',
    'BGPPeerAddressFamilyFilterSet',

    'OSPFInstanceFilterSet',
    'OSPFAreaFilterSet',
    'OSPFInterfaceFilterSet',

    'EIGRPRouterFilterSet',
    'EIGRPAddressFamilyFilterSet',
    'EIGRPNetworkFilterSet',
    'EIGRPInterfaceFilterSet',

    'PrefixListFilterSet',
    'PrefixListEntryFilterSet',
    'RouteMapFilterSet',
    'RouteMapEntryFilterSet',

    'CommunityListFilterSet',
    'CommunityFilterSet',
)
