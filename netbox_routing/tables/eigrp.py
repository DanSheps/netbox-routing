import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox_routing.models import EIGRPAddressFamily, EIGRPRouter, EIGRPInterface


__all__ = (
    'EIGRPAddressFamilyTable',
    'EIGRPRouterTable',
    'EIGRPNetworkTable',
    'EIGRPInterfaceTable',
)


class EIGRPRouterTable(NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = EIGRPRouter
        fields = ('pk', 'id', 'name', 'mode', 'pid', 'rid', 'device')
        default_columns = ('pk', 'id', 'name', 'device')


class EIGRPAddressFamilyTable(NetBoxTable):
    router = tables.Column(
        verbose_name=_('Router'),
        linkify=True
    )
    class Meta(NetBoxTable.Meta):
        model = EIGRPAddressFamily
        fields = ('pk', 'id', 'family', 'router')
        default_columns = ('pk', 'id', 'family', 'router')


class EIGRPNetworkTable(NetBoxTable):
    router = tables.Column(
        verbose_name=_('Router'),
        linkify=True
    )
    address_family = tables.Column(
        verbose_name=_('Address Family'),
        linkify=True
    )
    network = tables.Column(
        verbose_name=_('Network'),
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = EIGRPInterface
        fields = ('pk', 'id', 'router', 'address_family', 'network')
        default_columns = ('pk', 'id', 'router', 'address_family', 'network')


class EIGRPInterfaceTable(NetBoxTable):
    router = tables.Column(
        verbose_name=_('Router'),
        linkify=True
    )
    address_family = tables.Column(
        verbose_name=_('Address Family'),
        linkify=True
    )
    interface = tables.Column(
        verbose_name=_('Interface'),
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = EIGRPInterface
        fields = ('pk', 'id', 'router', 'address_family', 'interface', 'passive', 'bfd', 'authentication', 'passphrase')
        default_columns = ('pk', 'id', 'router', 'address_family', 'interface')
