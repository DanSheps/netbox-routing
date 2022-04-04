
from netbox.views.generic import ObjectListView, ObjectView, ObjectEditView, ObjectDeleteView
from netbox_routing.filtersets import PrefixListFilterSet, PrefixListEntryFilterSet, RouteMapEntryFilterSet, \
    RouteMapFilterSet
from netbox_routing.forms import PrefixListFilterSetForm, PrefixListForm, PrefixListEntryFilterSetForm, \
    PrefixListEntryForm, RouteMapEntryForm, RouteMapEntryFilterSetForm, RouteMapForm, RouteMapFilterSetForm
from netbox_routing.models import PrefixList, PrefixListEntry, RouteMapEntry, RouteMap
from netbox_routing.tables.objects import PrefixListTable, PrefixListEntryTable, RouteMapEntryTable, RouteMapTable


#
# Prefix List
#
class PrefixListListView(ObjectListView):
    queryset = PrefixList.objects.all()
    table = PrefixListTable
    filterset = PrefixListFilterSet
    filterset_form = PrefixListFilterSetForm


class PrefixListView(ObjectView):
    queryset = PrefixList.objects.all()
    template_name = 'netbox_routing/prefixlist.html'


class PrefixListEditView(ObjectEditView):
    queryset = PrefixList.objects.all()
    form = PrefixListForm


class PrefixListDeleteView(ObjectDeleteView):
    pass


#
# Prefix List Entry
#
class PrefixListEntryListView(ObjectListView):
    queryset = PrefixListEntry.objects.all()
    table = PrefixListEntryTable
    filterset = PrefixListEntryFilterSet
    filterset_form = PrefixListEntryFilterSetForm


class PrefixListEntryView(ObjectView):
    queryset = PrefixListEntry.objects.all()
    template_name = 'netbox_routing/prefixlist.html'


class PrefixListEntryEditView(ObjectEditView):
    queryset = PrefixListEntry.objects.all()
    form = PrefixListEntryForm


class PrefixListEntryDeleteView(ObjectDeleteView):
    pass


#
# Route Map
#
class RouteMapListView(ObjectListView):
    queryset = RouteMap.objects.all()
    table = RouteMapTable
    filterset = RouteMapFilterSet
    filterset_form = RouteMapFilterSetForm


class RouteMapView(ObjectView):
    queryset = RouteMap.objects.all()
    template_name = 'netbox_routing/routemap.html'


class RouteMapEditView(ObjectEditView):
    queryset = RouteMap.objects.all()
    form = RouteMapForm


class RouteMapDeleteView(ObjectDeleteView):
    pass


#
# Prefix List Entry
#
class RouteMapEntryListView(ObjectListView):
    queryset = RouteMapEntry.objects.all()
    table = RouteMapEntryTable
    filterset = RouteMapEntryFilterSet
    filterset_form = RouteMapEntryFilterSetForm


class RouteMapEntryView(ObjectView):
    queryset = RouteMapEntry.objects.all()
    template_name = 'netbox_routing/prefixlist.html'


class RouteMapEntryEditView(ObjectEditView):
    queryset = RouteMapEntry.objects.all()
    form = RouteMapEntryForm


class RouteMapEntryDeleteView(ObjectDeleteView):
    pass
