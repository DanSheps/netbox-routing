from netbox.forms import NetBoxModelFilterSetForm
from netbox_routing.models.objects import *


class PrefixListFilterForm(NetBoxModelFilterSetForm):
    model = PrefixList


class PrefixListEntryFilterForm(NetBoxModelFilterSetForm):
    model = PrefixListEntry


class RouteMapFilterForm(NetBoxModelFilterSetForm):
    model = RouteMap


class RouteMapEntryFilterForm(NetBoxModelFilterSetForm):
    model = RouteMapEntry


class ASPathFilterForm(NetBoxModelFilterSetForm):
    model = ASPath


class ASPathEntryFilterForm(NetBoxModelFilterSetForm):
    model = ASPathEntry
