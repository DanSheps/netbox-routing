import strawberry_django
from strawberry_django import StrFilterLookup

from netbox.graphql.filters import PrimaryModelFilter
from netbox_routing import models
from netbox_routing.graphql.filter_mixins import VRFMixin, DeviceMixin

__all__ = ('StaticRouteFilter',)


@strawberry_django.filter(models.StaticRoute, lookups=True)
class StaticRouteFilter(VRFMixin, DeviceMixin, PrimaryModelFilter):
    prefix: StrFilterLookup | None = strawberry_django.filter_field()
    next_hop: StrFilterLookup | None = strawberry_django.filter_field()
