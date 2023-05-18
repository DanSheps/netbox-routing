from django.db import models
from django.db.models import CheckConstraint, Q
from django.urls import reverse

from ipam.fields import IPNetworkField
from netbox.models import NetBoxModel
from netbox_routing.fields.ip import IPAddressField


__all__ = (
    'StaticRoute'
)


class StaticRoute(NetBoxModel):
    devices = models.ManyToManyField(
        to='dcim.Device',
        related_name='static_routes'
    )
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
        verbose_name='Metric'
    )
    permanent = models.BooleanField()

    clone_fields = (
        'vrf', 'metric', 'permanent'
    )
    prerequisite_models = (
        'dcim.Device',
        'ipam.VRF',
    )

    class Meta:
        ordering = ['vrf', 'prefix', 'metric']
        constraints = (
            CheckConstraint(check=Q(Q(metric__lte=255) & Q(metric__gte=0)), name='metric_gte_lte'),
            models.UniqueConstraint(
                'vrf', 'prefix', 'next_hop',
                name='%(app_label)s_%(class)s_unique_vrf_prefix_nexthop',
                violation_error_message="VRF, Prefix and Next Hop must be unique."
            ),
        )

    def __str__(self):
        if self.vrf is None:
            return f'{self.prefix} NH {self.next_hop}'
        return f'{self.prefix} VRF {self.vrf} NH {self.next_hop}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:staticroute', args=[self.pk])
