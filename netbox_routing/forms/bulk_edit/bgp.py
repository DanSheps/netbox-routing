from django import forms
from django.utils.translation import gettext as _

from dcim.models import Device
from ipam.models import ASN, VRF, IPAddress
from netbox.forms import NetBoxModelBulkEditForm
from netbox_routing.choices import BGPAddressFamilyChoices
from netbox_routing.models import PrefixList, RouteMap
from utilities.forms.fields import CSVModelChoiceField, CSVChoiceField, CSVModelMultipleChoiceField, \
    DynamicModelChoiceField

from tenancy.models import Tenant

from netbox_routing.models.bgp import *


__all__ = (
    'BGPRouterBulkEditForm',
    'BGPScopeBulkEditForm',
    'BGPAddressFamilyBulkEditForm',
    'BGPPeerTemplateBulkEditForm',
    'BGPPolicyTemplateBulkEditForm',
    'BGPSessionTemplateBulkEditForm',
    'BGPPeerBulkEditForm',
    'BGPPeerAddressFamilyBulkEditForm',
)

from utilities.forms.widgets import BulkEditNullBooleanSelect


class PolicyMixin:
    enabled = forms.NullBooleanField(
        label=_('Enabled'),
        widget=BulkEditNullBooleanSelect,
        required=False,
    )
    prefixlist_out = DynamicModelChoiceField(
        queryset=PrefixList.objects.all(),
        required=False,
        selector=True,
        label=_('Outbound Prefix List'),
    )
    prefixlist_in = DynamicModelChoiceField(
        queryset=PrefixList.objects.all(),
        required=False,
        selector=True,
        label=_('Inbound Prefix List'),
    )
    routemap_out = DynamicModelChoiceField(
        queryset=RouteMap.objects.all(),
        required=False,
        selector=True,
        label=_('Inbound Route Map'),
    )
    routemap_in = DynamicModelChoiceField(
        queryset=RouteMap.objects.all(),
        required=False,
        selector=True,
        label=_('OutboundRoute Map'),
    )


class TenantMixin:
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        selector=True,
        label=_('Tenant'),
    )


class BGPRouterBulkEditForm(TenantMixin, NetBoxModelBulkEditForm):
    asn = DynamicModelChoiceField(
        queryset=ASN.objects.all(),
        required=False,
        selector=True,
        label=_('ASN'),
    )

    class Meta:
        model = BGPRouter
        fields = ('asn', 'tenant', 'description', 'comments', )


class BGPScopeBulkEditForm(TenantMixin, NetBoxModelBulkEditForm):

    class Meta:
        model = BGPScope
        fields = ('tenant', 'description', 'comments', )


class BGPAddressFamilyBulkEditForm(TenantMixin, NetBoxModelBulkEditForm):

    class Meta:
        model = BGPAddressFamily
        fields = ('tenant', 'description', 'comments', )


class BGPSessionTemplateBulkEditForm(TenantMixin, NetBoxModelBulkEditForm):
    asn = DynamicModelChoiceField(
        queryset=ASN.objects.all(),
        required=False,
        selector=True,
        label=_('ASN'),
    )
    enabled = forms.NullBooleanField(
        label=_('Enabled'),
        widget=BulkEditNullBooleanSelect,
        required=False,
    )
    bfd = forms.NullBooleanField(
        label=_('BFD'),
        widget=BulkEditNullBooleanSelect,
        required=False,
    )

    class Meta:
        model = BGPSessionTemplate
        fields = ('enabled', 'asn', 'bfd', 'password', 'tenant', 'description', 'comments', )


class BGPPolicyTemplateBulkEditForm(PolicyMixin, TenantMixin, NetBoxModelBulkEditForm):
    enabled = forms.NullBooleanField(
        label=_('Enabled'),
        widget=BulkEditNullBooleanSelect,
        required=False,
    )

    class Meta:
        model = BGPPolicyTemplate
        fields = (
            'enabled', 'prefixlist_out', 'prefixlist_in', 'routemap_out', 'routemap_in', 'tenant', 'description',
            'comments',
        )


class BGPPeerTemplateBulkEditForm(TenantMixin, NetBoxModelBulkEditForm):
    remote_as = DynamicModelChoiceField(
        queryset=ASN.objects.all(),
        required=False,
        selector=True,
        label=_('Remote AS'),
    )
    enabled = forms.NullBooleanField(
        label=_('Enabled'),
        widget=BulkEditNullBooleanSelect,
        required=False,
    )

    class Meta:
        model = BGPPeerTemplate
        fields = (
            'remote_as', 'enabled', 'tenant', 'description', 'comments',
        )


class BGPPeerBulkEditForm(TenantMixin, NetBoxModelBulkEditForm):
    peer_group = DynamicModelChoiceField(
        queryset=BGPPeerTemplate.objects.all(),
        required=False,
        selector=True,
        label=_('Peer Template'),
    )
    peer_session = DynamicModelChoiceField(
        queryset=BGPSessionTemplate.objects.all(),
        required=False,
        selector=True,
        label=_('Session Template'),
    )
    remote_as = DynamicModelChoiceField(
        queryset=ASN.objects.all(),
        required=False,
        selector=True,
        label=_('Remote AS'),
    )
    local_as = DynamicModelChoiceField(
        queryset=ASN.objects.all(),
        required=False,
        selector=True,
        label=_('Local AS'),
    )
    enabled = forms.NullBooleanField(
        label=_('Enabled'),
        widget=BulkEditNullBooleanSelect,
        required=False,
    )
    bfd = forms.NullBooleanField(
        label=_('BFD'),
        widget=BulkEditNullBooleanSelect,
        required=False,
    )

    class Meta:
        model = BGPPeer
        fields = (
            'peer_group', 'peer_session', 'remote_as', 'enabled', 'local_as', 'bfd', 'password', 'tenant',
            'description', 'comments',
        )


class BGPPeerAddressFamilyBulkEditForm(PolicyMixin, TenantMixin, NetBoxModelBulkEditForm):
    peer_group = DynamicModelChoiceField(
        queryset=BGPPeerTemplate.objects.all(),
        required=False,
        selector=True,
        label=_('Peer Template'),
    )
    peer_policy = DynamicModelChoiceField(
        queryset=BGPPolicyTemplate.objects.all(),
        required=False,
        selector=True,
        label=_('Policy Template'),
    )

    class Meta:
        model = BGPPeerAddressFamily
        fields = (
            'peer_group', 'peer_policy', 'enabled', 'prefixlist_out', 'prefixlist_in', 'routemap_out', 'routemap_in',
            'tenant', 'description', 'comments',
        )
