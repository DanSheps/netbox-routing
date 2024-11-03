from django.db import models
from django.utils.translation import gettext as _

from netbox.models import PrimaryModel


class Community(PrimaryModel):
    community = models.CharField(
        max_length=255,
        verbose_name=_('Community'),
    )
    tenant = models.ForeignKey(
        to='tenant.Tenant',
        on_delete=models.PROTECT,
        related_name='communities',
        verbose_name=_('Device'),
    )

    class Meta:
        verbose_name = _('Community')

    def __str__(self):
        return f'{self.community}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('plugins:netbox_routing:community', args=[self.pk])


class CommunityList(PrimaryModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_('List')
    )
    communities = models.ManyToManyField(
        to=Community,
        related_name='community_lists'
    )
    tenant = models.ForeignKey(
        to='tenants.Tenant',
        on_delete=models.PROTECT,
        related_name='communities',
        verbose_name=_('Device'),
    )

    class Meta:
        verbose_name = _('Community List')

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('plugins:netbox_routing:communitylist', args=[self.pk])
