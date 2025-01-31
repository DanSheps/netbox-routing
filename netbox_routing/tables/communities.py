import django_tables2 as tables
from django.utils.translation import gettext as _

from netbox.tables import NetBoxTable
from netbox_routing.models.communities import *


class CommunityListTable(NetBoxTable):
    tenant = tables.Column(
        verbose_name=_('Tenant'),
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = CommunityList
        fields = ('pk', 'id', 'name', 'communities', 'tenant')
        default_columns = ('pk', 'id', 'name')


class CommunityTable(NetBoxTable):
    tenant = tables.Column(
        verbose_name=_('Tenant'),
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = Community
        fields = ('pk', 'id', 'community', 'tenant')
        default_columns = ('pk', 'id', 'community')
