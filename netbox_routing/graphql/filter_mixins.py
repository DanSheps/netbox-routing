from typing import Annotated

import strawberry
import strawberry_django
from strawberry import ID


class DeviceMixin:
    device: (
        Annotated['DeviceFilter', strawberry.lazy('dcim.graphql.filters')] | None
    ) = strawberry_django.filter_field()
    device_id: ID | None = strawberry_django.filter_field()


class InterfaceMixin(DeviceMixin):
    device: (
        Annotated['DeviceFilter', strawberry.lazy('dcim.graphql.filters')] | None
    ) = strawberry_django.filter_field()
    device_id: ID | None = strawberry_django.filter_field()
    interface: (
        Annotated['InterfaceFilter', strawberry.lazy('dcim.graphql.filters')] | None
    ) = strawberry_django.filter_field()
    interface_id: ID | None = strawberry_django.filter_field()


class VRFMixin:
    vrf: Annotated['VRFFilter', strawberry.lazy('ipam.graphql.filters')] | None = (
        strawberry_django.filter_field()
    )


class NetworkPrefixMixin:
    network: (
        Annotated['PrefixFilter', strawberry.lazy('ipam.graphql.filters')] | None
    ) = strawberry_django.filter_field()
    network_id: ID | None = strawberry_django.filter_field()
