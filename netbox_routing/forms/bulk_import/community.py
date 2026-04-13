from django.utils.translation import gettext as _

from ipam.models import Role
from netbox.forms import NetBoxModelImportForm
from tenancy.models import Tenant
from utilities.forms.fields import CSVModelChoiceField

from netbox_routing.models.community import Community, CommunityList, CommunityListEntry

__all__ = (
    'CommunityImportForm',
    'CommunityListImportForm',
    'CommunityListEntryImportForm',
)


class CommunityImportForm(NetBoxModelImportForm):
    role = CSVModelChoiceField(
        queryset=Role.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Role name'),
    )
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Tenant name'),
    )

    class Meta:
        model = Community
        fields = (
            'community', 'status', 'role', 'tenant',
            'description', 'comments', 'tags',
        )


class CommunityListImportForm(NetBoxModelImportForm):
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Tenant name'),
    )

    class Meta:
        model = CommunityList
        fields = (
            'name', 'tenant',
            'description', 'comments', 'tags',
        )


class CommunityListEntryImportForm(NetBoxModelImportForm):
    community_list = CSVModelChoiceField(
        queryset=CommunityList.objects.all(),
        required=True,
        to_field_name='name',
        help_text=_('Community list name'),
    )
    community = CSVModelChoiceField(
        queryset=Community.objects.all(),
        required=True,
        to_field_name='community',
        help_text=_('Community value'),
    )

    class Meta:
        model = CommunityListEntry
        fields = (
            'community_list', 'action', 'community',
            'description', 'comments', 'tags',
        )
