import strawberry_django
from netbox.graphql.filter_mixins import autotype_decorator, BaseFilterMixin

from netbox_routing import filtersets, models

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


@strawberry_django.filter(models.EIGRPRouter, lookups=True)
@autotype_decorator(filtersets.EIGRPRouterFilterSet)
class EIGRPRouterFilter(BaseFilterMixin):
    rid: str


@strawberry_django.filter(models.EIGRPAddressFamily, lookups=True)
@autotype_decorator(filtersets.EIGRPAddressFamilyFilterSet)
class EIGRPAddressFamilyFilter(BaseFilterMixin):
    rid: str


@strawberry_django.filter(models.EIGRPNetwork, lookups=True)
@autotype_decorator(filtersets.EIGRPNetworkFilterSet)
class EIGRPNetworkFilter(BaseFilterMixin):
    pass


@strawberry_django.filter(models.EIGRPInterface, lookups=True)
@autotype_decorator(filtersets.EIGRPInterfaceFilterSet)
class EIGRPInterfaceFilter(BaseFilterMixin):
    pass
