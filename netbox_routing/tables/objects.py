import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable, columns
from netbox_routing.models.objects import *


class PrefixListTable(NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = PrefixList
        fields = ('pk', 'id', 'name')
        default_columns = ('pk', 'id', 'name')


class PrefixListEntryTable(NetBoxTable):
    prefix_list = tables.Column(verbose_name=_('Prefix List'), linkify=True)
    action = columns.ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = PrefixListEntry
        fields = ('pk', 'id', 'prefix_list', 'sequence', 'action', 'prefix', 'le', 'ge')
        default_columns = (
            'pk',
            'id',
            'prefix_list',
            'sequence',
            'action',
            'prefix',
            'le',
            'ge',
        )


class RouteMapTable(NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = RouteMap
        fields = ('pk', 'id', 'name')
        default_columns = ('pk', 'id', 'name')


class RouteMapEntryTable(NetBoxTable):
    route_map = tables.Column(verbose_name=_('Route Map'), linkify=True)
    action = columns.ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = RouteMapEntry
        fields = ('pk', 'id', 'route_map', 'sequence', 'action')
        default_columns = ('pk', 'id', 'route_map', 'sequence', 'action')


class ASPathTable(NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = ASPath
        fields = ('pk', 'id', 'name')
        default_columns = ('pk', 'id', 'name')


class ASPathEntryTable(NetBoxTable):
    aspath = tables.Column(verbose_name=_('AS Path'), linkify=True)
    action = columns.ChoiceFieldColumn()
    asn = tables.Column(verbose_name=_('ASN'), linkify=True)

    class Meta(NetBoxTable.Meta):
        model = ASPathEntry
        fields = (
            'pk',
            'id',
            'aspath',
            'sequence',
            'action',
            'asn',
        )
        default_columns = (
            'pk',
            'id',
            'aspath',
            'sequence',
            'action',
            'asn',
        )
