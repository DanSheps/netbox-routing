from netbox.views.generic import ObjectView, ObjectEditView, ObjectListView, ObjectDeleteView, BulkImportView, \
    BulkEditView, BulkDeleteView
from netbox_routing.filtersets.bgp import *
from netbox_routing.forms.bgp import *
from netbox_routing.forms.filtersets.bgp import *
from netbox_routing.models.bgp import *
from netbox_routing.tables.bgp import *
from utilities.views import register_model_view


#
# BGP Router Views
#
@register_model_view(BGPRouter, name='list')
class BGPRouterListView(ObjectListView):
    queryset = BGPRouter.objects.all()
    table = BGPRouterTable
    filterset = BGPRouterFilterSet
    filterset_form = BGPRouterFilterForm


@register_model_view(BGPRouter)
class BGPRouterView(ObjectView):
    queryset = BGPRouter.objects.all()
    template_name = 'netbox_routing/bgprouter.html'


@register_model_view(BGPRouter, name='edit')
class BGPRouterEditView(ObjectEditView):
    queryset = BGPRouter.objects.all()
    form = BGPRouterForm


@register_model_view(BGPRouter, name='delete')
class BGPRouterDeleteView(ObjectDeleteView):
    queryset = BGPRouter.objects.all()


@register_model_view(BGPRouter, name='bulk_import')
class BGPRouterBulkImportView(BulkImportView):
    queryset = BGPRouter.objects.all()
    model_form = BGPRouterImportForm


@register_model_view(BGPRouter, name='bulk_edit')
class BGPRouterBulkEditView(BulkEditView):
    queryset = BGPRouter.objects.all()
    filterset = BGPRouterFilterSet
    table = BGPRouterTable
    form = BGPRouterBulkEditForm


@register_model_view(BGPRouter, name='bulk_delete')
class BGPRouterBulkDeleteView(BulkDeleteView):
    queryset = BGPRouter.objects.all()
    filterset = BGPRouterFilterSet
    table = BGPRouterTable


#
# BGP Scope Views
#
@register_model_view(BGPScope, name='list')
class BGPScopeListView(ObjectListView):
    queryset = BGPScope.objects.all()
    table = BGPScopeTable
    filterset = BGPScopeFilterSet
    filterset_form = BGPScopeFilterForm


@register_model_view(BGPScope)
class BGPScopeView(ObjectView):
    queryset = BGPScope.objects.all()
    template_name = 'netbox_routing/bgpscope.html'


@register_model_view(BGPScope, name='edit')
class BGPScopeEditView(ObjectEditView):
    queryset = BGPScope.objects.all()
    form = BGPScopeForm


@register_model_view(BGPScope, name='delete')
class BGPScopeDeleteView(ObjectDeleteView):
    queryset = BGPScope.objects.all()


@register_model_view(BGPScope, name='bulk_import')
class BGPScopeBulkImportView(BulkImportView):
    queryset = BGPScope.objects.all()
    model_form = BGPScopeImportForm


@register_model_view(BGPScope, name='bulk_edit')
class BGPScopeBulkEditView(BulkEditView):
    queryset = BGPScope.objects.all()
    filterset = BGPScopeFilterSet
    table = BGPScopeTable
    form = BGPScopeBulkEditForm


@register_model_view(BGPScope, name='bulk_delete')
class BGPScopeBulkDeleteView(BulkDeleteView):
    queryset = BGPScope.objects.all()
    filterset = BGPScopeFilterSet
    table = BGPScopeTable


#
# BGP Peer Session View
#
@register_model_view(BGPSessionTemplate, name='list')
class BGPSessionTemplateListView(ObjectListView):
    queryset = BGPSessionTemplate.objects.all()
    table = BGPSessionTemplateTable
    filterset = BGPSessionTemplateFilterSet
    filterset_form = BGPSessionTemplateFilterForm


@register_model_view(BGPSessionTemplate)
class BGPSessionTemplateView(ObjectView):
    queryset = BGPSessionTemplate.objects.all()
    template_name = 'netbox_routing/bgpscope.html'


