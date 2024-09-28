from netbox_routing.api._serializers.objects import (
    PrefixListSerializer, PrefixListEntrySerializer, RouteMapSerializer, RouteMapEntrySerializer
)
from netbox_routing.api._serializers.static import StaticRouteSerializer
from netbox_routing.api._serializers.bgp import (
    BGPRouterSerializer, BGPScopeSerializer, BGPAddressFamilySerializer, BGPSettingSerializer
)
from netbox_routing.api._serializers.ospf import *
from netbox_routing.api._serializers.eigrp import *

__all__ = (
    'StaticRouteSerializer',

    'OSPFInstanceSerializer',
    'OSPFAreaSerializer',
    'OSPFInterfaceSerializer',

    'EIGRPRouterSerializer',
    'EIGRPAddressFamilySerializer',
    'EIGRPNetworkSerializer',
    'EIGRPInterfaceSerializer',

    'PrefixListSerializer',
    'PrefixListEntrySerializer',
    'RouteMapSerializer',
    'RouteMapEntrySerializer',

    'BGPRouterSerializer',
    'BGPScopeSerializer',
    'BGPAddressFamilySerializer',
    'BGPSettingSerializer',
)