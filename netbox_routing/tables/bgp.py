import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox_routing.models import BGPRouter, BGPSetting, BGPScope, BGPAddressFamily


__all__ = (
    'BGPRouterTable',
    'BGPScopeTable',
    'BGPAddressFamilyTable',
    'BGPSettingTable',
)



class BGPRouterTable(NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = BGPRouter
        fields = ('pk', 'id', 'device', 'asn')
        default_columns = ('pk', 'id', 'device', 'asn')


class BGPScopeTable(NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = BGPScope
        fields = ('pk', 'id', 'router', 'vrf')
        default_columns = ('pk', 'id', 'router', 'vrf')


class BGPAddressFamilyTable(NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = BGPAddressFamily
        fields = ('pk', 'id', 'scope', 'address_family')
        default_columns = ('pk', 'id', 'scope', 'address_family')


class BGPSettingTable(NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = BGPSetting
        fields = ('pk', 'id', 'assigned_object', 'key', 'value')
        default_columns = ('pk', 'id', 'assigned_object', 'key', 'value')
