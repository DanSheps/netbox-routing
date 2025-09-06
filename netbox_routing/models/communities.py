from django.db import models
from django.utils.translation import gettext as _

from netbox.models import PrimaryModel


__all__ = (
    'CommunityList',
    'Community',
)


class CommunityList(PrimaryModel):
    name = models.CharField(
        verbose_name=_('List'),
        max_length=255,
    )
    communities = models.ManyToManyField(
        verbose_name=_('Communities'),
        to='netbox_routing.Community',
        related_name='community_lists',
    )
    tenant = models.ForeignKey(
        verbose_name=_('Tenant'),
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='community_lists',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('Community List')

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse('plugins:netbox_routing:communitylist', args=[self.pk])


class Community(PrimaryModel):
    community = models.CharField(
        verbose_name=_('Community'),
        max_length=255,
    )
    tenant = models.ForeignKey(
        verbose_name=_('Tenant'),
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='communities',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('Community')

    def __str__(self):
        return f'{self.community}'

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse('plugins:netbox_routing:community', args=[self.pk])
