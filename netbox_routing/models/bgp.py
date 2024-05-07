from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext as _

from netbox.models import NetBoxModel, NestedGroupModel
from netbox_routing import choices
from netbox_routing.choices.bgp import BGPSettingChoices, BGPAddressFamilyChoices, BFDChoices
from netbox_routing.constants.bgp import BGPSETTING_ASSIGNMENT_MODELS, BGPAF_ASSIGNMENT_MODELS, \
    BGPPEER_ASSIGNMENT_MODELS, BGPPEERAF_ASSIGNMENT_MODELS
from netbox_routing.fields.ip import IPAddressField


class BGPSetting(NetBoxModel):
    assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=BGPSETTING_ASSIGNMENT_MODELS,
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True
    )
    assigned_object_id = models.PositiveBigIntegerField(
        blank=True,
        null=True
    )
    assigned_object = GenericForeignKey(
        ct_field='assigned_object_type',
        fk_field='assigned_object_id'
    )
    key = models.CharField(
        choices=BGPSettingChoices,
    )
    value = models.CharField()

    class Meta:
        verbose_name = 'BGP Setting'

    def __str__(self):
        return f'{self.assigned_object}: {self.key}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('plugins:netbox_routing:bgpsetting', args=[self.pk])


class BGPRouter(NetBoxModel):
    device = models.ForeignKey(
        to='dcim.Device',
        on_delete=models.PROTECT,
        related_name='router',
        verbose_name='Device'
    )
    asn = models.ForeignKey(
        to='ipam.ASN',
        on_delete=models.PROTECT,
        related_name='router',
        verbose_name='ASN'
    )
    settings = GenericRelation(
        to='netbox_routing.BGPSetting',
        related_name='router',
        related_query_name='router',
        content_type_field='assigned_object_type',
        object_id_field='assigned_object_id'
    )

    class Meta:
        verbose_name = 'BGP Router'

    def __str__(self):
        return f'{self.device} ({self.asn})'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('plugins:netbox_routing:bgprouter', args=[self.pk])


class BGPScope(NetBoxModel):
    router = models.ForeignKey(
        to=BGPRouter,
        on_delete=models.PROTECT,
        related_name='scopes',
        blank=False,
        null=False
    )
    vrf = models.ForeignKey(
        to='ipam.VRF',
        on_delete=models.PROTECT,
        related_name='scopes',
        blank=True,
        null=True
    )

    settings = GenericRelation(
        to='netbox_routing.BGPSetting',
        related_name='scope',
        related_query_name='scope',
        content_type_field='assigned_object_type',
        object_id_field='assigned_object_id'
    )

    class Meta:
        verbose_name = 'BGP Scope'

    def __str__(self):
        return f'{self.router}: {self.vrf or "Global VRF"}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('plugins:netbox_routing:bgpscope', args=[self.pk])


class BGPAddressFamily(NetBoxModel):
    scope = models.ForeignKey(
        to=BGPScope,
        on_delete=models.PROTECT,
        related_name='address_families',
        verbose_name=_('BGP Scope')
    )
    address_family = models.CharField(
        max_length=50,
        choices=BGPAddressFamilyChoices,
        verbose_name=_('PoE type')
    )
    settings = GenericRelation(
        to='netbox_routing.BGPSetting',
        related_name='address_family',
        related_query_name='address_family',
        content_type_field='assigned_object_type',
        object_id_field='assigned_object_id'
    )

    class Meta:
        verbose_name = 'BGP Address Family'

    def __str__(self):
        return f'{self.scope} ({self.get_address_family_display()})'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('plugins:netbox_routing:bgpaddressfamily', args=[self.pk])


class BGPSessionTemplate(NetBoxModel):
    name = models.CharField(
        verbose_name='Name',
        max_length=255
    )
    router = models.ForeignKey(
        to=BGPRouter,
        on_delete=models.PROTECT,
        related_name='session_templates',
    )
    parent = models.ForeignKey(
        to='netbox_routing.BGPSessionTemplate',
        on_delete=models.PROTECT,
        related_name='children',
        blank=True,
        null=True
    )
    enabled = models.BooleanField(
        blank=True,
        null=True
    )
    asn = models.ForeignKey(
        to='ipam.ASN',
        on_delete=models.PROTECT,
        related_name='session_templates',
        blank=True,
        null=True
    )
    bfd = models.CharField(
        max_length=50,
        choices=BFDChoices,
        blank=True,
        null=True,
    )
    password = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )


