from django.db import models
from django.db.models import CheckConstraint, Q

from ipam.fields import IPNetworkField
from netbox.models import NetBoxModel
from netbox_routing.fields.ip import IPAddressField


class StaticRoute(NetBoxModel):
    vrf = models.ForeignKey(
        to='ipam.VRF',
        on_delete=models.PROTECT,
        related_name='staticroutes',
        blank=True,
        null=True,
        verbose_name='VRF'
    )
    prefix = IPNetworkField(help_text='IPv4 or IPv6 network with mask')
    next_hop = IPAddressField()
    name = models.CharField(
        max_length=50,
        verbose_name='Name',
        blank=True,
        null=True,
        help_text='Optional name for this static route'
    )
    metric = models.PositiveSmallIntegerField(
        verbose_name='Metric',
        max_length=3
    )
    permanent = models.BooleanField()

    class Meta:
        constraints = [
            CheckConstraint(check=Q(Q(metric__lte=255) & Q(metric__gte=0)), name='metric_gte_lte')
        ]
