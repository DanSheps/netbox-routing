from typing import Annotated, List, Union

import strawberry
import strawberry_django

from netbox.graphql.types import PrimaryObjectType
from .filters import *

from netbox_routing import models

__all__ = (
    'StaticRouteType',
    'OSPFInstanceType',
    'OSPFAreaType',
    'OSPFInterfaceType',
    'EIGRPRouterType',
    'EIGRPAddressFamilyType',
    'EIGRPNetworkType',
    'EIGRPInterfaceType',
    'CommunityType',
    'CommunityListType',
    'CommunityListEntryType',
    'ASPathType',
    'ASPathEntryType',
    'PrefixListType',
    'PrefixListEntryType',
    'RouteMapType',
    'RouteMapEntryType',
    'BGPPeerTemplateType',
    'BGPPolicyTemplateType',
    'BGPSessionTemplateType',
    'BGPRouterType',
    'BGPScopeType',
    'BGPAddressFamilyType',
    'BGPPeerType',
    'BGPPeerAddressFamilyType',
)


@strawberry_django.type(models.StaticRoute, fields='__all__', filters=StaticRouteFilter)
class StaticRouteType(PrimaryObjectType):

    name: str
    devices: List[Annotated["DeviceType", strawberry.lazy('dcim.graphql.types')]] | None
    vrf: Annotated["VRFType", strawberry.lazy('ipam.graphql.types')] | None
    prefix: str | None
    next_hop: str | None
    metric: int | None
    permanent: bool | None


@strawberry_django.type(
    models.OSPFInstance, fields='__all__', filters=OSPFInstanceFilter
)
class OSPFInstanceType(PrimaryObjectType):

    name: str
    device: Annotated["DeviceType", strawberry.lazy('dcim.graphql.types')]
    vrf: Annotated["VRFType", strawberry.lazy('ipam.graphql.types')] | None
    router_id: str
    process_id: str


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
    passive: bool | None
    priority: str | None
    bfd: bool | None
    authentication: str | None
    passphrase: str | None


@strawberry_django.type(models.EIGRPRouter, fields='__all__', filters=EIGRPRouterFilter)
class EIGRPRouterType(PrimaryObjectType):

    device: Annotated["DeviceType", strawberry.lazy('dcim.graphql.types')]
    rid: str
    type: str
    name: str
    pid: str


@strawberry_django.type(
    models.EIGRPAddressFamily, fields='__all__', filters=EIGRPAddressFamilyFilter
)
class EIGRPAddressFamilyType(PrimaryObjectType):

    router: Annotated[
        "EIGRPRouterType", strawberry.lazy('netbox_routing.graphql.types')
    ]
    rid: str


@strawberry_django.type(
    models.EIGRPNetwork, fields='__all__', filters=EIGRPNetworkFilter
)
class EIGRPNetworkType(PrimaryObjectType):

    router: Annotated[
        "EIGRPRouterType", strawberry.lazy('netbox_routing.graphql.types')
    ]
    address_family: (
        Annotated[
            "EIGRPAddressFamilyType", strawberry.lazy('netbox_routing.graphql.types')
        ]
        | None
    )
    network: Annotated["PrefixType", strawberry.lazy('ipam.graphql.types')]


@strawberry_django.type(
    models.EIGRPInterface, fields='__all__', filters=EIGRPInterfaceFilter
)
class EIGRPInterfaceType(PrimaryObjectType):

    router: Annotated[
        "EIGRPRouterType", strawberry.lazy('netbox_routing.graphql.types')
    ]
    address_family: (
        Annotated[
            "EIGRPAddressFamilyType", strawberry.lazy('netbox_routing.graphql.types')
        ]
        | None
    )
    interface: Annotated["InterfaceType", strawberry.lazy('dcim.graphql.types')]
    passive: str | None
    bfd: bool | None
    authentication: str | None
    passphrase: str | None


@strawberry_django.type(models.Community, fields='__all__', filters=CommunityFilter)
class CommunityType(PrimaryObjectType):

    community: str
    status: str
    role: Annotated["RoleType", strawberry.lazy('ipam.graphql.types')] | None
    tenant: Annotated["TenantType", strawberry.lazy('tenancy.graphql.types')] | None


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


@strawberry_django.type(models.ASPath, fields='__all__', filters=ASPathFilter)
class ASPathType(PrimaryObjectType):

    name: str


@strawberry_django.type(models.ASPathEntry, fields='__all__', filters=ASPathEntryFilter)
class ASPathEntryType(PrimaryObjectType):

    aspath: Annotated["ASPathType", strawberry.lazy('netbox_routing.graphql.types')]
    action: str
    sequence: int
    pattern: str | None


@strawberry_django.type(models.PrefixList, fields='__all__', filters=PrefixListFilter)
class PrefixListType(PrimaryObjectType):

    name: str


@strawberry_django.type(
    models.PrefixListEntry, fields='__all__', filters=PrefixListEntryFilter
)
class PrefixListEntryType(PrimaryObjectType):

    prefix_list: Annotated[
        "PrefixListType", strawberry.lazy('netbox_routing.graphql.types')
    ]
    action: str
    sequence: int
    prefix: str | None
    le: int | None
    ge: int | None


@strawberry_django.type(models.RouteMap, fields='__all__', filters=RouteMapFilter)
class RouteMapType(PrimaryObjectType):
    name: str


