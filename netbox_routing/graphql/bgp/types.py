from typing import Annotated, Union, List

import strawberry
import strawberry_django

from netbox.graphql.types import PrimaryObjectType

from netbox_routing import models
from netbox_routing.graphql.bgp.filters import (
    BGPSettingFilter,
    BGPPeerTemplateFilter,
    BGPPolicyTemplateFilter,
    BGPSessionTemplateFilter,
    BGPRouterFilter,
    BGPScopeFilter,
    BGPAddressFamilyFilter,
    BGPPeerFilter,
    BGPPeerAddressFamilyFilter,
)
from netbox_routing.graphql.objects.types import PrefixListType, RouteMapType

__all__ = (
    'BGPPeerTemplateType',
    'BGPPolicyTemplateType',
    'BGPSessionTemplateType',
    'BGPRouterType',
    'BGPScopeType',
    'BGPAddressFamilyType',
    'BGPPeerType',
    'BGPPeerAddressFamilyType',
)

from netbox_routing.graphql.types_mixin import BGPSettingsMixin


@strawberry_django.type(
    models.BGPSetting,
    fields='__all__',
    exclude=['assigned_object_type', 'assigned_object_id'],
    filters=BGPSettingFilter,
)
class BGPSettingType(PrimaryObjectType):

    assigned_object_type: (
        Annotated["ContentTypeType", strawberry.lazy('netbox.graphql.types')] | None
    )  # noqa: F821
    assigned_object: Union[
        Annotated[
            'BGPPeerTemplateType', strawberry.lazy('netbox_routing.graphql.types')
        ],
        Annotated[
            'BGPPolicyTemplateType', strawberry.lazy('netbox_routing.graphql.types')
        ],
        Annotated[
            'BGPSessionTemplateType', strawberry.lazy('netbox_routing.graphql.types')
        ],
        Annotated['BGPRouterType', strawberry.lazy('netbox_routing.graphql.types')],
        Annotated['BGPScopeType', strawberry.lazy('netbox_routing.graphql.types')],
        Annotated[
            'BGPAddressFamilyType', strawberry.lazy('netbox_routing.graphql.types')
        ],
        Annotated['BGPPeerType', strawberry.lazy('netbox_routing.graphql.types')],
        Annotated[
            'BGPPeerAddressFamilyType', strawberry.lazy('netbox_routing.graphql.types')
        ],
    ]
    key: str
    value: (
        Annotated["ASNType", strawberry.lazy('ipam.graphql.types')] | None
    )  # noqa: F821


@strawberry_django.type(
    models.BGPPeerTemplate, fields='__all__', filters=BGPPeerTemplateFilter
)
class BGPPeerTemplateType(PrimaryObjectType):

    name: str
    remote_as: (
        Annotated["ASNType", strawberry.lazy('ipam.graphql.types')] | None
    )  # noqa: F821
    enabled: bool | None
    tenant: (
        Annotated["TenantType", strawberry.lazy('tenancy.graphql.types')] | None
    )  # noqa: F821


@strawberry_django.type(
    models.BGPPolicyTemplate, fields='__all__', filters=BGPPolicyTemplateFilter
)
class BGPPolicyTemplateType(PrimaryObjectType):

    name: str
    parents: (
        List[
            Annotated[
                "BGPPolicyTemplateType", strawberry.lazy('netbox_routing.graphql.types')
            ]
        ]
        | None
    )
    enabled: bool | None
    prefixlist_in: (
        Annotated["PrefixListType", strawberry.lazy('netbox_routing.graphql.types')]
        | None
    )
    prefixlist_out: (
        Annotated["PrefixListType", strawberry.lazy('netbox_routing.graphql.types')]
        | None
    )
    routemap_in: (
        Annotated["RouteMapType", strawberry.lazy('netbox_routing.graphql.types')]
        | None
    )
    routemap_out: (
        Annotated["RouteMapType", strawberry.lazy('netbox_routing.graphql.types')]
        | None
    )
    tenant: (
        Annotated["TenantType", strawberry.lazy('tenancy.graphql.types')] | None
    )  # noqa: F821


@strawberry_django.type(
    models.BGPSessionTemplate, fields='__all__', filters=BGPSessionTemplateFilter
)
class BGPSessionTemplateType(BGPSettingsMixin, PrimaryObjectType):

    name: str
    parent: (
        Annotated[
            "BGPSessionTemplateType", strawberry.lazy('netbox_routing.graphql.types')
        ]
        | None
    )
    enabled: bool | None
    remote_as: (
        Annotated["ASNType", strawberry.lazy('ipam.graphql.types')] | None
    )  # noqa: F821
    local_as: (
        Annotated["ASNType", strawberry.lazy('ipam.graphql.types')] | None
    )  # noqa: F821
    bfd: bool | None
    password: str | None
    tenant: Annotated["TenantType", strawberry.lazy('tenancy.graphql.types')] | None


