from django import forms
from django.utils.translation import gettext as _

from dcim.models import Device
from ipam.models import ASN, VRF
from netbox.forms import NetBoxModelFilterSetForm
from netbox_routing.choices import BGPAddressFamilyChoices
from netbox_routing.models import BGPRouter, BGPSetting, BGPAddressFamily, BGPScope
from utilities.forms.fields import TagFilterField, DynamicModelMultipleChoiceField


__all__ = (
    'BGPRouterFilterForm',
    'BGPScopeFilterForm',
    'BGPAddressFamilyFilterForm',
    'BGPSettingFilterForm',
)


class BGPRouterFilterForm(NetBoxModelFilterSetForm):
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_('Device'),
    )
    asn_id = DynamicModelMultipleChoiceField(
        queryset=ASN.objects.all(),
        required=False,
        selector=True,
        label=_('ASN'),
    )
    model = BGPRouter
    fieldsets = (
        (None, ('q', 'filter_id', 'tag', 'device_id', 'asn_id')),
    )
    tag = TagFilterField(model)


class BGPScopeFilterForm(NetBoxModelFilterSetForm):
    router_id = DynamicModelMultipleChoiceField(
        queryset=BGPRouter.objects.all(),
        required=False,
        selector=True,
        label=_('Router'),
    )
    vrf_id = DynamicModelMultipleChoiceField(
        queryset=VRF.objects.all(),
        required=False,
        selector=True,
        label=_('VRF'),
    )
    model = BGPScope
    fieldsets = (
        (None, ('q', 'filter_id', 'tag', 'router_id', 'vrf_id')),
    )
    tag = TagFilterField(model)


class BGPAddressFamilyFilterForm(NetBoxModelFilterSetForm):
    scope_id = DynamicModelMultipleChoiceField(
        queryset=BGPRouter.objects.all(),
        required=False,
        selector=True,
        label=_('Router'),
    )
    address_family = forms.MultipleChoiceField(
        choices=BGPAddressFamilyChoices,
        required=False,
        label=_('Address Family'),
    )
    model = BGPAddressFamily
    fieldsets = (
        (None, ('q', 'filter_id', 'tag', 'scope_id', 'address_family')),
    )
    tag = TagFilterField(model)


class BGPSettingFilterForm(NetBoxModelFilterSetForm):
    model = BGPSetting
    fieldsets = (
        (None, ('q', 'filter_id', 'tag', )),
    )
    tag = TagFilterField(model)
