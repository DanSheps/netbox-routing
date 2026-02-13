import django_tables2 as tables
from django.utils.translation import gettext as _

from netbox.tables import NetBoxTable, columns, ManyToManyColumn
from netbox_routing.models.bgp import *

__all__ = (
    'BGPSettingTable',
    'BGPRouterTable',
    'BGPScopeTable',
    'BGPAddressFamilyTable',
    'BGPPeerTable',
    'BGPPeerAddressFamilyTable',
    'BGPPeerTemplateTable',
    'BGPPolicyTemplateTable',
    'BGPSessionTemplateTable',
)

from tenancy.tables import TenancyColumnsMixin


class BGPSettingTable(NetBoxTable):
    assigned_object_type = columns.ContentTypeColumn(verbose_name=_('Object Type'))
    assigned_object = tables.Column(
        linkify=True, orderable=False, verbose_name=_('Object')
    )

    class Meta(NetBoxTable.Meta):
        model = BGPSetting
        fields = ('pk', 'id', 'assigned_object_type', 'assigned_object', 'key', 'value')
        default_columns = (
            'pk',
            'id',
            'assigned_object_type',
            'assigned_object',
            'key',
            'value',
        )


class BGPPeerTemplateTable(TenancyColumnsMixin, NetBoxTable):
    name = tables.Column(
        verbose_name=_('Name'),
        linkify=True,
    )

    class Meta(NetBoxTable.Meta):
        model = BGPPeerTemplate
        fields = (
            'pk',
            'id',
            'name',
        )
        default_columns = ('pk', 'id', 'name')


class BGPPolicyTemplateTable(TenancyColumnsMixin, NetBoxTable):
    name = tables.Column(
        verbose_name=_('Name'),
        linkify=True,
    )
    parents = ManyToManyColumn(
        verbose_name=_('Parents'),
        linkify_item=True,
    )

    class Meta(NetBoxTable.Meta):
        model = BGPPolicyTemplate
        fields = (
            'pk',
            'id',
            'name',
            'parents',
            'enabled',
            'prefixlist_out',
            'prefixlist_in',
            'routemap_out',
            'routemap_in',
            'tenant',
        )
        default_columns = ('pk', 'id', 'name')


class BGPSessionTemplateTable(TenancyColumnsMixin, NetBoxTable):
    name = tables.Column(
        verbose_name=_('Name'),
        linkify=True,
    )
    parent = tables.Column(
        verbose_name=_('Parent'),
        linkify=True,
    )
    asn = tables.Column(
        verbose_name=_('Parent'),
        linkify=True,
    )

    class Meta(NetBoxTable.Meta):
        model = BGPSessionTemplate
        fields = (
            'pk',
            'id',
            'name',
            'parent',
            'enabled',
            'local_as',
            'remote_as',
            'bfd',
            'password',
            'tenant',
        )
        default_columns = ('pk', 'id', 'name')


class BGPRouterTable(TenancyColumnsMixin, NetBoxTable):
    name = tables.Column(linkify=True, verbose_name=_('Name'))
    assigned_object_type = columns.ContentTypeColumn(verbose_name=_('Object Type'))
    assigned_object = tables.Column(
        linkify=True, orderable=False, verbose_name=_('Object')
    )

    class Meta(NetBoxTable.Meta):
        model = BGPRouter
        fields = (
            'pk',
            'id',
            'name',
            'assigned_object_type',
            'assigned_object',
            'asn',
            'tenant_group',
            'tenant',
        )
        default_columns = ('pk', 'id', 'name', 'assigned_object', 'asn')


class BGPScopeTable(TenancyColumnsMixin, NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = BGPScope
        fields = (
            'pk',
            'id',
            'router',
            'vrf',
            'tenant_group',
            'tenant',
        )
        default_columns = ('pk', 'id', 'router', 'vrf')


class BGPAddressFamilyTable(TenancyColumnsMixin, NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = BGPAddressFamily
        fields = (
            'pk',
            'id',
            'scope',
            'address_family',
            'tenant_group',
            'tenant',
        )
        default_columns = ('pk', 'id', 'scope', 'address_family')


class BGPPeerTable(TenancyColumnsMixin, NetBoxTable):
    name = tables.Column(linkify=True, verbose_name=_('Name'))
    scope = tables.Column(linkify=True, verbose_name=_('Scope'))
    peer = tables.Column(linkify=True, verbose_name=_('Scope'))
    source = tables.Column(linkify=True, verbose_name=_('Scope'))
    peer_group = tables.Column(linkify=True, verbose_name=_('Scope'))
    peer_session = tables.Column(linkify=True, verbose_name=_('Scope'))
    remote_as = tables.Column(linkify=True, verbose_name=_('Scope'))
    local_as = tables.Column(linkify=True, verbose_name=_('Scope'))

    class Meta(NetBoxTable.Meta):
        model = BGPPeer
        fields = (
            'pk',
            'id',
            'name',
            'scope',
            'peer',
            'source',
            'peer_group',
            'peer_session',
            'remote_as',
            'status',
            'local_as',
            'bfd',
            'password',
            'tenant_group',
            'tenant',
            'address_families',
        )
        default_columns = (
            'pk',
            'id',
            'name',
            'scope',
            'peer',
            'remote_as',
            'enabled',
            'status',
        )


class BGPPeerAddressFamilyTable(TenancyColumnsMixin, NetBoxTable):
    assigned_object_type = columns.ContentTypeColumn(verbose_name=_('Object Type'))
    assigned_object = tables.Column(
        linkify=True, orderable=False, verbose_name=_('Object')
    )
    address_family = tables.Column(
        linkify=True,
        verbose_name=_('Address Family'),
    )
    peer_policy = tables.Column(
        linkify=True,
        verbose_name=_('Peer Policy'),
    )
    prefixlist_in = tables.Column(
        linkify=True,
        verbose_name=_('Prefix List (in)'),
    )
    prefixlist_out = tables.Column(
        linkify=True,
        verbose_name=_('Prefix List (out)'),
    )
    routemap_in = tables.Column(
        linkify=True,
        verbose_name=_('Route Map (in)'),
    )
    routemap_out = tables.Column(
        linkify=True,
        verbose_name=_('Route Map (out)'),
    )

    class Meta(NetBoxTable.Meta):
        model = BGPPeerAddressFamily
        fields = (
            'pk',
            'id',
            'assigned_object_type',
            'assigned_object',
            'address_family',
            'peer_policy',
            'enabled',
            'prefixlist_in',
            'prefixlist_out',
            'routemap_in',
            'routemap_out',
        )
        default_columns = (
            'pk',
            'id',
            'assigned_object_type',
            'assigned_object',
            'address_family',
            'enabled',
        )