@register_model_view(BGPSessionTemplate, name='edit')
class BGPSessionTemplateEditView(ObjectEditView):
    queryset = BGPSessionTemplate.objects.all()
    form = BGPSessionTemplateForm


@register_model_view(BGPSessionTemplate, name='delete')
class BGPSessionTemplateDeleteView(ObjectDeleteView):
    queryset = BGPSessionTemplate.objects.all()


@register_model_view(BGPSessionTemplate, name='bulk_import')
class BGPSessionTemplateBulkImportView(BulkImportView):
    queryset = BGPSessionTemplate.objects.all()
    model_form = BGPSessionTemplateImportForm


@register_model_view(BGPSessionTemplate, name='bulk_edit')
class BGPSessionTemplateBulkEditView(BulkEditView):
    queryset = BGPSessionTemplate.objects.all()
    filterset = BGPSessionTemplateFilterSet
    table = BGPSessionTemplateTable
    form = BGPSessionTemplateBulkEditForm


@register_model_view(BGPSessionTemplate, name='bulk_delete')
class BGPSessionTemplateBulkDeleteView(BulkDeleteView):
    queryset = BGPSessionTemplate.objects.all()
    filterset = BGPSessionTemplateFilterSet
    table = BGPSessionTemplateTable


#
# BGP Peer Policy View
#
@register_model_view(BGPPolicyTemplate, name='list')
class BGPPolicyTemplateListView(ObjectListView):
    queryset = BGPPolicyTemplate.objects.all()
    table = BGPPolicyTemplateTable
    filterset = BGPPolicyTemplateFilterSet
    filterset_form = BGPPolicyTemplateFilterForm


@register_model_view(BGPPolicyTemplate)
class BGPPolicyTemplateView(ObjectView):
    queryset = BGPPolicyTemplate.objects.all()
    template_name = 'netbox_routing/bgpscope.html'


@register_model_view(BGPPolicyTemplate, name='edit')
class BGPPolicyTemplateEditView(ObjectEditView):
    queryset = BGPPolicyTemplate.objects.all()
    form = BGPPolicyTemplateForm


@register_model_view(BGPPolicyTemplate, name='delete')
class BGPPolicyTemplateDeleteView(ObjectDeleteView):
    queryset = BGPPolicyTemplate.objects.all()


@register_model_view(BGPPolicyTemplate, name='bulk_import')
class BGPPolicyTemplateBulkImportView(BulkImportView):
    queryset = BGPPolicyTemplate.objects.all()
    model_form = BGPPolicyTemplateImportForm


@register_model_view(BGPPolicyTemplate, name='bulk_edit')
class BGPPolicyTemplateBulkEditView(BulkEditView):
    queryset = BGPPolicyTemplate.objects.all()
    filterset = BGPPolicyTemplateFilterSet
    table = BGPPolicyTemplateTable
    form = BGPPolicyTemplateBulkEditForm


@register_model_view(BGPPolicyTemplate, name='bulk_delete')
class BGPPolicyTemplateBulkDeleteView(BulkDeleteView):
    queryset = BGPPolicyTemplate.objects.all()
    filterset = BGPPolicyTemplateFilterSet
    table = BGPPolicyTemplateTable


#
# BGP Peer Template Views
#
@register_model_view(BGPPeerTemplate, name='list')
class BGPPeerTemplateListView(ObjectListView):
    queryset = BGPPeerTemplate.objects.all()
    table = BGPPeerTemplateTable
    filterset = BGPPeerTemplateFilterSet
    filterset_form = BGPPeerTemplateFilterForm


@register_model_view(BGPPeerTemplate)
class BGPPeerTemplateView(ObjectView):
    queryset = BGPPeerTemplate.objects.all()
    template_name = 'netbox_routing/bgpscope.html'


@register_model_view(BGPPeerTemplate, name='edit')
class BGPPeerTemplateEditView(ObjectEditView):
    queryset = BGPPeerTemplate.objects.all()
    form = BGPPeerTemplateForm


@register_model_view(BGPPeerTemplate, name='delete')
class BGPPeerTemplateDeleteView(ObjectDeleteView):
    queryset = BGPPeerTemplate.objects.all()


