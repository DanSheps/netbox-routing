from netbox.tables import NetBoxTable
from netbox_routing.models import PrefixList, PrefixListEntry, RouteMap, RouteMapEntry


class PrefixListTable(NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = PrefixList
        fields = ('pk', 'id', 'name')
        default_columns = ('pk', 'id', 'name')


class PrefixListEntryTable(NetBoxTable):
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
    class Meta(NetBoxTable.Meta):
        model = RouteMapEntry
        fields = ('pk', 'id', 'route_map', 'sequence', 'type')
        default_columns = ('pk', 'id', 'route_map', 'sequence', 'type')
