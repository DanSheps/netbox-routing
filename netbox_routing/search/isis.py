# SPDX-License-Identifier: Apache-2.0

from netbox.search import SearchIndex, register_search

from netbox_routing.models.isis import (
    ISISInstance,
    ISISInterface,
    ISISSetting,
    ISISLevel,
    ISISInterfaceLevel,
    ISISSegmentRouting,
    ISISFlexAlgo,
    ISISPrefixSID,
    ISISSRv6Locator,
)

__all__ = (
    'ISISInstanceIndex',
    'ISISInterfaceIndex',
    'ISISSettingIndex',
    'ISISLevelIndex',
    'ISISInterfaceLevelIndex',
    'ISISSegmentRoutingIndex',
    'ISISFlexAlgoIndex',
    'ISISPrefixSIDIndex',
    'ISISSRv6LocatorIndex',
)


@register_search
class ISISFlexAlgoIndex(SearchIndex):
    model = ISISFlexAlgo
    fields = (('metric_type', 200), ('comments', 5000))
    display_attrs = ('instance', 'algo_id', 'metric_type')


@register_search
class ISISPrefixSIDIndex(SearchIndex):
    model = ISISPrefixSID
    fields = (('comments', 5000),)
    display_attrs = ('interface', 'algorithm', 'sid_index')


@register_search
class ISISSRv6LocatorIndex(SearchIndex):
    model = ISISSRv6Locator
    fields = (('name', 100), ('flavor', 200), ('comments', 5000))
    display_attrs = ('instance', 'name', 'prefix')


@register_search
class ISISLevelIndex(SearchIndex):
    model = ISISLevel
    fields = (('comments', 5000),)
    display_attrs = ('instance', 'level')


@register_search
class ISISInterfaceLevelIndex(SearchIndex):
    model = ISISInterfaceLevel
    fields = (('comments', 5000),)
    display_attrs = ('interface', 'level')


@register_search
class ISISSegmentRoutingIndex(SearchIndex):
    model = ISISSegmentRouting
    fields = (('prefix_sid_range', 200), ('comments', 5000))
    display_attrs = ('instance', 'prefix_sid_range')


@register_search
class ISISSettingIndex(SearchIndex):
    model = ISISSetting
    fields = (
        ('key', 100),
        ('value', 200),
        ('comments', 5000),
    )
    display_attrs = ('assigned_object_type', 'key', 'value')


@register_search
class ISISInstanceIndex(SearchIndex):
    model = ISISInstance
    fields = (
        ('process_tag', 100),
        ('net', 200),
        ('is_type', 300),
        ('comments', 5000),
    )
    display_attrs = ('device', 'vrf')


@register_search
class ISISInterfaceIndex(SearchIndex):
    model = ISISInterface
    fields = (
        ('address_family', 100),
        ('circuit_type', 200),
        ('network_type', 300),
        ('comments', 5000),
    )
    display_attrs = ('instance', 'interface')
