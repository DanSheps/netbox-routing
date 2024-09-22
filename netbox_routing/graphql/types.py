from typing import Annotated, List

import strawberry
import strawberry_django

from netbox.graphql.types import NetBoxObjectType
from .filters import *

from netbox_routing import models

__all__ = (
    'StaticRouteType',
    'OSPFInstanceType',
    'OSPFAreaType',
    'OSPFInterfaceType',
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


@strawberry_django.type(
    models.OSPFInstance,
    fields='__all__',
    filters=OSPFInstanceFilter
)
class OSPFInstanceType(NetBoxObjectType):

    name: str
    device: Annotated["DeviceType", strawberry.lazy('dcim.graphql.types')]
    router_id: str
    process_id: str


@strawberry_django.type(
    models.OSPFArea,
    fields='__all__',
    filters=OSPFAreaFilter
)
class OSPFAreaType(NetBoxObjectType):

    area_id: str


@strawberry_django.type(
    models.OSPFInterface,
    fields='__all__',
    filters=OSPFInterfaceFilter
)
class OSPFInterfaceType(NetBoxObjectType):

    device: Annotated["DeviceType", strawberry.lazy('dcim.graphql.types')]
    instance: Annotated["OSPFInstanceType", strawberry.lazy('netbox_routing.graphql.types')]
    area: Annotated["OSPFAreaType", strawberry.lazy('netbox_routing.graphql.types')]
    interface: Annotated["InterfaceType", strawberry.lazy('dcim.graphql.types')]
    priority: str | None
    bfd: bool | None
    authentication: str | None
    passphrase: str | None

