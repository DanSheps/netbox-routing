from netbox.object_actions import CloneObject, EditObject, DeleteObject
from netbox.views.generic import (
    ObjectView,
    ObjectEditView,
    ObjectListView,
    ObjectDeleteView,
    ObjectChildrenView,
)

from utilities.views import register_model_view, ViewTab

from netbox_routing.filtersets.bgp import *
from netbox_routing.forms.bgp import *
from netbox_routing.models.bgp import *
from netbox_routing.tables.bgp import *

__all__ = (
    'BGPSettingListView',
    'BGPSettingView',
    'BGPSettingEditView',
    'BGPSettingDeleteView',
    'BGPRouterListView',
    'BGPRouterView',
    'BGPRouterEditView',
    'BGPRouterDeleteView',
    'BGPScopeListView',
    'BGPScopeView',
    'BGPScopeEditView',
    'BGPScopeDeleteView',
    'BGPAddressFamilyListView',
    'BGPAddressFamilyView',
    'BGPAddressFamilyEditView',
    'BGPAddressFamilyDeleteView',
)


@register_model_view(BGPAddressFamily, name='settings')
class BGPSettingViewMixin:
    child_model = BGPSetting
    table = BGPSettingTable
    filterset = BGPSettingFilterSet
    filterset_form = BGPSettingFilterForm
    actions = ObjectChildrenView.actions


#
# BGP Settings
#
@register_model_view(BGPSetting, name='list', path='', detail=False)
class BGPSettingListView(ObjectListView):
    queryset = BGPSetting.objects.all()
    table = BGPSettingTable
    filterset = BGPSettingFilterSet
    filterset_form = BGPSettingFilterForm


@register_model_view(BGPSetting)
class BGPSettingView(ObjectView):
    queryset = BGPSetting.objects.all()


@register_model_view(BGPSetting, name='add', detail=False)
@register_model_view(BGPSetting, name='edit')
class BGPSettingEditView(ObjectEditView):
    queryset = BGPSetting.objects.all()
    form = BGPSettingForm


@register_model_view(BGPSetting, name='delete')
class BGPSettingDeleteView(ObjectDeleteView):
    queryset = BGPSetting.objects.all()


#
# BGP Templates
#
@register_model_view(BGPPeerTemplate, name='list', path='', detail=False)
class BGPPeerTemplateListView(ObjectListView):
    queryset = BGPPeerTemplate.objects.all()
    table = BGPPeerTemplateTable
    filterset = BGPPeerTemplateFilterSet
    filterset_form = BGPPeerTemplateFilterForm


@register_model_view(BGPPeerTemplate)
class BGPPeerTemplateView(ObjectView):
    queryset = BGPPeerTemplate.objects.all()


@register_model_view(BGPPeerTemplate, name='add', detail=False)
@register_model_view(BGPPeerTemplate, name='edit')
class BGPPeerTemplateEditView(ObjectEditView):
    queryset = BGPPeerTemplate.objects.all()
    form = BGPPeerTemplateForm


@register_model_view(BGPPeerTemplate, name='delete')
class BGPPeerTemplateDeleteView(ObjectDeleteView):
    queryset = BGPPeerTemplate.objects.all()


@register_model_view(BGPPolicyTemplate, name='list', path='', detail=False)
class BGPPolicyTemplateListView(ObjectListView):
    queryset = BGPPolicyTemplate.objects.all()
    table = BGPPolicyTemplateTable
    filterset = BGPPolicyTemplateFilterSet
    filterset_form = BGPPolicyTemplateFilterForm


@register_model_view(BGPPolicyTemplate)
class BGPPolicyTemplateView(ObjectView):
    queryset = BGPPolicyTemplate.objects.all()


@register_model_view(BGPPolicyTemplate, name='add', detail=False)
@register_model_view(BGPPolicyTemplate, name='edit')
class BGPPolicyTemplateEditView(ObjectEditView):
    queryset = BGPPolicyTemplate.objects.all()
    form = BGPPolicyTemplateForm


@register_model_view(BGPPolicyTemplate, name='delete')
class BGPPolicyTemplateDeleteView(ObjectDeleteView):
    queryset = BGPPolicyTemplate.objects.all()


@register_model_view(BGPSessionTemplate, name='list', path='', detail=False)
class BGPSessionTemplateListView(ObjectListView):
    queryset = BGPSessionTemplate.objects.all()
    table = BGPSessionTemplateTable
    filterset = BGPSessionTemplateFilterSet
    filterset_form = BGPSessionTemplateFilterForm


