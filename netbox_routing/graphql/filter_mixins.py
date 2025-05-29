from typing import Annotated

import strawberry
import strawberry_django
from strawberry import ID

from core.graphql.filter_mixins import BaseObjectTypeFilterMixin


class DeviceMixin(BaseObjectTypeFilterMixin):
    device: Annotated['DeviceFilter', strawberry.lazy('dcim.graphql.filters')] | None = strawberry_django.filter_field()
    device_id: ID | None = strawberry_django.filter_field()


class InterfaceMixin(DeviceMixin, BaseObjectTypeFilterMixin):
    device: Annotated['DeviceFilter', strawberry.lazy('dcim.graphql.filters')] | None = strawberry_django.filter_field()
    device_id: ID | None = strawberry_django.filter_field()
    interface: Annotated['InterfaceFilter', strawberry.lazy('dcim.graphql.filters')] | None = strawberry_django.filter_field()
    interface_id: ID | None = strawberry_django.filter_field()


class VRFMixin:
    vrf: Annotated['VRFFilter', strawberry.lazy('ipam.graphql.filters')] | None = strawberry_django.filter_field()


class NetworkPrefixMixin(BaseObjectTypeFilterMixin):
    network: Annotated['PrefixFilter', strawberry.lazy('ipam.graphql.filters')] | None = strawberry_django.filter_field()
    network_id: ID | None = strawberry_django.filter_field()
