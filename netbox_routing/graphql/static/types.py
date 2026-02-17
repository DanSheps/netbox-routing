from typing import List, Annotated

import strawberry
import strawberry_django

from netbox.graphql.types import PrimaryObjectType
from netbox_routing import models
from netbox_routing.graphql.static.filters import StaticRouteFilter

__all__ = ('StaticRouteType',)


@strawberry_django.type(models.StaticRoute, fields='__all__', filters=StaticRouteFilter)
class StaticRouteType(PrimaryObjectType):

    name: str
    devices: List[Annotated["DeviceType", strawberry.lazy('dcim.graphql.types')]] | None
    vrf: Annotated["VRFType", strawberry.lazy('ipam.graphql.types')] | None
    prefix: str | None
    next_hop: str | None
    metric: int | None
    permanent: bool | None
