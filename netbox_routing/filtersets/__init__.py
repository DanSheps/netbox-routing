from .static import StaticRouteFilterSet
from .objects import PrefixListFilterSet, PrefixListEntryFilterSet, RouteMapFilterSet, RouteMapEntryFilterSet
from .ospf import *
from .bgp import *
from .eigrp import *


__all__ = (
    'StaticRouteFilterSet',

    'BGPSettingFilterSet',
    'BGPRouterFilterSet',

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
)
