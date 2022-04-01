from django.db import models
from django.db.models import F, Q, CheckConstraint

from ipam.fields import IPNetworkField
from netbox.models import NetBoxModel


class RouteMap(NetBoxModel):
    pass


class PrefixList(NetBoxModel):
    name = models.CharField()


class PrefixListEntry(NetBoxModel):
    prefix_list = models.ForeignKey(
        to="netbox_routing.PrefixList",
        on_delete=models.PROTECT,
        related_name='entries',
        verbose_name='Prefix List'
    )
    prefix = IPNetworkField(help_text='IPv4 or IPv6 network with mask')
    ge = models.PositiveSmallIntegerField()
    le = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [
            CheckConstraint(
                name='prefixlistentry_ge_gt_le',
                check=Q(Q(ge__isnull=False) & Q(le_isnull=False) & Q(ge__lt=F('le')) & Q(le__gt=F('ge')))
            ),
            CheckConstraint(
                name='prefixlistentry_ge_gt_le',
                check=Q(Q(ge__isnull=False) & Q(le_isnull=False) & Q(ge__lt=F('le')) & Q(le__gt=F('ge')))
            )
        ]
