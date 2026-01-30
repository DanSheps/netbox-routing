from typing import Annotated

import strawberry
import strawberry_django
from strawberry import ID
from strawberry_django import FilterLookup

from netbox.graphql.filters import PrimaryModelFilter
from netbox_routing import models
from netbox_routing.graphql.filter_mixins import VRFMixin, DeviceMixin, InterfaceMixin

__all__ = (
    'OSPFAreaFilter',
    'OSPFInstanceFilter',
    'OSPFInterfaceFilter',
)


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
