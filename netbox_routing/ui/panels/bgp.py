from django.utils.translation import gettext_lazy as _

from netbox.ui import attrs, panels
from netbox_routing.ui.attributes import ContentTypeAttribute

__all__ = (
    'BGPSettingPanel',
    'BGPPeerTemplatePanel',
    'BGPPolicyTemplatePanel',
    'BGPSessionTemplatePanel',
    'BGPPolicyFilteringPanel',
    'BGPRouterPanel',
    'BGPRouterTemplatesPanel',
    'BGPScopePanel',
    'BGPAddressFamilyPanel',
    'BGPPeerPanel',
    'BGPPeerAddressFamilyPanel',
    'BGPPeerSettingPanel',
    'BFDProfilePanel',
    'BFDProfileSessionPanel',
)


class BFDProfilePanel(panels.ObjectAttributesPanel):
    name = attrs.TextAttr('name', label=_('Name'))
    description = attrs.TextAttr('description', label=_('Description'))
    tenants = attrs.RelatedObjectAttr('tenants', linkify=True)


class BFDProfileSessionPanel(panels.ObjectAttributesPanel):
    min_rx_int = attrs.NumericAttr('min_rx_int', label=_('Min Receive'))
    min_tx_int = attrs.NumericAttr('min_tx_int', label=_('Min Transmit'))
    multiplier = attrs.NumericAttr('multiplier', label=_('Multiplier'))
    hold = attrs.NumericAttr('hold', label=_('Hold Time'))


class BGPPolicyFilteringPanel(panels.ObjectAttributesPanel):
    prefixlist_out = attrs.RelatedObjectAttr('prefixlist_out', linkify=True)
    prefixlist_in = attrs.RelatedObjectAttr('prefixlist_in', linkify=True)
    routemap_out = attrs.RelatedObjectAttr('routemap_out', linkify=True)
    routemap_in = attrs.RelatedObjectAttr('routemap_in', linkify=True)


class BGPPeerSettingPanel(panels.ObjectAttributesPanel):
    enabled = attrs.BooleanAttr('enabled', label=_('Enabled'))
    password = attrs.TextAttr('password', label=_('Password'))
    ttl = attrs.TextAttr('ttl', label=_('TTL'))
    bfd_profile = attrs.RelatedObjectAttr('bfd_profile', linkify=True)


class BGPSettingPanel(panels.ObjectAttributesPanel):
    assigned_object_type = ContentTypeAttribute('assigned_object_type', label=_('Type'))
    assigned_object = attrs.RelatedObjectAttr('assigned_object', linkify=True)
    name = attrs.TextAttr('key', label=_('Name'))
    value = attrs.TextAttr('value')


class BGPPeerTemplatePanel(panels.ObjectAttributesPanel):
    name = attrs.TextAttr('name', label=_('Name'))
    remote_as = attrs.TextAttr('remote_as', label=_('Remote AS'))
    enabled = attrs.BooleanAttr('enabled', label=_('Enabled'))
    tenant = attrs.RelatedObjectAttr('tenant', linkify=True)


class BGPPolicyTemplatePanel(panels.ObjectAttributesPanel):
    name = attrs.TextAttr('name', label=_('Name'))
    parents = attrs.RelatedObjectListAttr('parents', linkify=True)
    tenants = attrs.RelatedObjectAttr('tenants', linkify=True)


class BGPSessionTemplatePanel(panels.ObjectAttributesPanel):
    name = attrs.TextAttr('name', label=_('Name'))
    remote_as = attrs.RelatedObjectAttr('remote_as', label=_('Remote AS'), linkify=True)
    local_as = attrs.RelatedObjectAttr('local_as', label=_('Local AS'), linkify=True)
    tenants = attrs.RelatedObjectAttr('tenants', linkify=True)


class BGPRouterPanel(panels.ObjectAttributesPanel):
    name = attrs.TextAttr('name', label=_('Name'))
    assigned_object_type = ContentTypeAttribute('assigned_object_type', label=_('Type'))
    assigned_object = attrs.RelatedObjectAttr('assigned_object', linkify=True)
    asn = attrs.RelatedObjectAttr('asn', label=_('ASN'), linkify=True)
    description = attrs.TextAttr('description', label=_('Description'))
    tenants = attrs.RelatedObjectAttr('tenants', linkify=True)


class BGPRouterTemplatesPanel(panels.ObjectAttributesPanel):
    peer_templates = attrs.RelatedObjectListAttr('peer_templates', linkify=True)
    policy_templates = attrs.RelatedObjectListAttr('policy_templates', linkify=True)
    session_templates = attrs.RelatedObjectListAttr('session_templates', linkify=True)


class BGPScopePanel(panels.ObjectAttributesPanel):
    router = attrs.RelatedObjectAttr('router', linkify=True)
    vrf = attrs.RelatedObjectAttr('vrf', linkify=True)
    description = attrs.TextAttr('description', label=_('Description'))
    tenants = attrs.RelatedObjectAttr('tenants', linkify=True)


class BGPAddressFamilyPanel(panels.ObjectAttributesPanel):
    scope = attrs.RelatedObjectAttr('router', linkify=True)
    address_family = attrs.ChoiceAttr('address_family', label=_('Address Family'))
    description = attrs.TextAttr('description', label=_('Description'))
    tenants = attrs.RelatedObjectAttr('tenants', linkify=True)


class BGPPeerPanel(panels.ObjectAttributesPanel):
    scope = attrs.RelatedObjectAttr('scope', linkify=True)
    peer = attrs.RelatedObjectAttr('peer', linkify=True)
    remote_as = attrs.RelatedObjectAttr('remote_as', label=_('Remote AS'), linkify=True)
    local_as = attrs.RelatedObjectAttr('local_as', label=_('Local AS'), linkify=True)
    status = attrs.ChoiceAttr('status', label=_('Status'))
    description = attrs.TextAttr('description', label=_('Description'))
    tenants = attrs.RelatedObjectAttr('tenants', linkify=True)


class BGPPeerAddressFamilyPanel(panels.ObjectAttributesPanel):
    assigned_object = attrs.RelatedObjectAttr('assigned_object', linkify=True)
    address_family = attrs.RelatedObjectAttr(
        'address_family', linkify=True, label=_('Address Family')
    )
    enabled = attrs.BooleanAttr('enabled', label=_('Enabled'))
