import django_filters
import netaddr
from django.db.models import Q
from django.utils.translation import gettext as _

from ipam.models import Prefix
from netbox.filtersets import NetBoxModelFilterSet
from utilities.filtersets import register_filterset

from netbox_routing.models.objects import *
from netbox_routing.models.community import *

__all__ = (
    'CustomPrefixFilterSet',
    'PrefixListFilterSet',
    'PrefixListEntryFilterSet',
    'RouteMapFilterSet',
    'RouteMapEntryFilterSet',
    'ASPathFilterSet',
    'ASPathEntryFilterSet',
)


class ASPathFilterSet(NetBoxModelFilterSet):
    route_map_entry_id = django_filters.ModelMultipleChoiceFilter(
        field_name='route_map_entries',
        queryset=RouteMapEntry.objects.all(),
        label=_('Route Map Entry (ID)'),
    )

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


@register_filterset
class PrefixListFilterSet(NetBoxModelFilterSet):
    route_map_entry_id = django_filters.ModelMultipleChoiceFilter(
        field_name='route_map_entries',
        queryset=RouteMapEntry.objects.all(),
        label=_('Route Map Entry (ID)'),
    )

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
    prefix_id = django_filters.ModelMultipleChoiceFilter(
        field_name='prefixes',
        queryset=Prefix.objects.all(),
        label=_('Prefix (ID)'),
    )
    prefix = django_filters.ModelMultipleChoiceFilter(
        field_name='prefixes__prefix',
        queryset=Prefix.objects.all(),
        to_field_name='prefix',
        label=_('Prefix (Name)'),
    )
    custom_prefix_id = django_filters.ModelMultipleChoiceFilter(
        field_name='custom_prefixes',
        queryset=CustomPrefix.objects.all(),
        label=_('Custom Prefix (ID)'),
    )
    custom_prefix = django_filters.ModelMultipleChoiceFilter(
        field_name='custom_prefixes__prefix',
        queryset=CustomPrefix.objects.all(),
        to_field_name='prefix',
        label=_('Custom Prefix (Name)'),
    )

    class Meta:
        model = PrefixListEntry
        fields = (
            'prefix_list_id',
            'prefix_list',
            'prefix_id',
            'prefix',
            'custom_prefix_id',
            'custom_prefix',
            'sequence',
            'action',
            'le',
            'ge',
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(prefix_list__name__icontains=value)
        qs_filter |= Q(prefixes__prefix__icontains=value)
        qs_filter |= Q(custom_prefixes__prefix__icontains=value)

        return queryset.filter(qs_filter).distinct()

    def filter_prefix(self, queryset, name, value):
        if not value.strip():
            return queryset
        try:
            query = str(netaddr.IPNetwork(value).cidr)
            return queryset.filter(prefix=query)
        except (netaddr.AddrFormatError, ValueError):
            return queryset.none()


class CustomPrefixFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = CustomPrefix
        fields = ()

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(prefix__icontains=value)

        return queryset.filter(qs_filter).distinct()


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
    match_prefix_list_id = django_filters.ModelMultipleChoiceFilter(
        field_name='match_prefix_list',
        queryset=PrefixList.objects.all(),
        label=_('Prefix List (ID)'),
    )
    match_prefix_list = django_filters.ModelMultipleChoiceFilter(
        field_name='match_prefix_list__name',
        queryset=PrefixList.objects.all(),
        to_field_name='name',
        label=_('Prefix List (Name)'),
    )
    match_community_list_id = django_filters.ModelMultipleChoiceFilter(
        field_name='match_community_list',
        queryset=CommunityList.objects.all(),
        label=_('Community List (ID)'),
    )
    match_community_list = django_filters.ModelMultipleChoiceFilter(
        field_name='match_community_list__name',
        queryset=CommunityList.objects.all(),
        to_field_name='name',
        label=_('Community List (Name)'),
    )
    match_community_id = django_filters.ModelMultipleChoiceFilter(
        field_name='match_community',
        queryset=Community.objects.all(),
        label=_('Community (ID)'),
    )
    match_community = django_filters.ModelMultipleChoiceFilter(
        field_name='match_community__community',
        queryset=Community.objects.all(),
        to_field_name='community',
        label=_('Community (Community)'),
    )
    match_aspath_id = django_filters.ModelMultipleChoiceFilter(
        field_name='match_aspath',
        queryset=ASPath.objects.all(),
        label=_('AS Path List (ID)'),
    )
    match_aspath = django_filters.ModelMultipleChoiceFilter(
        field_name='match_aspath__name',
        queryset=ASPath.objects.all(),
        to_field_name='name',
        label=_('AS Path List (Name)'),
    )

    class Meta:
        model = RouteMapEntry
        fields = (
            'route_map_id',
            'route_map',
            'sequence',
            'action',
            'match_prefix_list_id',
            'match_prefix_list',
            'match_community_list_id',
            'match_community_list',
            'match_community_id',
            'match_community',
            'match_aspath_id',
            'match_aspath',
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(route_map__name__icontains=value)
        qs_filter |= Q(match__icontains=value)
        qs_filter |= Q(set__icontains=value)
        return queryset.filter(qs_filter).distinct()
