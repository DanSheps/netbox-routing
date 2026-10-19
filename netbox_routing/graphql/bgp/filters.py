from typing import TYPE_CHECKING, Annotated

import strawberry
import strawberry_django
from strawberry import ID
from strawberry_django import FilterLookup, StrFilterLookup

from netbox.graphql.filters import PrimaryModelFilter
from netbox_routing import models
from netbox_routing.graphql.filter_mixins import VRFMixin
from tenancy.graphql.filter_mixins import TenancyFilterMixin

if TYPE_CHECKING:
    from core.graphql.filters import ContentTypeFilter
    from ipam.graphql.filters import ASNFilter, IPAddressFilter

__all__ = (
    'BGPSettingFilter',
    'BGPPeerTemplateFilter',
    'BGPPolicyTemplateFilter',
    'BGPSessionTemplateFilter',
    'BGPRouterFilter',
    'BGPScopeFilter',
    'BGPAddressFamilyFilter',
    'BGPPeerFilter',
    'BGPPeerAddressFamilyFilter',
    'BFDProfileFilter',
)


@strawberry_django.filter(models.BGPPeerTemplate, lookups=True)
class BGPPeerTemplateFilter(TenancyFilterMixin, PrimaryModelFilter):
    name: StrFilterLookup | None = strawberry_django.filter_field()
    remote_as: (
        Annotated['ASNFilter', strawberry.lazy('ipam.graphql.filters')]
        | None
    ) = strawberry_django.filter_field()
    remote_as_id: ID | None = strawberry_django.filter_field()
    enabled: FilterLookup[bool] | None = strawberry_django.filter_field()


@strawberry_django.filter(models.BGPPolicyTemplate, lookups=True)
class BGPPolicyTemplateFilter(TenancyFilterMixin, PrimaryModelFilter):
    name: StrFilterLookup | None = strawberry_django.filter_field()
    enabled: FilterLookup[bool] | None = strawberry_django.filter_field()


@strawberry_django.filter(models.BGPSessionTemplate, lookups=True)
class BGPSessionTemplateFilter(TenancyFilterMixin, PrimaryModelFilter):
    name: StrFilterLookup | None = strawberry_django.filter_field()
    local_as: (
        Annotated['ASNFilter', strawberry.lazy('ipam.graphql.filters')]
        | None
    ) = strawberry_django.filter_field()
    local_as_id: ID | None = strawberry_django.filter_field()
    remote_as: (
        Annotated['ASNFilter', strawberry.lazy('ipam.graphql.filters')]
        | None
    ) = strawberry_django.filter_field()
    remote_as_id: ID | None = strawberry_django.filter_field()
    enabled: FilterLookup[bool] | None = strawberry_django.filter_field()


@strawberry_django.filter(models.BGPRouter, lookups=True)
class BGPRouterFilter(TenancyFilterMixin, PrimaryModelFilter):
    name: StrFilterLookup | None = strawberry_django.filter_field()
    assigned_object_type: (
        Annotated['ContentTypeFilter', strawberry.lazy('core.graphql.filters')]
        | None
    ) = strawberry_django.filter_field()
    assigned_object_id: ID | None = strawberry_django.filter_field()
    asn: (
        Annotated['ASNFilter', strawberry.lazy('ipam.graphql.filters')]
        | None
    ) = strawberry_django.filter_field()
    asn_id: ID | None = strawberry_django.filter_field()


@strawberry_django.filter(models.BGPScope, lookups=True)
class BGPScopeFilter(VRFMixin, TenancyFilterMixin, PrimaryModelFilter):
    router: (
        Annotated['BGPRouterFilter', strawberry.lazy('netbox_routing.graphql.filters')]
        | None
    ) = strawberry_django.filter_field()
    router_id: ID | None = strawberry_django.filter_field()


@strawberry_django.filter(models.BGPAddressFamily, lookups=True)
class BGPAddressFamilyFilter(TenancyFilterMixin, PrimaryModelFilter):
    scope: (
        Annotated['BGPScopeFilter', strawberry.lazy('netbox_routing.graphql.filters')]
        | None
    ) = strawberry_django.filter_field()
    scope_id: ID | None = strawberry_django.filter_field()
    address_family: StrFilterLookup | None = strawberry_django.filter_field()


@strawberry_django.filter(models.BGPPeer, lookups=True)
class BGPPeerFilter(TenancyFilterMixin, PrimaryModelFilter):
    name: StrFilterLookup | None = strawberry_django.filter_field()
    scope: (
        Annotated['BGPScopeFilter', strawberry.lazy('netbox_routing.graphql.filters')]
        | None
    ) = strawberry_django.filter_field()
    scope_id: ID | None = strawberry_django.filter_field()
    peer: (
        Annotated['IPAddressFilter', strawberry.lazy('ipam.graphql.filters')]
        | None
    ) = strawberry_django.filter_field()
    peer_id: ID | None = strawberry_django.filter_field()
    source: (
        Annotated['IPAddressFilter', strawberry.lazy('ipam.graphql.filters')]
        | None
    ) = strawberry_django.filter_field()
    source_id: ID | None = strawberry_django.filter_field()
    peer_group: (
        Annotated['BGPPeerTemplateFilter', strawberry.lazy('netbox_routing.graphql.filters')]
        | None
    ) = strawberry_django.filter_field()
    peer_group_id: ID | None = strawberry_django.filter_field()
    remote_as: (
        Annotated['ASNFilter', strawberry.lazy('ipam.graphql.filters')]
        | None
    ) = strawberry_django.filter_field()
    remote_as_id: ID | None = strawberry_django.filter_field()
    local_as: (
        Annotated['ASNFilter', strawberry.lazy('ipam.graphql.filters')]
        | None
    ) = strawberry_django.filter_field()
    local_as_id: ID | None = strawberry_django.filter_field()
    enabled: FilterLookup[bool] | None = strawberry_django.filter_field()
    status: StrFilterLookup | None = strawberry_django.filter_field()


@strawberry_django.filter(models.BGPPeerAddressFamily, lookups=True)
class BGPPeerAddressFamilyFilter(TenancyFilterMixin, PrimaryModelFilter):
    assigned_object_type: (
        Annotated['ContentTypeFilter', strawberry.lazy('core.graphql.filters')]
        | None
    ) = strawberry_django.filter_field()
    assigned_object_id: ID | None = strawberry_django.filter_field()
    address_family: (
        Annotated['BGPAddressFamilyFilter', strawberry.lazy('netbox_routing.graphql.filters')]
        | None
    ) = strawberry_django.filter_field()
    address_family_id: ID | None = strawberry_django.filter_field()
    enabled: FilterLookup[bool] | None = strawberry_django.filter_field()


@strawberry_django.filter(models.BGPSetting, lookups=True)
class BGPSettingFilter(PrimaryModelFilter):
    pass


@strawberry_django.filter(models.BFDProfile, lookups=True)
class BFDProfileFilter(TenancyFilterMixin, PrimaryModelFilter):
    name: StrFilterLookup | None = strawberry_django.filter_field()
