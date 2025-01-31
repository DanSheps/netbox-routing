from netbox.forms import NetBoxModelFilterSetForm
from netbox_routing.models import PrefixList, PrefixListEntry, RouteMap, RouteMapEntry


__all__ = (
    'PrefixListFilterForm',
    'PrefixListEntryFilterForm',
    'RouteMapFilterForm',
    'RouteMapEntryFilterForm',
)


class PrefixListFilterForm(NetBoxModelFilterSetForm):
    model = PrefixList


class PrefixListEntryFilterForm(NetBoxModelFilterSetForm):
    model = PrefixListEntry


class RouteMapFilterForm(NetBoxModelFilterSetForm):
    model = RouteMap


class RouteMapEntryFilterForm(NetBoxModelFilterSetForm):
    model = RouteMapEntry
