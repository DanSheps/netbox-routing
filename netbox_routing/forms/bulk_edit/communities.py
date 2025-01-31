from django.utils.translation import gettext as _

from netbox.forms import NetBoxModelBulkEditForm
from utilities.forms.fields import DynamicModelChoiceField, CommentField, DynamicModelMultipleChoiceField
from utilities.forms.rendering import FieldSet

from tenancy.models import Tenant

from netbox_routing.models.communities import *


__all__ = (
    'CommunityListBulkEditForm',
    'CommunityBulkEditForm',
)


class CommunityListBulkEditForm(NetBoxModelBulkEditForm):
    communities = DynamicModelMultipleChoiceField(
        queryset=Community.objects.all(),
        required=True,
        selector=True,
        label=_('Communities'),
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=True,
        selector=True,
        label=_('Tenant'),
    )
    comments = CommentField()

    model = CommunityList
    fieldsets = (
        FieldSet('communities', 'tenant', 'description', 'tags'),
    )
    nullable_fields = ('communities', 'tenant', 'description', 'tags', )


class CommunityBulkEditForm(NetBoxModelBulkEditForm):
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=True,
        selector=True,
        label=_('Tenant'),
    )
    comments = CommentField()

    model = Community
    fieldsets = (
        FieldSet('tenant', 'description', 'tags'),
    )
    nullable_fields = ('tenant', 'description', 'tags', )
