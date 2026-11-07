from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models import ManyToManyField
from django.urls import reverse
from django.utils.translation import gettext as _

from netbox.models import PrimaryModel
from netbox_routing.choices.bgp import *
from netbox_routing.constants.bgp import *
from netbox_routing.models.base import SearchAttributeMixin

__all__ = (
    'BGPSetting',
    'BGPPeerTemplate',
    'BGPPolicyTemplate',
    'BGPSessionTemplate',
    'BGPRouter',
    'BGPScope',
    'BGPAddressFamily',
    'BGPPeer',
    'BGPPeerAddressFamily',
    'BFDProfile',
)


class BGPSetting(SearchAttributeMixin, PrimaryModel):
    assigned_object_type = models.ForeignKey(
        verbose_name=_('Assigned Object Type'),
        to=ContentType,
        limit_choices_to=BGPSETTING_ASSIGNMENT_MODELS,
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True,
    )
    assigned_object_id = models.PositiveBigIntegerField(
        verbose_name=_('Assigned Object ID'), blank=True, null=True
    )
    assigned_object = GenericForeignKey(
        ct_field='assigned_object_type', fk_field='assigned_object_id'
    )
    key = models.CharField(
        verbose_name=_('Setting Name'),
        choices=BGPSettingChoices,
    )
    value = models.CharField(
        verbose_name=_('Setting Value'),
    )

    class Meta:
        verbose_name = 'BGP Setting'
        verbose_name_plural = 'BGP Settings'
        ordering = (
            'assigned_object_type',
            'assigned_object_id',
            'key',
            'pk',
        )
        constraints = [
            models.UniqueConstraint(
                fields=('assigned_object_type', 'assigned_object_id', 'key'),
                name='netbox_routing_bgpsettings_unique',
            ),
        ]

    def __str__(self):
        return f'{self.assigned_object}: {self.key}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:bgpsetting', args=[self.pk])


class BGPSessionTemplate(PrimaryModel):
    name = models.CharField(verbose_name=_('Name'), max_length=100)
    parent = models.ForeignKey(
        verbose_name=_('Parent'),
        to='netbox_routing.BGPSessionTemplate',
        on_delete=models.PROTECT,
        related_name='children',
        blank=True,
        null=True,
    )
    enabled = models.BooleanField(verbose_name=_('Enabled'), blank=True, null=True)
    local_as = models.ForeignKey(
        verbose_name=_('ASN'),
        to='ipam.ASN',
        on_delete=models.PROTECT,
        related_name='session_templates_local_as',
        blank=True,
        null=True,
    )
    remote_as = models.ForeignKey(
        verbose_name=_('ASN'),
        to='ipam.ASN',
        on_delete=models.PROTECT,
        related_name='session_templates_remote_as',
        blank=True,
        null=True,
    )
    ttl = models.PositiveSmallIntegerField(
        verbose_name=_('TTL'),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(255)],
    )
    bfd = models.ForeignKey(
        verbose_name=_('BFD PRofile'),
        to='netbox_routing.BFDProfile',
        on_delete=models.PROTECT,
        related_name='bgp_session_templates',
        blank=True,
        null=True,
    )
    password = models.CharField(
        verbose_name=_('Password'),
        max_length=255,
        blank=True,
        null=True,
    )
    tenant = models.ForeignKey(
        verbose_name=_('Tenant'),
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='bgp_peer_session_templates',
        blank=True,
        null=True,
    )

    clone_fields = (
        'name',
        'parent',
        'enabled',
        'remote_as',
        'local_as',
        'bfd',
        'ttl',
        'password',
        'tenant',
    )
    prerequisite_models = ('netbox_routing.BGPRouter',)

    class Meta:
        verbose_name = 'BGP Session Template'
        verbose_name_plural = 'BGP Session Templates'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=('name',),
                name='%(app_label)s_%(class)s_name',
            ),
        ]

    def __str__(self):
        return f'{self.name}'


