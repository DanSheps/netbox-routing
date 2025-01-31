from django.utils.translation import gettext as _

from netbox.forms import NetBoxModelForm
from utilities.forms.fields import DynamicModelChoiceField, CommentField, DynamicModelMultipleChoiceField
from utilities.forms.rendering import FieldSet

from tenancy.models import Tenant

from netbox_routing.models.communities import *


__all__ = (
    'CommunityListForm',
    'CommunityForm',
)


class CommunityListForm(NetBoxModelForm):
    tenant = DynamicModelChoiceField(
        label=_('Tenant'),
        queryset=Tenant.objects.all(),
        required=False
    )
    communities = DynamicModelMultipleChoiceField(
        queryset=Community.objects.all(),
        required=True,
        selector=True,
        label=_('Communities'),
    )
    comments = CommentField()

    fieldsets = (
        FieldSet('name', 'description', 'tags', name=_('Community List')),
        FieldSet('communities', name=_('Communities')),
        FieldSet('tenant', name=_('Tenancy')),
    )

    class Meta:
        model = CommunityList
        fields = ('name', 'communities', 'tenant', 'description', 'comments', )


class CommunityForm(NetBoxModelForm):
    tenant = DynamicModelChoiceField(
        label=_('Tenant'),
        queryset=Tenant.objects.all(),
        required=False
    )
    comments = CommentField()

    fieldsets = (
        FieldSet('community', 'description', 'tags', name=_('Community')),
        FieldSet('tenant', name=_('Tenancy')),
    )

    class Meta:
        model = Community
        fields = ('community', 'tenant', 'description', 'comments', )
