from netbox_routing.api._serializers.objects import *
from netbox_routing.api._serializers.community import *
from netbox_routing.api._serializers.static import StaticRouteSerializer
from netbox_routing.api._serializers.bgp import *
from netbox_routing.api._serializers.ospf import *
from netbox_routing.api._serializers.eigrp import *

__all__ = (
    'CommunitySerializer',
    'CommunityListSerializer',
    'CommunityListEntrySerializer',
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
    'BGPSettingSerializer',
    'BGPRouterSerializer',
    'BGPScopeSerializer',
    'BGPAddressFamilySerializer',
    'BGPPeerSerializer',
)
