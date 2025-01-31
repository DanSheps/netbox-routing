from django.utils.translation import gettext as _

from netbox.forms import NetBoxModelImportForm
from utilities.forms.fields import CSVModelChoiceField

from tenancy.models import Tenant

from netbox_routing.models.communities import *


__all__ = (
    'CommunityListBulkImportForm',
    'CommunityBulkImportForm',
)


class CommunityListBulkImportForm(NetBoxModelImportForm):
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        label=_('Tenant'),
    )

    class Meta:
        model = CommunityList
        fields = ('name', 'tenant', 'description', 'comments', )


class CommunityBulkImportForm(NetBoxModelImportForm):
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        label=_('Tenant'),
    )

    class Meta:
        model = Community
        fields = ('community', 'tenant', 'description', 'comments', )
