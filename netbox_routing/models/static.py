from django.db import models
from django.db.models import CheckConstraint, Q
from django.urls import reverse
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError

from dcim.models.device_components import Interface
from ipam.fields import IPNetworkField
from netbox.models import PrimaryModel
from netbox_routing.fields.ip import IPAddressField


__all__ = ('StaticRoute',)


class StaticRoute(PrimaryModel):
    devices = models.ManyToManyField(to='dcim.Device', related_name='static_routes')
    vrf = models.ForeignKey(
        to='ipam.VRF',
        on_delete=models.PROTECT,
        related_name='staticroutes',
        blank=True,
        null=True,
        verbose_name='VRF',
    )
    prefix = IPNetworkField(
        help_text=_('IPv4 or IPv6 network with mask'),
    )
    next_hop = IPAddressField(
        verbose_name=_('Next Hop'),
        blank=True,
        null=True,
    )
    interface_next_hop = models.CharField(
        verbose_name='Interface Next Hop',
        help_text='Forwarding interface, for routes without IP address as next hop',
        blank=True,
        null=True
    )
    name = models.CharField(
        max_length=50,
        verbose_name='Name',
        blank=True,
        null=True,
        help_text='Optional name for this static route',
    )
    metric = models.PositiveSmallIntegerField(
        verbose_name='Metric',
        blank=True,
        default=1,
    )
    permanent = models.BooleanField(
        default=False,
        blank=True,
        null=True,
    )

    tag = models.IntegerField(
        verbose_name='Route Tag',
        help_text='Optional tag for this static route',
        blank=True,
        null=True,
    )

    clone_fields = ('vrf', 'metric', 'permanent')
    prerequisite_models = ('dcim.Device',)

    class Meta:
        ordering = ['vrf', 'prefix', 'metric']
        constraints = (
            CheckConstraint(
                check=Q(Q(metric__lte=255) & Q(metric__gte=0)), name='metric_gte_lte'
            ),
            models.UniqueConstraint(
                'vrf',
                'prefix',
                'next_hop',
                name='%(app_label)s_%(class)s_unique_vrf_prefix_nexthop',
                violation_error_message="VRF, Prefix and Next Hop must be unique.",
            ),
        )

    def __str__(self):
        next_hop = ('VRF' if self.vrf else '')
        next_hop += (str(self.next_hop) if self.next_hop else '')
        next_hop += (' via ' + self.interface_next_hop if self.interface_next_hop else '')
        return f'{self.prefix} next-hop {next_hop}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_routing:staticroute', args=[self.pk])

    def clean(self):
        super().clean()
        if not self.interface_next_hop and not self.next_hop:
            raise ValidationError({
                "next_hop" : "A route requires set either an IP next hop or an Interface next hop."
            })