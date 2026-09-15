# SPDX-License-Identifier: Apache-2.0

from typing import Annotated, Union

import strawberry
import strawberry_django

from netbox.graphql.types import PrimaryObjectType
from netbox_routing import models
from netbox_routing.graphql.isis.filters import (
    ISISInstanceFilter,
    ISISInterfaceFilter,
    ISISSettingFilter,
    ISISLevelFilter,
    ISISInterfaceLevelFilter,
    ISISSegmentRoutingFilter,
    ISISFlexAlgoFilter,
    ISISPrefixSIDFilter,
    ISISSRv6LocatorFilter,
)

__all__ = (
    'ISISInstanceType',
    'ISISInterfaceType',
    'ISISSettingType',
    'ISISLevelType',
    'ISISInterfaceLevelType',
    'ISISSegmentRoutingType',
    'ISISFlexAlgoType',
    'ISISPrefixSIDType',
    'ISISSRv6LocatorType',
)


@strawberry_django.type(
    models.ISISFlexAlgo, fields='__all__', filters=ISISFlexAlgoFilter
)
class ISISFlexAlgoType(PrimaryObjectType):
    instance: Annotated[
        'ISISInstanceType', strawberry.lazy('netbox_routing.graphql.types')
    ]
    algo_id: int


@strawberry_django.type(
    models.ISISPrefixSID, fields='__all__', filters=ISISPrefixSIDFilter
)
class ISISPrefixSIDType(PrimaryObjectType):
    interface: Annotated[
        'ISISInterfaceType', strawberry.lazy('netbox_routing.graphql.types')
    ]
    algorithm: int


@strawberry_django.type(
    models.ISISSRv6Locator, fields='__all__', filters=ISISSRv6LocatorFilter
)
class ISISSRv6LocatorType(PrimaryObjectType):
    instance: Annotated[
        'ISISInstanceType', strawberry.lazy('netbox_routing.graphql.types')
    ]
    name: str
    # prefix is an IPNetworkField; expose it as a string (mirrors StaticRouteType.prefix).
    # vendor_ext (JSONField) is auto-mapped to the JSON scalar by fields='__all__'.
    prefix: str | None


class ISISSettingsMixin:
    settings: list[
        Annotated['ISISSettingType', strawberry.lazy('netbox_routing.graphql.types')]
    ]


@strawberry_django.type(
    models.ISISLevel,
    # Drop fields='__all__' so exclude is honoured — keeps the plaintext per-level
    # auth_key off the schema (auth_type stays). See ISISSettingType below.
    exclude=['auth_key'],
    filters=ISISLevelFilter,
)
class ISISLevelType(PrimaryObjectType):
    instance: Annotated[
        'ISISInstanceType', strawberry.lazy('netbox_routing.graphql.types')
    ]
    level: int


@strawberry_django.type(
    models.ISISInterfaceLevel, fields='__all__', filters=ISISInterfaceLevelFilter
)
class ISISInterfaceLevelType(PrimaryObjectType):
    interface: Annotated[
        'ISISInterfaceType', strawberry.lazy('netbox_routing.graphql.types')
    ]
    level: int


@strawberry_django.type(
    models.ISISSegmentRouting, fields='__all__', filters=ISISSegmentRoutingFilter
)
class ISISSegmentRoutingType(PrimaryObjectType):
    instance: Annotated[
        'ISISInstanceType', strawberry.lazy('netbox_routing.graphql.types')
    ]


@strawberry_django.type(
    models.ISISSetting,
    # NB: `exclude` is only honoured when `fields='__all__'` is NOT also set —
    # otherwise `fields` wins and the raw GFK columns leak onto the schema. So we
    # rely on `exclude` alone (= all fields minus the excluded ones). The
    # non-secret `assigned_object_type` is re-added below as a typed
    # ContentTypeType; `assigned_object_id` stays hidden in favour of the
    # resolved `assigned_object` union.
    exclude=['assigned_object_type', 'assigned_object_id'],
    filters=ISISSettingFilter,
)
class ISISSettingType(PrimaryObjectType):

    assigned_object_type: (
        Annotated["ContentTypeType", strawberry.lazy('netbox.graphql.types')] | None
    )
    assigned_object: Union[
        Annotated['ISISInstanceType', strawberry.lazy('netbox_routing.graphql.types')],
        Annotated['ISISInterfaceType', strawberry.lazy('netbox_routing.graphql.types')],
        None,
    ]
    key: str
    value: str


@strawberry_django.type(
    models.ISISInstance,
    exclude=['area_auth_key', 'domain_auth_key'],
    filters=ISISInstanceFilter,
)
class ISISInstanceType(ISISSettingsMixin, PrimaryObjectType):

    device: Annotated["DeviceType", strawberry.lazy('dcim.graphql.types')]
    vrf: Annotated["VRFType", strawberry.lazy('ipam.graphql.types')] | None
    process_tag: str
    net: str
    is_type: str
    metric_style: str
    overload_bit: bool | None
    area_auth_type: str
    domain_auth_type: str


@strawberry_django.type(
    models.ISISInterface,
    exclude=['hello_auth_key'],
    filters=ISISInterfaceFilter,
)
class ISISInterfaceType(ISISSettingsMixin, PrimaryObjectType):

    instance: Annotated[
        "ISISInstanceType", strawberry.lazy('netbox_routing.graphql.types')
    ]
    interface: Annotated["InterfaceType", strawberry.lazy('dcim.graphql.types')]
    address_family: str
    circuit_type: str | None
    network_type: str | None
    metric: int | None
    passive: bool | None
    hello_auth_type: str | None
    bfd_enabled: bool | None
