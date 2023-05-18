import django_filters
import netaddr
from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet
from netbox_routing.models import StaticRoute


class StaticRouteFilterSet(NetBoxModelFilterSet):

    prefix = django_filters.CharFilter(
        method='filter_prefix',
        label='Prefix',
    )

    next_hop = django_filters.CharFilter(
        method='filter_address',
        label='Prefix',
    )

    class Meta:
        model = StaticRoute
        fields = ('vrf', 'prefix', 'devices', 'metric', 'next_hop')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(devices__name__icontains=value) |
            Q(vrf__name__icontains=value) |
            Q(vrf__rd__icontains=value) |
            Q(prefix__icontains=value) |
            Q(next_hop__icontains=value) |
            Q(name__icontains=value)
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

    def filter_address(self, queryset, name, value):
        if not value.strip():
            return queryset
        try:
            query = str(netaddr.IPAddress(value))
            return queryset.filter(prefix=query)
        except (netaddr.AddrFormatError, ValueError):
            return queryset.none()