@register_model_view(BGPSessionTemplate)
class BGPSessionTemplateView(ObjectView):
    queryset = BGPSessionTemplate.objects.all()


@register_model_view(BGPSessionTemplate, name='add', detail=False)
@register_model_view(BGPSessionTemplate, name='edit')
class BGPSessionTemplateEditView(ObjectEditView):
    queryset = BGPSessionTemplate.objects.all()
    form = BGPSessionTemplateForm


@register_model_view(BGPSessionTemplate, name='delete')
class BGPSessionTemplateDeleteView(ObjectDeleteView):
    queryset = BGPSessionTemplate.objects.all()


#
# BGP Router Views
#
@register_model_view(BGPRouter, name='list', path='', detail=False)
class BGPRouterListView(ObjectListView):
    queryset = BGPRouter.objects.all()
    table = BGPRouterTable
    filterset = BGPRouterFilterSet
    filterset_form = BGPRouterFilterForm


@register_model_view(BGPRouter)
class BGPRouterView(ObjectView):
    queryset = BGPRouter.objects.all()
    template_name = 'netbox_routing/bgprouter.html'


@register_model_view(BGPRouter, name='add', detail=False)
@register_model_view(BGPRouter, name='edit')
class BGPRouterEditView(ObjectEditView):
    queryset = BGPRouter.objects.all()
    form = BGPRouterForm


@register_model_view(BGPRouter, name='delete')
class BGPRouterDeleteView(ObjectDeleteView):
    queryset = BGPRouter.objects.all()