class BGPPolicyTemplate(PrimaryModel):
    name = models.CharField(verbose_name=_('Name'), max_length=100)
    parents = models.ManyToManyField(
        verbose_name=_('Parent Policies'),
        to='netbox_routing.BGPPolicyTemplate',
        related_name='children',
    )
    enabled = models.BooleanField(verbose_name=_('Enabled'), blank=True, null=True)
    prefixlist_out = models.ForeignKey(
        verbose_name=_('Outbound Prefix List'),
        to='netbox_routing.PrefixList',
        on_delete=models.PROTECT,
        related_name='template_afs_out',
        blank=True,
        null=True,
    )
    prefixlist_in = models.ForeignKey(
        verbose_name=_('Inbound Prefix List'),
        to='netbox_routing.PrefixList',
        on_delete=models.PROTECT,
        related_name='template_afs_in',
        blank=True,
        null=True,
    )
    routemap_out = models.ForeignKey(
        verbose_name=_('Outbound Route Map'),
        to='netbox_routing.RouteMap',
        on_delete=models.PROTECT,
        related_name='template_afs_out',
        blank=True,
        null=True,
    )
    routemap_in = models.ForeignKey(
        verbose_name=_('Inbound Route Map'),
        to='netbox_routing.RouteMap',
        on_delete=models.PROTECT,
        related_name='template_afs_in',
        blank=True,
        null=True,
    )
    tenant = models.ForeignKey(
        verbose_name=_('Tenant'),
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='bgp_peer_policy_templates',
        blank=True,
        null=True,
    )

    clone_fields = (
        'name',
        'parents',
        'enabled',
        'prefixlist_out',
        'prefixlist_in',
        'routemap_out',
        'routemap_in',
    )
    prerequisite_models = ('netbox_routing.BGPRouter',)

    class Meta:
        verbose_name = 'BGP Policy Template'
        verbose_name_plural = 'BGP Policy Templates'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=('name',),
                name='%(app_label)s_%(class)s_name',
            ),
        ]

    def __str__(self):
        return f'{self.name}'


class BGPPeerTemplate(PrimaryModel):
    name = models.CharField(verbose_name=_('Name'), max_length=100)
    remote_as = models.ForeignKey(
        verbose_name=_('Remote AS'),
        to='ipam.ASN',
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True,
    )
    enabled = models.BooleanField(verbose_name=_('Enabled'), blank=True, null=True)
    tenant = models.ForeignKey(
        verbose_name=_('Tenant'),
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='bgp_peer_templates',
        blank=True,
        null=True,
    )
    address_families = GenericRelation(
        verbose_name=_('Address Families'),
        to='netbox_routing.BGPPeerAddressFamily',
        related_query_name='peer_group',
        related_name='peer_group',
        content_type_field='assigned_object_type',
        object_id_field='assigned_object_id',
    )

    clone_fields = ('name', 'remote_as', 'enabled')

    class Meta:
        verbose_name = 'BGP Peer Template'
        verbose_name_plural = 'BGP Peer Templates'
        ordering = ('name', 'pk')
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'remote_as'),
                name='%(app_label)s_%(class)s_name_remote_as',
            ),
        ]

    def __str__(self):
        return f'{self.name}'


