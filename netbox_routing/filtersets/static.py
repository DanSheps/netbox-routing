import django_filters
import netaddr
from django.db.models import Q

from dcim.models import Device
from ipam.models import VRF
from netbox.filtersets import NetBoxModelFilterSet
from netbox_routing.models import StaticRoute


class StaticRouteFilterSet(NetBoxModelFilterSet):

    device = django_filters.ModelMultipleChoiceFilter(
        field_name='devices__name',
        queryset=Device.objects.all(),
        to_field_name='name',
        label='Device (name)',
    )
    device_id = django_filters.ModelMultipleChoiceFilter(
        field_name='devices',
        queryset=Device.objects.all(),
        label='Device (ID)',
    )
    vrf = django_filters.ModelMultipleChoiceFilter(
        field_name='vrf__name',
        queryset=VRF.objects.all(),
        to_field_name='name',
        label='VRF (name)',
    )
    vrf_id = django_filters.ModelMultipleChoiceFilter(
        field_name='vrf',
        queryset=VRF.objects.all(),
        label='VRF (ID)',
    )

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
        fields = ('name', 'devices', 'device', 'device_id', 'vrf', 'vrf_id', 'prefix', 'metric', 'next_hop')

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
            return queryset.filter(**{f'{name}': query})
        except (netaddr.AddrFormatError, ValueError):
            return queryset.none()

    def filter_address(self, queryset, name, value):
        if not value.strip():
            return queryset
        try:
            query = netaddr.IPAddress(value)
            return queryset.filter(**{f'{name}': query})
        except (netaddr.AddrFormatError, ValueError) as e:
            return queryset.none()