@strawberry_django.type(
    models.RouteMapEntry, fields='__all__', filters=RouteMapEntryFilter
)
class RouteMapEntryType(PrimaryObjectType):

    route_map: Annotated[
        "RouteMapType", strawberry.lazy('netbox_routing.graphql.types')
    ]
    action: str
    sequence: int
    # match: Dict | None
    # set: Dict | None


@strawberry_django.type(
    models.BGPSetting,
    fields='__all__',
    exclude=['assigned_object_type', 'assigned_object_id'],
    filters=BGPSettingFilter,
)
class BGPSettingType(PrimaryObjectType):

    assigned_object_type: (
        Annotated["ContentTypeType", strawberry.lazy('netbox.graphql.types')] | None
    )
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
    value: Annotated["ASNType", strawberry.lazy('ipam.graphql.types')] | None


@strawberry_django.type(
    models.BGPPeerTemplate, fields='__all__', filters=BGPPeerTemplateFilter
)
class BGPPeerTemplateType(PrimaryObjectType):

    name: str
    remote_as: Annotated["ASNType", strawberry.lazy('ipam.graphql.types')] | None
    enabled: bool | None
    tenant: Annotated["TenantType", strawberry.lazy('tenancy.graphql.types')] | None


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
    tenant: Annotated["TenantType", strawberry.lazy('tenancy.graphql.types')] | None


@strawberry_django.type(
    models.BGPSessionTemplate, fields='__all__', filters=BGPSessionTemplateFilter
)
class BGPSessionTemplateType(PrimaryObjectType):

    name: str
    parent: (
        Annotated[
            "BGPSessionTemplateType", strawberry.lazy('netbox_routing.graphql.types')
        ]
        | None
    )
    enabled: bool | None
    remote_as: Annotated["ASNType", strawberry.lazy('ipam.graphql.types')] | None
    local_as: Annotated["ASNType", strawberry.lazy('ipam.graphql.types')] | None
    bfd: bool | None
    password: str | None
    tenant: Annotated["TenantType", strawberry.lazy('tenancy.graphql.types')] | None


@strawberry_django.type(
    models.BGPRouter,
    fields='__all__',
    exclude=['assigned_object_type', 'assigned_object_id'],
    filters=BGPRouterFilter,
)
class BGPRouterType(PrimaryObjectType):

    name: str
    assigned_object_type: (
        Annotated["ContentTypeType", strawberry.lazy('netbox.graphql.types')] | None
    )
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
    settings: (
        List[
            Annotated['BGPSettingType', strawberry.lazy('netbox_routing.graphql.types')]
        ]
        | None
    )
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
    tenant: Annotated["TenantType", strawberry.lazy('tenancy.graphql.types')] | None


@strawberry_django.type(models.BGPScope, fields='__all__', filters=BGPScopeFilter)
class BGPScopeType(PrimaryObjectType):

    name: str
    router: Annotated["BGPRouterType", strawberry.lazy('netbox_routing.graphql.types')]
    vrf: Annotated["VRFType", strawberry.lazy('ipam.graphql.types')] | None
    settings: (
        List[
            Annotated['BGPSettingType', strawberry.lazy('netbox_routing.graphql.types')]
        ]
        | None
    )
    tenant: Annotated["TenantType", strawberry.lazy('tenancy.graphql.types')] | None


@strawberry_django.type(
    models.BGPAddressFamily, fields='__all__', filters=BGPAddressFamilyFilter
)
class BGPAddressFamilyType(PrimaryObjectType):

    name: str
    scope: Annotated["BGPScopeType", strawberry.lazy('netbox_routing.graphql.types')]
    address_family: str | None
    settings: (
        List[
            Annotated['BGPSettingType', strawberry.lazy('netbox_routing.graphql.types')]
        ]
        | None
    )
    tenant: Annotated["TenantType", strawberry.lazy('tenancy.graphql.types')] | None


@strawberry_django.type(models.BGPPeer, fields='__all__', filters=BGPPeerFilter)
class BGPPeerType(PrimaryObjectType):

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
    peer: Annotated["IPAddressType", strawberry.lazy('ipam.graphql.types')]
    source: Annotated["IPAddressType", strawberry.lazy('ipam.graphql.types')] | None
    remote_as: Annotated["ASNType", strawberry.lazy('ipam.graphql.types')] | None
    local_as: Annotated["ASNType", strawberry.lazy('ipam.graphql.types')] | None
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
    settings: (
        List[
            Annotated['BGPSettingType', strawberry.lazy('netbox_routing.graphql.types')]
        ]
        | None
    )
    tenant: Annotated["TenantType", strawberry.lazy('tenancy.graphql.types')] | None


@strawberry_django.type(
    models.BGPPeerAddressFamily,
    fields='__all__',
    exclude=['assigned_object_type', 'assigned_object_id'],
    filters=BGPPeerAddressFamilyFilter,
)
class BGPPeerAddressFamilyType(PrimaryObjectType):

    assigned_object_type: (
        Annotated["ContentTypeType", strawberry.lazy('netbox.graphql.types')] | None
    )
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
    address_families: (
        List[
            Annotated[
                'BGPPeerAddressFamilyType',
                strawberry.lazy('netbox_routing.graphql.types'),
            ]
        ]
        | None
    )
    settings: (
        List[
            Annotated['BGPSettingType', strawberry.lazy('netbox_routing.graphql.types')]
        ]
        | None
    )
    tenant: Annotated["TenantType", strawberry.lazy('tenancy.graphql.types')] | None
