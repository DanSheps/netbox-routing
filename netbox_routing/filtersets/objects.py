import django_filters
import netaddr
from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet
from netbox_routing.models import PrefixList, PrefixListEntry, RouteMapEntry, RouteMap


class PrefixListFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = PrefixList
        fields = ()

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name=value)
        )
        return queryset.filter(qs_filter).distinct()


class PrefixListEntryFilterSet(NetBoxModelFilterSet):

    prefix = django_filters.CharFilter(
        method='filter_prefix',
        label='Prefix',
    )

    class Meta:
        model = PrefixListEntry
        fields = ('prefix_list', 'prefix', 'sequence', 'type', 'le', 'ge')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(prefix_list__name__icontains=value) |
            Q(prefix__icontains=value) |
            Q(type=value)
        )
        return queryset.filter(qs_filter).distinct()

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

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
        )
        return queryset.filter(qs_filter).distinct()


class RouteMapEntryFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = RouteMapEntry
        fields = ('route_map', 'sequence', 'type')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(route_map__name__icontains=value) |
            Q(type=value)
        )
        return queryset.filter(qs_filter).distinct()
