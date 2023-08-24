from .static import StaticRouteSerializer
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

    # Nested Serializers
    'NestedPrefixListSerializer',
    'NestedPrefixListEntrySerializer',
    'NestedRouteMapSerializer',
    'NestedRouteMapEntrySerializer',
    'NestedStaticRouteSerializer'

)
