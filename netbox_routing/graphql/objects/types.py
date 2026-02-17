from typing import Annotated, Union

import strawberry
import strawberry_django

from netbox.graphql.types import PrimaryObjectType
from netbox_routing import models
from netbox_routing.graphql.objects.filters import *

__all__ = (
    'ASPathType',
    'ASPathEntryType',
    'PrefixListType',
    'PrefixListEntryType',
    'RouteMapType',
    'RouteMapEntryType',
    'CustomPrefixType',
)


@strawberry_django.type(models.ASPath, fields='__all__', filters=ASPathFilter)
class ASPathType(PrimaryObjectType):

    name: str


@strawberry_django.type(
    models.ASPathEntry,
    fields='__all__',
    filters=ASPathEntryFilter,
    select_related=[
        'aspath',
    ],
)
class ASPathEntryType(PrimaryObjectType):

    aspath: Annotated["ASPathType", strawberry.lazy('netbox_routing.graphql.types')]
    action: str
    sequence: int
    pattern: str | None


@strawberry_django.type(models.PrefixList, fields='__all__', filters=PrefixListFilter)
class PrefixListType(PrimaryObjectType):

    name: str


@strawberry_django.type(
    models.PrefixListEntry,
    fields='__all__',
    exclude=['assigned_prefix_type', 'assigned_prefix_id'],
    filters=PrefixListEntryFilter,
    select_related=[
        'prefix_list',
    ],
)
class PrefixListEntryType(PrimaryObjectType):

    prefix_list: Annotated[
        "PrefixListType", strawberry.lazy('netbox_routing.graphql.types')
    ]
    action: str
    sequence: int
    assigned_prefix_type: (
        Annotated["ContentTypeType", strawberry.lazy('netbox.graphql.types')] | None
    )  # noqa: F821
    assigned_prefix: (
        Union[
            Annotated["PrefixType", strawberry.lazy('ipam.graphql.types')],
            Annotated[
                "CustomPrefixType", strawberry.lazy('netbox_routing.graphql.types')
            ],
        ]
        | None
    )
    le: int | None
    ge: int | None


@strawberry_django.type(models.RouteMap, fields='__all__', filters=RouteMapFilter)
class RouteMapType(PrimaryObjectType):
    name: str


@strawberry_django.type(
    models.RouteMapEntry,
    fields='__all__',
    filters=RouteMapEntryFilter,
    select_related=[
        'route_map',
    ],
)
class RouteMapEntryType(PrimaryObjectType):

    route_map: Annotated[
        "RouteMapType", strawberry.lazy('netbox_routing.graphql.types')
    ]
    action: str
    sequence: int
    # match: Dict | None
    # set: Dict | None


@strawberry_django.type(
    models.CustomPrefix,
    fields='__all__',
    filters=CustomPrefixFilter,
)
class CustomPrefixType(PrimaryObjectType):
    prefix: str
