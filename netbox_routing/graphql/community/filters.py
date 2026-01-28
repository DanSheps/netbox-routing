from typing import Annotated

import strawberry
import strawberry_django
from strawberry import ID

from ipam.graphql.filters import RoleFilter
from netbox.graphql.filters import PrimaryModelFilter
from netbox_routing import models
from tenancy.graphql.filter_mixins import TenancyFilterMixin

__all__ = (
    'CommunityFilter',
    'CommunityListFilter',
    'CommunityListEntryFilter',
)


@strawberry_django.filter(models.Community, lookups=True)
class CommunityFilter(TenancyFilterMixin, PrimaryModelFilter):
    role: (
        Annotated[
            'RoleFilter',
            strawberry.lazy('ipam.graphql.filters'),
        ]
        | None
    ) = strawberry_django.filter_field()
    role_id: ID | None = strawberry_django.filter_field()


@strawberry_django.filter(models.CommunityList, lookups=True)
class CommunityListFilter(TenancyFilterMixin, PrimaryModelFilter):
    pass


@strawberry_django.filter(models.CommunityListEntry, lookups=True)
class CommunityListEntryFilter(PrimaryModelFilter):
    community_list: (
        Annotated[
            'CommunityListFilter',
            strawberry.lazy('netbox_routing.graphql.filters'),
        ]
        | None
    ) = strawberry_django.filter_field()
    community_list_id: ID | None = strawberry_django.filter_field()

    community: (
        Annotated[
            'CommunityFilter',
            strawberry.lazy('netbox_routing.graphql.filters'),
        ]
        | None
    ) = strawberry_django.filter_field()
    community_id: ID | None = strawberry_django.filter_field()
