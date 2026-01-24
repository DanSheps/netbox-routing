from django import forms
from django.utils.translation import gettext as _

from ipam.models import Role
from netbox.forms import PrimaryModelBulkEditForm
from netbox_routing.choices import CommunityStatusChoices
from netbox_routing.forms.bulk_edit.base import TenantBulkEditMixin
from utilities.forms import add_blank_choice
from utilities.forms.fields import DynamicModelChoiceField
from utilities.forms.rendering import FieldSet

from netbox_routing.models.community import *


class CommunityBulkEditForm(TenantBulkEditMixin, PrimaryModelBulkEditForm):
    role = DynamicModelChoiceField(
        label=_('Role'),
        queryset=Role.objects.all(),
        required=False,
        selector=True,
    )
    status = forms.ChoiceField(
        label=_('Status'),
        choices=add_blank_choice(CommunityStatusChoices),
        required=False,
    )

    model = Community
    fieldsets = (
        FieldSet(
            'status',
            'role',
            'description',
        ),
        FieldSet('tenant', name=_('Tenancy')),
    )
    nullable_fields = (
        'role',
        'tenant',
        'description',
    )


class CommunityListBulkEditForm(TenantBulkEditMixin, PrimaryModelBulkEditForm):
    model = Community
    fieldsets = (
        FieldSet(
            'description',
        ),
        FieldSet('tenant', name=_('Tenancy')),
    )
    nullable_fields = (
        'description',
        'tenant',
    )


class CommunityListEntryBulkEditForm(PrimaryModelBulkEditForm):
    community_list = DynamicModelChoiceField(
        label=_('Community List'),
        queryset=CommunityList.objects.all(),
        required=False,
        selector=True,
    )
    community = DynamicModelChoiceField(
        label=_('Community'),
        queryset=Community.objects.all(),
        required=False,
        selector=True,
    )
    model = Community
    fieldsets = (
        FieldSet(
            'community_list',
            'action',
            'community',
            'description',
        ),
    )
    nullable_fields = ('description',)
