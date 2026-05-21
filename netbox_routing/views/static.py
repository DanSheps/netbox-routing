from django.utils.translation import gettext_lazy as _

from dcim.filtersets import DeviceFilterSet
from dcim.models import Device
from dcim.tables import DeviceTable
from extras.ui.panels import TagsPanel
from netbox.views.generic import (
    ObjectListView,
    ObjectEditView,
    ObjectView,
    ObjectDeleteView,
    ObjectChildrenView,
    BulkDeleteView,
    BulkEditView,
    BulkImportView,
)
from netbox.ui import panels, layout
from utilities.views import register_model_view, ViewTab

from netbox_routing.filtersets.static import StaticRouteFilterSet
from netbox_routing.forms import StaticRouteForm
from netbox_routing.forms.bulk_edit import StaticRouteBulkEditForm
from netbox_routing.forms.filtersets.static import StaticRouteFilterForm
from netbox_routing.forms.bulk_import import StaticRouteImportForm
from netbox_routing.models import StaticRoute
from netbox_routing.tables.static import StaticRouteTable
from netbox_routing.ui import *

__all__ = (
    'StaticRouteListView',
    'StaticRouteView',
    'StaticRouteDevicesView',
    'StaticRouteEditView',
    'StaticRouteBulkEditView',
    'StaticRouteDeleteView',
    'StaticRouteBulkDeleteView',
    'StaticRouteBulkImportView',
)


@register_model_view(StaticRoute, name='list', path='', detail=False)
class StaticRouteListView(ObjectListView):
    queryset = StaticRoute.objects.all()
    table = StaticRouteTable
    filterset = StaticRouteFilterSet
    filterset_form = StaticRouteFilterForm


@register_model_view(StaticRoute)
class StaticRouteView(ObjectView):
    queryset = StaticRoute.objects.all()
    template_name = 'generic/object.html'
    layout = layout.SimpleLayout(
        left_panels=[
            StaticRoutePanel(),
            StaticRouteRoutePanel(title=_('Route Parameters')),
            TagsPanel(),
        ],
        right_panels=[
            panels.CommentsPanel(),
            panels.RelatedObjectsPanel(),
        ],
    )


@register_model_view(StaticRoute, name='devices')
class StaticRouteDevicesView(ObjectChildrenView):
    queryset = StaticRoute.objects.all()
    child_model = Device
    table = DeviceTable
    filterset = DeviceFilterSet
    tab = ViewTab(
        label='Assigned Devices',
        badge=lambda obj: Device.objects.filter(static_routes=obj).count(),
        permission='dcim.view_device',
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(static_routes=parent)


@register_model_view(StaticRoute, name='add', detail=False)
@register_model_view(StaticRoute, name='edit')
class StaticRouteEditView(ObjectEditView):
    queryset = StaticRoute.objects.all()
    form = StaticRouteForm


@register_model_view(StaticRoute, name='delete')
class StaticRouteDeleteView(ObjectDeleteView):
    queryset = StaticRoute.objects.all()


@register_model_view(StaticRoute, name='bulk_edit', detail=False)
class StaticRouteBulkEditView(BulkEditView):
    queryset = StaticRoute.objects.all()
    filterset = StaticRouteFilterSet
    table = StaticRouteTable
    form = StaticRouteBulkEditForm


@register_model_view(StaticRoute, name='bulk_delete', detail=False)
class StaticRouteBulkDeleteView(BulkDeleteView):
    queryset = StaticRoute.objects.all()
    filterset = StaticRouteFilterSet
    table = StaticRouteTable


@register_model_view(StaticRoute, name='bulk_import', detail=False)
class StaticRouteBulkImportView(BulkImportView):
    queryset = StaticRoute.objects.all()
    model_form = StaticRouteImportForm
