from netbox.forms import NetBoxModelForm
from netbox_routing.models import PrefixList, PrefixListEntry, RouteMap, RouteMapEntry


class PrefixListForm(NetBoxModelForm):

    class Meta:
        model = PrefixList
        fields = ('name',)


class PrefixListEntryForm(NetBoxModelForm):

    class Meta:
        model = PrefixListEntry
        fields = ('prefix_list', 'sequence', 'type', 'prefix', 'le', 'ge')


class RouteMapForm(NetBoxModelForm):

    class Meta:
        model = RouteMap
        fields = ('name',)


class RouteMapEntryForm(NetBoxModelForm):

    class Meta:
        model = RouteMapEntry
        fields = ('route_map', 'sequence', 'type')
