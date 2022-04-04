import django_filters
import netaddr

from netbox.filtersets import NetBoxModelFilterSet
from netbox_routing.models import PrefixList, PrefixListEntry, RouteMapEntry, RouteMap


class PrefixListFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = PrefixList
        fields = ()


class PrefixListEntryFilterSet(NetBoxModelFilterSet):

    prefix = django_filters.CharFilter(
        method='filter_prefix',
        label='Prefix',
    )

    class Meta:
        model = PrefixListEntry
        fields = ('prefix_list', 'prefix', 'sequence', 'type', 'le', 'ge')

    def filter_prefix(self, queryset, name, value):
        if not value.strip():
            return queryset
        try:
            query = str(netaddr.IPNetwork(value).cidr)
            return queryset.filter(prefix=query)
        except (netaddr.AddrFormatError, ValueError):
            return queryset.none()


class RouteMapFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = RouteMap
        fields = ()


class RouteMapEntryFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = RouteMapEntry
        fields = ('route_map', 'sequence', 'type')
