from .static import NestedStaticRouteSerializer
from .bgp import NestedBGPRouterSerializer, NestedBGPScopeSerializer, NestedBGPAddressFamilySerializer, \
    NestedBGPSettingSerializer
from .objects import NestedPrefixListSerializer, NestedPrefixListEntrySerializer, NestedRouteMapSerializer,\
    NestedRouteMapEntrySerializer

__all__ = (
    'NestedStaticRouteSerializer',

    'NestedBGPRouterSerializer',
    'NestedBGPScopeSerializer',
    'NestedBGPAddressFamilySerializer',
    'NestedBGPSettingSerializer',

    'NestedPrefixListSerializer',
    'NestedPrefixListEntrySerializer',
    'NestedRouteMapSerializer',
    'NestedRouteMapEntrySerializer',
)
