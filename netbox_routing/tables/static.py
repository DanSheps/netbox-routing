from netbox.tables import NetBoxTable
from netbox_routing.models import StaticRoute


class StaticRouteTable(NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = StaticRoute
        fields = ('pk', 'id', 'vrf', 'prefix', 'next_hop', 'name')
        default_columns = ('pk', 'id', 'vrf', 'prefix', 'next_hop', 'name')
