from django import forms
from django.utils.translation import gettext as _

from dcim.models import Device
from ipam.models import ASN, VRF, IPAddress
from netbox.forms import NetBoxModelImportForm
from netbox_routing.choices import BGPAddressFamilyChoices
from netbox_routing.models import PrefixList, RouteMap
from utilities.forms.fields import CSVModelChoiceField, CSVChoiceField, CSVModelMultipleChoiceField

from tenancy.models import Tenant

from netbox_routing.models.bgp import *


__all__ = (
    'BGPRouterImportForm',
    'BGPScopeImportForm',
    'BGPAddressFamilyImportForm',
    'BGPPeerTemplateImportForm',
    'BGPPolicyTemplateImportForm',
    'BGPSessionTemplateImportForm',
    'BGPPeerImportForm',
    'BGPPeerAddressFamilyImportForm',
)


class BGPRouterImportForm(NetBoxModelImportForm):
    device = CSVModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label=_('Device'),
    )
    asn = CSVModelChoiceField(
        queryset=ASN.objects.all(),
        required=False,
        label=_('ASN'),
    )
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        label=_('Tenant'),
    )

    class Meta:
        model = BGPRouter
        fields = ('device', 'asn', 'tenant', 'description', 'comments', )


class BGPScopeImportForm(NetBoxModelImportForm):
    router = CSVModelChoiceField(
        queryset=BGPRouter.objects.all(),
        required=False,
        label=_('Router'),
    )
    vrf = CSVModelChoiceField(
        queryset=VRF.objects.all(),
        required=False,
        label=_('VRF'),
    )
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        label=_('Tenant'),
    )

    class Meta:
        model = BGPScope
        fields = ('router', 'vrf', 'tenant', 'description', 'comments', )


class BGPAddressFamilyImportForm(NetBoxModelImportForm):
    scope = CSVModelChoiceField(
        queryset=BGPScope.objects.all(),
        required=False,
        label=_('Scope'),
    )
    address_family = CSVChoiceField(
        choices=BGPAddressFamilyChoices,
        required=False,
        label=_('Address Family'),
    )
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        label=_('Tenant'),
    )

    class Meta:
        model = BGPAddressFamily
        fields = ('scope', 'address_family', 'tenant', 'description', 'comments', )


class BGPSessionTemplateImportForm(NetBoxModelImportForm):
    router = CSVModelChoiceField(
        queryset=BGPRouter.objects.all(),
        required=False,
        label=_('Router'),
    )
    parent = CSVModelChoiceField(
        queryset=BGPSessionTemplate.objects.all(),
        required=False,
        label=_('Session Template'),
    )
    asn = CSVModelChoiceField(
        queryset=ASN.objects.all(),
        required=False,
        label=_('ASN'),
    )
    enabled = forms.BooleanField(
        label=_('Enabled'),
        required=False,
    )
    bfd = forms.BooleanField(
        label=_('BFD'),
        required=False,
    )
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        label=_('Tenant'),
    )

    class Meta:
        model = BGPSessionTemplate
        fields = (
            'name', 'router', 'parent', 'enabled', 'asn', 'bfd', 'password', 'tenant', 'description', 'comments',
        )


class BGPPolicyTemplateImportForm(NetBoxModelImportForm):
    router = CSVModelChoiceField(
        queryset=BGPRouter.objects.all(),
        required=False,
        label=_('Router'),
    )
    parents = CSVModelMultipleChoiceField(
        queryset=BGPSessionTemplate.objects.all(),
        required=False,
        label=_('Session Template'),
    )
    prefixlist_out = CSVModelChoiceField(
        queryset=PrefixList.objects.all(),
        required=False,
        label=_('Prefix List'),
    )
    prefixlist_in = CSVModelChoiceField(
        queryset=PrefixList.objects.all(),
        required=False,
        label=_('Prefix List'),
    )
    routemap_out = CSVModelChoiceField(
        queryset=RouteMap.objects.all(),
        required=False,
        label=_('Route Map'),
    )
    routemap_in = CSVModelChoiceField(
        queryset=RouteMap.objects.all(),
        required=False,
        label=_('Route Map'),
    )
    enabled = forms.BooleanField(
        label=_('Enabled'),
        required=False,
    )
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        label=_('Tenant'),
    )

    class Meta:
        model = BGPPolicyTemplate
        fields = (
            'name', 'router', 'parents', 'enabled', 'prefixlist_out', 'prefixlist_in', 'routemap_out', 'routemap_in',
            'tenant', 'description', 'comments',
        )


