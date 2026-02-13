import django_filters
import netaddr
from django.db.models import Q
from django.utils.translation import gettext as _

from netbox.filtersets import NetBoxModelFilterSet
from utilities.filtersets import register_filterset

from netbox_routing.models.objects import *

__all__ = (
    'PrefixListFilterSet',
    'PrefixListEntryFilterSet',
    'RouteMapFilterSet',
    'RouteMapEntryFilterSet',
    'ASPathFilterSet',
    'ASPathEntryFilterSet',
)


@register_filterset
class PrefixListFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = PrefixList
        fields = ('family',)

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value)
        return queryset.filter(qs_filter).distinct()


class PrefixListEntryFilterSet(NetBoxModelFilterSet):
    prefix_list_id = django_filters.ModelMultipleChoiceFilter(
        field_name='prefix_list',
        queryset=PrefixList.objects.all(),
        label=_('Prefix List (ID)'),
    )
    prefix_list = django_filters.ModelMultipleChoiceFilter(
        field_name='prefix_list__name',
        queryset=PrefixList.objects.all(),
        to_field_name='name',
        label=_('Prefix List (Name)'),
    )
    prefix = django_filters.CharFilter(
        method='filter_prefix',
        label='Prefix',
    )

    class Meta:
        model = PrefixListEntry
        fields = (
            'prefix_list_id',
            'prefix_list',
            'prefix',
            'sequence',
            'action',
            'le',
            'ge',
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(prefix_list__name__icontains=value)
        qs_filter |= Q(prefix__icontains=value)

        return queryset.filter(qs_filter).distinct()

    def filter_prefix(self, queryset, name, value):
        if not value.strip():
            return queryset
        try:
            query = str(netaddr.IPNetwork(value).cidr)
            return queryset.filter(prefix=query)
        except (netaddr.AddrFormatError, ValueError):
            return queryset.none()


@register_filterset
class RouteMapFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = RouteMap
        fields = ()

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value)
        return queryset.filter(qs_filter).distinct()


@register_filterset
class RouteMapEntryFilterSet(NetBoxModelFilterSet):
    route_map_id = django_filters.ModelMultipleChoiceFilter(
        field_name='route_map',
        queryset=RouteMap.objects.all(),
        label=_('Route Map (ID)'),
    )
    route_map = django_filters.ModelMultipleChoiceFilter(
        field_name='route_map__name',
        queryset=RouteMap.objects.all(),
        to_field_name='name',
        label=_('Route Map (Name)'),
    )

    class Meta:
        model = RouteMapEntry
        fields = ('route_map_id', 'route_map', 'sequence', 'action')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(route_map__name__icontains=value)
        qs_filter |= Q(match__icontains=value)
        qs_filter |= Q(set__icontains=value)
        return queryset.filter(qs_filter).distinct()


class ASPathFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = ASPath
        fields = ()

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value)
        return queryset.filter(qs_filter).distinct()


@register_filterset
class ASPathEntryFilterSet(NetBoxModelFilterSet):
    aspath_id = django_filters.ModelMultipleChoiceFilter(
        field_name='aspath',
        queryset=ASPath.objects.all(),
        label=_('AS-Path (ID)'),
    )
    aspath = django_filters.ModelMultipleChoiceFilter(
        field_name='aspath__name',
        queryset=ASPath.objects.all(),
        to_field_name='name',
        label=_('AS-Path (Name)'),
    )

    class Meta:
        model = ASPathEntry
        fields = (
            'aspath_id',
            'aspath',
            'action',
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(aspath__name__icontains=value)
            | Q(pattern__icontains=value)
            | Q(action=value)
        )
        return queryset.filter(qs_filter).distinct()
