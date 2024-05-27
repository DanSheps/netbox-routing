
from netbox.views.generic import ObjectListView, ObjectView, ObjectEditView, ObjectDeleteView, ObjectChildrenView, \
    BulkDeleteView, BulkEditView
from netbox_routing.filtersets import PrefixListFilterSet, PrefixListEntryFilterSet, RouteMapEntryFilterSet, \
    RouteMapFilterSet
from netbox_routing.forms import PrefixListFilterForm, PrefixListForm, PrefixListEntryFilterForm, \
    PrefixListEntryForm, RouteMapEntryForm, RouteMapEntryFilterForm, RouteMapForm, RouteMapFilterForm, \
    PrefixListEntryBulkEditForm, RouteMapEntryBulkEditForm
from netbox_routing.models import PrefixList, PrefixListEntry, RouteMapEntry, RouteMap
from netbox_routing.tables.objects import PrefixListTable, PrefixListEntryTable, RouteMapEntryTable, RouteMapTable
from utilities.views import register_model_view, ViewTab


#
# Prefix List
#
@register_model_view(PrefixList, name='list')
class PrefixListListView(ObjectListView):
    queryset = PrefixList.objects.all()
    table = PrefixListTable
    filterset = PrefixListFilterSet
    filterset_form = PrefixListFilterForm


@register_model_view(PrefixList)
class PrefixListView(ObjectView):
    queryset = PrefixList.objects.all()
    template_name = 'netbox_routing/prefixlist.html'


@register_model_view(PrefixList, name='entries')
class PrefixListEntriesView(ObjectChildrenView):
    template_name = 'netbox_routing/objecttable.html'
    queryset = PrefixList.objects.all()
    child_model = PrefixListEntry
    table = PrefixListEntryTable
    filterset = PrefixListEntryFilterSet
    actions = {
        'add': {'add'},
        'edit': {'change'},
        'delete': {'delete'},
        'bulk_edit': {'change'},
        'bulk_delete': {'delete'}
    }
    tab = ViewTab(
        label='Entries',
        badge=lambda obj: PrefixListEntry.objects.filter(prefix_list=obj).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(prefix_list=parent)

    def get_extra_context(self, request, instance):

        return {
            'url_parent': 'plugins:netbox_routing:prefixlist_entries',
            'url_add': 'plugins:netbox_routing:prefixlistentry_add',
            'url_bulk_edit': 'plugins:netbox_routing:prefixlistentry_bulk_edit',
            'url_bulk_delete': 'plugins:netbox_routing:prefixlistentry_bulk_delete',
            'parent_name': 'prefix_list',
            'parent_view': 'prefixlist',
            'parent_view_path': 'entries',
            'view': 'prefixlistentry'
        }


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
    filterset_form = PrefixListEntryFilterForm


class PrefixListEntryView(ObjectView):
    queryset = PrefixListEntry.objects.all()
    template_name = 'netbox_routing/prefixlistentry.html'


class PrefixListEntryEditView(ObjectEditView):
    queryset = PrefixListEntry.objects.all()
    form = PrefixListEntryForm


class PrefixListEntryDeleteView(ObjectDeleteView):
    pass


class PrefixListEntryBulkEditView(BulkEditView):
    queryset = PrefixListEntry.objects.all()
    filterset = PrefixListEntryFilterSet
    table = PrefixListEntryTable
    form = PrefixListEntryBulkEditForm


class PrefixListEntryBulkDeleteView(BulkDeleteView):
    queryset = PrefixListEntry.objects.all()
    filterset = PrefixListEntryFilterSet
    table = PrefixListEntryTable


#
# Route Map
#
class RouteMapListView(ObjectListView):
    queryset = RouteMap.objects.all()
    table = RouteMapTable
    filterset = RouteMapFilterSet
    filterset_form = RouteMapFilterForm


class RouteMapView(ObjectView):
    queryset = RouteMap.objects.all()
    template_name = 'netbox_routing/routemap.html'


@register_model_view(RouteMap, name='entries')
class RouteMapEntriesView(ObjectChildrenView):
    template_name = 'netbox_routing/objecttable.html'
    queryset = RouteMap.objects.all()
    child_model = RouteMapEntry
    table = RouteMapEntryTable
    filterset = RouteMapEntryFilterSet
    actions = {
        'add': {'add'},
        'edit': {'change'},
        'delete': {'delete'},
        'bulk_edit': {'change'},
        'bulk_delete': {'delete'}
    }
    tab = ViewTab(
        label='Entries',
        badge=lambda obj: RouteMapEntry.objects.filter(route_map=obj).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(route_map=parent)

    def get_extra_context(self, request, instance):

        return {
            'url_parent': 'plugins:netbox_routing:routemap_entries',
            'url_add': 'plugins:netbox_routing:routemapentry_add',
            'url_bulk_edit': 'plugins:netbox_routing:routemapentry_bulk_edit',
            'url_bulk_delete': 'plugins:netbox_routing:routemapentry_bulk_delete',
            'parent_name': 'route_map',
            'parent_view': 'routemap',
            'parent_view_path': 'entries',
            'view': 'routemapentry'
        }


class RouteMapEditView(ObjectEditView):
    queryset = RouteMap.objects.all()
    form = RouteMapForm


class RouteMapDeleteView(ObjectDeleteView):
    pass


#
# Route Map Entry
#
class RouteMapEntryListView(ObjectListView):
    queryset = RouteMapEntry.objects.all()
    table = RouteMapEntryTable
    filterset = RouteMapEntryFilterSet
    filterset_form = RouteMapEntryFilterForm


class RouteMapEntryView(ObjectView):
    queryset = RouteMapEntry.objects.all()
    template_name = 'netbox_routing/routemapentry.html'


class RouteMapEntryEditView(ObjectEditView):
    queryset = RouteMapEntry.objects.all()
    form = RouteMapEntryForm


class RouteMapEntryDeleteView(ObjectDeleteView):
    pass


class RouteMapEntryBulkEditView(BulkEditView):
    queryset = RouteMapEntry.objects.all()
    filterset = RouteMapEntryFilterSet
    table = RouteMapEntryTable
    form = RouteMapEntryBulkEditForm


class RouteMapEntryBulkDeleteView(BulkDeleteView):
    queryset = RouteMapEntry.objects.all()
    filterset = RouteMapEntryFilterSet
    table = RouteMapEntryTable
