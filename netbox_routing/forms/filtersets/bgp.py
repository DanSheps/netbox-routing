from django import forms
from django.utils.translation import gettext as _

from dcim.models import Device
from ipam.models import ASN, VRF, IPAddress
from netbox.forms import NetBoxModelFilterSetForm
from tenancy.models import Tenant
from utilities.forms.fields import TagFilterField, DynamicModelMultipleChoiceField
from utilities.forms.rendering import FieldSet

from netbox_routing.choices import BGPAddressFamilyChoices
from netbox_routing.models.bgp import *


__all__ = (
    'BGPRouterFilterForm',
    'BGPScopeFilterForm',
    'BGPSessionTemplateFilterForm',
    'BGPPolicyTemplateFilterForm',
    'BGPPeerTemplateFilterForm',
    'BGPAddressFamilyFilterForm',
    'BGPPeerFilterForm',
    'BGPPeerAddressFamilyFilterForm',
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
    tenant_id = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        selector=True,
        label=_('Tenant')
    )

    model = BGPRouter
    fieldsets = (
       FieldSet('q', 'filter_id', 'tag', 'device_id', 'asn_id', 'tenant_id', ),
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
    tenant_id = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        selector=True,
        label=_('Tenant')
    )

    model = BGPScope
    fieldsets = (
       FieldSet('q', 'filter_id', 'tag', 'router_id', 'vrf_id', 'tenant_id'),
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
    tenant_id = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        selector=True,
        label=_('Tenant')
    )

    model = BGPAddressFamily
    fieldsets = (
       FieldSet('q', 'filter_id', 'tag', 'scope_id', 'address_family', 'tenant_id', ),
    )
    tag = TagFilterField(model)


class BGPSessionTemplateFilterForm(NetBoxModelFilterSetForm):
    router_id = DynamicModelMultipleChoiceField(
        queryset=BGPRouter.objects.all(),
        required=False,
        selector=True,
        label=_('Router'),
    )
    parent_id = DynamicModelMultipleChoiceField(
        queryset=BGPSessionTemplate.objects.all(),
        required=False,
        selector=True,
        label=_('Parent Session Template'),
    )
    tenant_id = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        selector=True,
        label=_('Tenant')
    )

    model = BGPSessionTemplate
    fieldsets = (
       FieldSet('q', 'filter_id', 'tag', 'router_id', 'parent_id', 'tenant_id', ),
    )
    tag = TagFilterField(model)


class BGPPolicyTemplateFilterForm(NetBoxModelFilterSetForm):
    router_id = DynamicModelMultipleChoiceField(
        queryset=BGPRouter.objects.all(),
        required=False,
        selector=True,
        label=_('Router'),
    )
    tenant_id = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        selector=True,
        label=_('Tenant')
    )

    model = BGPPolicyTemplate
    fieldsets = (
       FieldSet('q', 'filter_id', 'tag', 'router_id', 'tenant_id', ),
    )
    tag = TagFilterField(model)


class BGPPeerFilterForm(NetBoxModelFilterSetForm):
    peer_id = DynamicModelMultipleChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
        selector=True,
        label=_('Peer Address'),
    )
    tenant_id = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        selector=True,
        label=_('Tenant')
    )

    model = BGPPeer
    fieldsets = (
       FieldSet('q', 'filter_id', 'tag', 'peer_id', 'tenant_id', ),
    )
    tag = TagFilterField(model)


class BGPPeerTemplateFilterForm(NetBoxModelFilterSetForm):
    tenant_id = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        selector=True,
        label=_('Tenant')
    )

    model = BGPPeerTemplate
    fieldsets = (
       FieldSet('q', 'filter_id', 'tag', 'tenant_id', ),
    )
    tag = TagFilterField(model)


class BGPPeerAddressFamilyFilterForm(NetBoxModelFilterSetForm):
    peer_template_id = DynamicModelMultipleChoiceField(
        queryset=BGPPeerTemplate.objects.all(),
        required=False,
        selector=True,
        label=_('Peer'),
    )
    peer_id = DynamicModelMultipleChoiceField(
        queryset=BGPPeer.objects.all(),
        required=False,
        selector=True,
        label=_('Peer'),
    )
    tenant_id = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        selector=True,
        label=_('Tenant')
    )

    model = BGPPeerAddressFamily
    fieldsets = (
       FieldSet('q', 'filter_id', 'tag', 'peer_id', 'tenant_id', ),
    )
    tag = TagFilterField(model)


class BGPSettingFilterForm(NetBoxModelFilterSetForm):
    model = BGPSetting
    fieldsets = (
       FieldSet('q', 'filter_id', 'tag'),
    )
    tag = TagFilterField(model)
