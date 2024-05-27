from netbox.views.generic import ObjectListView, ObjectEditView, ObjectView, ObjectDeleteView, ObjectChildrenView, \
    BulkImportView, BulkEditView, BulkDeleteView
from netbox_routing.filtersets.ospf import OSPFInterfaceFilterSet, OSPFAreaFilterSet, OSPFInstanceFilterSet
from netbox_routing.forms import OSPFInstanceFilterForm, OSPFInstanceForm, OSPFAreaFilterForm, OSPFAreaForm, \
    OSPFInterfaceFilterForm, OSPFInterfaceForm, OSPFInterfaceBulkEditForm, OSPFInterfaceImportForm
from netbox_routing.forms.bulk_import.ospf import OSPFAreaImportForm, OSPFInstanceImportForm
from netbox_routing.tables.ospf import OSPFAreaTable, OSPFInstanceTable, OSPFInterfaceTable
from utilities.views import register_model_view, ViewTab

from netbox_routing.models import OSPFArea, OSPFInstance, OSPFInterface


__all__ = (
    'OSPFInstanceListView',
    'OSPFInstanceView',
    'OSPFInstanceInterfacesView',
    'OSPFInstanceEditView',
    'OSPFInstanceDeleteView',

    'OSPFAreaListView',
    'OSPFAreaView',
    'OSPFAreaInterfacesView',
    'OSPFAreaEditView',
    'OSPFAreaDeleteView',

    'OSPFInterfaceListView',
    'OSPFInterfaceView',
    'OSPFInterfaceEditView',
    'OSPFInterfaceDeleteView',
)


#
# Instance
#
@register_model_view(OSPFInstance, name='list')
class OSPFInstanceListView(ObjectListView):
    queryset = OSPFInstance.objects.all()
    table = OSPFInstanceTable
    filterset = OSPFInstanceFilterSet
    filterset_form = OSPFInstanceFilterForm


@register_model_view(OSPFInstance)
class OSPFInstanceView(ObjectView):
    queryset = OSPFInstance.objects.all()
    template_name = 'netbox_routing/ospfinstance.html'


@register_model_view(OSPFInstance, name='interfaces')
class OSPFInstanceInterfacesView(ObjectChildrenView):
    template_name = 'netbox_routing/object_children.html'
    queryset = OSPFInstance.objects.all()
    child_model = OSPFInterface
    table = OSPFInterfaceTable
    filterset = OSPFInterfaceFilterSet
    tab = ViewTab(
        label='Interfaces',
        badge=lambda obj: OSPFInterface.objects.filter(instance=obj).count(),
        hide_if_empty=False,
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(instance=parent)


@register_model_view(OSPFInstance, name='edit')
class OSPFInstanceEditView(ObjectEditView):
    queryset = OSPFInstance.objects.all()
    form = OSPFInstanceForm


@register_model_view(OSPFInstance, name='delete')
class OSPFInstanceDeleteView(ObjectDeleteView):
    queryset = OSPFInstance.objects.all()


class OSPFInstanceBulkImportView(BulkImportView):
    queryset = OSPFInstance.objects.all()
    model_form = OSPFInstanceImportForm


#
# Area
#
@register_model_view(OSPFArea, name='list')
class OSPFAreaListView(ObjectListView):
    queryset = OSPFArea.objects.all()
    table = OSPFAreaTable
    filterset = OSPFAreaFilterSet
    filterset_form = OSPFAreaFilterForm


@register_model_view(OSPFArea)
class OSPFAreaView(ObjectView):
    queryset = OSPFArea.objects.all()
    template_name = 'netbox_routing/ospfarea.html'


@register_model_view(OSPFArea, name='interfaces')
class OSPFAreaInterfacesView(ObjectChildrenView):
    template_name = 'netbox_routing/object_children.html'
    queryset = OSPFArea.objects.all()
    child_model = OSPFInterface
    table = OSPFInterfaceTable
    filterset = OSPFInterfaceFilterSet
    tab = ViewTab(
        label='Interfaces',
        badge=lambda obj: OSPFInterface.objects.filter(area=obj).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(area=parent)


@register_model_view(OSPFArea, name='edit')
class OSPFAreaEditView(ObjectEditView):
    queryset = OSPFArea.objects.all()
    form = OSPFAreaForm


@register_model_view(OSPFArea, name='delete')
class OSPFAreaDeleteView(ObjectDeleteView):
    queryset = OSPFArea.objects.all()


class OSPFAreaBulkImportView(BulkImportView):
    queryset = OSPFArea.objects.all()
    model_form = OSPFAreaImportForm


#
# Interface
#
@register_model_view(OSPFInterface, name='list')
class OSPFInterfaceListView(ObjectListView):
    queryset = OSPFInterface.objects.all()
    table = OSPFInterfaceTable
    filterset = OSPFInterfaceFilterSet
    filterset_form = OSPFInterfaceFilterForm


@register_model_view(OSPFInterface)
class OSPFInterfaceView(ObjectView):
    queryset = OSPFInterface.objects.all()
    template_name = 'netbox_routing/ospfinterface.html'


@register_model_view(OSPFInterface, name='edit')
class OSPFInterfaceEditView(ObjectEditView):
    queryset = OSPFInterface.objects.all()
    form = OSPFInterfaceForm


@register_model_view(OSPFInterface, name='delete')
class OSPFInterfaceDeleteView(ObjectDeleteView):
    queryset = OSPFInterface.objects.all()


class OSPFInterfaceBulkImportView(BulkImportView):
    queryset = OSPFInterface.objects.all()
    model_form = OSPFInterfaceImportForm


class OSPFInterfaceBulkEditView(BulkEditView):
    queryset = OSPFInterface.objects.all()
    filterset = OSPFInterfaceFilterSet
    table = OSPFInterfaceTable
    form = OSPFInterfaceBulkEditForm


class OSPFInterfaceBulkDeleteView(BulkDeleteView):
    queryset = OSPFInterface.objects.all()
    filterset = OSPFInterfaceFilterSet
    table = OSPFInterfaceTable
