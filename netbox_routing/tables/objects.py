import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable, columns
from netbox_routing.models import PrefixList, PrefixListEntry, RouteMap, RouteMapEntry


class PrefixListTable(NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = PrefixList
        fields = ('pk', 'id', 'name')
        default_columns = ('pk', 'id', 'name')


class PrefixListEntryTable(NetBoxTable):
    prefix_list = tables.Column(
        verbose_name=_('Prefix List'),
        linkify=True
    )
    type = columns.ChoiceFieldColumn()
    class Meta(NetBoxTable.Meta):
        model = PrefixListEntry
        fields = ('pk', 'id', 'prefix_list', 'sequence', 'type', 'prefix', 'le', 'ge')
        default_columns = ('pk', 'id', 'prefix_list', 'sequence', 'type', 'prefix', 'le', 'ge')


class RouteMapTable(NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = RouteMap
        fields = ('pk', 'id', 'name')
        default_columns = ('pk', 'id', 'name')


class RouteMapEntryTable(NetBoxTable):
    route_map = tables.Column(
        verbose_name=_('Route Map'),
        linkify=True
    )
    type = columns.ChoiceFieldColumn()
    class Meta(NetBoxTable.Meta):
        model = RouteMapEntry
        fields = ('pk', 'id', 'route_map', 'sequence', 'type')
        default_columns = ('pk', 'id', 'route_map', 'sequence', 'type')
