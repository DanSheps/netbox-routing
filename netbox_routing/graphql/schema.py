import strawberry
import strawberry_django

from .bgp.types import (
    BGPPeerTemplateType,
    BGPPolicyTemplateType,
    BGPSessionTemplateType,
    BGPRouterType,
    BGPScopeType,
    BGPAddressFamilyType,
    BGPPeerType,
    BGPPeerAddressFamilyType,
    BFDProfileType,
)
from .community.types import CommunityType, CommunityListType, CommunityListEntryType
from .eigrp.types import (
    EIGRPRouterType,
    EIGRPAddressFamilyType,
    EIGRPNetworkType,
    EIGRPInterfaceType,
)
from .objects.types import (
    ASPathType,
    ASPathEntryType,
    PrefixListType,
    PrefixListEntryType,
    RouteMapType,
    RouteMapEntryType,
)
from .ospf.types import OSPFInstanceType, OSPFAreaType, OSPFInterfaceType
from .static.types import StaticRouteType


@strawberry.type(name="Query")
class StaticRouteQuery:
    static_route: StaticRouteType = strawberry_django.field()
    static_route_list: list[StaticRouteType] = strawberry_django.field()


@strawberry.type(name="Query")
class OSPFQuery:
    ospf_instance: OSPFInstanceType = strawberry_django.field()
    ospf_instance_list: list[OSPFInstanceType] = strawberry_django.field()

    ospf_area: OSPFAreaType = strawberry_django.field()
    ospf_area_list: list[OSPFAreaType] = strawberry_django.field()

    ospf_interface: OSPFInterfaceType = strawberry_django.field()
    ospf_interface_list: list[OSPFInterfaceType] = strawberry_django.field()


@strawberry.type(name="Query")
class EIGRPQuery:
    eigrp_router: EIGRPRouterType = strawberry_django.field()
    eigrp_router_list: list[EIGRPRouterType] = strawberry_django.field()

    eigrp_address_family: EIGRPAddressFamilyType = strawberry_django.field()
    eigrp_address_family_list: list[EIGRPAddressFamilyType] = strawberry_django.field()

    eigrp_network: EIGRPNetworkType = strawberry_django.field()
    eigrp_network_list: list[EIGRPNetworkType] = strawberry_django.field()

    eigrp_interface: EIGRPInterfaceType = strawberry_django.field()
    eigrp_interface_list: list[EIGRPInterfaceType] = strawberry_django.field()


@strawberry.type(name="Query")
class CommunityQuery:
    community: CommunityType = strawberry_django.field()
    community_list: list[CommunityType] = strawberry_django.field()


@strawberry.type(name="Query")
class CommunityListQuery:
    communitylist: CommunityListType = strawberry_django.field()
    communitylist_list: list[CommunityListType] = strawberry_django.field()


@strawberry.type(name="Query")
class CommunityListEntryQuery:
    communitylistentry: CommunityListEntryType = strawberry_django.field()
    communitylistentry_list: list[CommunityListEntryType] = strawberry_django.field()


@strawberry.type(name="Query")
class ASPathQuery:
    aspath: ASPathType = strawberry_django.field()
    aspath_list: list[ASPathType] = strawberry_django.field()


@strawberry.type(name="Query")
class ASPathEntryQuery:
    aspath_entry: ASPathEntryType = strawberry_django.field()
    aspath_entry_list: list[ASPathEntryType] = strawberry_django.field()


@strawberry.type(name="Query")
class PrefixListQuery:
    prefixlist: PrefixListType = strawberry_django.field()
    prefixlist_list: list[PrefixListType] = strawberry_django.field()


@strawberry.type(name="Query")
class PrefixListEntryQuery:
    prefixlist_entry: PrefixListEntryType = strawberry_django.field()
    prefixlist_entry_list: list[PrefixListEntryType] = strawberry_django.field()


@strawberry.type(name="Query")
class RouteMapQuery:
    route_map: RouteMapType = strawberry_django.field()
    route_map_list: list[RouteMapType] = strawberry_django.field()


@strawberry.type(name="Query")
class RouteMapEntryQuery:
    route_map_entry: RouteMapEntryType = strawberry_django.field()
    route_map_entry_list: list[RouteMapEntryType] = strawberry_django.field()


@strawberry.type(name="Query")
class BGPPeerTemplateQuery:
    bgp_peer_template: BGPPeerTemplateType = strawberry_django.field()
    bgp_peer_template_list: list[BGPPeerTemplateType] = strawberry_django.field()


@strawberry.type(name="Query")
class BGPPolicyTemplateQuery:
    bgp_policy_template: BGPPolicyTemplateType = strawberry_django.field()
    bgp_policy_template_list: list[BGPPolicyTemplateType] = strawberry_django.field()


@strawberry.type(name="Query")
class BGPSessionTemplateQuery:
    bgp_session_template: BGPSessionTemplateType = strawberry_django.field()
    bgp_session_template_list: list[BGPSessionTemplateType] = strawberry_django.field()


@strawberry.type(name="Query")
class BGPRouterQuery:
    bgp_router: BGPRouterType = strawberry_django.field()
    bgp_router_list: list[BGPRouterType] = strawberry_django.field()


@strawberry.type(name="Query")
class BGPScopeQuery:
    bgp_scope: BGPScopeType = strawberry_django.field()
    bgp_scope_list: list[BGPScopeType] = strawberry_django.field()


@strawberry.type(name="Query")
class BGPAddressFamilyQuery:
    bgp_address_family: BGPAddressFamilyType = strawberry_django.field()
    bgp_address_family_list: list[BGPAddressFamilyType] = strawberry_django.field()


@strawberry.type(name="Query")
class BGPPeerQuery:
    bgp_peer: BGPPeerType = strawberry_django.field()
    bgp_peer_list: list[BGPPeerType] = strawberry_django.field()


@strawberry.type(name="Query")
class BGPPeerAddressFamilyQuery:
    bgp_peer_address_family: BGPPeerAddressFamilyType = strawberry_django.field()
    bgp_peer_address_family_list: list[BGPPeerAddressFamilyType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class BFDProfileQuery:
    bfd_profile: BFDProfileType = strawberry_django.field()
    bfd_profile_list: list[BFDProfileType] = strawberry_django.field()


schema = [
    StaticRouteQuery,
    OSPFQuery,
    EIGRPQuery,
    CommunityQuery,
    CommunityListQuery,
    CommunityListEntryQuery,
    ASPathQuery,
    ASPathEntryQuery,
    PrefixListQuery,
    PrefixListEntryQuery,
    RouteMapQuery,
    RouteMapEntryQuery,
    BGPPeerTemplateQuery,
    BGPPolicyTemplateQuery,
    BGPSessionTemplateQuery,
    BGPRouterQuery,
    BGPScopeQuery,
    BGPAddressFamilyQuery,
    BGPPeerQuery,
    BGPPeerAddressFamilyQuery,
    BFDProfileQuery,
]
