from netbox.search import SearchIndex, register_search
from netbox_routing.models.bgp import *


@register_search
class BGPPeerTemplateIndex(SearchIndex):
    model = BGPPeerTemplate
    fields = (
        ('name', 100),
        ('description', 4000),
        ('comments', 5000),
    )
    display_attrs = ('name',)


@register_search
class BGPPolicyTemplateIndex(SearchIndex):
    model = BGPPolicyTemplate
    fields = (
        ('name', 100),
        ('description', 4000),
        ('comments', 5000),
    )
    display_attrs = ('name',)


@register_search
class BGPSessionTemplateIndex(SearchIndex):
    model = BGPSessionTemplate
    fields = (
        ('name', 100),
        ('parent', 200),
        ('description', 4000),
        ('comments', 5000),
    )
    display_attrs = ('name',)


@register_search
class BGPSettingIndex(SearchIndex):
    model = BGPSetting
    fields = (
        ('search_display_name', 50),
        ('key', 100),
        ('description', 4000),
        ('comments', 5000),
    )
    display_attrs = (
        'key',
        'assigned_object',
    )


@register_search
class BGPRouterIndex(SearchIndex):
    model = BGPRouter
    fields = (
        ('search_display_name', 50),
        ('name', 100),
        ('description', 4000),
        ('comments', 5000),
    )
    display_attrs = (
        'assigned_object',
        'name',
    )


@register_search
class BGPScopeIndex(SearchIndex):
    model = BGPScope
    fields = (
        ('router', 100),
        ('vrf', 200),
        ('description', 4000),
        ('comments', 5000),
    )
    display_attrs = (
        'router',
        'vrf',
    )


@register_search
class BGPAddressFamilyIndex(SearchIndex):
    model = BGPAddressFamily
    fields = (
        ('scope', 100),
        ('address_family', 500),
        ('description', 4000),
        ('comments', 5000),
    )
    display_attrs = (
        'scope',
        'address_family',
    )


@register_search
class BGPPeerIndex(SearchIndex):
    model = BGPPeer
    fields = (
        ('name', 100),
        ('peer', 200),
        ('remote_as', 210),
        ('source', 300),
        ('local_as', 310),
        ('description', 4000),
        ('comments', 5000),
    )
    display_attrs = (
        'name',
        'peer',
        'remote_as',
    )


@register_search
class BGPPeerAddressFamilyIndex(SearchIndex):
    model = BGPPeerAddressFamily
    fields = (
        ('search_display_name', 50),
        ('description', 4000),
        ('comments', 5000),
    )
    display_attrs = (
        'assigned_object',
        'address_family',
    )
