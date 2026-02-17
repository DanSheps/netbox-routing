from typing import Annotated

import strawberry
import strawberry_django

from netbox.graphql.types import PrimaryObjectType

from netbox_routing import models
from netbox_routing.graphql.community.filters import (
    CommunityFilter,
    CommunityListFilter,
    CommunityListEntryFilter,
)

__all__ = (
    'CommunityType',
    'CommunityListType',
    'CommunityListEntryType',
)


@strawberry_django.type(models.Community, fields='__all__', filters=CommunityFilter)
class CommunityType(PrimaryObjectType):

    community: str
    status: str
    role: (
        Annotated["RoleType", strawberry.lazy('ipam.graphql.types')] | None
    )  # noqa: F821
    tenant: (
        Annotated["TenantType", strawberry.lazy('tenancy.graphql.types')] | None
    )  # noqa: F821


@strawberry_django.type(
    models.CommunityList, fields='__all__', filters=CommunityListFilter
)
class CommunityListType(PrimaryObjectType):

    name: str
    tenant: Annotated["TenantType", strawberry.lazy('tenancy.graphql.types')] | None


@strawberry_django.type(
    models.CommunityListEntry, fields='__all__', filters=CommunityListEntryFilter
)
class CommunityListEntryType(PrimaryObjectType):

    community_list: Annotated[
        "CommunityListType", strawberry.lazy('netbox_routing.graphql.types')
    ]
    community: Annotated[
        "CommunityType", strawberry.lazy('netbox_routing.graphql.types')
    ]
