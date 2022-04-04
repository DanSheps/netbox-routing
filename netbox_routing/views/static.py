from dcim.models import Device
from dcim.tables import DeviceTable
from netbox.views.generic import ObjectListView, ObjectEditView, ObjectView, ObjectDeleteView
from netbox_routing.filtersets.static import StaticRouteFilterSet
from netbox_routing.forms import StaticRouteForm
from netbox_routing.forms.filtersets.static import StaticRouteFilterSetForm
from netbox_routing.models import StaticRoute
from netbox_routing.tables.static import StaticRouteTable


__all__ = (
    'StaticRouteListView',
    'StaticRouteView',
    'StaticRouteEditView',
    'StaticRouteDeleteView',
)


class StaticRouteListView(ObjectListView):
    queryset = StaticRoute.objects.all()
    table = StaticRouteTable
    filterset = StaticRouteFilterSet
    filterset_form = StaticRouteFilterSetForm


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


class StaticRouteEditView(ObjectEditView):
    queryset = StaticRoute.objects.all()
    form = StaticRouteForm


class StaticRouteDeleteView(ObjectDeleteView):
    pass
