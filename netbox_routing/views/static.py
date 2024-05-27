from dcim.filtersets import DeviceFilterSet
from dcim.models import Device
from dcim.tables import DeviceTable
from netbox.views.generic import ObjectListView, ObjectEditView, ObjectView, ObjectDeleteView, ObjectChildrenView
from netbox_routing.filtersets.static import StaticRouteFilterSet
from netbox_routing.forms import StaticRouteForm
from netbox_routing.forms.filtersets.static import StaticRouteFilterForm
from netbox_routing.models import StaticRoute
from netbox_routing.tables.static import StaticRouteTable


__all__ = (
    'StaticRouteListView',
    'StaticRouteView',
    'StaticRouteDevicesView',
    'StaticRouteEditView',
    'StaticRouteDeleteView',
)

from utilities.views import register_model_view, ViewTab


@register_model_view(StaticRoute, name='list')
class StaticRouteListView(ObjectListView):
    queryset = StaticRoute.objects.all()
    table = StaticRouteTable
    filterset = StaticRouteFilterSet
    filterset_form = StaticRouteFilterForm


@register_model_view(StaticRoute)
class StaticRouteView(ObjectView):
    queryset = StaticRoute.objects.all()
    template_name = 'netbox_routing/staticroute.html'


@register_model_view(StaticRoute, name='devices')
class StaticRouteDevicesView(ObjectChildrenView):
    template_name = 'netbox_routing/staticroute_devices.html'
    queryset = StaticRoute.objects.all()
    child_model = Device
    table = DeviceTable
    filterset = DeviceFilterSet
    tab = ViewTab(
        label='Assigned Devices',
        badge=lambda obj: Device.objects.filter(static_routes=obj).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.filter(static_routes=parent)


@register_model_view(StaticRoute, name='edit')
class StaticRouteEditView(ObjectEditView):
    queryset = StaticRoute.objects.all()
    form = StaticRouteForm


@register_model_view(StaticRoute, name='delete')
class StaticRouteDeleteView(ObjectDeleteView):
    queryset = StaticRoute.objects.all()