@register_model_view(BGPRouter, name='settings')
class BGPRouterSettingsView(BGPSettingViewMixin, ObjectChildrenView):
    queryset = BGPRouter.objects.all()
    tab = ViewTab(
        label='Settings',
        badge=lambda obj: BGPRouterSettingsView.child_model.objects.filter(
            router=obj
        ).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(router=parent)


@register_model_view(BGPRouter, name='peer_templates')
class BGPRouterPeerTemplatesView(ObjectChildrenView):
    queryset = BGPRouter.objects.all()
    child_model = BGPPeerTemplate
    table = BGPPeerTemplateTable
    filterset = BGPPeerTemplateFilterSet
    filterset_form = BGPPeerTemplateFilterForm
    actions = (CloneObject, EditObject, DeleteObject)
    tab = ViewTab(
        label='Peer Templates',
        badge=lambda obj: obj.peer_templates.count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(routers=parent)


@register_model_view(BGPRouter, name='policy_templates')
class BGPRouterPolicyTemplatesView(ObjectChildrenView):
    queryset = BGPRouter.objects.all()
    child_model = BGPPolicyTemplate
    table = BGPPolicyTemplateTable
    filterset = BGPPolicyTemplateFilterSet
    filterset_form = BGPPolicyTemplateFilterForm
    actions = (CloneObject, EditObject, DeleteObject)
    tab = ViewTab(
        label='Policy Templates',
        badge=lambda obj: obj.policy_templates.count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(routers=parent)


@register_model_view(BGPRouter, name='session_templates')
class BGPRouterSessionTemplatesView(ObjectChildrenView):
    queryset = BGPRouter.objects.all()
    child_model = BGPSessionTemplate
    table = BGPSessionTemplateTable
    filterset = BGPSessionTemplateFilterSet
    filterset_form = BGPSessionTemplateFilterForm
    actions = (CloneObject, EditObject, DeleteObject)
    tab = ViewTab(
        label='Session Templates',
        badge=lambda obj: obj.session_templates.count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(routers=parent)


#
# BGP Scope Views
#
@register_model_view(BGPScope, name='list', path='', detail=False)
class BGPScopeListView(ObjectListView):
    queryset = BGPScope.objects.all()
    table = BGPScopeTable
    filterset = BGPScopeFilterSet
    filterset_form = BGPScopeFilterForm


@register_model_view(BGPScope)
class BGPScopeView(ObjectView):
    queryset = BGPScope.objects.all()
    template_name = 'netbox_routing/bgpscope.html'


@register_model_view(BGPScope, name='add', detail=False)
@register_model_view(BGPScope, name='edit')
class BGPScopeEditView(ObjectEditView):
    queryset = BGPScope.objects.all()
    form = BGPScopeForm


@register_model_view(BGPScope, name='delete')
class BGPScopeDeleteView(ObjectDeleteView):
    queryset = BGPScope.objects.all()


#
# BGP Scope Views
#
@register_model_view(BGPAddressFamily, name='list', path='', detail=False)
class BGPAddressFamilyListView(ObjectListView):
    queryset = BGPAddressFamily.objects.all()
    table = BGPAddressFamilyTable
    filterset = BGPAddressFamilyFilterSet
    filterset_form = BGPAddressFamilyFilterForm


@register_model_view(BGPAddressFamily)
class BGPAddressFamilyView(ObjectView):
    queryset = BGPAddressFamily.objects.all()
    template_name = 'netbox_routing/bgpaddressfamily.html'


@register_model_view(BGPAddressFamily, name='add', detail=False)
@register_model_view(BGPAddressFamily, name='edit')
class BGPAddressFamilyEditView(ObjectEditView):
    queryset = BGPAddressFamily.objects.all()
    form = BGPAddressFamilyForm


@register_model_view(BGPAddressFamily, name='delete')
class BGPAddressFamilyDeleteView(ObjectDeleteView):
    queryset = BGPAddressFamily.objects.all()


@register_model_view(BGPAddressFamily, name='settings')
class BGPAddressFamilySettingsView(BGPSettingViewMixin, ObjectChildrenView):
    queryset = BGPAddressFamily.objects.all()
    tab = ViewTab(
        label='Settings',
        badge=lambda obj: BGPAddressFamilySettingsView.child_model.objects.filter(
            address_family=obj
        ).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(address_family=parent)


#
# BGP Peer Views
#
@register_model_view(BGPPeer, name='list', path='', detail=False)
class BGPPeerListView(ObjectListView):
    queryset = BGPPeer.objects.all()
    table = BGPPeerTable
    filterset = BGPPeerFilterSet
    filterset_form = BGPPeerFilterForm


@register_model_view(BGPPeer)
class BGPPeerView(ObjectView):
    queryset = BGPPeer.objects.all()


@register_model_view(BGPPeer, name='add', detail=False)
@register_model_view(BGPPeer, name='edit')
class BGPPeerEditView(ObjectEditView):
    queryset = BGPPeer.objects.all()
    form = BGPPeerForm


@register_model_view(BGPPeer, name='delete')
class BGPPeerDeleteView(ObjectDeleteView):
    queryset = BGPPeer.objects.all()


@register_model_view(BGPPeer, name='settings')
class BGPPeerSettingsView(BGPSettingViewMixin, ObjectChildrenView):
    queryset = BGPPeer.objects.all()
    tab = ViewTab(
        label='Settings',
        badge=lambda obj: BGPPeerSettingsView.child_model.objects.filter(
            peer=obj
        ).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(peer=parent)


@register_model_view(BGPPeer, name='address-families')
class BGPPeerAddressFamiliesView(ObjectChildrenView):
    queryset = BGPPeer.objects.all()
    child_model = BGPPeerAddressFamily
    table = BGPPeerAddressFamilyTable
    filterset = BGPPeerAddressFamilyFilterSet
    filterset_form = BGPPeerAddressFamilyFilterForm
    actions = ObjectChildrenView.actions
    tab = ViewTab(
        label='Address Families',
        badge=lambda obj: BGPPeerAddressFamiliesView.child_model.objects.filter(
            peer=obj
        ).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(peer=parent)


#
# BGP Peer Address Family Views
#
@register_model_view(BGPPeerAddressFamily, name='list', path='', detail=False)
class BGPPeerAddressFamilyListView(ObjectListView):
    queryset = BGPPeerAddressFamily.objects.all()
    table = BGPPeerAddressFamilyTable
    filterset = BGPPeerAddressFamilyFilterSet
    filterset_form = BGPPeerAddressFamilyFilterForm


@register_model_view(BGPPeerAddressFamily)
class BGPPeerAddressFamilyView(ObjectView):
    queryset = BGPPeerAddressFamily.objects.all()


@register_model_view(BGPPeerAddressFamily, name='add', detail=False)
@register_model_view(BGPPeerAddressFamily, name='edit')
class BGPPeerAddressFamilyEditView(ObjectEditView):
    queryset = BGPPeerAddressFamily.objects.all()
    form = BGPPeerAddressFamilyForm


@register_model_view(BGPPeerAddressFamily, name='delete')
class BGPPeerAddressFamilyDeleteView(ObjectDeleteView):
    queryset = BGPPeerAddressFamily.objects.all()


@register_model_view(BGPPeerAddressFamily, name='settings')
class BGPPeerAddressFamilySettingsView(BGPSettingViewMixin, ObjectChildrenView):
    queryset = BGPPeerAddressFamily.objects.all()
    tab = ViewTab(
        label='Settings',
        badge=lambda obj: BGPPeerAddressFamilySettingsView.child_model.objects.filter(
            peer_address_families=obj
        ).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(peer_address_families=parent)