class BGPRouter(SearchAttributeMixin, PrimaryModel):
    name = models.CharField(
        verbose_name=_('Name'), max_length=100, blank=True, null=True
    )
    assigned_object_type = models.ForeignKey(
        verbose_name=_('Assigned Object Type'),
        to=ContentType,
        limit_choices_to=BGPROUTER_ASSIGNMENT_MODEL,
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True,
    )
    assigned_object_id = models.PositiveBigIntegerField(
        verbose_name=_('Assigned Object ID'), blank=True, null=True
    )
    assigned_object = GenericForeignKey(
        ct_field='assigned_object_type', fk_field='assigned_object_id'
    )
    asn = models.ForeignKey(
        verbose_name=_('ASN'),
        to='ipam.ASN',
        on_delete=models.PROTECT,
        related_name='router',
    )
    settings = GenericRelation(
        verbose_name=_('Settings'),
        to='netbox_routing.BGPSetting',
        related_name='router',
        related_query_name='router',
        content_type_field='assigned_object_type',
        object_id_field='assigned_object_id',
    )
    tenant = models.ForeignKey(
        verbose_name=_('Tenant'),
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='bgp_routers',
        blank=True,
        null=True,
    )
    policy_templates = ManyToManyField(
        to='netbox_routing.BGPPolicyTemplate',
        related_name='routers',
        verbose_name=_('Policy Templates'),
    )
    session_templates = ManyToManyField(
        to='netbox_routing.BGPSessionTemplate',
        related_name='routers',
        verbose_name=_('Session Templates'),
    )
    peer_templates = ManyToManyField(
        to='netbox_routing.BGPPeerTemplate',
        related_name='routers',
        verbose_name=_('Peer Templates'),
    )

    clone_fields = (
        'region',
        'site_group',
        'site',
        'location',
        'device',
        'asn',
        'policy_templates',
        'session_templates',
        'peer_templates',
    )
    prerequisite_models = (
        'dcim.Device',
        'ipam.ASN',
    )

    class Meta:
        verbose_name = 'BGP Router'
        verbose_name_plural = 'BGP Routers'
        ordering = (
            'assigned_object_type',
            'assigned_object_id',
            'asn',
            'name',
        )
        constraints = [
            models.UniqueConstraint(
                fields=(
                    'assigned_object_type',
                    'assigned_object_id',
                    'asn',
                ),
                name='%(app_label)s_%(class)s_assigned_object_asn',
                nulls_distinct=False,
            ),
            models.UniqueConstraint(
                fields=(
                    'assigned_object_type',
                    'assigned_object_id',
                    'name',
                ),
                name='%(app_label)s_%(class)s_assigned_object_name',
                nulls_distinct=False,
            ),
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_identifier',
                condition=models.Q(asn__isnull=False) | models.Q(name__isnull=False),
            ),
        ]

    def clone(self):
        """
        Override clone to safely handle GenericRelations with inaccessible accessors.

        Strategy:
        1. Filter clone_fields to separate accessible and inaccessible fields
        2. Call parent clone() with only accessible fields
        3. Attempt to manually clone any inaccessible fields that have accessible accessors
        4. For non-existent fields (device, site, etc), check if assigned_object matches
           and if so, include the assignment in the clone
        """
        from django.contrib.contenttypes.fields import GenericForeignKey

        # Get the current clone_fields tuple
        original_clone_fields = getattr(self, 'clone_fields', ())
        accessible_fields = []
        inaccessible_fields = []
        pseudo_fields = []

        # Separate accessible from inaccessible fields
        for field_name in original_clone_fields:
            try:
                field = self._meta.get_field(field_name)

                # For GenericForeignKey, it's always accessible by design
                if isinstance(field, GenericForeignKey):
                    accessible_fields.append(field_name)
                    continue

                # For other fields, check if the accessor is available
                # GenericRelation fields may have related_name='+' which makes them inaccessible
                if hasattr(field, 'get_accessor_name'):
                    accessor_name = field.get_accessor_name()
                    if accessor_name and hasattr(self, accessor_name):
                        accessible_fields.append(field_name)
                    else:
                        inaccessible_fields.append(field_name)
                else:
                    # Regular fields are always accessible
                    accessible_fields.append(field_name)
            except Exception:
                # If field lookup fails, it's a pseudo-field (device, site, region, etc)
                # These refer to the type of assigned_object
                pseudo_fields.append(field_name)

        # Temporarily set clone_fields to only accessible fields and call parent
        self.clone_fields = tuple(accessible_fields)
        attrs = super().clone()

        # Restore original clone_fields
        self.clone_fields = original_clone_fields

        # Attempt to manually clone inaccessible fields that have accessible accessors
        for field_name in inaccessible_fields:
            try:
                field = self._meta.get_field(field_name)

                # Try to get the field value safely
                if hasattr(field, 'get_accessor_name'):
                    accessor_name = field.get_accessor_name()
                    if accessor_name and hasattr(self, accessor_name):
                        # Field has an accessible accessor; try to clone it
                        try:
                            field_value = field.value_from_object(self)
                            if field_value and isinstance(field, models.ManyToManyField):
                                attrs[field_name] = [v.pk for v in field_value]
                            elif field_value not in (None, ''):
                                attrs[field_name] = field_value
                        except AttributeError:
                            # If value_from_object fails, skip this field
                            pass
            except Exception:
                # If we can't process this field, skip it gracefully
                pass

        # Handle pseudo-fields (device, site, region, site_group, location)
        # These represent the type of the assigned_object
        if self.assigned_object_id is not None and self.assigned_object_type_id is not None:
            try:
                # Get the assigned object's model name (already lowercase from ContentType)
                assigned_model_name = self.assigned_object_type.model

                # Strategy 1: Check if any pseudo-field matches the assigned model type
                matched = False
                for field_name in pseudo_fields:
                    if field_name == assigned_model_name:
                        # This pseudo-field matches the assigned object type
                        attrs[field_name] = self.assigned_object.pk
                        matched = True
                        break

                # Strategy 2: If no pseudo-field matched but we have assigned_object,
                # still check all original clone_fields for matching model types
                # (in case the field was categorized differently)
                if not matched:
                    for field_name in original_clone_fields:
                        if field_name == assigned_model_name:
                            attrs[field_name] = self.assigned_object.pk
                            break

            except Exception:
                # If we can't determine the assigned object type, skip pseudo-fields
                pass

        return attrs

    def __str__(self):
        if self.name:
            if self.assigned_object:
                return f'{self.name} ({self.assigned_object}:{self.asn})'
            return f'{self.name} ({self.asn})'
        elif self.assigned_object:
            return f'{self.assigned_object}:{self.asn}'
        return f'{self.asn}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:bgprouter', args=[self.pk])


