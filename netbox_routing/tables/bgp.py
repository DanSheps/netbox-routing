import django_tables2 as tables
from django.utils.translation import gettext as _

from netbox.tables import NetBoxTable, columns
from netbox_routing.models.bgp import *

__all__ = (
    'BGPSettingTable',
    'BGPRouterTable',
    'BGPScopeTable',
    'BGPAddressFamilyTable',
    'BGPPeerTable',
    'BGPPeerAddressFamilyTable',
)


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


class BGPRouterTable(NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = BGPRouter
        fields = ('pk', 'id', 'device', 'asn')
        default_columns = ('pk', 'id', 'device', 'asn')


class BGPScopeTable(NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = BGPScope
        fields = ('pk', 'id', 'router', 'vrf')
        default_columns = ('pk', 'id', 'router', 'vrf')


class BGPAddressFamilyTable(NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = BGPAddressFamily
        fields = ('pk', 'id', 'scope', 'address_family')
        default_columns = ('pk', 'id', 'scope', 'address_family')


class BGPPeerTable(NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = BGPPeer
        fields = (
            'pk',
            'id',
            'scope',
            'peer',
            'peer_group',
            'peer_session',
            'remote_as',
            'enabled',
            'local_as',
            'bfd',
            'password',
            'tenant',
            'address_families',
        )
        default_columns = (
            'pk',
            'id',
            'scope',
            'peer',
            'remote_as',
            'enabled',
        )


class BGPPeerAddressFamilyTable(NetBoxTable):
    assigned_object_type = columns.ContentTypeColumn(verbose_name=_('Object Type'))
    assigned_object = tables.Column(
        linkify=True, orderable=False, verbose_name=_('Object')
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
