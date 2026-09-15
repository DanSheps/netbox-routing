# SPDX-License-Identifier: Apache-2.0

from typing import Annotated

import strawberry
import strawberry_django
from strawberry import ID
from strawberry_django import StrFilterLookup

from netbox.graphql.filters import PrimaryModelFilter
from netbox_routing import models
from netbox_routing.graphql.filter_mixins import VRFMixin, DeviceMixin, InterfaceMixin

__all__ = (
    'ISISInstanceFilter',
    'ISISInterfaceFilter',
    'ISISSettingFilter',
    'ISISLevelFilter',
    'ISISInterfaceLevelFilter',
    'ISISSegmentRoutingFilter',
    'ISISFlexAlgoFilter',
    'ISISPrefixSIDFilter',
    'ISISSRv6LocatorFilter',
)


@strawberry_django.filter(models.ISISFlexAlgo, lookups=True)
class ISISFlexAlgoFilter(PrimaryModelFilter):
    instance_id: ID | None = strawberry_django.filter_field()


@strawberry_django.filter(models.ISISPrefixSID, lookups=True)
class ISISPrefixSIDFilter(PrimaryModelFilter):
    interface_id: ID | None = strawberry_django.filter_field()


@strawberry_django.filter(models.ISISSRv6Locator, lookups=True)
class ISISSRv6LocatorFilter(PrimaryModelFilter):
    instance_id: ID | None = strawberry_django.filter_field()
    # prefix is an IPNetworkField; declare an explicit string lookup so schema build
    # does not choke on the custom field type (mirrors StaticRouteFilter.prefix).
    prefix: StrFilterLookup | None = strawberry_django.filter_field()


@strawberry_django.filter(models.ISISSetting, lookups=True)
class ISISSettingFilter(PrimaryModelFilter):
    pass


@strawberry_django.filter(models.ISISLevel, lookups=True)
class ISISLevelFilter(PrimaryModelFilter):
    instance_id: ID | None = strawberry_django.filter_field()


@strawberry_django.filter(models.ISISInterfaceLevel, lookups=True)
class ISISInterfaceLevelFilter(PrimaryModelFilter):
    interface_id: ID | None = strawberry_django.filter_field()


@strawberry_django.filter(models.ISISSegmentRouting, lookups=True)
class ISISSegmentRoutingFilter(PrimaryModelFilter):
    instance_id: ID | None = strawberry_django.filter_field()


@strawberry_django.filter(models.ISISInstance, lookups=True)
class ISISInstanceFilter(VRFMixin, DeviceMixin, PrimaryModelFilter):
    process_tag: StrFilterLookup | None = strawberry_django.filter_field()
    net: StrFilterLookup | None = strawberry_django.filter_field()


@strawberry_django.filter(models.ISISInterface, lookups=True)
class ISISInterfaceFilter(InterfaceMixin, PrimaryModelFilter):
    instance: (
        Annotated[
            'ISISInstanceFilter', strawberry.lazy('netbox_routing.graphql.filters')
        ]
        | None
    ) = strawberry_django.filter_field()
    instance_id: ID | None = strawberry_django.filter_field()