class BGPScope(PrimaryModel):
    router = models.ForeignKey(
        verbose_name=_('Router'),
        to=BGPRouter,
        on_delete=models.PROTECT,
        related_name='scopes',
        blank=False,
        null=False,
    )
    vrf = models.ForeignKey(
        verbose_name=_('VRF'),
        to='ipam.VRF',
        on_delete=models.PROTECT,
        related_name='scopes',
        blank=True,
        null=True,
    )
    tenant = models.ForeignKey(
        verbose_name=_('Tenant'),
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='bgp_scopes',
        blank=True,
        null=True,
    )

    settings = GenericRelation(
        verbose_name=_('Settings'),
        to='netbox_routing.BGPSetting',
        related_name='scope',
        related_query_name='scope',
        content_type_field='assigned_object_type',
        object_id_field='assigned_object_id',
    )

    clone_fields = (
        'router',
        'vrf',
    )
    prerequisite_models = ('netbox_routing.BGPRouter',)

    class Meta:
        verbose_name = 'BGP Scope'
        verbose_name_plural = 'BGP Scopes'
        ordering = ('router', 'vrf')
        constraints = [
            models.UniqueConstraint(
                fields=('router', 'vrf'),
                name='%(app_label)s_%(class)s_router_vrf',
                nulls_distinct=False,
            ),
        ]

    def __str__(self):
        return f'{self.router}: {self.vrf or "Global VRF"}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:bgpscope', args=[self.pk])


