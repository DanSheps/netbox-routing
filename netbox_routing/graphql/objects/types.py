from typing import Annotated

import strawberry
import strawberry_django

from netbox.graphql.types import PrimaryObjectType
from netbox_routing import models
from netbox_routing.graphql.objects.filters import (
    ASPathFilter,
    ASPathEntryFilter,
    PrefixListFilter,
    PrefixListEntryFilter,
    RouteMapFilter,
    RouteMapEntryFilter,
)

__all__ = (
    'ASPathType',
    'ASPathEntryType',
    'PrefixListType',
    'PrefixListEntryType',
    'RouteMapType',
    'RouteMapEntryType',
)


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
