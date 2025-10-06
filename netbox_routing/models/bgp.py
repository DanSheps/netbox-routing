from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from netbox.models import PrimaryModel
from netbox_routing.choices.bgp import *
from netbox_routing.constants.bgp import *


class BGPSetting(PrimaryModel):
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

    def __str__(self):
        return f'{self.assigned_object}: {self.key}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:bgpsetting', args=[self.pk])


class BGPRouter(PrimaryModel):
    device = models.ForeignKey(
        verbose_name=_('Device'),
        to='dcim.Device',
        on_delete=models.PROTECT,
        related_name='router',
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

    clone_fields = (
        'device',
        'asn',
    )
    prerequisite_models = (
        'dcim.Device',
        'ipam.ASN',
    )

    class Meta:
        verbose_name = 'BGP Router'

    def __str__(self):
        return f'{self.device} ({self.asn})'

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

    def __str__(self):
        return f'{self.router}: {self.vrf or "Global VRF"}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:bgpscope', args=[self.pk])


class BGPAddressFamily(PrimaryModel):
    scope = models.ForeignKey(
        verbose_name=_('Scope'),
        to=BGPScope,
        on_delete=models.PROTECT,
        related_name='address_families',
    )
    address_family = models.CharField(
        verbose_name=_('Address Family'), max_length=50, choices=BGPAddressFamilyChoices
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

    def __str__(self):
        return f'{self.scope} ({self.get_address_family_display()})'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:bgpaddressfamily', args=[self.pk])


class BGPSessionTemplate(PrimaryModel):
    name = models.CharField(verbose_name=_('Name'), max_length=255)
    router = models.ForeignKey(
        verbose_name=_('Router'),
        to=BGPRouter,
        on_delete=models.PROTECT,
        related_name='session_templates',
    )
    parent = models.ForeignKey(
        verbose_name=_('Parent'),
        to='netbox_routing.BGPSessionTemplate',
        on_delete=models.PROTECT,
        related_name='children',
        blank=True,
        null=True,
    )
    enabled = models.BooleanField(verbose_name=_('Enabled'), blank=True, null=True)
    asn = models.ForeignKey(
        verbose_name=_('ASN'),
        to='ipam.ASN',
        on_delete=models.PROTECT,
        related_name='session_templates',
        blank=True,
        null=True,
    )
    bfd = models.CharField(
        verbose_name=_('BFD'),
        max_length=50,
        choices=BFDChoices,
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
        'router',
        'parent',
        'enabled',
        'asn',
        'bfd',
        'password',
    )
    prerequisite_models = ('netbox_routing.BGPRouter',)

    class Meta:
        verbose_name = 'BGP Session Template'


class BGPPolicyTemplate(PrimaryModel):
    name = models.CharField(verbose_name=_('Name'), max_length=255)
    router = models.ForeignKey(
        to=BGPRouter,
        on_delete=models.PROTECT,
        related_name='policy_templates',
        blank=False,
        null=False,
    )
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
        'router',
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


class BGPPeerTemplate(PrimaryModel):
    name = models.CharField(verbose_name=_('Name'), max_length=255)
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
        content_type_field='assigned_object_type',
        object_id_field='assigned_object_id',
        related_query_name='peertemplate',
    )

    clone_fields = ('name', 'remote_as', 'enabled')

    class Meta:
        verbose_name = 'BGP Peer Template'


class BGPPeer(PrimaryModel):
    scope = models.ForeignKey(
        verbose_name=_('Scope'),
        to=BGPScope,
        on_delete=models.PROTECT,
        related_name='peers',
        blank=True,
        null=True,
    )
    peer = models.OneToOneField(
        verbose_name=_('Peer Address'),
        to='ipam.IPAddress',
        on_delete=models.PROTECT,
        related_name='peers',
        blank=False,
        null=False,
    )
    peer_group = models.ForeignKey(
        verbose_name=_('Peer Group'),
        to=BGPPeerTemplate,
        on_delete=models.PROTECT,
        related_name='peers',
        blank=True,
        null=True,
    )
    peer_session = models.ForeignKey(
        verbose_name=_('Peer Session'),
        to=BGPSessionTemplate,
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
    enabled = models.BooleanField(verbose_name=_('Enabled'), blank=True, null=True)
    local_as = models.ForeignKey(
        verbose_name=_('Local AS'),
        to='ipam.ASN',
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True,
    )
    bfd = models.BooleanField(verbose_name=_('BFD'), blank=True, null=True)
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

    def __str__(self):
        return f'{self.peer} ({self.remote_as})'

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse('plugins:netbox_routing:bgppeer', args=[self.pk])


class BGPPeerAddressFamily(PrimaryModel):
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
        to=BGPAddressFamily,
        on_delete=models.PROTECT,
        related_name='address_families',
    )
    peer_policy = models.ForeignKey(
        verbose_name=_('Peer Policy'),
        to=BGPPolicyTemplate,
        on_delete=models.PROTECT,
        related_name='peer_afs',
        blank=True,
        null=True,
    )
    enabled = models.BooleanField(verbose_name=_('Enabled'), blank=True, null=True)

    prefixlist_out = models.ForeignKey(
        verbose_name=_('Outbound Prefix List'),
        to='netbox_routing.PrefixList',
        on_delete=models.PROTECT,
        related_name='peer_afs_out',
        blank=True,
        null=True,
    )
    prefixlist_in = models.ForeignKey(
        verbose_name=_('Inbound Prefix List'),
        to='netbox_routing.PrefixList',
        on_delete=models.PROTECT,
        related_name='peer_afs_in',
        blank=True,
        null=True,
    )
    routemap_out = models.ForeignKey(
        verbose_name=_('Outbound Route Map'),
        to='netbox_routing.RouteMap',
        on_delete=models.PROTECT,
        related_name='peer_afs_out',
        blank=True,
        null=True,
    )
    routemap_in = models.ForeignKey(
        verbose_name=_('Inbound Route Map'),
        to='netbox_routing.RouteMap',
        on_delete=models.PROTECT,
        related_name='peer_afs_in',
        blank=True,
        null=True,
    )
    tenant = models.ForeignKey(
        verbose_name=_('Tenant'),
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='bgp_peer_afs',
        blank=True,
        null=True,
    )

    clone_fields = (
        'address_family',
        'peer_session',
        'enabled',
        'prefixlist_out',
        'prefixlist_in',
        'routemap_out',
        'routemap_in',
    )
    prerequisite_models = (
        'netbox_routing.BGPRouter',
        'netbox_routing.BGPScope',
    )

    class Meta:
        verbose_name = 'BGP Peer Address Family'