class BGPAddressFamily(PrimaryModel):
    scope = models.ForeignKey(
        verbose_name=_('Scope'),
        to='netbox_routing.BGPScope',
        on_delete=models.PROTECT,
        related_name='address_families',
    )
    address_family = models.CharField(
        verbose_name=_('Address Family'), max_length=50, choices=BGPAddressFamilyChoices
    )
    enabled = models.BooleanField(verbose_name=_('Enabled'), blank=True, null=True)
    prefixlist_out = models.ForeignKey(
        verbose_name=_('Outbound Prefix List'),
        to='netbox_routing.PrefixList',
        on_delete=models.PROTECT,
        related_name='address_families_out',
        blank=True,
        null=True,
    )
    prefixlist_in = models.ForeignKey(
        verbose_name=_('Inbound Prefix List'),
        to='netbox_routing.PrefixList',
        on_delete=models.PROTECT,
        related_name='address_families_in',
        blank=True,
        null=True,
    )
    routemap_out = models.ForeignKey(
        verbose_name=_('Outbound Route Map'),
        to='netbox_routing.RouteMap',
        on_delete=models.PROTECT,
        related_name='address_families_out',
        blank=True,
        null=True,
    )
    routemap_in = models.ForeignKey(
        verbose_name=_('Inbound Route Map'),
        to='netbox_routing.RouteMap',
        on_delete=models.PROTECT,
        related_name='address_families_in',
        blank=True,
        null=True,
    )
    redistribute_routemap = models.ForeignKey(
        verbose_name=_('Redistribute Connected Route Map'),
        to='netbox_routing.RouteMap',
        on_delete=models.PROTECT,
        related_name='address_families_redistribute',
        blank=True,
        null=True,
    )
    vrf_in = models.ForeignKey(
        verbose_name=_('Import VRF'),
        to='ipam.VRF',
        on_delete=models.PROTECT,
        related_name='address_families_in',
        blank=True,
        null=True,
    )
    tenant = models.ForeignKey(
        verbose_name=_('Tenant'),
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='bgp_address_families',
        blank=True,
        null=True,
    )
    settings = GenericRelation(
        verbose_name=_('Settings'),
        to='netbox_routing.BGPSetting',
        related_name='address_family',
        related_query_name='address_family',
        content_type_field='assigned_object_type',
        object_id_field='assigned_object_id',
    )

    clone_fields = (
        'scope',
        'address_family',
    )
    prerequisite_models = ('netbox_routing.BGPScope',)

    class Meta:
        verbose_name = 'BGP Address Family'
        verbose_name_plural = 'BGP Address Families'
        ordering = ('scope', 'address_family')
        constraints = [
            models.UniqueConstraint(
                fields=('scope', 'address_family'),
                name='%(app_label)s_%(class)s_scope_address_family',
            ),
        ]

    def __str__(self):
        return f'{self.scope} ({self.get_address_family_display()})'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:bgpaddressfamily', args=[self.pk])