@strawberry_django.type(
    models.BGPRouter,
    fields='__all__',
    exclude=['assigned_object_type', 'assigned_object_id'],
    filters=BGPRouterFilter,
    select_related=[
        'asn',
    ],
)
class BGPRouterType(BGPSettingsMixin, PrimaryObjectType):

    name: str
    assigned_object_type: (
        Annotated["ContentTypeType", strawberry.lazy('netbox.graphql.types')] | None
    )  # noqa: F821
    assigned_object: Union[
        Annotated['RegionType', strawberry.lazy('dcim.graphql.types')],
        Annotated['SiteType', strawberry.lazy('dcim.graphql.types')],
        Annotated['SiteGroupType', strawberry.lazy('dcim.graphql.types')],
        Annotated['LocationType', strawberry.lazy('dcim.graphql.types')],
        Annotated['DeviceType', strawberry.lazy('dcim.graphql.types')],
        Annotated['ClusterType', strawberry.lazy('virtualization.graphql.types')],
        Annotated[
            'VirtualMachineType', strawberry.lazy('virtualization.graphql.types')
        ],
    ]
    asn: Annotated["ASNType", strawberry.lazy('ipam.graphql.types')]
    peer_templates: (
        List[
            Annotated[
                'BGPPeerTemplateType', strawberry.lazy('netbox_routing.graphql.types')
            ]
        ]
        | None
    )
    policy_templates: (
        List[
            Annotated[
                'BGPPolicyTemplateType', strawberry.lazy('netbox_routing.graphql.types')
            ]
        ]
        | None
    )
    session_templates: (
        List[
            Annotated[
                'BGPSessionTemplateType',
                strawberry.lazy('netbox_routing.graphql.types'),
            ]
        ]
        | None
    )
    tenant: (
        Annotated["TenantType", strawberry.lazy('tenancy.graphql.types')] | None
    )  # noqa: F821


@strawberry_django.type(
    models.BGPScope,
    fields='__all__',
    filters=BGPScopeFilter,
    select_related=[
        'router',
        'vrf',
    ],
)
class BGPScopeType(BGPSettingsMixin, PrimaryObjectType):

    router: Annotated["BGPRouterType", strawberry.lazy('netbox_routing.graphql.types')]
    vrf: (
        Annotated["VRFType", strawberry.lazy('ipam.graphql.types')] | None
    )  # noqa: F821
    tenant: (
        Annotated["TenantType", strawberry.lazy('tenancy.graphql.types')] | None
    )  # noqa: F821


@strawberry_django.type(
    models.BGPAddressFamily,
    fields='__all__',
    filters=BGPAddressFamilyFilter,
    select_related=[
        'scope',
    ],
)
class BGPAddressFamilyType(BGPSettingsMixin, PrimaryObjectType):

    scope: Annotated["BGPScopeType", strawberry.lazy('netbox_routing.graphql.types')]
    address_family: str | None
    tenant: (
        Annotated["TenantType", strawberry.lazy('tenancy.graphql.types')] | None
    )  # noqa: F821


@strawberry_django.type(
    models.BGPPeer,
    fields='__all__',
    filters=BGPPeerFilter,
    select_related=['scope', 'peer', 'remote_as'],
)
class BGPPeerType(BGPSettingsMixin, PrimaryObjectType):

    name: str
    enabled: bool | None
    scope: (
        Annotated["BGPScopeType", strawberry.lazy('netbox_routing.graphql.types')]
        | None
    )
    peer_group: (
        Annotated[
            "BGPPeerTemplateType", strawberry.lazy('netbox_routing.graphql.types')
        ]
        | None
    )
    peer_session: (
        Annotated[
            "BGPSessionTemplateType", strawberry.lazy('netbox_routing.graphql.types')
        ]
        | None
    )
    peer: Annotated[
        "IPAddressType", strawberry.lazy('ipam.graphql.types')
    ]  # noqa: F821
    source: (
        Annotated["IPAddressType", strawberry.lazy('ipam.graphql.types')] | None
    )  # noqa: F821
    remote_as: (
        Annotated["ASNType", strawberry.lazy('ipam.graphql.types')] | None
    )  # noqa: F821
    local_as: (
        Annotated["ASNType", strawberry.lazy('ipam.graphql.types')] | None
    )  # noqa: F821
    bfd: bool | None
    password: str | None
    address_families: (
        List[
            Annotated[
                'BGPPeerAddressFamilyType',
                strawberry.lazy('netbox_routing.graphql.types'),
            ]
        ]
        | None
    )
    tenant: (
        Annotated["TenantType", strawberry.lazy('tenancy.graphql.types')] | None
    )  # noqa: F821


@strawberry_django.type(
    models.BGPPeerAddressFamily,
    fields='__all__',
    exclude=['assigned_object_type', 'assigned_object_id'],
    filters=BGPPeerAddressFamilyFilter,
    select_related=[
        'assigned_object_type',
        'address_family',
    ],
)
class BGPPeerAddressFamilyType(BGPSettingsMixin, PrimaryObjectType):

    assigned_object_type: (
        Annotated["ContentTypeType", strawberry.lazy('netbox.graphql.types')] | None
    )  # noqa: F821
    assigned_object: (
        Union[
            Annotated["BGPPeerType", strawberry.lazy('netbox_routing.graphql.types')],
            Annotated[
                "BGPPeerTemplateType", strawberry.lazy('netbox_routing.graphql.types')
            ],
        ]
        | None
    )
    peer_policy: (
        Annotated[
            "BGPPolicyTemplateType", strawberry.lazy('netbox_routing.graphql.types')
        ]
        | None
    )
    enabled: bool | None
    prefixlist_in: (
        Annotated['PrefixListType', strawberry.lazy('netbox_routing.graphql.types')]
        | None
    )
    prefixlist_out: (
        Annotated['PrefixListType', strawberry.lazy('netbox_routing.graphql.types')]
        | None
    )
    routemap_in: (
        Annotated['RouteMapType', strawberry.lazy('netbox_routing.graphql.types')]
        | None
    )
    routemap_out: (
        Annotated['RouteMapType', strawberry.lazy('netbox_routing.graphql.types')]
        | None
    )
    address_family: (
        Annotated[
            'BGPAddressFamilyType',
            strawberry.lazy('netbox_routing.graphql.types'),
        ]
        | None
    )
    tenant: (
        Annotated["TenantType", strawberry.lazy('tenancy.graphql.types')] | None
    )  # noqa: F821
