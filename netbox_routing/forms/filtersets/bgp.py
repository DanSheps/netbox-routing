from django import forms
from django.utils.translation import gettext as _

from dcim.models import Device
from ipam.models import ASN, VRF, IPAddress
from netbox.forms import NetBoxModelFilterSetForm, PrimaryModelFilterSetForm
from netbox_routing.models import PrefixList, RouteMap
from tenancy.forms import TenancyFilterForm
from utilities.forms.fields import TagFilterField, DynamicModelMultipleChoiceField
from utilities.forms.rendering import FieldSet

from netbox_routing.choices.bgp import *
from netbox_routing.models.bgp import *

__all__ = (
    'BGPSettingFilterForm',
    'BGPRouterFilterForm',
    'BGPScopeFilterForm',
    'BGPAddressFamilyFilterForm',
    'BGPPeerFilterForm',
    'BGPPeerAddressFamilyFilterForm',
    'BGPPeerTemplateFilterForm',
    'BGPPolicyTemplateFilterForm',
    'BGPSessionTemplateFilterForm',
    'BFDProfileFilterForm',
)


class BGPPolicyFilterFormMixin(forms.Form):
    prefixlist_in_id = DynamicModelMultipleChoiceField(
        queryset=PrefixList.objects.all(),
        required=False,
        selector=True,
        label=_('Incoming Prefix List'),
    )
    prefixlist_out_id = DynamicModelMultipleChoiceField(
        queryset=PrefixList.objects.all(),
        required=False,
        selector=True,
        label=_('Outgoing Prefix List'),
    )
    routemap_in_id = DynamicModelMultipleChoiceField(
        queryset=RouteMap.objects.all(),
        required=False,
        selector=True,
        label=_('Incoming Route Map'),
    )
    routemap_out_id = DynamicModelMultipleChoiceField(
        queryset=RouteMap.objects.all(),
        required=False,
        selector=True,
        label=_('Outgoing Route Map'),
    )


class SessionFilterFormMixin(forms.Form):
    local_as_id = DynamicModelMultipleChoiceField(
        queryset=ASN.objects.all(),
        required=False,
        selector=True,
        label=_('Local AS'),
    )
    remote_as_id = DynamicModelMultipleChoiceField(
        queryset=ASN.objects.all(),
        required=False,
        selector=True,
        label=_('Remote AS'),
    )


class BGPSettingFilterForm(TenancyFilterForm, PrimaryModelFilterSetForm):
    model = BGPSetting
    fieldsets = (FieldSet('q', 'filter_id', 'tag'),
        FieldSet('key'),)
    tag = TagFilterField(model)


class BGPPeerTemplateFilterForm(TenancyFilterForm, PrimaryModelFilterSetForm):
    model = BGPPeerTemplate
    fieldsets = (FieldSet('q', 'filter_id', 'tag'),
        FieldSet('name'),)
    tag = TagFilterField(model)


class BGPPolicyTemplateFilterForm(BGPPolicyFilterFormMixin, TenancyFilterForm, PrimaryModelFilterSetForm):
    model = BGPPolicyTemplate
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('name'),
        FieldSet(
            'prefixlist_in_id',
            'prefixlist_out_id',
            'routemap_in_id',
            'routemap_out_id',
            name=_('Filtering'),
        ),
        FieldSet('tenant_group_id', 'tenant_id', name=_('Tenancy')),
    )
    name = forms.CharField()
    tag = TagFilterField(model)


class BGPSessionTemplateFilterForm(SessionFilterFormMixin, TenancyFilterForm, PrimaryModelFilterSetForm):
    model = BGPSessionTemplate
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('name'),
        FieldSet('enabled', 'local_as_id', 'remote_as_id', name=_('Session')),
        FieldSet('ttl', 'bfd', name=_('Parameters')),
        FieldSet('tenant_group_id', 'tenant_id', name=_('Tenancy')),
    )
    tag = TagFilterField(model)


class BGPRouterFilterForm(
    TenancyFilterForm,
    # ContactModelFilterForm,
    PrimaryModelFilterSetForm,
):
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
    fieldsets = (FieldSet('q', 'filter_id', 'tag', 'device_id', 'asn_id'),)
    tag = TagFilterField(model)


class BGPScopeFilterForm(
    TenancyFilterForm,
    # ContactModelFilterForm,
    NetBoxModelFilterSetForm,
):
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
    fieldsets = (FieldSet('q', 'filter_id', 'tag', 'router_id', 'vrf_id'),)
    tag = TagFilterField(model)


class BGPAddressFamilyFilterForm(TenancyFilterForm, NetBoxModelFilterSetForm):
    scope_id = DynamicModelMultipleChoiceField(
        queryset=BGPScope.objects.all(),
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
    fieldsets = (FieldSet('q', 'filter_id', 'tag', 'scope_id', 'address_family'),)
    tag = TagFilterField(model)


class BGPPeerFilterForm(
    TenancyFilterForm,
    # ContactModelFilterForm,
    NetBoxModelFilterSetForm,
):
    scope_id = DynamicModelMultipleChoiceField(
        queryset=BGPScope.objects.all(),
        required=False,
        selector=True,
        label=_('Scope'),
    )
    peer_id = DynamicModelMultipleChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
        selector=True,
        label=_('Peer'),
    )
    peer_group_id = DynamicModelMultipleChoiceField(
        queryset=BGPPeerTemplate.objects.all(),
        required=False,
        selector=True,
        label=_('Peer Group'),
    )
    remote_as_id = DynamicModelMultipleChoiceField(
        queryset=ASN.objects.all(),
        required=False,
        selector=True,
        label=_('Remote AS'),
    )
    local_as_id = DynamicModelMultipleChoiceField(
        queryset=ASN.objects.all(),
        required=False,
        selector=True,
        label=_('Local AS'),
    )
    model = BGPPeer
    fieldsets = (
        FieldSet(
            'q',
            'filter_id',
            'tag',
            'scope_id',
            'peer_id',
            'peer_group_id',
            'remote_as_id',
            'local_as_id',
            'status',
            'enabled',
        ),
    )
    tag = TagFilterField(model)


class BGPPeerAddressFamilyFilterForm(
    TenancyFilterForm,
    # ContactModelFilterForm,
    NetBoxModelFilterSetForm,
):
    peer_id = DynamicModelMultipleChoiceField(
        queryset=BGPPeer.objects.all(),
        required=False,
        selector=True,
        label=_('Peer'),
    )
    peer_group_id = DynamicModelMultipleChoiceField(
        queryset=BGPPeerTemplate.objects.all(),
        required=False,
        selector=True,
        label=_('Peer Group'),
    )
    address_family_id = DynamicModelMultipleChoiceField(
        queryset=BGPAddressFamily.objects.all(),
        required=False,
        selector=True,
        label=_('Address Family'),
    )
    model = BGPPeerAddressFamily
    fieldsets = (
        FieldSet(
            'q',
            'filter_id',
            'tag',
            'peer_id',
            'peer_group_id',
            'address_family_id',
            'enabled',
        ),
    )
    tag = TagFilterField(model)


class BFDProfileFilterForm(
    TenancyFilterForm,
    # ContactModelFilterForm,
    NetBoxModelFilterSetForm,
):
    model = BFDProfile
    fieldsets = (
        FieldSet(
            'q',
            'filter_id',
            'tag',
        ),
    )
    tag = TagFilterField(model)
