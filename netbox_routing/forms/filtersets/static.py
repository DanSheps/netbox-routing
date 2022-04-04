from netbox.forms import NetBoxModelFilterSetForm
from netbox_routing.models import StaticRoute


class StaticRouteFilterSetForm(NetBoxModelFilterSetForm):
    model = StaticRoute