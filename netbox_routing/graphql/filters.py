from typing import Annotated

import strawberry
import strawberry_django
from strawberry import ID
from strawberry_django import FilterLookup

from netbox.graphql.filters import PrimaryModelFilter
from ipam.graphql.filters import RoleFilter
from tenancy.graphql.filter_mixins import TenancyFilterMixin

from netbox_routing import models
from netbox_routing.graphql.filter_mixins import (
    DeviceMixin,
    InterfaceMixin,
    VRFMixin,
    NetworkPrefixMixin,
)

__all__ = (
    'StaticRouteFilter',
    'OSPFInstanceFilter',
    'OSPFAreaFilter',
    'OSPFInterfaceFilter',
    'EIGRPRouterFilter',
    'EIGRPAddressFamilyFilter',
    'EIGRPNetworkFilter',
    'EIGRPInterfaceFilter',
    'CommunityFilter',
    'CommunityListFilter',
    'CommunityListEntryFilter',
    'ASPathFilter',
    'ASPathEntryFilter',
    'PrefixListFilter',
    'PrefixListEntryFilter',
    'RouteMapFilter',
    'RouteMapEntryFilter',
)


@strawberry_django.filter(models.StaticRoute, lookups=True)
class StaticRouteFilter(VRFMixin, DeviceMixin, PrimaryModelFilter):
    prefix: FilterLookup[str] | None = strawberry_django.filter_field()
    next_hop: FilterLookup[str] | None = strawberry_django.filter_field()


@strawberry_django.filter(models.OSPFInstance, lookups=True)
class OSPFInstanceFilter(VRFMixin, DeviceMixin, PrimaryModelFilter):
    router_id: FilterLookup[str] | None = strawberry_django.filter_field()


@strawberry_django.filter(models.OSPFArea, lookups=True)
class OSPFAreaFilter(PrimaryModelFilter):
    area_id: FilterLookup[str] | None = strawberry_django.filter_field()


@strawberry_django.filter(models.OSPFInterface, lookups=True)
class OSPFInterfaceFilter(InterfaceMixin, VRFMixin, PrimaryModelFilter):
    instance: (
        Annotated[
            'OSPFInstanceFilter', strawberry.lazy('netbox_routing.graphql.filters')
        ]
        | None
    ) = strawberry_django.filter_field()
    instance_id: ID | None = strawberry_django.filter_field()
    area: (
        Annotated['OSPFAreaFilter', strawberry.lazy('netbox_routing.graphql.filters')]
        | None
    ) = strawberry_django.filter_field()
    area_id: ID | None = strawberry_django.filter_field()


@strawberry_django.filter(models.EIGRPRouter, lookups=True)
class EIGRPRouterFilter(DeviceMixin, PrimaryModelFilter):
    rid: FilterLookup[str] | None = strawberry_django.filter_field()


@strawberry_django.filter(models.EIGRPAddressFamily, lookups=True)
class EIGRPAddressFamilyFilter(PrimaryModelFilter):
    router: (
        Annotated[
            'EIGRPRouterFilter', strawberry.lazy('netbox_routing.graphql.filters')
        ]
        | None
    ) = strawberry_django.filter_field()
    router_id: ID | None = strawberry_django.filter_field()
    rid: FilterLookup[str] | None = strawberry_django.filter_field()


@strawberry_django.filter(models.EIGRPNetwork, lookups=True)
class EIGRPNetworkFilter(NetworkPrefixMixin, PrimaryModelFilter):
    router: (
        Annotated[
            'EIGRPRouterFilter', strawberry.lazy('netbox_routing.graphql.filters')
        ]
        | None
    ) = strawberry_django.filter_field()
    router_id: ID | None = strawberry_django.filter_field()
    address_family: (
        Annotated[
            'EIGRPAddressFamilyFilter',
            strawberry.lazy('netbox_routing.graphql.filters'),
        ]
        | None
    ) = strawberry_django.filter_field()
    address_family_id: ID | None = strawberry_django.filter_field()


@strawberry_django.filter(models.EIGRPInterface, lookups=True)
class EIGRPInterfaceFilter(InterfaceMixin, PrimaryModelFilter):
    router: (
        Annotated[
            'EIGRPRouterFilter', strawberry.lazy('netbox_routing.graphql.filters')
        ]
        | None
    ) = strawberry_django.filter_field()
    router_id: ID | None = strawberry_django.filter_field()
    address_family: (
        Annotated[
            'EIGRPAddressFamilyFilter',
            strawberry.lazy('netbox_routing.graphql.filters'),
        ]
        | None
    ) = strawberry_django.filter_field()
    address_family_id: ID | None = strawberry_django.filter_field()


@strawberry_django.filter(models.Community, lookups=True)
class CommunityFilter(TenancyFilterMixin, PrimaryModelFilter):
    role: (
        Annotated[
            'RoleFilter',
            strawberry.lazy('ipam.graphql.filters'),
        ]
        | None
    ) = strawberry_django.filter_field()
    role_id: ID | None = strawberry_django.filter_field()


@strawberry_django.filter(models.CommunityList, lookups=True)
class CommunityListFilter(TenancyFilterMixin, PrimaryModelFilter):
    pass


@strawberry_django.filter(models.CommunityListEntry, lookups=True)
class CommunityListEntryFilter(PrimaryModelFilter):
    community_list: (
        Annotated[
            'CommunityListFilter',
            strawberry.lazy('netbox_routing.graphql.filters'),
        ]
        | None
    ) = strawberry_django.filter_field()
    community_list_id: ID | None = strawberry_django.filter_field()

    community: (
        Annotated[
            'CommunityFilter',
            strawberry.lazy('netbox_routing.graphql.filters'),
        ]
        | None
    ) = strawberry_django.filter_field()
    community_id: ID | None = strawberry_django.filter_field()


@strawberry_django.filter(models.ASPath, lookups=True)
class ASPathFilter(PrimaryModelFilter):
    pass


@strawberry_django.filter(models.ASPathEntry, lookups=True)
class ASPathEntryFilter(PrimaryModelFilter):
    aspath: (
        Annotated[
            'ASPathFilter',
            strawberry.lazy('netbox_routing.graphql.filters'),
        ]
        | None
    ) = strawberry_django.filter_field()
    aspath_id: ID | None = strawberry_django.filter_field()


@strawberry_django.filter(models.PrefixList, lookups=True)
class PrefixListFilter(PrimaryModelFilter):
    pass


@strawberry_django.filter(models.PrefixListEntry, lookups=True)
class PrefixListEntryFilter(PrimaryModelFilter):
    prefix_list: (
        Annotated[
            'PrefixListFilter',
            strawberry.lazy('netbox_routing.graphql.filters'),
        ]
        | None
    ) = strawberry_django.filter_field()
    prefix_list_id: ID | None = strawberry_django.filter_field()


@strawberry_django.filter(models.RouteMap, lookups=True)
class RouteMapFilter(PrimaryModelFilter):
    pass


@strawberry_django.filter(models.RouteMapEntry, lookups=True)
class RouteMapEntryFilter(PrimaryModelFilter):
    route_map: (
        Annotated[
            'RouteMapFilter',
            strawberry.lazy('netbox_routing.graphql.filters'),
        ]
        | None
    ) = strawberry_django.filter_field()
    route_map_id: ID | None = strawberry_django.filter_field()
