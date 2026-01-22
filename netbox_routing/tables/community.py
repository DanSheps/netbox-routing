import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox_routing.models.community import *


__all__ = (
    'CommunityTable',
    'CommunityListTable',
    'CommunityListEntryTable',
)


class CommunityTable(NetBoxTable):
    community = tables.Column(verbose_name=_('Name'), linkify=True)
    role = tables.Column(verbose_name=_('Role'), linkify=True)

    class Meta(NetBoxTable.Meta):
        model = Community
        fields = (
            'pk',
            'id',
            'community',
            'role',
            'status',
        )
        default_columns = (
            'pk',
            'id',
            'community',
        )


class CommunityListTable(NetBoxTable):
    name = tables.Column(verbose_name=_('Name'), linkify=True)

    class Meta(NetBoxTable.Meta):
        model = CommunityList
        fields = (
            'pk',
            'id',
            'name',
        )
        default_columns = (
            'pk',
            'id',
            'name',
        )


class CommunityListEntryTable(NetBoxTable):
    community_list = tables.Column(verbose_name=_('Community List'), linkify=True)
    community = tables.Column(verbose_name=_('Community'), linkify=True)

    class Meta(NetBoxTable.Meta):
        model = CommunityListEntry
        fields = (
            'pk',
            'id',
            'community_list',
            'action',
            'community',
        )
        default_columns = (
            'pk',
            'id',
            'community_list',
            'action',
            'community',
        )