class BGPPeerTemplateImportForm(NetBoxModelImportForm):
    remote_as = CSVModelChoiceField(
        queryset=ASN.objects.all(),
        required=False,
        label=_('Remote AS'),
    )
    enabled = forms.BooleanField(
        label=_('Enabled'),
        required=False,
    )
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        label=_('Tenant'),
    )

    class Meta:
        model = BGPPeerTemplate
        fields = (
            'name', 'remote_as', 'enabled', 'tenant', 'description', 'comments',
        )


class BGPPeerImportForm(NetBoxModelImportForm):
    scope = CSVModelChoiceField(
        queryset=BGPScope.objects.all(),
        required=False,
        label=_('Scope'),
    )
    peer = CSVModelChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
        label=_('Peer IP Address'),
    )
    peer_group = CSVModelChoiceField(
        queryset=BGPPeerTemplate.objects.all(),
        required=False,
        label=_('Peer Template'),
    )
    peer_session = CSVModelChoiceField(
        queryset=BGPSessionTemplate.objects.all(),
        required=False,
        label=_('Session Template'),
    )
    remote_as = CSVModelChoiceField(
        queryset=ASN.objects.all(),
        required=False,
        label=_('Remote AS'),
    )
    local_as = CSVModelChoiceField(
        queryset=ASN.objects.all(),
        required=False,
        label=_('Local AS'),
    )
    enabled = forms.BooleanField(
        label=_('Enabled'),
        required=False,
    )
    bfd = forms.BooleanField(
        label=_('BFD'),
        required=False,
    )
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        label=_('Tenant'),
    )

    class Meta:
        model = BGPPeer
        fields = (
            'scope', 'peer', 'peer_group', 'peer_session', 'remote_as', 'enabled', 'local_as', 'bfd', 'password',
            'tenant', 'description', 'comments',
        )


class BGPPeerAddressFamilyImportForm(NetBoxModelImportForm):
    peer = CSVModelChoiceField(
        queryset=BGPPeer.objects.all(),
        required=False,
        label=_('Peer'),
    )
    peer_group = CSVModelChoiceField(
        queryset=BGPPeerTemplate.objects.all(),
        required=False,
        label=_('Peer Template'),
    )
    address_family = CSVModelChoiceField(
        queryset=BGPAddressFamily.objects.all(),
        required=False,
        label=_('Session Template'),
    )
    peer_policy = CSVModelChoiceField(
        queryset=BGPPolicyTemplate.objects.all(),
        required=False,
        label=_('Policy Template'),
    )
    prefixlist_out = CSVModelChoiceField(
        queryset=PrefixList.objects.all(),
        required=False,
        label=_('Prefix List'),
    )
    prefixlist_in = CSVModelChoiceField(
        queryset=PrefixList.objects.all(),
        required=False,
        label=_('Prefix List'),
    )
    routemap_out = CSVModelChoiceField(
        queryset=RouteMap.objects.all(),
        required=False,
        label=_('Route Map'),
    )
    routemap_in = CSVModelChoiceField(
        queryset=RouteMap.objects.all(),
        required=False,
        label=_('Route Map'),
    )
    enabled = forms.BooleanField(
        label=_('Enabled'),
        required=False,
    )
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        label=_('Tenant'),
    )

    class Meta:
        model = BGPPeerAddressFamily
        fields = (
            'peer', 'peer_group', 'address_family', 'peer_policy', 'enabled', 'prefixlist_out', 'prefixlist_in',
            'routemap_out', 'routemap_in', 'tenant', 'description', 'comments',
        )
    def __init__(self, data=None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        if data:
            # Limit interface queryset by assigned device
            if data.get('peer'):
                self.fields['peer'].queryset = BGPPeer.objects.filter(pk=data['peer'])
            # Limit interface queryset by assigned device
            elif data.get('peer_group'):
                self.fields['interface'].queryset = BGPPeerTemplate.objects.filter(pk=data['peer_group'])

    def save(self, *args, **kwargs):

        # Set interface assignment
        if self.cleaned_data.get('peer'):
            self.instance.assigned_object = self.cleaned_data['peer']
        elif self.cleaned_data.get('peer_group'):
            self.instance.assigned_object = self.cleaned_data['peer_group']
