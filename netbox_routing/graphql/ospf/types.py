from typing import Annotated

import strawberry
import strawberry_django

from netbox.graphql.types import PrimaryObjectType
from netbox_routing import models
from netbox_routing.graphql.ospf.filters import (
    OSPFInstanceFilter,
    OSPFAreaFilter,
    OSPFInterfaceFilter,
)

__all__ = (
    'OSPFInstanceType',
    'OSPFAreaType',
    'OSPFInterfaceType',
)


@strawberry_django.type(
    models.OSPFInstance, fields='__all__', filters=OSPFInstanceFilter
)
class OSPFInstanceType(PrimaryObjectType):
    name: str
    device: Annotated["DeviceType", strawberry.lazy('dcim.graphql.types')]
    vrf: Annotated["VRFType", strawberry.lazy('ipam.graphql.types')] | None
    router_id: str
    process_id: str
    reference_bandwidth: int | None
    timers_spf_initial: int | None
    timers_spf_hold: int | None
    timers_spf_max: int | None
    timers_lsa_initial: int | None
    timers_lsa_hold: int | None
    timers_lsa_max: int | None
    distance: int | None
    distance_intra_area: int | None
    distance_inter_area: int | None
    distance_external: int | None
    default_information_originate: str | None
    default_information_metric: int | None
    default_information_metric_type: str | None
    max_metric_router_lsa: bool | None
    max_metric_on_startup: int | None
    passive_interface_default: bool | None


@strawberry_django.type(models.OSPFArea, fields='__all__', filters=OSPFAreaFilter)
class OSPFAreaType(PrimaryObjectType):
    area_id: str
    area_type: str


@strawberry_django.type(
    models.OSPFInterface, fields='__all__', filters=OSPFInterfaceFilter
)
class OSPFInterfaceType(PrimaryObjectType):
    instance: Annotated[
        "OSPFInstanceType", strawberry.lazy('netbox_routing.graphql.types')
    ]
    area: Annotated["OSPFAreaType", strawberry.lazy('netbox_routing.graphql.types')]
    interface: Annotated["InterfaceType", strawberry.lazy('dcim.graphql.types')]
    network_type: str | None
    passive: bool | None
    priority: str | None
    bfd: bool | None
    authentication: str | None
    passphrase: str | None
