from django import forms
from django.utils.translation import gettext as _

from tenancy.models import Tenant
from utilities.forms.fields import DynamicModelChoiceField

__all__ = ('TenantBulkEditMixin',)


class TenantBulkEditMixin(forms.Form):
    tenant = DynamicModelChoiceField(
        label=_('Tenant'), queryset=Tenant.objects.all(), required=False
    )


class EnableMixin(forms.Form):
    enabled = forms.BooleanField(label=_('Enabled'), required=False)
