from dcim.filtersets import DeviceFilterSet
from dcim.models import Device
from dcim.tables import DeviceTable
from netbox.views.generic import ObjectListView, ObjectEditView, ObjectView, ObjectDeleteView, ObjectChildrenView
from netbox_routing.filtersets.static import StaticRouteFilterSet
from netbox_routing.forms import StaticRouteForm
from netbox_routing.forms.filtersets.static import StaticRouteFilterSetForm
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
    filterset_form = StaticRouteFilterSetForm


@register_model_view(StaticRoute)
class StaticRouteView(ObjectView):
    queryset = StaticRoute.objects.all()
    template_name = 'netbox_routing/staticroute.html'

    def get_extra_context(self, request, instance):
        devices = instance.devices.all()

        devices_table = DeviceTable(
            list(devices),
            exclude=('tenant', 'device_role', 'serial', 'asset_tag', 'face', 'primary_ip', 'airflow', 'primary_ip4',
            'primary_ip6', 'cluster', 'virtual_chassis', 'vc_position', 'vc_priority', 'comments', 'contacts', 'tags',
            'created', 'last_updated',),
            orderable=False
        )

        return {
            'devices': devices_table,
        }


@register_model_view(StaticRoute, name='assignments')
class StaticRouteDevicesView(ObjectChildrenView):
    # template_name = 'dcim//.html'
    queryset = StaticRoute.objects.all()
    child_model = Device
    table = DeviceTable
    filterset = DeviceFilterSet
    actions = []
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
    pass
