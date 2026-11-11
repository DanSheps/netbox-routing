from typing import TYPE_CHECKING, Annotated

import strawberry
import strawberry_django
from strawberry import ID
from strawberry_django import BaseFilterLookup, FilterLookup, StrFilterLookup

from netbox.graphql.filters import PrimaryModelFilter
from netbox_routing import models
from netbox_routing.graphql.filter_mixins import VRFMixin, DeviceMixin, InterfaceMixin

if TYPE_CHECKING:
    from netbox.graphql.filter_lookups import IntegerLookup

IntegerLookupType = Annotated[
    'IntegerLookup', strawberry.lazy('netbox.graphql.filter_lookups')
]

__all__ = (
    'OSPFAreaFilter',
    'OSPFInstanceFilter',
    'OSPFInterfaceFilter',
)


@strawberry_django.filter(models.OSPFInstance, lookups=True)
class OSPFInstanceFilter(VRFMixin, DeviceMixin, PrimaryModelFilter):
    router_id: BaseFilterLookup[str] | None = strawberry_django.filter_field()
    reference_bandwidth: IntegerLookupType | None = strawberry_django.filter_field()
    timers_spf_initial: IntegerLookupType | None = strawberry_django.filter_field()
    timers_spf_hold: IntegerLookupType | None = strawberry_django.filter_field()
    timers_spf_max: IntegerLookupType | None = strawberry_django.filter_field()
    timers_lsa_initial: IntegerLookupType | None = strawberry_django.filter_field()
    timers_lsa_hold: IntegerLookupType | None = strawberry_django.filter_field()
    timers_lsa_max: IntegerLookupType | None = strawberry_django.filter_field()
    distance: IntegerLookupType | None = strawberry_django.filter_field()
    distance_intra_area: IntegerLookupType | None = strawberry_django.filter_field()
    distance_inter_area: IntegerLookupType | None = strawberry_django.filter_field()
    distance_external: IntegerLookupType | None = strawberry_django.filter_field()
    default_information_originate: StrFilterLookup | None = (
        strawberry_django.filter_field()
    )
    default_information_metric: IntegerLookupType | None = (
        strawberry_django.filter_field()
    )
    default_information_metric_type: StrFilterLookup | None = (
        strawberry_django.filter_field()
    )
    max_metric_router_lsa: FilterLookup[bool] | None = strawberry_django.filter_field()
    max_metric_on_startup: IntegerLookupType | None = strawberry_django.filter_field()
    passive_interface_default: FilterLookup[bool] | None = (
        strawberry_django.filter_field()
    )


@strawberry_django.filter(models.OSPFArea, lookups=True)
class OSPFAreaFilter(PrimaryModelFilter):
    area_id: StrFilterLookup | None = strawberry_django.filter_field()


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
