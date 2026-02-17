from netbox import object_actions
from netbox.views.generic import (
    ObjectListView,
    ObjectView,
    ObjectEditView,
    ObjectDeleteView,
    ObjectChildrenView,
    BulkDeleteView,
    BulkEditView,
)
from utilities.views import register_model_view, ViewTab
from netbox_routing.filtersets.objects import *
from netbox_routing.forms.objects import *
from netbox_routing.models.objects import *
from netbox_routing.tables.objects import *


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
    template_name = 'netbox_routing/objectchildrentable.html'
    queryset = PrefixList.objects.all()
    child_model = PrefixListEntry
    table = PrefixListEntryTable
    filterset = PrefixListEntryFilterSet
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
    queryset = PrefixList.objects.all()


@register_model_view(PrefixList, name='bulk_edit', detail=False)
class PrefixListBulkEditView(BulkEditView):
    queryset = PrefixList.objects.all()
    filterset = PrefixListFilterSet
    form = PrefixListBulkEditForm
    table = PrefixListTable


@register_model_view(PrefixList, name='bulk_delete', detail=False)
class PrefixListBulkDeleteView(BulkDeleteView):
    queryset = PrefixList.objects.all()
    filterset = PrefixListFilterSet
    table = PrefixListTable


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
    queryset = PrefixListEntry.objects.all()


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
# Custom Prefix
#


@register_model_view(CustomPrefix, name='list', path='', detail=False)
class CustomPrefixListView(ObjectListView):
    queryset = CustomPrefix.objects.all()
    table = CustomPrefixTable
    filterset = CustomPrefixFilterSet
    filterset_form = CustomPrefixFilterForm
    actions = (object_actions.AddObject,)


@register_model_view(CustomPrefix)
class CustomPrefixView(ObjectView):
    queryset = CustomPrefix.objects.all()
    template_name = 'netbox_routing/customprefix.html'


@register_model_view(CustomPrefix, name='add', detail=False)
@register_model_view(CustomPrefix, name='edit')
class CustomPrefixEditView(ObjectEditView):
    queryset = CustomPrefix.objects.all()
    form = CustomPrefixForm


@register_model_view(CustomPrefix, name='delete')
class CustomPrefixDeleteView(ObjectDeleteView):
    queryset = CustomPrefix.objects.all()


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
    template_name = 'netbox_routing/objectchildrentable.html'
    queryset = RouteMap.objects.all()
    child_model = RouteMapEntry
    table = RouteMapEntryTable
    filterset = RouteMapEntryFilterSet
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
    queryset = RouteMap.objects.all()


@register_model_view(RouteMap, name='bulk_edit', detail=False)
class RouteMapBulkEditView(BulkEditView):
    queryset = RouteMap.objects.all()
    filterset = RouteMapFilterSet
    form = RouteMapBulkEditForm
    table = RouteMapTable


@register_model_view(RouteMap, name='bulk_delete', detail=False)
class RouteMapBulkDeleteView(BulkDeleteView):
    queryset = RouteMap.objects.all()
    filterset = RouteMapFilterSet
    table = RouteMapTable


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
    queryset = RouteMapEntry.objects.all()


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


#
# AS Path
#
@register_model_view(ASPath, name='list', path='', detail=False)
class ASPathListView(ObjectListView):
    queryset = ASPath.objects.all()
    filterset = ASPathFilterSet
    filterset_form = ASPathFilterForm
    table = ASPathTable


@register_model_view(ASPath)
class ASPathView(ObjectView):
    queryset = ASPath.objects.all()
    template_name = 'netbox_routing/aspath.html'


@register_model_view(ASPath, name='add', detail=False)
@register_model_view(ASPath, name='edit')
class ASPathEditView(ObjectEditView):
    queryset = ASPath.objects.all()
    form = ASPathForm


@register_model_view(ASPath, name='delete')
class ASPathDeleteView(ObjectDeleteView):
    queryset = ASPath.objects.all()


@register_model_view(ASPath, name='bulk_edit', detail=False)
class ASPathBulkEditView(BulkEditView):
    queryset = ASPath.objects.all()
    filterset = ASPathFilterSet
    form = ASPathBulkEditForm
    table = ASPathTable


@register_model_view(ASPath, name='bulk_delete', detail=False)
class ASPathBulkDeleteView(BulkDeleteView):
    queryset = ASPath.objects.all()
    filterset = ASPathFilterSet
    table = ASPathTable


@register_model_view(ASPath, name='entries')
class ASPathEntriesView(ObjectChildrenView):
    template_name = 'netbox_routing/objectchildrentable.html'
    queryset = ASPath.objects.all()
    child_model = ASPathEntry
    table = ASPathEntryTable
    filterset = ASPathEntryFilterSet
    tab = ViewTab(
        label='Entries',
        badge=lambda obj: ASPathEntry.objects.filter(aspath=obj).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(aspath=parent)

    def get_extra_context(self, request, instance):
        print(self.actions)

        return {
            'url_parent': 'plugins:netbox_routing:aspath_entries',
            'url_add': 'plugins:netbox_routing:aspathentry_add',
            'url_bulk_edit': 'plugins:netbox_routing:aspathentry_bulk_edit',
            'url_bulk_delete': 'plugins:netbox_routing:aspathentry_bulk_delete',
            'parent_name': 'aspath',
            'parent_view': 'aspath',
            'parent_view_path': 'entries',
            'view': 'aspathentry',
        }


#
# Route Map Entry
#
@register_model_view(ASPathEntry, name='list', path='', detail=False)
class ASPathEntryListView(ObjectListView):
    queryset = ASPathEntry.objects.all()
    table = ASPathEntryTable
    filterset = ASPathEntryFilterSet
    filterset_form = ASPathEntryFilterForm


@register_model_view(ASPathEntry)
class ASPathEntryView(ObjectView):
    queryset = ASPathEntry.objects.all()
    template_name = 'netbox_routing/aspathentry.html'


@register_model_view(ASPathEntry, name='add', detail=False)
@register_model_view(ASPathEntry, name='edit')
class ASPathEntryEditView(ObjectEditView):
    queryset = ASPathEntry.objects.all()
    form = ASPathEntryForm


@register_model_view(ASPathEntry, name='delete')
class ASPathEntryDeleteView(ObjectDeleteView):
    queryset = ASPathEntry.objects.all()


@register_model_view(ASPathEntry, name='bulk_edit', detail=False)
class ASPathEntryBulkEditView(BulkEditView):
    queryset = ASPathEntry.objects.all()
    filterset = ASPathEntryFilterSet
    table = ASPathEntryTable
    form = ASPathEntryBulkEditForm


@register_model_view(ASPathEntry, name='bulk_delete', detail=False)
class ASPathEntryBulkDeleteView(BulkDeleteView):
    queryset = ASPathEntry.objects.all()
    filterset = ASPathEntryFilterSet
    table = ASPathEntryTable
