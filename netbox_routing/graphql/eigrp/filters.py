from typing import Annotated

import strawberry
import strawberry_django
from strawberry import ID
from strawberry_django import FilterLookup

from netbox.graphql.filters import PrimaryModelFilter
from netbox_routing import models
from netbox_routing.graphql.filter_mixins import (
    DeviceMixin,
    NetworkPrefixMixin,
    InterfaceMixin,
)

__all__ = (
    'EIGRPRouterFilter',
    'EIGRPAddressFamilyFilter',
    'EIGRPNetworkFilter',
    'EIGRPInterfaceFilter',
)


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
