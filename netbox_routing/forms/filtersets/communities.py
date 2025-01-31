from django.utils.translation import gettext as _

from netbox.forms import NetBoxModelFilterSetForm
from utilities.forms.fields import DynamicModelMultipleChoiceField, TagFilterField

from tenancy.models import Tenant

from netbox_routing.models.communities import *
from utilities.forms.rendering import FieldSet


__all__ = (
    'CommunityListFilterForm',
    'CommunityFilterForm',
)


class CommunityListFilterForm(NetBoxModelFilterSetForm):
    tenant_id = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        selector=True,
        label=_('Tenant')
    )
    community_id = DynamicModelMultipleChoiceField(
        queryset=Community.objects.all(),
        required=False,
        selector=True,
        label=_('Community')
    )

    model = CommunityList
    fieldsets = (
       FieldSet('q', 'filter_id', 'tag', 'tenant_id', 'community_id'),
    )
    tag = TagFilterField(model)


class CommunityFilterForm(NetBoxModelFilterSetForm):
    communinty_list_id = DynamicModelMultipleChoiceField(
        queryset=CommunityList.objects.all(),
        required=False,
        selector=True,
        label=_('Community List')
    )
    tenant_id = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        selector=True,
        label=_('Tenant')
    )

    model = CommunityList
    fieldsets = (
       FieldSet('q', 'filter_id', 'tag', 'tenant_id', 'community_list_id'),
    )
    tag = TagFilterField(model)
