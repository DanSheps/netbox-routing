from netbox.views.generic import ObjectListView, ObjectEditView, ObjectView, ObjectDeleteView, ObjectChildrenView, \
    BulkImportView, BulkEditView, BulkDeleteView
from netbox_routing.filtersets.eigrp import *
from netbox_routing.forms import *
from netbox_routing.tables.eigrp import *
from utilities.views import register_model_view, ViewTab

from netbox_routing.models import *


__all__ = (
    'EIGRPRouterListView',
    'EIGRPRouterView',
    'EIGRPRouterAddressFamiliesView',
    'EIGRPRouterInterfacesView',
    'EIGRPRouterNetworksView',
    'EIGRPRouterEditView',
    'EIGRPRouterImportView',
    'EIGRPRouterBulkEditView',
    'EIGRPRouterDeleteView',
    'EIGRPRouterBulkDeleteView',

    'EIGRPAddressFamilyListView',
    'EIGRPAddressFamilyView',
    'EIGRPAddressFamilyInterfacesView',
    'EIGRPAddressFamilyNetworksView',
    'EIGRPAddressFamilyEditView',
    'EIGRPAddressFamilyBulkEditView',
    'EIGRPAddressFamilyDeleteView',
    'EIGRPAddressFamilyBulkDeleteView',

    'EIGRPNetworkListView',
    'EIGRPNetworkView',
    'EIGRPNetworkEditView',
    'EIGRPNetworkBulkEditView',
    'EIGRPNetworkDeleteView',
    'EIGRPNetworkBulkDeleteView',

    'EIGRPInterfaceListView',
    'EIGRPInterfaceView',
    'EIGRPInterfaceEditView',
    'EIGRPInterfaceBulkEditView',
    'EIGRPInterfaceDeleteView',
    'EIGRPInterfaceBulkDeleteView',
)


#
# Instance
#
@register_model_view(EIGRPRouter, name='list')
class EIGRPRouterListView(ObjectListView):
    queryset = EIGRPRouter.objects.all()
    table = EIGRPRouterTable
    filterset = EIGRPRouterFilterSet
    filterset_form = EIGRPRouterFilterForm


@register_model_view(EIGRPRouter)
class EIGRPRouterView(ObjectView):
    queryset = EIGRPRouter.objects.all()
    template_name = 'netbox_routing/eigrprouter.html'