@register_model_view(BGPPeerTemplate, name='bulk_import')
class BGPPeerTemplateBulkImportView(BulkImportView):
    queryset = BGPPeerTemplate.objects.all()
    model_form = BGPPeerTemplateImportForm


@register_model_view(BGPPeerTemplate, name='bulk_edit')
class BGPPeerTemplateBulkEditView(BulkEditView):
    queryset = BGPPeerTemplate.objects.all()
    filterset = BGPPeerTemplateFilterSet
    table = BGPPeerTemplateTable
    form = BGPPeerTemplateBulkEditForm


@register_model_view(BGPPeerTemplate, name='bulk_delete')
class BGPPeerTemplateBulkDeleteView(BulkDeleteView):
    queryset = BGPPeerTemplate.objects.all()
    filterset = BGPPeerTemplateFilterSet
    table = BGPPeerTemplateTable


#
# BGP Address Family
#
@register_model_view(BGPAddressFamily, name='list')
class BGPAddressFamilyListView(ObjectListView):
    queryset = BGPAddressFamily.objects.all()
    table = BGPAddressFamilyTable
    filterset = BGPAddressFamilyFilterSet
    filterset_form = BGPAddressFamilyFilterForm


@register_model_view(BGPAddressFamily)
class BGPAddressFamilyView(ObjectView):
    queryset = BGPAddressFamily.objects.all()
    template_name = 'netbox_routing/bgpaddressfamily.html'


@register_model_view(BGPAddressFamily, name='edit')
class BGPAddressFamilyEditView(ObjectEditView):
    queryset = BGPAddressFamily.objects.all()
    form = BGPAddressFamilyForm


@register_model_view(BGPAddressFamily, name='delete')
class BGPAddressFamilyDeleteView(ObjectDeleteView):
    queryset = BGPAddressFamily.objects.all()


@register_model_view(BGPAddressFamily, name='bulk_import')
class BGPAddressFamilyBulkImportView(BulkImportView):
    queryset = BGPAddressFamily.objects.all()
    model_form = BGPAddressFamilyImportForm


@register_model_view(BGPAddressFamily, name='bulk_edit')
class BGPAddressFamilyBulkEditView(BulkEditView):
    queryset = BGPAddressFamily.objects.all()
    filterset = BGPAddressFamilyFilterSet
    table = BGPAddressFamilyTable
    form = BGPAddressFamilyBulkEditForm


@register_model_view(BGPAddressFamily, name='bulk_delete')
class BGPAddressFamilyBulkDeleteView(BulkDeleteView):
    queryset = BGPAddressFamily.objects.all()
    filterset = BGPAddressFamilyFilterSet
    table = BGPAddressFamilyTable


#
# BGP Session Template
#
@register_model_view(BGPSessionTemplate, name='list')
class BGPSessionTemplateListView(ObjectListView):
    queryset = BGPSessionTemplate.objects.all()
    table = BGPSessionTemplateTable
    filterset = BGPSessionTemplateFilterSet
    filterset_form = BGPSessionTemplateFilterForm


@register_model_view(BGPSessionTemplate)
class BGPSessionTemplateView(ObjectView):
    queryset = BGPSessionTemplate.objects.all()
    template_name = 'netbox_routing/bgpsessiontemplate.html'


@register_model_view(BGPSessionTemplate, name='edit')
class BGPSessionTemplateEditView(ObjectEditView):
    queryset = BGPSessionTemplate.objects.all()
    form = BGPSessionTemplateForm


@register_model_view(BGPSessionTemplate, name='delete')
class BGPSessionTemplateDeleteView(ObjectDeleteView):
    queryset = BGPSessionTemplate.objects.all()


@register_model_view(BGPSessionTemplate, name='bulk_import')
class BGPSessionTemplateBulkImportView(BulkImportView):
    queryset = BGPSessionTemplate.objects.all()
    model_form = BGPSessionTemplateImportForm


