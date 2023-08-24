import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox_routing.models import StaticRoute


class StaticRouteTable(NetBoxTable):
    devices = tables.ManyToManyColumn(
        verbose_name=_('Devices'),
    )
    class Meta(NetBoxTable.Meta):
        model = StaticRoute
        fields = ('pk', 'id', 'devices', 'vrf', 'prefix', 'next_hop', 'name')
        default_columns = ('pk', 'id', 'devices', 'vrf', 'prefix', 'next_hop', 'name')
