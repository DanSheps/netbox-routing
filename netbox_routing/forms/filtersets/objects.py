from netbox.forms import NetBoxModelFilterSetForm
from netbox_routing.models.objects import *

__all__ = (
    'CustomPrefixFilterForm',
    'PrefixListFilterForm',
    'PrefixListEntryFilterForm',
    'RouteMapFilterForm',
    'RouteMapEntryFilterForm',
    'ASPathFilterForm',
    'ASPathEntryFilterForm',
)


class PrefixListFilterForm(NetBoxModelFilterSetForm):
    model = PrefixList


class PrefixListEntryFilterForm(NetBoxModelFilterSetForm):
    model = PrefixListEntry


class CustomPrefixFilterForm(NetBoxModelFilterSetForm):
    model = CustomPrefix


class RouteMapFilterForm(NetBoxModelFilterSetForm):
    model = RouteMap


class RouteMapEntryFilterForm(NetBoxModelFilterSetForm):
    model = RouteMapEntry


class ASPathFilterForm(NetBoxModelFilterSetForm):
    model = ASPath


class ASPathEntryFilterForm(NetBoxModelFilterSetForm):
    model = ASPathEntry
