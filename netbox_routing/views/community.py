from netbox.views.generic import (
    ObjectListView,
    ObjectView,
    ObjectEditView,
    ObjectDeleteView,
    ObjectChildrenView,
    BulkEditView,
    BulkDeleteView,
)
from utilities.views import register_model_view, ViewTab

from netbox_routing.filtersets.community import *
from netbox_routing.forms.community import *
from netbox_routing.models.community import *
from netbox_routing.tables.community import *

__all__ = (
    'CommunityListListView',
    'CommunityListDetailView',
    'CommunityListEditView',
    'CommunityListDeleteView',
    'CommunityListEntriesView',
    'CommunityListBulkEditView',
    'CommunityListBulkDeleteView',
    'CommunityListView',
    'CommunityDetailView',
    'CommunityEditView',
    'CommunityDeleteView',
    'CommunityBulkEditView',
    'CommunityBulkDeleteView',
    'CommunityListEntryListView',
    'CommunityListEntryDetailView',
    'CommunityListEntryEditView',
    'CommunityListEntryDeleteView',
    'CommunityListEntryBulkEditView',
    'CommunityListEntryBulkDeleteView',
)


#
# Prefix List
#
@register_model_view(CommunityList, name='list', path='', detail=False)
class CommunityListListView(ObjectListView):
    queryset = CommunityList.objects.all()
    table = CommunityListTable
    filterset = CommunityListFilterSet
    filterset_form = CommunityListFilterForm


@register_model_view(CommunityList)
class CommunityListDetailView(ObjectView):
    queryset = CommunityList.objects.all()
    template_name = 'netbox_routing/communitylist.html'


@register_model_view(CommunityList, name='add', detail=False)
@register_model_view(CommunityList, name='edit')
class CommunityListEditView(ObjectEditView):
    queryset = CommunityList.objects.all()
    form = CommunityListForm


@register_model_view(CommunityList, name='delete')
class CommunityListDeleteView(ObjectDeleteView):
    queryset = CommunityList.objects.all()


@register_model_view(CommunityList, name='entries')
class CommunityListEntriesView(ObjectChildrenView):
    queryset = CommunityList.objects.all()
    child_model = CommunityListEntry
    table = CommunityListEntryTable
    filterset = CommunityListEntryFilterSet
    filterset_form = CommunityListEntryFilterForm
    actions = ObjectChildrenView.actions
    tab = ViewTab(
        label='Entries',
        badge=lambda obj: CommunityListEntriesView.child_model.objects.filter(
            community_list=obj
        ).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(community_list=parent)


@register_model_view(CommunityList, name='bulk_edit', detail=False)
class CommunityListBulkEditView(BulkEditView):
    queryset = CommunityList.objects.all()
    filterset = CommunityListFilterForm
    form = CommunityListBulkEditForm
    table = CommunityListTable


@register_model_view(CommunityList, name='bulk_delete', detail=False)
class CommunityListBulkDeleteView(BulkDeleteView):
    queryset = CommunityList.objects.all()
    filterset = CommunityListFilterForm
    table = CommunityListTable


#
# Community
#


@register_model_view(Community, name='list', path='', detail=False)
class CommunityListView(ObjectListView):
    queryset = Community.objects.all()
    table = CommunityTable
    filterset = CommunityFilterSet
    filterset_form = CommunityFilterForm


@register_model_view(Community)
class CommunityDetailView(ObjectView):
    queryset = Community.objects.all()
    template_name = 'netbox_routing/community.html'


@register_model_view(Community, name='add', detail=False)
@register_model_view(Community, name='edit')
class CommunityEditView(ObjectEditView):
    queryset = Community.objects.all()
    form = CommunityForm


@register_model_view(Community, name='delete')
class CommunityDeleteView(ObjectDeleteView):
    queryset = Community.objects.all()


@register_model_view(Community, name='bulk_edit', detail=False)
class CommunityBulkEditView(BulkEditView):
    queryset = Community.objects.all()
    filterset = CommunityFilterForm
    form = CommunityBulkEditForm
    table = CommunityTable


@register_model_view(Community, name='bulk_delete', detail=False)
class CommunityBulkDeleteView(BulkDeleteView):
    queryset = Community.objects.all()
    filterset = CommunityFilterForm
    table = CommunityTable


#
# Community List Entry
#


@register_model_view(CommunityListEntry, name='list', path='', detail=False)
class CommunityListEntryListView(ObjectListView):
    queryset = CommunityListEntry.objects.all()
    table = CommunityListEntryTable
    filterset = CommunityListEntryFilterSet
    filterset_form = CommunityListEntryFilterForm


@register_model_view(CommunityListEntry)
class CommunityListEntryDetailView(ObjectView):
    queryset = CommunityListEntry.objects.all()
    template_name = 'netbox_routing/communitylistentry.html'


@register_model_view(CommunityListEntry, name='add', detail=False)
@register_model_view(CommunityListEntry, name='edit')
class CommunityListEntryEditView(ObjectEditView):
    queryset = CommunityListEntry.objects.all()
    form = CommunityListEntryForm


@register_model_view(CommunityListEntry, name='delete')
class CommunityListEntryDeleteView(ObjectDeleteView):
    queryset = CommunityListEntry.objects.all()


@register_model_view(CommunityListEntry, name='bulk_edit', detail=False)
class CommunityListEntryBulkEditView(BulkEditView):
    queryset = CommunityListEntry.objects.all()
    filterset = CommunityListEntryFilterForm
    form = CommunityListEntryBulkEditForm
    table = CommunityListEntryTable


@register_model_view(CommunityListEntry, name='bulk_delete', detail=False)
class CommunityListEntryBulkDeleteView(BulkDeleteView):
    queryset = CommunityListEntry.objects.all()
    filterset = CommunityListEntryFilterForm
    table = CommunityListEntryTable