class BGPPeer(PrimaryModel):
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=100,
        blank=True,
        null=True,
    )
    scope = models.ForeignKey(
        verbose_name=_('Scope'),
        to='netbox_routing.BGPScope',
        on_delete=models.PROTECT,
        related_name='peers',
        blank=True,
        null=True,
    )
    peer = models.ForeignKey(
        verbose_name=_('Peer Address'),
        to='ipam.IPAddress',
        on_delete=models.PROTECT,
        related_name='remote_peers',
        blank=True,
        null=True,
    )
    interface = models.ForeignKey(
        verbose_name=_('Interface'),
        to='dcim.Interface',
        on_delete=models.PROTECT,
        related_name='remote_peers',
        blank=True,
        null=True,
    )
    source = models.ForeignKey(
        verbose_name=_('Source Address'),
        to='ipam.IPAddress',
        on_delete=models.PROTECT,
        related_name='source_peers',
        blank=True,
        null=True,
    )
    peer_group = models.ForeignKey(
        verbose_name=_('Peer Group'),
        to='netbox_routing.BGPPeerTemplate',
        on_delete=models.PROTECT,
        related_name='peers',
        blank=True,
        null=True,
    )
    peer_session = models.ForeignKey(
        verbose_name=_('Peer Session'),
        to='netbox_routing.BGPSessionTemplate',
        on_delete=models.PROTECT,
        related_name='peers',
        blank=True,
        null=True,
    )
    remote_as = models.ForeignKey(
        verbose_name=_('Remote AS'),
        to='ipam.ASN',
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True,
    )
    remote_as_list = models.ManyToManyField(
        verbose_name=_('Remote AS List'),
        to='ipam.ASN',
        related_name='+',
        blank=True,
    )
    enabled = models.BooleanField(verbose_name=_('Enabled'), blank=True, null=True)
    status = models.CharField(
        verbose_name=_('Status'),
        max_length=10,
        choices=BGPStatusChoices,
        null=True,
        blank=True,
    )
    local_as = models.ForeignKey(
        verbose_name=_('Local AS'),
        to='ipam.ASN',
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True,
    )
    bfd = models.ForeignKey(
        verbose_name=_('BFD PRofile'),
        to='netbox_routing.BFDProfile',
        on_delete=models.PROTECT,
        related_name='bgp_peers',
        blank=True,
        null=True,
    )
    ttl = models.PositiveSmallIntegerField(
        verbose_name=_('TTL'),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(255)],
    )
    password = models.CharField(
        verbose_name=_('Password'), max_length=255, blank=True, null=True
    )
    tenant = models.ForeignKey(
        verbose_name=_('Tenant'),
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='bgp_peers',
        blank=True,
        null=True,
    )
    address_families = GenericRelation(
        verbose_name=_('Address Families'),
        to='netbox_routing.BGPPeerAddressFamily',
        content_type_field='assigned_object_type',
        object_id_field='assigned_object_id',
        related_query_name='peer',
    )
    settings = GenericRelation(
        verbose_name=_('Settings'),
        to='netbox_routing.BGPSetting',
        related_name='peer',
        related_query_name='peer',
        content_type_field='assigned_object_type',
        object_id_field='assigned_object_id',
    )

    clone_fields = (
        'scope',
        'remote_as',
        'local_as',
        'enabled',
        'bfd',
        'password',
    )
    prerequisite_models = (
        'netbox_routing.BGPRouter',
        'netbox_routing.BGPScope',
    )

    class Meta:
        verbose_name = 'BGP Peer'
        verbose_name_plural = 'BGP Peers'
        ordering = (
            'scope',
            'peer',
            'interface',
            'name',
            'pk',
        )
        constraints = [
            models.UniqueConstraint(
                fields=('scope', 'peer'),
                condition=Q(peer__isnull=False),
                name='%(app_label)s_%(class)s_scope_peer_unique',
            ),
            models.UniqueConstraint(
                fields=('scope', 'interface'),
                condition=Q(interface__isnull=False),
                name='%(app_label)s_%(class)s_scope_interface_unique',
            ),
        ]

    def clean(self):
        super().clean()

        has_peer = self.peer is not None
        has_interface = self.interface is not None

        if has_peer and has_interface:
            raise ValidationError(
                {
                    'peer': 'Cannot have a Peer IP and a Peer Interface on the same BGP Peer',
                    'interface': 'Cannot have a Peer IP and a Peer Interface on the same BGP Peer',
                }
            )

        if not (has_peer or has_interface):
            raise ValidationError(
                {
                    'peer': 'Either peer or interface must be set.',
                    'interface': 'Either peer or interface must be set.',
                }
            )

        remote_as = self.remote_as
        remote_as_list = getattr(self, '_m2m_values', {}).get('remote_as_list')
        if remote_as_list is None:
            if self._state.adding:
                remote_as_list = []
            else:
                remote_as_list = list(self.remote_as_list.all())

        if remote_as and remote_as_list:
            raise ValidationError(
                {
                    'remote_as': 'Cannot have both a Remote AS and a Remote AS List.',
                    'remote_as_list': 'Cannot have both a Remote AS and a Remote AS List.',
                }
            )

    def __str__(self):
        if self.peer is not None:
            peer = self.peer
        elif self.interface is not None:
            peer = self.interface
        else:
            peer = self.name or 'Unknown peer'

        if self.remote_as:
            return f'{peer} ({self.remote_as})'
        return str(peer)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse('plugins:netbox_routing:bgppeer', args=[self.pk])


