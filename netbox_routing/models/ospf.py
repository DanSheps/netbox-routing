from django.db import models

from netbox.models import NetBoxModel, WebhooksMixin, ChangeLoggedModel

from netbox_routing.fields.ip import IPAddressField


__all__ = (
    'OSPFInstance',
    'OSPFArea',
)


class OSPFInstance(NetBoxModel):
    router_id = IPAddressField()
    process_id = models.IntegerField()


class OSPFArea(NetBoxModel):
    instance = models.ForeignKey(
        to='netbox_routing.OSPFInstance'
    )
    area_id = models.IntegerField()
    interfaces = models.ManyToManyField(
        to='netbox_routing.OSPFArea',
        on_delete=models.PROTECT,
        related_name='ospf',
        blank=False,
        null=False
    )
