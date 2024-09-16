import strawberry_django

from netbox_routing import filtersets, models

from netbox.graphql.filter_mixins import autotype_decorator, BaseFilterMixin

__all__ = (
    'StaticRouteFilter',
)


@strawberry_django.filter(models.StaticRoute, lookups=True)
@autotype_decorator(filtersets.StaticRouteFilterSet)
class StaticRouteFilter(BaseFilterMixin):
    prefix: str
    next_hop: str
