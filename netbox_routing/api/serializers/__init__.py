from .static import StaticRouteSerializer
from .bgp import BGPRouterSerializer, BGPScopeSerializer, BGPAddressFamilySerializer, BGPSettingSerializer
from .ospf import *
from .objects import PrefixListSerializer, PrefixListEntrySerializer, RouteMapSerializer, RouteMapEntrySerializer
from ..nested_serializers import *

__all__ = (
    'StaticRouteSerializer',

    'OSPFInstanceSerializer',
    'OSPFAreaSerializer',
    'OSPFInterfaceSerializer',

    'PrefixListSerializer',
    'PrefixListEntrySerializer',
    'RouteMapSerializer',
    'RouteMapEntrySerializer',

    'BGPRouterSerializer',
    'BGPScopeSerializer',
    'BGPAddressFamilySerializer',
    'BGPSettingSerializer',

    # Nested Serializers
    'NestedStaticRouteSerializer',

    'NestedBGPRouterSerializer',
    'NestedBGPScopeSerializer',
    'NestedBGPAddressFamilySerializer',
    'NestedBGPSettingSerializer',

    # Nested Serializers
    'NestedPrefixListSerializer',
    'NestedPrefixListEntrySerializer',
    'NestedRouteMapSerializer',
    'NestedRouteMapEntrySerializer',
    'NestedStaticRouteSerializer'
)
