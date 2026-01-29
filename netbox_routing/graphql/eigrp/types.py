from typing import Annotated

import strawberry
import strawberry_django

from netbox.graphql.types import PrimaryObjectType
from netbox_routing import models
from netbox_routing.graphql.eigrp.filters import (
    EIGRPRouterFilter,
    EIGRPAddressFamilyFilter,
    EIGRPNetworkFilter,
    EIGRPInterfaceFilter,
)

__all__ = (
    'EIGRPRouterType',
    'EIGRPAddressFamilyType',
    'EIGRPNetworkType',
    'EIGRPInterfaceType',
)


@strawberry_django.type(models.EIGRPRouter, fields='__all__', filters=EIGRPRouterFilter)
class EIGRPRouterType(PrimaryObjectType):

    device: Annotated["DeviceType", strawberry.lazy('dcim.graphql.types')]  # noqa: F821
    rid: str
    type: str
    name: str
    pid: str


@strawberry_django.type(
    models.EIGRPAddressFamily, fields='__all__', filters=EIGRPAddressFamilyFilter
)
class EIGRPAddressFamilyType(PrimaryObjectType):

    router: Annotated[
        "EIGRPRouterType", strawberry.lazy('netbox_routing.graphql.types')
    ]
    rid: str


@strawberry_django.type(
    models.EIGRPNetwork, fields='__all__', filters=EIGRPNetworkFilter
)
class EIGRPNetworkType(PrimaryObjectType):

    router: Annotated[
        "EIGRPRouterType", strawberry.lazy('netbox_routing.graphql.types')
    ]
    address_family: (
        Annotated[
            "EIGRPAddressFamilyType", strawberry.lazy('netbox_routing.graphql.types')
        ]
        | None
    )
    network: Annotated[
        "PrefixType", strawberry.lazy('ipam.graphql.types')
    ]  # noqa: F821


@strawberry_django.type(
    models.EIGRPInterface, fields='__all__', filters=EIGRPInterfaceFilter
)
class EIGRPInterfaceType(PrimaryObjectType):

    router: Annotated[
        "EIGRPRouterType", strawberry.lazy('netbox_routing.graphql.types')
    ]
    address_family: (
        Annotated[
            "EIGRPAddressFamilyType", strawberry.lazy('netbox_routing.graphql.types')
        ]
        | None
    )
    interface: Annotated[
        "InterfaceType", strawberry.lazy('dcim.graphql.types')
    ]  # noqa: F821
    passive: str | None
    bfd: bool | None
    authentication: str | None
    passphrase: str | None
