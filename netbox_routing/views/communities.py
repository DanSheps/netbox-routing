
from netbox.views.generic import ObjectListView, ObjectView, ObjectEditView, ObjectDeleteView, BulkDeleteView, \
    BulkEditView, ObjectChildrenView, BulkImportView
from netbox_routing.forms.bulk_import.communities import CommunityListBulkImportForm, CommunityBulkImportForm
from utilities.views import register_model_view, ViewTab

from netbox_routing.filtersets.communities import *
from netbox_routing.forms.communities import *
from netbox_routing.tables.communities import *


__all__ = (
    'CommunityListListView',
    'CommunityListView',
    'CommunityListEditView',
    'CommunityListDeleteView',
    'CommunityListBulkImportView',
    'CommunityListBulkEditView',
    'CommunityListBulkDeleteView',

    'CommunityListView',
    'CommunityView',
    'CommunityEditView',
    'CommunityDeleteView',
    'CommunityBulkImportView',
    'CommunityBulkEditView',
    'CommunityBulkDeleteView',
)


#
# Community List
#
@register_model_view(CommunityList, name='list')
class CommunityListListView(ObjectListView):
    queryset = CommunityList.objects.all()
    table = CommunityListTable
    filterset = CommunityListFilterSet
    filterset_form = CommunityListFilterForm


@register_model_view(CommunityList)
class CommunityListView(ObjectView):
    queryset = CommunityList.objects.all()
    template_name = 'netbox_routing/communitylist.html'


@register_model_view(CommunityList, name='edit')
class CommunityListEditView(ObjectEditView):
    queryset = CommunityList.objects.all()
    form = CommunityListForm


@register_model_view(CommunityList, name='delete')
class CommunityListDeleteView(ObjectDeleteView):
    queryset = CommunityList.objects.all()


@register_model_view(CommunityList, name='bulk_import')
class CommunityListBulkImportView(BulkImportView):
    queryset = CommunityList.objects.all()
    model_form = CommunityListBulkImportForm


@register_model_view(CommunityList, name='bulk_edit')
class CommunityListBulkEditView(BulkEditView):
    queryset = CommunityList.objects.all()
    filterset = CommunityListFilterSet
    table = CommunityListTable
    form = CommunityListBulkEditForm


@register_model_view(CommunityList, name='bulk_delete')
class CommunityListBulkDeleteView(BulkDeleteView):
    queryset = CommunityList.objects.all()
    filterset = CommunityListFilterSet
    table = CommunityListTable


@register_model_view(CommunityList, name='communities')
class CommunityListCommunitiesView(ObjectChildrenView):
    queryset = CommunityList.objects.all()
    child_model = Community
    table = CommunityTable
    filterset = CommunityFilterSet
    tab = ViewTab(
        label='Communities',
        badge=lambda obj: Community.objects.filter(community_lists=obj).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(community_lists=parent)


#
# Community
#
@register_model_view(Community, name='list')
class CommunityListView(ObjectListView):
    queryset = Community.objects.all()
    table = CommunityTable
    filterset = CommunityFilterSet
    filterset_form = CommunityFilterForm


@register_model_view(Community)
class CommunityView(ObjectView):
    queryset = Community.objects.all()
    template_name = 'netbox_routing/community.html'


@register_model_view(Community, name='edit')
class CommunityEditView(ObjectEditView):
    queryset = Community.objects.all()
    form = CommunityForm


@register_model_view(Community, name='delete')
class CommunityDeleteView(ObjectDeleteView):
    queryset = Community.objects.all()


@register_model_view(Community, name='bulk_import')
class CommunityBulkImportView(BulkImportView):
    queryset = Community.objects.all()
    model_form = CommunityBulkImportForm


@register_model_view(Community, name='bulk_edit')
class CommunityBulkEditView(BulkEditView):
    queryset = Community.objects.all()
    filterset = CommunityFilterSet
    table = CommunityTable
    form = CommunityBulkEditForm


@register_model_view(Community, name='bulk_delete')
class CommunityBulkDeleteView(BulkDeleteView):
    queryset = Community.objects.all()
    filterset = CommunityFilterSet
    table = CommunityTable