class BGPPeerAddressFamily(SearchAttributeMixin, PrimaryModel):
    assigned_object_type = models.ForeignKey(
        verbose_name=_('Assigned Object Type'),
        to=ContentType,
        limit_choices_to=BGPPEERAF_ASSIGNMENT_MODELS,
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True,
    )
    assigned_object_id = models.PositiveBigIntegerField(
        verbose_name=_('Assigned Object ID'), blank=True, null=True
    )
    assigned_object = GenericForeignKey(
        ct_field='assigned_object_type', fk_field='assigned_object_id'
    )
    address_family = models.ForeignKey(
        verbose_name=_('Address Family'),
        to='netbox_routing.BGPAddressFamily',
        on_delete=models.PROTECT,
        related_name='peer_address_families',
    )
    peer_policy = models.ForeignKey(
        verbose_name=_('Peer Policy'),
        to='netbox_routing.BGPPolicyTemplate',
        on_delete=models.PROTECT,
        related_name='peer_address_families',
        blank=True,
        null=True,
    )
    enabled = models.BooleanField(verbose_name=_('Enabled'), blank=True, null=True)

    prefixlist_out = models.ForeignKey(
        verbose_name=_('Outbound Prefix List'),
        to='netbox_routing.PrefixList',
        on_delete=models.PROTECT,
        related_name='peer_address_families_out',
        blank=True,
        null=True,
    )
    prefixlist_in = models.ForeignKey(
        verbose_name=_('Inbound Prefix List'),
        to='netbox_routing.PrefixList',
        on_delete=models.PROTECT,
        related_name='peer_address_families_in',
        blank=True,
        null=True,
    )
    routemap_out = models.ForeignKey(
        verbose_name=_('Outbound Route Map'),
        to='netbox_routing.RouteMap',
        on_delete=models.PROTECT,
        related_name='peer_address_families_out',
        blank=True,
        null=True,
    )
    routemap_in = models.ForeignKey(
        verbose_name=_('Inbound Route Map'),
        to='netbox_routing.RouteMap',
        on_delete=models.PROTECT,
        related_name='peer_address_families_in',
        blank=True,
        null=True,
    )
    tenant = models.ForeignKey(
        verbose_name=_('Tenant'),
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='bgp_peer_address_families',
        blank=True,
        null=True,
    )
    settings = GenericRelation(
        verbose_name=_('Settings'),
        to='netbox_routing.BGPSetting',
        related_name='peer_address_families',
        related_query_name='peer_address_families',
        content_type_field='assigned_object_type',
        object_id_field='assigned_object_id',
    )

    clone_fields = (
        'address_family',
        'peer_policy',
        'enabled',
        'prefixlist_out',
        'prefixlist_in',
        'routemap_out',
        'routemap_in',
        'tenant',
    )
    prerequisite_models = (
        'netbox_routing.BGPRouter',
        'netbox_routing.BGPScope',
    )

    class Meta:
        verbose_name = 'BGP Peer Address Family'
        verbose_name_plural = 'BGP Peer Address Families'
        ordering = (
            'assigned_object_type',
            'assigned_object_id',
            'address_family',
            'pk',
        )
        constraints = [
            models.UniqueConstraint(
                fields=('assigned_object_type', 'assigned_object_id', 'address_family'),
                name='%(app_label)s_%(class)s_assigned_object_address_family',
            ),
        ]

    def __str__(self):
        return f'{self.assigned_object} ({self.address_family})'


class BFDProfile(PrimaryModel):
    name = models.CharField(verbose_name=_('Name'), max_length=100)
    min_tx_int = models.PositiveIntegerField(
        verbose_name=_('Min TX Interval'),
        validators=[MinValueValidator(60), MaxValueValidator(60000)],
    )
    min_rx_int = models.PositiveIntegerField(
        verbose_name=_('Min RX Interval'),
        validators=[MinValueValidator(60), MaxValueValidator(60000)],
    )
    multiplier = models.PositiveSmallIntegerField(
        verbose_name=_('Multiplier'),
        validators=[MinValueValidator(0), MaxValueValidator(255)],
    )
    hold = models.PositiveIntegerField(
        verbose_name=_('Hold Time'),
        blank=True,
        null=True,
        validators=[MinValueValidator(60), MaxValueValidator(60000)],
    )
    tenant = models.ForeignKey(
        verbose_name=_('Tenant'),
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='bfd_profiles',
        blank=True,
        null=True,
    )

    clone_fields = ('tenant',)
    prerequisite_models = (
        'netbox_routing.BGPRouter',
        'netbox_routing.BGPScope',
    )

    class Meta:
        verbose_name = 'BFD Profile'
        verbose_name_plural = 'BFD Profiles'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=('name',),
                name='%(app_label)s_%(class)s_name',
            ),
        ]

    def __str__(self):
        return f'{self.name}'
