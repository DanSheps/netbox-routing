from django.utils.translation import gettext as _

from netbox.forms import PrimaryModelForm
from tenancy.forms import TenancyForm
from utilities.forms.rendering import FieldSet

from netbox_routing.models.community import *

__all__ = (
    'CommunityListForm',
    'CommunityListEntryForm',
    'CommunityForm',
)


class CommunityListForm(TenancyForm, PrimaryModelForm):

    fieldsets = (
        FieldSet('name', 'description'),
        FieldSet('tenant_group', 'tenant', name=_('Tenancy')),
    )

    class Meta:
        model = CommunityList
        fields = [
            'name',
            'tenant_group',
            'tenant',
            'description',
            'comments',
            'tags',
            'owner',
        ]


class CommunityForm(TenancyForm, PrimaryModelForm):

    fieldsets = (
        FieldSet('community', 'status', 'role', 'description'),
        FieldSet('tenant_group', 'tenant', name=_('Tenancy')),
    )

    class Meta:
        model = Community
        fields = [
            'community',
            'status',
            'role',
            'tenant_group',
            'tenant',
            'description',
            'comments',
            'tags',
            'owner',
        ]


class CommunityListEntryForm(PrimaryModelForm):

    fieldsets = (FieldSet('community_list', 'action', 'community', 'description'),)

    class Meta:
        model = CommunityListEntry
        fields = [
            'community_list',
            'action',
            'community',
            'description',
            'comments',
            'tags',
            'owner',
        ]
