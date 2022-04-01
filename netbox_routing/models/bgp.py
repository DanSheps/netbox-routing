from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from netbox.models import NetBoxModel, NestedGroupModel
from netbox_routing import choices
from netbox_routing.constants.bgp import BGPSETTING_ASSIGNMENT_MODELS, BGPAF_ASSIGNMENT_MODELS, \
    BGPNEIGHBOR_ASSIGNMENT_MODELS
from netbox_routing.fields.ip import IPAddressField


class BGPSettings(NetBoxModel):
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
    router_id = IPAddressField()
    auto_summary = models.BooleanField()
    bgp_additional_paths_install = models.BooleanField()
    bgp_additional_paths_receive = models.BooleanField()
    bgp_additional_paths_send = models.BooleanField()
    bgp_asnotation_dot = models.BooleanField()
    bgp_graceful_restart = models.BooleanField()

    default_information_originate = models.BooleanField(verbose_name='Default Information Originate')
    default_metric = models.PositiveBigIntegerField(verbose_name='Default Metric')
    distance_ebgp = models.PositiveSmallIntegerField(verbose_name='eBGP Distance')
    distance_ibgp = models.PositiveSmallIntegerField(verbose_name='iBGP Distance')
    distance_embgp = models.PositiveSmallIntegerField(verbose_name='eBGP Distance (MultiProtocol)')
    distance_imbgp = models.PositiveSmallIntegerField(verbose_name='iBGP Distance (MultiProtocol)')
    paths_maximum = models.PositiveSmallIntegerField(verbose_name='Maximum Paths')
    paths_maximum_secondary = models.PositiveSmallIntegerField(verbose_name='Maximum Secondary Paths')
    timers_keepalive = models.PositiveSmallIntegerField(verbose_name='Keepalive Timer')
    timers_hold = models.PositiveSmallIntegerField(verbose_name='Hold Timer')


class BGPRouter(NetBoxModel):
    asn = models.ForeignKey(
        to='ipam.ASN',
        on_delete=models.PROTECT,
        related_name='router',
        verbose_name='ASN'
    )


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
        blank=False,
        null=False
    )


class BGPAddressFamily(NetBoxModel):
    assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=BGPAF_ASSIGNMENT_MODELS,
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


class BGPTemplateSession(NetBoxModel):
    pass


class BGPTemplatePolicy(NetBoxModel):
    pass


class BGPTemplatePeer(NetBoxModel):
    pass


class BGPPeerGroup(NetBoxModel):
    pass


class BGPPeer(NetBoxModel):
    assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=BGPNEIGHBOR_ASSIGNMENT_MODELS,
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
    remote_as = models.ForeignKey(
        to='ipam.ASN',
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True
    )


class BGPPeerAddressFamily(NetBoxModel):
    remote_as = models.ForeignKey(
        to=BGPNeighbor,
        on_delete=models.PROTECT,
        related_name='neighbors',
        blank=True,
        null=True
    )
    address_family = models.CharField(
        choices=choices.BGPAddressFamilies
    )
