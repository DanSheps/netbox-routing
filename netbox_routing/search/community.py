from netbox.search import SearchIndex, register_search
from netbox_routing.models.community import *


@register_search
class CommunityIndex(SearchIndex):
    model = Community
    fields = (
        ('community', 100),
        ('description', 4000),
        ('comments', 5000),
    )
    display_attrs = ('community',)


@register_search
class CommunityListIndex(SearchIndex):
    model = CommunityList
    fields = (
        ('name', 100),
        ('description', 4000),
        ('comments', 5000),
    )
    display_attrs = ('name',)


@register_search
class CommunityListEntryIndex(SearchIndex):
    model = CommunityListEntry
    fields = (
        ('community_list', 100),
        ('community', 100),
        ('description', 4000),
        ('comments', 5000),
    )
    display_attrs = (
        'community_list',
        'community',
    )
