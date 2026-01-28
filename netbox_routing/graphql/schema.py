from typing import List

import strawberry
import strawberry_django

from .types import *


@strawberry.type(name="Query")
class StaticRouteQuery:
    static_route: StaticRouteType = strawberry_django.field()
    static_route_list: List[StaticRouteType] = strawberry_django.field()


@strawberry.type(name="Query")
class OSPFQuery:
    ospf_instance: OSPFInstanceType = strawberry_django.field()
    ospf_instance_list: List[OSPFInstanceType] = strawberry_django.field()

    ospf_area: OSPFAreaType = strawberry_django.field()
    ospf_area_list: List[OSPFAreaType] = strawberry_django.field()

    ospf_interface: OSPFInterfaceType = strawberry_django.field()
    ospf_interface_list: List[OSPFInterfaceType] = strawberry_django.field()


@strawberry.type(name="Query")
class EIGRPQuery:
    eigrp_router: EIGRPRouterType = strawberry_django.field()
    eigrp_router_list: List[EIGRPRouterType] = strawberry_django.field()

    eigrp_address_family: EIGRPAddressFamilyType = strawberry_django.field()
    eigrp_address_family_list: List[EIGRPAddressFamilyType] = strawberry_django.field()

    eigrp_network: EIGRPNetworkType = strawberry_django.field()
    eigrp_network_list: List[EIGRPNetworkType] = strawberry_django.field()

    eigrp_interface: EIGRPInterfaceType = strawberry_django.field()
    eigrp_interface_list: List[EIGRPInterfaceType] = strawberry_django.field()


@strawberry.type(name="Query")
class CommunityQuery:
    community: CommunityType = strawberry_django.field()
    community_list: List[CommunityType] = strawberry_django.field()


@strawberry.type(name="Query")
class CommunityListQuery:
    communitylist: CommunityListType = strawberry_django.field()
    communitylist_list: List[CommunityListType] = strawberry_django.field()


@strawberry.type(name="Query")
class CommunityListEntryQuery:
    communitylistentry: CommunityListEntryType = strawberry_django.field()
    communitylistentry_list: List[CommunityListEntryType] = strawberry_django.field()


@strawberry.type(name="Query")
class ASPathQuery:
    aspath: ASPathType = strawberry_django.field()
    aspath_list: List[ASPathType] = strawberry_django.field()


@strawberry.type(name="Query")
class ASPathEntryQuery:
    aspath_entry: ASPathEntryType = strawberry_django.field()
    aspath_entry_list: List[ASPathEntryType] = strawberry_django.field()


@strawberry.type(name="Query")
class PrefixListQuery:
    prefixlist: PrefixListType = strawberry_django.field()
    prefixlist_list: List[PrefixListType] = strawberry_django.field()


@strawberry.type(name="Query")
class PrefixListEntryQuery:
    prefixlist_entry: PrefixListEntryType = strawberry_django.field()
    prefixlist_entry_list: List[PrefixListEntryType] = strawberry_django.field()


@strawberry.type(name="Query")
class RouteMapQuery:
    route_map: RouteMapType = strawberry_django.field()
    route_map_list: List[RouteMapType] = strawberry_django.field()


@strawberry.type(name="Query")
class RouteMapEntryQuery:
    route_map_entry: RouteMapEntryType = strawberry_django.field()
    route_map_entry_list: List[RouteMapEntryType] = strawberry_django.field()


@strawberry.type(name="Query")
class BGPPeerTemplateQuery:
    bgp_peer_template: BGPPeerTemplateType = strawberry_django.field()
    bgp_peer_template_list: List[BGPPeerTemplateType] = strawberry_django.field()


@strawberry.type(name="Query")
class BGPPolicyTemplateQuery:
    bgp_policy_template: BGPPolicyTemplateType = strawberry_django.field()
    bgp_policy_template_list: List[BGPPolicyTemplateType] = strawberry_django.field()


@strawberry.type(name="Query")
class BGPSessionTemplateQuery:
    bgp_session_template: BGPSessionTemplateType = strawberry_django.field()
    bgp_session_template_list: List[BGPSessionTemplateType] = strawberry_django.field()


@strawberry.type(name="Query")
class BGPRouterQuery:
    bgp_router: BGPRouterType = strawberry_django.field()
    bgp_router_list: List[BGPRouterType] = strawberry_django.field()


@strawberry.type(name="Query")
class BGPScopeQuery:
    bgp_scope: BGPScopeType = strawberry_django.field()
    bgp_scope_list: List[BGPScopeType] = strawberry_django.field()


@strawberry.type(name="Query")
class BGPAddressFamilyQuery:
    bgp_address_family: BGPAddressFamilyType = strawberry_django.field()
    bgp_address_family_list: List[BGPAddressFamilyType] = strawberry_django.field()


@strawberry.type(name="Query")
class BGPPeerQuery:
    bgp_peer: BGPPeerType = strawberry_django.field()
    bgp_peer_list: List[BGPPeerType] = strawberry_django.field()


@strawberry.type(name="Query")
class BGPPeerAddressFamilyQuery:
    bgp_peer_address_family: BGPPeerAddressFamilyType = strawberry_django.field()
    bgp_peer_address_family_list: List[BGPPeerAddressFamilyType] = (
        strawberry_django.field()
    )


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
]
