from netbox.search import SearchIndex, register_search
from netbox_routing.models.objects import *


@register_search
class ASPathIndex(SearchIndex):
    model = ASPath
    fields = (
        ('name', 100),
        ('description', 4000),
        ('comments', 5000),
    )
    display_attrs = ('name',)


@register_search
class ASPathEntryIndex(SearchIndex):
    model = ASPathEntry
    fields = (
        ('aspath', 100),
        ('pattern', 100),
        ('description', 4000),
        ('comments', 5000),
    )
    display_attrs = (
        'aspath',
        'pattern',
    )


@register_search
class PrefixListIndex(SearchIndex):
    model = PrefixList
    fields = (
        ('name', 100),
        ('description', 4000),
        ('comments', 5000),
    )
    display_attrs = ('name',)


@register_search
class PrefixListEntryIndex(SearchIndex):
    model = PrefixListEntry
    fields = (
        ('prefix_list', 100),
        ('prefix', 150),
        ('description', 4000),
        ('comments', 5000),
    )
    display_attrs = (
        'prefix_list',
        'prefix',
    )


@register_search
class RouteMapIndex(SearchIndex):
    model = RouteMap
    fields = (
        ('name', 100),
        ('description', 4000),
        ('comments', 5000),
    )
    display_attrs = ('name',)


@register_search
class RouteMapEntryIndex(SearchIndex):
    model = RouteMapEntry
    fields = (
        ('route_map', 100),
        ('match', 200),
        ('set', 300),
        ('description', 4000),
        ('comments', 5000),
    )
    display_attrs = ('route_map',)