@register_model_view(EIGRPRouter, name='address_families')
class EIGRPRouterAddressFamiliesView(ObjectChildrenView):
    queryset = EIGRPRouter.objects.all()
    child_model = EIGRPAddressFamily
    table = EIGRPAddressFamilyTable
    filterset = EIGRPAddressFamilyFilterSet
    tab = ViewTab(
        label='Address Families',
        badge=lambda obj: EIGRPAddressFamily.objects.filter(router=obj).count(),
        hide_if_empty=False,
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(router=parent)


@register_model_view(EIGRPRouter, name='interfaces')
class EIGRPRouterInterfacesView(ObjectChildrenView):
    queryset = EIGRPRouter.objects.all()
    child_model = EIGRPInterface
    table = EIGRPInterfaceTable
    filterset = EIGRPInterfaceFilterSet
    tab = ViewTab(
        label='Interfaces',
        badge=lambda obj: EIGRPInterface.objects.filter(router=obj).count(),
        hide_if_empty=False,
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(router=parent)


@register_model_view(EIGRPRouter, name='networks')
class EIGRPRouterNetworksView(ObjectChildrenView):
    queryset = EIGRPRouter.objects.all()
    child_model = EIGRPNetwork
    table = EIGRPNetworkTable
    filterset = EIGRPNetworkFilterSet
    tab = ViewTab(
        label='Networks',
        badge=lambda obj: EIGRPNetwork.objects.filter(router=obj).count(),
        hide_if_empty=False,
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(router=parent)


@register_model_view(EIGRPRouter, name='edit')
class EIGRPRouterEditView(ObjectEditView):
    queryset = EIGRPRouter.objects.all()
    form = EIGRPRouterForm


@register_model_view(EIGRPRouter, name='bulk_edit')
class EIGRPRouterBulkEditView(BulkEditView):
    queryset = EIGRPRouter.objects.all()
    filterset = EIGRPRouterFilterSet
    table = EIGRPRouterTable
    form = EIGRPRouterBulkEditForm


@register_model_view(EIGRPRouter, name='delete')
class EIGRPRouterDeleteView(ObjectDeleteView):
    queryset = EIGRPRouter.objects.all()


@register_model_view(EIGRPRouter, name='bulk_delete')
class EIGRPRouterBulkDeleteView(BulkDeleteView):
    queryset = EIGRPRouter.objects.all()
    filterset = EIGRPRouterFilterSet
    table = EIGRPRouterTable


class EIGRPRouterImportView(BulkImportView):
    queryset = EIGRPRouter.objects.all()
    model_form = EIGRPRouterImportForm

#
# Address Family
#
@register_model_view(EIGRPAddressFamily, name='list')
class EIGRPAddressFamilyListView(ObjectListView):
    queryset = EIGRPAddressFamily.objects.all()
    table = EIGRPAddressFamilyTable
    filterset = EIGRPAddressFamilyFilterSet
    filterset_form = EIGRPAddressFamilyFilterForm


@register_model_view(EIGRPAddressFamily)
class EIGRPAddressFamilyView(ObjectView):
    queryset = EIGRPAddressFamily.objects.all()
    template_name = 'netbox_routing/eigrpaddressfamily.html'


@register_model_view(EIGRPAddressFamily, name='interfaces')
class EIGRPAddressFamilyInterfacesView(ObjectChildrenView):
    #template_name = 'netbox_routing/object_children.html'
    queryset = EIGRPAddressFamily.objects.all()
    child_model = EIGRPInterface
    table = EIGRPInterfaceTable
    filterset = EIGRPInterfaceFilterSet
    tab = ViewTab(
        label='Interfaces',
        badge=lambda obj: EIGRPInterface.objects.filter(address_family=obj).count(),
    )


@register_model_view(EIGRPAddressFamily, name='networks')
class EIGRPAddressFamilyNetworksView(ObjectChildrenView):
    #template_name = 'netbox_routing/object_children.html'
    queryset = EIGRPAddressFamily.objects.all()
    child_model = EIGRPNetwork
    table = EIGRPNetworkTable
    filterset = EIGRPNetworkFilterSet
    tab = ViewTab(
        label='Interfaces',
        badge=lambda obj: EIGRPInterface.objects.filter(address_family=obj).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(address_famiily=parent)


@register_model_view(EIGRPAddressFamily, name='edit')
class EIGRPAddressFamilyEditView(ObjectEditView):
    queryset = EIGRPAddressFamily.objects.all()
    form = EIGRPAddressFamilyForm


@register_model_view(EIGRPAddressFamily, name='bulk_edit')
class EIGRPAddressFamilyBulkEditView(BulkEditView):
    queryset = EIGRPAddressFamily.objects.all()
    table = EIGRPAddressFamilyTable
    filterset = EIGRPAddressFamilyFilterSet
    form = EIGRPAddressFamilyBulkEditForm


@register_model_view(EIGRPAddressFamily, name='delete')
class EIGRPAddressFamilyDeleteView(ObjectDeleteView):
    queryset = EIGRPAddressFamily.objects.all()


@register_model_view(EIGRPAddressFamily, name='delete')
class EIGRPAddressFamilyBulkDeleteView(BulkDeleteView):
    queryset = EIGRPAddressFamily.objects.all()
    table = EIGRPAddressFamilyTable
    filterset = EIGRPAddressFamilyFilterSet


class EIGRPAddressFamilyImportView(BulkImportView):
    queryset = EIGRPAddressFamily.objects.all()
    model_form = EIGRPAddressFamilyImportForm


#
# Network
#
@register_model_view(EIGRPNetwork, name='list')
class EIGRPNetworkListView(ObjectListView):
    queryset = EIGRPNetwork.objects.all()
    table = EIGRPNetworkTable
    filterset = EIGRPNetworkFilterSet
    filterset_form = EIGRPNetworkFilterForm


@register_model_view(EIGRPNetwork)
class EIGRPNetworkView(ObjectView):
    queryset = EIGRPNetwork.objects.all()
    template_name = 'netbox_routing/eigrpnetwork.html'


@register_model_view(EIGRPNetwork, name='edit')
class EIGRPNetworkEditView(ObjectEditView):
    queryset = EIGRPNetwork.objects.all()
    form = EIGRPNetworkForm


@register_model_view(EIGRPNetwork, name='delete')
class EIGRPNetworkDeleteView(ObjectDeleteView):
    queryset = EIGRPNetwork.objects.all()


class EIGRPNetworkImportView(BulkImportView):
    queryset = EIGRPNetwork.objects.all()
    model_form = EIGRPNetworkImportForm


class EIGRPNetworkBulkEditView(BulkEditView):
    queryset = EIGRPNetwork.objects.all()
    filterset = EIGRPNetworkFilterSet
    table = EIGRPNetworkTable
    form = EIGRPNetworkBulkEditForm


class EIGRPNetworkBulkDeleteView(BulkDeleteView):
    queryset = EIGRPNetwork.objects.all()
    filterset = EIGRPNetworkFilterSet
    table = EIGRPNetworkTable


#
# Interface
#
@register_model_view(EIGRPInterface, name='list')
class EIGRPInterfaceListView(ObjectListView):
    queryset = EIGRPInterface.objects.all()
    table = EIGRPInterfaceTable
    filterset = EIGRPInterfaceFilterSet
    filterset_form = EIGRPInterfaceFilterForm


@register_model_view(EIGRPInterface)
class EIGRPInterfaceView(ObjectView):
    queryset = EIGRPInterface.objects.all()
    template_name = 'netbox_routing/eigrpinterface.html'


@register_model_view(EIGRPInterface, name='edit')
class EIGRPInterfaceEditView(ObjectEditView):
    queryset = EIGRPInterface.objects.all()
    form = EIGRPInterfaceForm


@register_model_view(EIGRPInterface, name='delete')
class EIGRPInterfaceDeleteView(ObjectDeleteView):
    queryset = EIGRPInterface.objects.all()


class EIGRPInterfaceImportView(BulkImportView):
    queryset = EIGRPInterface.objects.all()
    model_form = EIGRPInterfaceImportForm


class EIGRPInterfaceBulkEditView(BulkEditView):
    queryset = EIGRPInterface.objects.all()
    filterset = EIGRPInterfaceFilterSet
    table = EIGRPInterfaceTable
    form = EIGRPInterfaceBulkEditForm


class EIGRPInterfaceBulkDeleteView(BulkDeleteView):
    queryset = EIGRPInterface.objects.all()
    filterset = EIGRPInterfaceFilterSet
    table = EIGRPInterfaceTable
