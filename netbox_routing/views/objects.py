from netbox.views.generic import (
    ObjectListView,
    ObjectView,
    ObjectEditView,
    ObjectDeleteView,
    ObjectChildrenView,
    BulkDeleteView,
    BulkEditView,
)
from netbox_routing.filtersets import (
    PrefixListFilterSet,
    PrefixListEntryFilterSet,
    RouteMapEntryFilterSet,
    RouteMapFilterSet,
)
from netbox_routing.forms import (
    PrefixListFilterForm,
    PrefixListForm,
    PrefixListEntryFilterForm,
    PrefixListEntryForm,
    RouteMapEntryForm,
    RouteMapEntryFilterForm,
    RouteMapForm,
    RouteMapFilterForm,
    PrefixListEntryBulkEditForm,
    RouteMapEntryBulkEditForm,
)
from netbox_routing.models import PrefixList, PrefixListEntry, RouteMapEntry, RouteMap
from netbox_routing.tables.objects import (
    PrefixListTable,
    PrefixListEntryTable,
    RouteMapEntryTable,
    RouteMapTable,
)
from utilities.views import register_model_view, ViewTab


#
# Prefix List
#
@register_model_view(PrefixList, name='list', path='', detail=False)
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
        'bulk_delete': {'delete'},
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
            'view': 'prefixlistentry',
        }


@register_model_view(PrefixList, name='add', detail=False)
@register_model_view(PrefixList, name='edit')
class PrefixListEditView(ObjectEditView):
    queryset = PrefixList.objects.all()
    form = PrefixListForm


@register_model_view(PrefixList, name='delete')
class PrefixListDeleteView(ObjectDeleteView):
    pass


#
# Prefix List Entry
#


@register_model_view(PrefixListEntry, name='list', path='', detail=False)
class PrefixListEntryListView(ObjectListView):
    queryset = PrefixListEntry.objects.all()
    table = PrefixListEntryTable
    filterset = PrefixListEntryFilterSet
    filterset_form = PrefixListEntryFilterForm


@register_model_view(PrefixListEntry)
class PrefixListEntryView(ObjectView):
    queryset = PrefixListEntry.objects.all()
    template_name = 'netbox_routing/prefixlistentry.html'


@register_model_view(PrefixListEntry, name='add', detail=False)
@register_model_view(PrefixListEntry, name='edit')
class PrefixListEntryEditView(ObjectEditView):
    queryset = PrefixListEntry.objects.all()
    form = PrefixListEntryForm


@register_model_view(PrefixListEntry, name='delete')
class PrefixListEntryDeleteView(ObjectDeleteView):
    pass


@register_model_view(PrefixListEntry, name='bulk_edit', detail=False)
class PrefixListEntryBulkEditView(BulkEditView):
    queryset = PrefixListEntry.objects.all()
    filterset = PrefixListEntryFilterSet
    table = PrefixListEntryTable
    form = PrefixListEntryBulkEditForm


@register_model_view(PrefixListEntry, name='bulk_delete', detail=False)
class PrefixListEntryBulkDeleteView(BulkDeleteView):
    queryset = PrefixListEntry.objects.all()
    filterset = PrefixListEntryFilterSet
    table = PrefixListEntryTable


#
# Route Map
#
@register_model_view(RouteMap, name='list', path='', detail=False)
class RouteMapListView(ObjectListView):
    queryset = RouteMap.objects.all()
    table = RouteMapTable
    filterset = RouteMapFilterSet
    filterset_form = RouteMapFilterForm


@register_model_view(RouteMap)
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
        'bulk_delete': {'delete'},
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
            'view': 'routemapentry',
        }


@register_model_view(RouteMap, name='add', detail=False)
@register_model_view(RouteMap, name='edit')
class RouteMapEditView(ObjectEditView):
    queryset = RouteMap.objects.all()
    form = RouteMapForm


@register_model_view(RouteMap, name='delete')
class RouteMapDeleteView(ObjectDeleteView):
    pass


#
# Route Map Entry
#
@register_model_view(RouteMapEntry, name='list', path='', detail=False)
class RouteMapEntryListView(ObjectListView):
    queryset = RouteMapEntry.objects.all()
    table = RouteMapEntryTable
    filterset = RouteMapEntryFilterSet
    filterset_form = RouteMapEntryFilterForm


@register_model_view(RouteMapEntry)
class RouteMapEntryView(ObjectView):
    queryset = RouteMapEntry.objects.all()
    template_name = 'netbox_routing/routemapentry.html'


@register_model_view(RouteMapEntry, name='add', detail=False)
@register_model_view(RouteMapEntry, name='edit')
class RouteMapEntryEditView(ObjectEditView):
    queryset = RouteMapEntry.objects.all()
    form = RouteMapEntryForm


@register_model_view(RouteMapEntry, name='delete')
class RouteMapEntryDeleteView(ObjectDeleteView):
    pass


@register_model_view(RouteMapEntry, name='bulk_edit', detail=False)
class RouteMapEntryBulkEditView(BulkEditView):
    queryset = RouteMapEntry.objects.all()
    filterset = RouteMapEntryFilterSet
    table = RouteMapEntryTable
    form = RouteMapEntryBulkEditForm


@register_model_view(RouteMapEntry, name='bulk_delete', detail=False)
class RouteMapEntryBulkDeleteView(BulkDeleteView):
    queryset = RouteMapEntry.objects.all()
    filterset = RouteMapEntryFilterSet
    table = RouteMapEntryTable
