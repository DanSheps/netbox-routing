import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox_routing.models.bgp import *

__all__ = (
    'BGPRouterTable',
    'BGPScopeTable',
    'BGPSessionTemplateTable',
    'BGPPolicyTemplateTable',
    'BGPPeerTemplateTable',
    'BGPAddressFamilyTable',
    'BGPPeerTable',
    'BGPPeerAddressFamilyTable',
    'BGPSettingTable',
)



class BGPRouterTable(NetBoxTable):
    device = tables.Column(
        verbose_name=_('Device'),
        linkify=True
    )
    asn = tables.Column(
        verbose_name=_('ASN'),
        linkify=True
    )
    tenant = tables.Column(
        verbose_name=_('Tenant'),
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = BGPRouter
        fields = ('pk', 'id', 'device', 'asn', 'tenant')
        default_columns = ('pk', 'id', 'device', 'asn')


class BGPScopeTable(NetBoxTable):
    router = tables.Column(
        verbose_name=_('Router'),
        linkify=True
    )
    vrf = tables.Column(
        verbose_name=_('VRF'),
        linkify=True
    )
    tenant = tables.Column(
        verbose_name=_('Tenant'),
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = BGPScope
        fields = ('pk', 'id', 'router', 'vrf', 'tenant')
        default_columns = ('pk', 'id', 'router', 'vrf')


class BGPPeerTemplateTable(NetBoxTable):
    remote_as = tables.Column(
        verbose_name=_('Remote AS'),
        linkify=True
    )
    tenant = tables.Column(
        verbose_name=_('Tenant'),
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = BGPPeerTemplate
        fields = ('pk', 'id', 'name', 'remote_as', 'enabled', 'tenant')
        default_columns = ('pk', 'id', 'name', 'remote_as')


class BGPAddressFamilyTable(NetBoxTable):
    address_family = tables.Column(
        verbose_name=_('Peer'),
        linkify=True
    )
    scope = tables.Column(
        verbose_name=_('Scope'),
        linkify=True
    )
    tenant = tables.Column(
        verbose_name=_('Tenant'),
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = BGPAddressFamily
        fields = ('pk', 'id', 'scope', 'address_family', 'tenant', )
        default_columns = ('pk', 'id', 'scope', 'address_family')


class BGPSessionTemplateTable(NetBoxTable):
    remote = tables.Column(
        verbose_name=_('Router'),
        linkify=True
    )
    parent = tables.Column(
        verbose_name=_('Parent'),
        linkify=True
    )
    tenant = tables.Column(
        verbose_name=_('Tenant'),
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = BGPSessionTemplate
        fields = ('pk', 'id', 'router', 'parent', 'name', 'enabled', 'asn',  'bfd', 'password', 'tenant', )
        default_columns = ('pk', 'id', 'router', 'parent', 'name', )


class BGPPolicyTemplateTable(NetBoxTable):
    router = tables.Column(
        verbose_name=_('Router'),
        linkify=True
    )
    tenant = tables.Column(
        verbose_name=_('Tenant'),
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = BGPPolicyTemplate
        fields = ('pk', 'id', 'name', 'router', 'enabled', 'tenant', )
        default_columns = ('pk', 'id', 'name', 'router',)


class BGPPeerTable(NetBoxTable):
    peer = tables.Column(
        verbose_name=_('Peer'),
        linkify=True
    )
    scope = tables.Column(
        verbose_name=_('Scope'),
        linkify=True
    )
    remote_as = tables.Column(
        verbose_name=_('Remote AS'),
        linkify=True
    )
    local_as = tables.Column(
        verbose_name=_('Local AS'),
        linkify=True
    )
    tenant = tables.Column(
        verbose_name=_('Tenant'),
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = BGPPeer
        fields = ('pk', 'id', 'peer', 'scope', 'remote_as', 'local_as', 'enabled', 'bfd', 'password', 'tenant', )
        default_columns = ('pk', 'id', 'peer', 'scope', 'remote_as', )


class BGPPeerAddressFamilyTable(NetBoxTable):
    assigned_object = tables.Column(
        verbose_name=_('Peer'),
        linkify=True
    )
    tenant = tables.Column(
        verbose_name=_('Tenant'),
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = BGPPeer
        fields = ('pk', 'id', 'peer', 'scope', 'remote_as', 'local_as', 'enabled', 'bfd', 'password', 'tenant', )
        default_columns = ('pk', 'id', 'peer', 'scope', 'remote_as', )


class BGPSettingTable(NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = BGPSetting
        fields = ('pk', 'id', 'assigned_object', 'key', 'value')
        default_columns = ('pk', 'id', 'assigned_object', 'key', 'value')
