from netbox.forms import NetBoxModelFilterSetForm
from netbox_routing.models import PrefixList, PrefixListEntry, RouteMap, RouteMapEntry


class PrefixListFilterSetForm(NetBoxModelFilterSetForm):
    model = PrefixList


class PrefixListEntryFilterSetForm(NetBoxModelFilterSetForm):
    model = PrefixListEntry


class RouteMapFilterSetForm(NetBoxModelFilterSetForm):
    model = RouteMap


class RouteMapEntryFilterSetForm(NetBoxModelFilterSetForm):
    model = RouteMapEntry