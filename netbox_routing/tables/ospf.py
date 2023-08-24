import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox_routing.models import OSPFArea, OSPFInstance, OSPFInterface


__all__ = (
    'OSPFAreaTable',
    'OSPFInstanceTable',
    'OSPFInterfaceTable',
)


class OSPFInstanceTable(NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = OSPFInstance
        fields = ('pk', 'id', 'name', 'router_id', 'process_id', 'device')
        default_columns = ('pk', 'id', 'name', 'router_id', 'process_id', 'device')


class OSPFAreaTable(NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = OSPFArea
        fields = ('pk', 'id', 'area_id')
        default_columns = ('pk', 'id', 'area_id')


class OSPFInterfaceTable(NetBoxTable):
    instance = tables.Column(
        verbose_name=_('Instance'),
        linkify=True
    )
    area = tables.Column(
        verbose_name=_('Area'),
        linkify=True
    )
    interface = tables.Column(
        verbose_name=_('Interface'),
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = OSPFInterface
        fields = ('pk', 'id', 'instance', 'area', 'interface', 'priority', 'bfd', 'authentication', 'passphrase')
        default_columns = ('pk', 'id', 'instance', 'area', 'interface')