@register_model_view(BGPSessionTemplate, name='bulk_edit')
class BGPSessionTemplateBulkEditView(BulkEditView):
    queryset = BGPSessionTemplate.objects.all()
    filterset = BGPSessionTemplateFilterSet
    table = BGPSessionTemplateTable
    form = BGPSessionTemplateBulkEditForm


@register_model_view(BGPSessionTemplate, name='bulk_delete')
class BGPSessionTemplateBulkDeleteView(BulkDeleteView):
    queryset = BGPSessionTemplate.objects.all()
    filterset = BGPSessionTemplateFilterSet
    table = BGPSessionTemplateTable


#
# BGP Peer
#
@register_model_view(BGPPeer, name='list')
class BGPPeerListView(ObjectListView):
    queryset = BGPPeer.objects.all()
    table = BGPPeerTable
    filterset = BGPPeerFilterSet
    filterset_form = BGPPeerFilterForm


@register_model_view(BGPPeer)
class BGPPeerView(ObjectView):
    queryset = BGPPeer.objects.all()
    template_name = 'netbox_routing/bgppeer.html'


@register_model_view(BGPPeer, name='edit')
class BGPPeerEditView(ObjectEditView):
    queryset = BGPPeer.objects.all()
    form = BGPPeerForm


@register_model_view(BGPPeer, name='delete')
class BGPPeerDeleteView(ObjectDeleteView):
    queryset = BGPPeer.objects.all()


@register_model_view(BGPPeer, name='bulk_import')
class BGPPeerBulkImportView(BulkImportView):
    queryset = BGPPeer.objects.all()
    model_form = BGPPeerImportForm


@register_model_view(BGPPeer, name='bulk_edit')
class BGPPeerBulkEditView(BulkEditView):
    queryset = BGPPeer.objects.all()
    filterset = BGPPeerFilterSet
    table = BGPPeerTable
    form = BGPPeerBulkEditForm


@register_model_view(BGPPeer, name='bulk_delete')
class BGPPeerBulkDeleteView(BulkDeleteView):
    queryset = BGPPeer.objects.all()
    filterset = BGPPeerFilterSet
    table = BGPPeerTable


#
# BGP Peer
#
@register_model_view(BGPPeerAddressFamily, name='list')
class BGPPeerAddressFamilyListView(ObjectListView):
    queryset = BGPPeerAddressFamily.objects.all()
    table = BGPPeerAddressFamilyTable
    filterset = BGPPeerAddressFamilyFilterSet
    filterset_form = BGPPeerAddressFamilyFilterForm


@register_model_view(BGPPeerAddressFamily)
class BGPPeerAddressFamilyView(ObjectView):
    queryset = BGPPeerAddressFamily.objects.all()
    template_name = 'netbox_routing/bgppeer.html'


@register_model_view(BGPPeerAddressFamily, name='edit')
class BGPPeerAddressFamilyEditView(ObjectEditView):
    queryset = BGPPeerAddressFamily.objects.all()
    form = BGPPeerAddressFamilyForm


@register_model_view(BGPPeerAddressFamily, name='delete')
class BGPPeerAddressFamilyDeleteView(ObjectDeleteView):
    queryset = BGPPeerAddressFamily.objects.all()


@register_model_view(BGPPeerAddressFamily, name='bulk_import')
class BGPPeerAddressFamilyBulkImportView(BulkImportView):
    queryset = BGPPeerAddressFamily.objects.all()
    model_form = BGPPeerAddressFamilyImportForm


@register_model_view(BGPPeerAddressFamily, name='bulk_edit')
class BGPPeerAddressFamilyBulkEditView(BulkEditView):
    queryset = BGPPeerAddressFamily.objects.all()
    filterset = BGPPeerAddressFamilyFilterSet
    table = BGPPeerAddressFamilyTable
    form = BGPPeerAddressFamilyBulkEditForm


@register_model_view(BGPPeerAddressFamily, name='bulk_delete')
class BGPPeerAddressFamilyBulkDeleteView(BulkDeleteView):
    queryset = BGPPeerAddressFamily.objects.all()
    filterset = BGPPeerAddressFamilyFilterSet
    table = BGPPeerAddressFamilyTable
