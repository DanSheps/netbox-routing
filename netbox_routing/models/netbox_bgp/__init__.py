from django.db import models
from taggit.managers import TaggableManager

from ipam.fields import IPNetworkField
from netbox.models import NetBoxModel


class AbsoluteURLMixin:
    def get_absolute_url(self):
        return None


class ASPathList(AbsoluteURLMixin, NetBoxModel):
    """
    as-path access list, as-path filter
    """

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        app_label = 'netbox_bgp'
        managed = False

    def __str__(self):
        return self.name


class TagMixin:
    tags = TaggableManager(
        through='extras.TaggedItem', ordering=('weight', 'name'), related_name='+'
    )


class ASPathListRule(AbsoluteURLMixin, NetBoxModel):
    aspath_list = models.ForeignKey(
        to=ASPathList, on_delete=models.CASCADE, related_name='aspathlistrules'
    )
    index = models.PositiveIntegerField()
    action = models.CharField(max_length=30)
    pattern = models.CharField(
        max_length=200,
    )
    description = models.CharField(max_length=200, blank=True)
    comments = models.TextField(blank=True)

    def __str__(self):
        return f'{self.aspath_list}: {self.action} {self.pattern}'

    class Meta:
        app_label = 'netbox_bgp'
        managed = False


class RoutingPolicy(AbsoluteURLMixin, NetBoxModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    comments = models.TextField(blank=True)
    weight = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'netbox_bgp'
        managed = False


class BGPPeerGroup(AbsoluteURLMixin, NetBoxModel):
    """ """

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Peer Groups'
        unique_together = ['name', 'description']
        ordering = ['name']
        app_label = 'netbox_bgp'
        managed = False

    def __str__(self):
        return self.name


class BGPBase(AbsoluteURLMixin, NetBoxModel):
    """ """

    site = models.ForeignKey(
        to='dcim.Site',
        on_delete=models.PROTECT,
        related_name="+",
        related_query_name="+",
        blank=True,
        null=True,
    )
    tenant = models.ForeignKey(
        to='tenancy.Tenant', on_delete=models.PROTECT, blank=True, null=True
    )
    status = models.CharField(max_length=50)
    role = models.ForeignKey(
        to='ipam.Role', on_delete=models.SET_NULL, blank=True, null=True
    )
    description = models.CharField(max_length=200, blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        abstract = True


class Community(BGPBase):
    """ """

    value = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = 'Communities'
        ordering = ['value']
        app_label = 'netbox_bgp'
        managed = False

    def __str__(self):
        return self.value


class CommunityList(AbsoluteURLMixin, NetBoxModel):
    """ """

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Community Lists'
        unique_together = ['name', 'description']
        ordering = ['name']
        app_label = 'netbox_bgp'
        managed = False

    def __str__(self):
        return self.name


class CommunityListRule(AbsoluteURLMixin, NetBoxModel):
    """ """

    community_list = models.ForeignKey(
        to=CommunityList, on_delete=models.CASCADE, related_name='commlistrules'
    )
    action = models.CharField(max_length=30)
    community = models.ForeignKey(
        to=Community,
        related_name='+',
        on_delete=models.CASCADE,
    )
    description = models.CharField(max_length=200, blank=True)
    comments = models.TextField(blank=True)

    def __str__(self):
        return f'{self.community_list}: {self.action} {self.community}'

    class Meta:
        ordering = ['community_list', 'community']
        app_label = 'netbox_bgp'
        managed = False


class PrefixList(AbsoluteURLMixin, NetBoxModel):
    """ """

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    family = models.CharField(max_length=10)
    comments = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Prefix Lists'
        unique_together = ['name', 'description', 'family']
        ordering = ['name']
        app_label = 'netbox_bgp'
        managed = False

    def __str__(self):
        return self.name


class PrefixListRule(AbsoluteURLMixin, NetBoxModel):
    """ """

    prefix_list = models.ForeignKey(
        to=PrefixList, on_delete=models.CASCADE, related_name='prefrules'
    )
    index = models.PositiveIntegerField()
    action = models.CharField(max_length=30)
    prefix = models.ForeignKey(
        to='ipam.Prefix',
        blank=True,
        null=True,
        related_name="+",
        related_query_name="+",
        on_delete=models.CASCADE,
    )
    prefix_custom = IPNetworkField(
        blank=True,
        null=True,
    )
    ge = models.PositiveSmallIntegerField(blank=True, null=True)
    le = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.CharField(max_length=200, blank=True)
    comments = models.TextField(blank=True)

    class Meta:
        unique_together = ('prefix_list', 'index')
        ordering = ['prefix_list', 'index']
        app_label = 'netbox_bgp'
        managed = False

    def __str__(self):
        return f'{self.prefix_list}: Rule {self.index}'


class BGPSession(AbsoluteURLMixin, NetBoxModel):
    name = models.CharField(max_length=256, blank=True, null=True)
    site = models.ForeignKey(
        to='dcim.Site', on_delete=models.SET_NULL, blank=True, null=True
    )
    tenant = models.ForeignKey(
        to='tenancy.Tenant', on_delete=models.PROTECT, blank=True, null=True
    )
    device = models.ForeignKey(
        to='dcim.Device',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    virtualmachine = models.ForeignKey(
        to='virtualization.VirtualMachine',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    local_address = models.ForeignKey(
        to='ipam.IPAddress',
        on_delete=models.PROTECT,
        related_name="+",
        related_query_name="+",
    )
    remote_address = models.ForeignKey(
        to='ipam.IPAddress',
        on_delete=models.PROTECT,
        related_name="+",
        related_query_name="+",
    )
    local_as = models.ForeignKey(
        to='ipam.ASN',
        on_delete=models.PROTECT,
        related_name='+',
        related_query_name='+',
    )
    remote_as = models.ForeignKey(
        to='ipam.ASN',
        on_delete=models.PROTECT,
        related_name="+",
        related_query_name="+",
    )
    status = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
    peer_group = models.ForeignKey(
        BGPPeerGroup, on_delete=models.SET_NULL, blank=True, null=True
    )
    prefix_list_in = models.ForeignKey(
        to=PrefixList,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='session_prefix_in',
    )
    prefix_list_out = models.ForeignKey(
        to=PrefixList,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='session_prefix_out',
    )
    comments = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'BGP Sessions'
        unique_together = [
            ['device', 'local_address', 'local_as', 'remote_address', 'remote_as'],
            [
                'virtualmachine',
                'local_address',
                'local_as',
                'remote_address',
                'remote_as',
            ],
        ]
        ordering = ('name', 'pk')  # Name may be null
        app_label = 'netbox_bgp'
        managed = False

    @property
    def label(self):
        """
        Return the session name if set; otherwise return a generated name if available.
        """
        if self.name:
            return self.name
        return f'{self.remote_address}:{self.remote_as}'

    def __str__(self):
        if self.device:
            return f'{self.device}:{self.label}'
        elif self.virtualmachine:
            return f'{self.virtualmachine}:{self.label}'
        else:
            return f'{self.label}'


class RoutingPolicyRule(AbsoluteURLMixin, NetBoxModel):
    routing_policy = models.ForeignKey(
        to=RoutingPolicy, on_delete=models.CASCADE, related_name='rules'
    )
    index = models.PositiveIntegerField()
    action = models.CharField(max_length=30)
    description = models.CharField(max_length=500, blank=True)
    continue_entry = models.PositiveIntegerField(blank=True, null=True)
    match_custom = models.JSONField(
        blank=True,
        null=True,
    )
    set_actions = models.JSONField(
        blank=True,
        null=True,
    )
    comments = models.TextField(blank=True)

    def __str__(self):
        return f'{self.routing_policy}: Rule {self.index}'

    class Meta:
        ordering = ['routing_policy', 'index']
        unique_together = ('routing_policy', 'index')
        ordering = ['routing_policy', 'index']
        app_label = 'netbox_bgp'
        managed = False


class BGPPeerGroup_ImportPolicies(models.Model):

    bgppeergroup = models.ForeignKey(
        to='BGPPeerGroup',
        on_delete=models.CASCADE,
        related_name="import_policies",
        related_query_name="import_policies",
    )

    routingpolicy = models.ForeignKey(
        to='RoutingPolicy',
        on_delete=models.CASCADE,
        related_name="+",
        related_query_name="+",
    )

    class Meta:
        app_label = 'netbox_bgp'
        db_table = 'netbox_bgp_bgppeergroup_import_policies'
        managed = False


class BGPPeerGroup_ExportPolicies(models.Model):

    bgppeergroup = models.ForeignKey(
        to='BGPPeerGroup',
        on_delete=models.CASCADE,
        related_name="export_policies",
        related_query_name="export_policies",
    )

    routingpolicy = models.ForeignKey(
        to='RoutingPolicy',
        on_delete=models.CASCADE,
        related_name="group_export_policies",
        related_query_name="group_export_policies",
    )

    class Meta:
        app_label = 'netbox_bgp'
        db_table = 'netbox_bgp_bgppeergroup_export_policies'
        managed = False


class BGPSession_ImportPolicies(models.Model):

    bgpsession = models.ForeignKey(
        to='BGPSession',
        on_delete=models.CASCADE,
        related_name="import_policies",
        related_query_name="import_policies",
    )

    routingpolicy = models.ForeignKey(
        to='RoutingPolicy',
        on_delete=models.CASCADE,
        related_name="group_import_policies",
        related_query_name="group_import_policies",
    )

    class Meta:
        app_label = 'netbox_bgp'
        db_table = 'netbox_bgp_bgpsession_import_policies'
        managed = False


class BGPSession_ExportPolicies(models.Model):

    bgpsession = models.ForeignKey(
        to='BGPSession',
        on_delete=models.CASCADE,
        related_name="export_policies",
        related_query_name="export_policies",
    )

    routingpolicy = models.ForeignKey(
        to='RoutingPolicy',
        on_delete=models.CASCADE,
        related_name="session_export_policies",
        related_query_name="session_export_policies",
    )

    class Meta:
        app_label = 'netbox_bgp'
        db_table = 'netbox_bgp_bgpsession_export_policies'
        managed = False


class RoutingPolicyRule_Match_Community(models.Model):

    routingpolicyrule = models.ForeignKey(
        to='RoutingPolicyRule',
        on_delete=models.CASCADE,
        related_name="match_community",
        related_query_name="match_community",
    )

    community = models.ForeignKey(
        to='Community',
        on_delete=models.CASCADE,
        related_name="+",
        related_query_name="+",
    )

    class Meta:
        app_label = 'netbox_bgp'
        db_table = 'netbox_bgp_routingpolicyrule_match_community'
        managed = False


class RoutingPolicyRule_Match_CommunityList(models.Model):

    routingpolicyrule = models.ForeignKey(
        to='RoutingPolicyRule',
        on_delete=models.CASCADE,
        related_name="match_community_list",
        related_query_name="match_community_list",
    )

    communitylist = models.ForeignKey(
        to='CommunityList',
        on_delete=models.CASCADE,
        related_name="+",
        related_query_name="+",
    )

    class Meta:
        app_label = 'netbox_bgp'
        db_table = 'netbox_bgp_routingpolicyrule_match_community_list'
        managed = False


class RoutingPolicyRule_Match_ASPathList(models.Model):

    routingpolicyrule = models.ForeignKey(
        to='RoutingPolicyRule',
        on_delete=models.CASCADE,
        related_name="match_aspath_list",
        related_query_name="match_aspath_list",
    )

    aspathlist = models.ForeignKey(
        to='ASPathList',
        on_delete=models.CASCADE,
        related_name="+",
        related_query_name="+",
    )

    class Meta:
        app_label = 'netbox_bgp'
        db_table = 'netbox_bgp_routingpolicyrule_match_aspath_list'
        managed = False


class RoutingPolicyRule_Match_IPAddress(models.Model):

    routingpolicyrule = models.ForeignKey(
        to='RoutingPolicyRule',
        on_delete=models.CASCADE,
        related_name="match_ip_address",
        related_query_name="match_ip_address",
    )

    prefixlist = models.ForeignKey(
        to='PrefixList',
        on_delete=models.CASCADE,
        related_name="+",
        related_query_name="+",
    )

    class Meta:
        app_label = 'netbox_bgp'
        db_table = 'netbox_bgp_routingpolicyrule_match_ip_address'
        managed = False


class RoutingPolicyRule_Match_IPV6Address(models.Model):

    routingpolicyrule = models.ForeignKey(
        to='RoutingPolicyRule',
        on_delete=models.CASCADE,
        related_name="match_ipv6_address",
        related_query_name="match_ipv6_address",
    )

    prefixlist = models.ForeignKey(
        to='PrefixList',
        on_delete=models.CASCADE,
        related_name="+",
        related_query_name="+",
    )

    class Meta:
        app_label = 'netbox_bgp'
        db_table = 'netbox_bgp_routingpolicyrule_match_ipv6_address'
        managed = False
