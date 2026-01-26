from typing import Annotated, List

import strawberry
import strawberry_django

from netbox.graphql.types import PrimaryObjectType
from .filters import *

from netbox_routing import models

__all__ = (
    'StaticRouteType',
    'OSPFInstanceType',
    'OSPFAreaType',
    'OSPFInterfaceType',
    'EIGRPRouterType',
    'EIGRPAddressFamilyType',
    'EIGRPNetworkType',
    'EIGRPInterfaceType',
    'CommunityType',
    'CommunityListType',
    'CommunityListEntryType',
    'ASPathType',
    'ASPathEntryType',
    'PrefixListType',
    'PrefixListEntryType',
    'RouteMapType',
    'RouteMapEntryType',
)


@strawberry_django.type(models.StaticRoute, fields='__all__', filters=StaticRouteFilter)
class StaticRouteType(PrimaryObjectType):

    name: str
    devices: List[Annotated["DeviceType", strawberry.lazy('dcim.graphql.types')]] | None
    vrf: Annotated["VRFType", strawberry.lazy('ipam.graphql.types')] | None
    prefix: str | None
    next_hop: str | None
    metric: int | None
    permanent: bool | None


@strawberry_django.type(
    models.OSPFInstance, fields='__all__', filters=OSPFInstanceFilter
)
class OSPFInstanceType(PrimaryObjectType):

    name: str
    device: Annotated["DeviceType", strawberry.lazy('dcim.graphql.types')]
    vrf: Annotated["VRFType", strawberry.lazy('ipam.graphql.types')] | None
    router_id: str
    process_id: str


@strawberry_django.type(models.OSPFArea, fields='__all__', filters=OSPFAreaFilter)
class OSPFAreaType(PrimaryObjectType):

    area_id: str
    area_type: str


@strawberry_django.type(
    models.OSPFInterface, fields='__all__', filters=OSPFInterfaceFilter
)
class OSPFInterfaceType(PrimaryObjectType):

    instance: Annotated[
        "OSPFInstanceType", strawberry.lazy('netbox_routing.graphql.types')
    ]
    area: Annotated["OSPFAreaType", strawberry.lazy('netbox_routing.graphql.types')]
    interface: Annotated["InterfaceType", strawberry.lazy('dcim.graphql.types')]
    passive: bool | None
    priority: str | None
    bfd: bool | None
    authentication: str | None
    passphrase: str | None


@strawberry_django.type(models.EIGRPRouter, fields='__all__', filters=EIGRPRouterFilter)
class EIGRPRouterType(PrimaryObjectType):

    device: Annotated["DeviceType", strawberry.lazy('dcim.graphql.types')]
    rid: str
    type: str
    name: str
    pid: str


@strawberry_django.type(
    models.EIGRPAddressFamily, fields='__all__', filters=EIGRPAddressFamilyFilter
)
class EIGRPAddressFamilyType(PrimaryObjectType):

    router: Annotated[
        "EIGRPRouterType", strawberry.lazy('netbox_routing.graphql.types')
    ]
    rid: str


@strawberry_django.type(
    models.EIGRPNetwork, fields='__all__', filters=EIGRPNetworkFilter
)
class EIGRPNetworkType(PrimaryObjectType):

    router: Annotated[
        "EIGRPRouterType", strawberry.lazy('netbox_routing.graphql.types')
    ]
    address_family: (
        Annotated[
            "EIGRPAddressFamilyType", strawberry.lazy('netbox_routing.graphql.types')
        ]
        | None
    )
    network: Annotated["PrefixType", strawberry.lazy('ipam.graphql.types')]


@strawberry_django.type(
    models.EIGRPInterface, fields='__all__', filters=EIGRPInterfaceFilter
)
class EIGRPInterfaceType(PrimaryObjectType):

    router: Annotated[
        "EIGRPRouterType", strawberry.lazy('netbox_routing.graphql.types')
    ]
    address_family: (
        Annotated[
            "EIGRPAddressFamilyType", strawberry.lazy('netbox_routing.graphql.types')
        ]
        | None
    )
    interface: Annotated["InterfaceType", strawberry.lazy('dcim.graphql.types')]
    passive: str | None
    bfd: bool | None
    authentication: str | None
    passphrase: str | None


@strawberry_django.type(models.Community, fields='__all__', filters=CommunityFilter)
class CommunityType(PrimaryObjectType):

    community: str
    status: str
    role: Annotated["RoleType", strawberry.lazy('ipam.graphql.types')] | None
    tenant: Annotated["TenantType", strawberry.lazy('tenancy.graphql.types')] | None


@strawberry_django.type(
    models.CommunityList, fields='__all__', filters=CommunityListFilter
)
class CommunityListType(PrimaryObjectType):

    name: str
    tenant: Annotated["TenantType", strawberry.lazy('tenancy.graphql.types')] | None


@strawberry_django.type(
    models.CommunityListEntry, fields='__all__', filters=CommunityListEntryFilter
)
class CommunityListEntryType(PrimaryObjectType):

    community_list: Annotated[
        "CommunityListType", strawberry.lazy('netbox_routing.graphql.types')
    ]
    community: Annotated[
        "CommunityType", strawberry.lazy('netbox_routing.graphql.types')
    ]


@strawberry_django.type(models.ASPath, fields='__all__', filters=ASPathFilter)
class ASPathType(PrimaryObjectType):

    name: str


@strawberry_django.type(models.ASPathEntry, fields='__all__', filters=ASPathEntryFilter)
class ASPathEntryType(PrimaryObjectType):

    aspath: Annotated["ASPathType", strawberry.lazy('netbox_routing.graphql.types')]
    action: str
    sequence: int
    pattern: str | None


@strawberry_django.type(models.PrefixList, fields='__all__', filters=PrefixListFilter)
class PrefixListType(PrimaryObjectType):

    name: str


@strawberry_django.type(
    models.PrefixListEntry, fields='__all__', filters=PrefixListEntryFilter
)
class PrefixListEntryType(PrimaryObjectType):

    prefix_list: Annotated[
        "PrefixListType", strawberry.lazy('netbox_routing.graphql.types')
    ]
    action: str
    sequence: int
    prefix: str | None
    le: int | None
    ge: int | None


@strawberry_django.type(models.RouteMap, fields='__all__', filters=RouteMapFilter)
class RouteMapType(PrimaryObjectType):
    name: str


@strawberry_django.type(
    models.RouteMapEntry, fields='__all__', filters=RouteMapEntryFilter
)
class RouteMapEntryType(PrimaryObjectType):

    route_map: Annotated[
        "RouteMapType", strawberry.lazy('netbox_routing.graphql.types')
    ]
    action: str
    sequence: int
    # match: Dict | None
    # set: Dict | None
