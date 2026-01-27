import json
import netaddr

from django.db.models import Model
from netaddr import IPNetwork

from ipam.models import RIR, ASN, VRF, IPAddress
from utilities.querysets import RestrictedQuerySet


class IPAddressFieldMixin:
    def model_to_dict(self, instance, fields, api=False):
        model_dict = super().model_to_dict(instance, fields, api)
        for key, value in list(model_dict.items()):
            if api:
                if type(value) is netaddr.IPAddress:
                    model_dict[key] = str(value)
            elif not api and key in [
                'router_id',
            ]:
                if type(value) is netaddr.IPAddress:
                    model_dict[key] = str(value)
        return model_dict


class AutomatedModelCreationMixin:

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        items = []
        for seq in range(1, 4):
            kwargs = {}
            for field in cls.routing_required_fields:
                if type(field) is tuple:
                    field, mapped_field = field
                else:
                    field, mapped_field = field, None

                if (
                    mapped_field
                    and hasattr(cls, mapped_field)
                    and isinstance(getattr(cls, mapped_field), RestrictedQuerySet)
                ):
                    kwargs[field] = getattr(cls, mapped_field)[seq - 1]
                elif (
                    mapped_field
                    and hasattr(cls, mapped_field)
                    and type(getattr(cls, mapped_field)) in [list, tuple]
                ):
                    kwargs[field] = getattr(cls, mapped_field)[seq - 1]
                elif mapped_field and hasattr(cls, mapped_field):
                    kwargs[field] = getattr(cls, mapped_field)
                elif field == 'name':
                    kwargs[field] = (f'{cls.model._meta.verbose_name}: {seq}',)
                elif field == 'sequence':
                    kwargs[field] = seq
                elif hasattr(cls, field):
                    kwargs[field] = getattr(cls, field)

            instance = cls.model(**kwargs)
            instance.full_clean()
            items.append(instance)
        cls.model.objects.bulk_create(items)


class AutomatedFormDataCreationMixin:

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        try:
            sequence = cls.model.objects.last().sequence + 1
        except Exception:
            sequence = 0

        kwargs = {}
        for field in cls.routing_required_fields:
            if type(field) is tuple:
                field, mapped_field = field
            else:
                field, mapped_field = field, None

            if (
                mapped_field
                and hasattr(cls, mapped_field)
                and isinstance(getattr(cls, mapped_field), RestrictedQuerySet)
            ):
                kwargs[field] = getattr(cls, mapped_field)[-1].pk
            elif (
                mapped_field
                and hasattr(cls, mapped_field)
                and type(getattr(cls, mapped_field)) in [list, tuple]
            ):
                kwargs[field] = getattr(cls, mapped_field)[-1]
            elif (
                mapped_field
                and hasattr(cls, mapped_field)
                and isinstance(getattr(cls, mapped_field), Model)
            ):
                kwargs[field] = getattr(cls, mapped_field).pk
            elif mapped_field and hasattr(cls, mapped_field):
                kwargs[field] = getattr(cls, mapped_field)
            elif field == 'name':
                kwargs[field] = f'{cls.model._meta.verbose_name}: {sequence}'
            elif field == 'sequence':
                kwargs[field] = sequence
            elif hasattr(cls, field) and isinstance(getattr(cls, field), Model):
                kwargs[field] = getattr(cls, field).pk
            elif hasattr(cls, field) and type(getattr(cls, field)) in [
                list,
                tuple,
                dict,
            ]:
                kwargs[field] = json.dumps(getattr(cls, field))
            elif hasattr(cls, field):
                kwargs[field] = getattr(cls, field)

        cls.form_data = kwargs


class ASNMixin:
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.rir = RIR.objects.create(name='ARIN')
        for asn in range(64512, 64520):
            ASN.objects.create(rir=cls.rir, asn=asn)

        cls.asn = ASN.objects.first()
        cls.asns = ASN.objects.all()


class VRFMixin:
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        for vrf_id in range(1, 11):
            VRF.objects.create(name=f'VRF {vrf_id}', rd=f'64512:{vrf_id}')

        cls.vrf = VRF.objects.first()
        cls.vrfs = VRF.objects.all()


class AddressesMixin:
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        for i in range(1, 11):
            IPAddress.objects.create(address=IPNetwork(f'10.0.0.{i}/24'))

        cls.ip_address = IPAddress.objects.first()
        cls.ip_addresses = IPAddress.objects.all()
        cls.peer_address = IPAddress.objects.get(address=IPNetwork('10.0.0.1/24'))
        cls.source_address = IPAddress.objects.get(address=IPNetwork('10.0.0.2/24'))


class BulkEditMixin:
    bulk_edit_data = {
        'description': 'Test Description',
    }


class PluginBaseURLMixin:
    def _get_base_url(self):
        return 'plugins:{}:{}_{{}}'.format(
            self.model._meta.app_label, self.model._meta.model_name
        )
