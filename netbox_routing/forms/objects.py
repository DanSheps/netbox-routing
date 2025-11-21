from netbox.forms import NetBoxModelForm
from netbox_routing.models import RoutingPrefixList, PrefixListEntry, RouteMap, RouteMapEntry


class PrefixListForm(NetBoxModelForm):

    class Meta:
        model = RoutingPrefixList
        fields = (
            'name',
            'description',
            'comments',
        )


class PrefixListEntryForm(NetBoxModelForm):

    class Meta:
        model = PrefixListEntry
        fields = (
            'prefix_list',
            'sequence',
            'type',
            'prefix',
            'le',
            'ge',
            'description',
            'comments',
        )


class RouteMapForm(NetBoxModelForm):

    class Meta:
        model = RouteMap
        fields = (
            'name',
            'description',
            'comments',
        )


class RouteMapEntryForm(NetBoxModelForm):

    class Meta:
        model = RouteMapEntry
        fields = (
            'route_map',
            'sequence',
            'type',
            'description',
            'comments',
        )
