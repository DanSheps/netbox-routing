from typing import Annotated, List

import strawberry
import strawberry_django

from netbox.graphql.types import NetBoxObjectType
from .filters import *

from netbox_routing import models

__all__ = (
    'StaticRouteType',
)


@strawberry_django.type(
    models.StaticRoute,
    fields='__all__',
    filters=StaticRouteFilter
)
class StaticRouteType(NetBoxObjectType):

    name: str
    devices: List[Annotated["DeviceType", strawberry.lazy('dcim.graphql.types')]] | None
    vrf: Annotated["VRFType", strawberry.lazy('ipam.graphql.types')] | None
    prefix: str | None
    next_hop: str | None
    metric: int | None
    permanent: bool | None

