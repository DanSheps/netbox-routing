from typing import Annotated

import strawberry
import strawberry_django
from strawberry import ID
from strawberry_django import FilterLookup

from netbox.graphql.filters import PrimaryModelFilter
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