class BGPPoliyTemplate(NetBoxModel):
    name = models.CharField(
        verbose_name='Name',
        max_length=255
    )
    router = models.ForeignKey(
        to=BGPRouter,
        on_delete=models.PROTECT,
        related_name='policy_templates',
        blank=False,
        null=False
    )
    enabled = models.BooleanField(
        blank=True,
        null=True
    )
    prefixlist_out = models.ForeignKey(
        to='netbox_routing.PrefixList',
        on_delete=models.PROTECT,
        related_name='template_afs_out',
        blank=True,
        null=True
    )
    prefixlist_in = models.ForeignKey(
        to='netbox_routing.PrefixList',
        on_delete=models.PROTECT,
        related_name='template_afs_in',
        blank=True,
        null=True
    )
    routemap_out = models.ForeignKey(
        to='netbox_routing.RouteMap',
        on_delete=models.PROTECT,
        related_name='template_afs_out',
        blank=True,
        null=True
    )
    routemap_in = models.ForeignKey(
        to='netbox_routing.RouteMap',
        on_delete=models.PROTECT,
        related_name='template_afs_in',
        blank=True,
        null=True
    )


class BGPPeerTemplate(NetBoxModel):
    name = models.CharField(
        verbose_name='Name',
        max_length=255
    )
    remote_as = models.ForeignKey(
        to='ipam.ASN',
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True
    )
    enabled = models.BooleanField(
        blank=True,
        null=True
    )


class BGPPeer(NetBoxModel):
    assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=BGPPEER_ASSIGNMENT_MODELS,
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True
    )
    assigned_object_id = models.PositiveBigIntegerField(
        blank=True,
        null=True
    )
    assigned_object = GenericForeignKey(
        ct_field='assigned_object_type',
        fk_field='assigned_object_id'
    )
    peer = IPAddressField()
    peer_group = models.ForeignKey(
        to=BGPPeerTemplate,
        on_delete=models.PROTECT,
        related_name='peers',
        blank=True,
        null=True
    )
    peer_policy = models.ForeignKey(
        to=BGPPoliyTemplate,
        on_delete=models.PROTECT,
        related_name='peers',
        blank=True,
        null=True
    )
    remote_as = models.ForeignKey(
        to='ipam.ASN',
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True
    )
    enabled = models.BooleanField(
        blank=True,
        null=True
    )


class BGPPeerAddressFamily(NetBoxModel):
    assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=BGPPEERAF_ASSIGNMENT_MODELS,
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True
    )
    assigned_object_id = models.PositiveBigIntegerField(
        blank=True,
        null=True
    )
    assigned_object = GenericForeignKey(
        ct_field='assigned_object_type',
        fk_field='assigned_object_id'
    )
    address_family = models.ForeignKey(
        to=BGPAddressFamily,
        on_delete=models.PROTECT,
        related_name='address_families'
    )

    peer_session = models.ForeignKey(
        to=BGPSessionTemplate,
        on_delete=models.PROTECT,
        related_name='peer_afs',
        blank=True,
        null=True
    )
    enabled = models.BooleanField(
        blank=True,
        null=True
    )

    prefixlist_out = models.ForeignKey(
        to='netbox_routing.PrefixList',
        on_delete=models.PROTECT,
        related_name='peer_afs_out',
        blank=True,
        null=True
    )
    prefixlist_in = models.ForeignKey(
        to='netbox_routing.PrefixList',
        on_delete=models.PROTECT,
        related_name='peer_afs_in',
        blank=True,
        null=True
    )
    routemap_out = models.ForeignKey(
        to='netbox_routing.RouteMap',
        on_delete=models.PROTECT,
        related_name='peer_afs_out',
        blank=True,
        null=True
    )
    routemap_in = models.ForeignKey(
        to='netbox_routing.RouteMap',
        on_delete=models.PROTECT,
        related_name='peer_afs_in',
        blank=True,
        null=True
    )
