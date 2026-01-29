import strawberry_django

from netbox.graphql.filters import PrimaryModelFilter
from netbox_routing import models

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
)


@strawberry_django.filter(models.BGPPeerTemplate, lookups=True)
class BGPPeerTemplateFilter(PrimaryModelFilter):
    pass


@strawberry_django.filter(models.BGPPolicyTemplate, lookups=True)
class BGPPolicyTemplateFilter(PrimaryModelFilter):
    pass


@strawberry_django.filter(models.BGPSessionTemplate, lookups=True)
class BGPSessionTemplateFilter(PrimaryModelFilter):
    pass


@strawberry_django.filter(models.BGPRouter, lookups=True)
class BGPRouterFilter(PrimaryModelFilter):
    pass


@strawberry_django.filter(models.BGPScope, lookups=True)
class BGPScopeFilter(PrimaryModelFilter):
    pass


@strawberry_django.filter(models.BGPAddressFamily, lookups=True)
class BGPAddressFamilyFilter(PrimaryModelFilter):
    pass


@strawberry_django.filter(models.BGPPeer, lookups=True)
class BGPPeerFilter(PrimaryModelFilter):
    pass


@strawberry_django.filter(models.BGPPeerAddressFamily, lookups=True)
class BGPPeerAddressFamilyFilter(PrimaryModelFilter):
    pass


@strawberry_django.filter(models.BGPSetting, lookups=True)
class BGPSettingFilter(PrimaryModelFilter):
    pass
