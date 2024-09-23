from typing import Annotated

import strawberry
import strawberry_django

from netbox_routing import filtersets, models

from netbox.graphql.filter_mixins import autotype_decorator, BaseFilterMixin

__all__ = (
    'StaticRouteFilter',
    'OSPFInstanceFilter',
    'OSPFAreaFilter',
    'OSPFInterfaceFilter',
)


@strawberry_django.filter(models.StaticRoute, lookups=True)
@autotype_decorator(filtersets.StaticRouteFilterSet)
class StaticRouteFilter(BaseFilterMixin):
    prefix: str
    next_hop: str


@strawberry_django.filter(models.OSPFInstance, lookups=True)
@autotype_decorator(filtersets.OSPFInstanceFilterSet)
class OSPFInstanceFilter(BaseFilterMixin):
    router_id: str


@strawberry_django.filter(models.OSPFArea, lookups=True)
@autotype_decorator(filtersets.OSPFAreaFilterSet)
class OSPFAreaFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(models.OSPFInterface, lookups=True)
@autotype_decorator(filtersets.OSPFInterfaceFilterSet)
class OSPFInterfaceFilter(BaseFilterMixin):
    pass
