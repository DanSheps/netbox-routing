from typing import Annotated, List, Union

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
    
    'EIGRPRouterType',
    'EIGRPAddressFamilyType',
    'EIGRPNetworkType',
    'EIGRPInterfaceType',
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
    vrf: Annotated["VRFType", strawberry.lazy('ipam.graphql.types')] | None
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

    instance: Annotated["OSPFInstanceType", strawberry.lazy('netbox_routing.graphql.types')]
    area: Annotated["OSPFAreaType", strawberry.lazy('netbox_routing.graphql.types')]
    interface: Annotated["InterfaceType", strawberry.lazy('dcim.graphql.types')]
    passive: bool | None
    priority: str | None
    bfd: bool | None
    authentication: str | None
    passphrase: str | None


@strawberry_django.type(
    models.EIGRPRouter,
    fields='__all__',
    filters=EIGRPRouterFilter
)
class EIGRPRouterType(NetBoxObjectType):

    device: Annotated["DeviceType", strawberry.lazy('dcim.graphql.types')]
    rid: str
    type: str
    name: str
    pid: str


@strawberry_django.type(
    models.EIGRPAddressFamily,
    fields='__all__',
    filters=EIGRPAddressFamilyFilter
)
class EIGRPAddressFamilyType(NetBoxObjectType):

    router: Annotated["EIGRPRouterType", strawberry.lazy('netbox_routing.graphql.types')]
    rid: str


@strawberry_django.type(
    models.EIGRPNetwork,
    fields='__all__',
    filters=EIGRPNetworkFilter
)
class EIGRPNetworkType(NetBoxObjectType):

    router: Annotated["EIGRPRouterType", strawberry.lazy('netbox_routing.graphql.types')]
    address_family: Annotated["EIGRPAddressFamilyType", strawberry.lazy('netbox_routing.graphql.types')] | None
    network: Annotated["PrefixType", strawberry.lazy('ipam.graphql.types')]


@strawberry_django.type(
    models.EIGRPInterface,
    fields='__all__',
    filters=EIGRPInterfaceFilter
)
class EIGRPInterfaceType(NetBoxObjectType):

    router: Annotated["EIGRPRouterType", strawberry.lazy('netbox_routing.graphql.types')]
    address_family: Annotated["EIGRPAddressFamilyType", strawberry.lazy('netbox_routing.graphql.types')] | None
    interface: Annotated["InterfaceType", strawberry.lazy('dcim.graphql.types')]
    passive: str | None
    bfd: bool | None
    authentication: str | None
    passphrase: str | None

