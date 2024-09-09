from ipam.models import VRF
from netbox.forms import NetBoxModelFilterSetForm
from netbox_routing.models import StaticRoute
from utilities.forms.fields import DynamicModelMultipleChoiceField, TagFilterField
from django.utils.translation import gettext as _

from utilities.forms.rendering import FieldSet


class StaticRouteFilterForm(NetBoxModelFilterSetForm):
    model = StaticRoute
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag', 'vrf'),
    )
    vrf = DynamicModelMultipleChoiceField(
        queryset=VRF.objects.all(),
        required=False,
        selector=True,
        label=_('VRF'),
    )
    tag = TagFilterField(model)