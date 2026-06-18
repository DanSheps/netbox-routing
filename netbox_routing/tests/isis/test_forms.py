# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase

from dcim.models import Interface
from ipam.models import VRF
from utilities.testing import create_test_device

from netbox_routing.forms import ISISInstanceForm, ISISInterfaceForm
from netbox_routing.forms.bulk_edit.isis import (
    ISISInstanceBulkEditForm,
    ISISInterfaceBulkEditForm,
    ISISSettingBulkEditForm,
)
from netbox_routing.models import ISISInstance

__all__ = (
    'ISISBulkEditFieldsetTestCase',
    'ISISInstanceFormTestCase',
    'ISISInterfaceFormTestCase',
)


class ISISBulkEditFieldsetTestCase(TestCase):
    """Every bulk-edit form that declares a `comments` CommentField must also
    list it in `fieldsets` — NetBox only renders fields named in a fieldset, so
    an omitted field is silently unreachable in the UI."""

    @staticmethod
    def _fieldset_names(form):
        return {
            item
            for fieldset in form.fieldsets
            for item in fieldset.items
            if isinstance(item, str)
        }

    def test_comments_rendered_in_bulk_edit_fieldsets(self):
        for form_cls in (
            ISISSettingBulkEditForm,
            ISISInstanceBulkEditForm,
            ISISInterfaceBulkEditForm,
        ):
            with self.subTest(form=form_cls.__name__):
                form = form_cls()
                self.assertIn('comments', form.fields)
                self.assertIn('comments', self._fieldset_names(form))

    def test_is_type_is_bulk_nullable(self):
        # is_type is an editable, optional field in the IS-IS fieldset; it must
        # also be in nullable_fields or it can't be cleared via bulk edit (the
        # same omission would silently strand the field, like metric_style).
        form = ISISInstanceBulkEditForm()
        self.assertIn('is_type', form.fields)
        self.assertFalse(form.fields['is_type'].required)
        self.assertIn('is_type', form.nullable_fields)

    def test_passive_is_bulk_nullable(self):
        # passive is an editable, optional ISISInterface field and ISISInterface.passive is
        # null=True, so it must be in nullable_fields or it cannot be cleared via bulk edit.
        form = ISISInterfaceBulkEditForm()
        self.assertIn('passive', form.fields)
        self.assertFalse(form.fields['passive'].required)
        self.assertIn('passive', form.nullable_fields)


class ISISInstanceFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.vrf = VRF.objects.create(name='Test VRF')
        cls.device = create_test_device(name='Device 1')

    def test_instance(self):
        form = ISISInstanceForm(
            data={
                'device': self.device.pk,
                'process_tag': '',
                'net': '49.0001.0000.0000.0001.00',
                'is_type': 'level-1-2',
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertTrue(form.save())

    def test_instance_with_vrf(self):
        form = ISISInstanceForm(
            data={
                'device': self.device.pk,
                'vrf': self.vrf.pk,
                'process_tag': 'CORE',
                'net': '49.0001.0000.0000.0002.00',
                'is_type': 'level-2-only',
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertTrue(form.save())

    def test_settings_persist_with_commit_true(self):
        """commit=True (the default) upserts the EAV ISISSetting rows immediately."""
        from django.contrib.contenttypes.models import ContentType

        from netbox_routing.models import ISISSetting

        form = ISISInstanceForm(
            data={
                'device': self.device.pk,
                'net': '49.0001.0000.0000.0008.00',
                'is_type': 'level-1-2',
                'default_route_tag': 77,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        obj = form.save()
        ct = ContentType.objects.get_for_model(obj)
        setting = ISISSetting.objects.get(
            assigned_object_type=ct, assigned_object_id=obj.pk, key='default_route_tag'
        )
        self.assertEqual(setting.value, '77')

    def test_settings_persist_with_commit_false_via_save_m2m(self):
        """Regression: callers may use save(commit=False) -> instance.save()
        -> save_m2m(). The submitted ISISSetting values must survive that path instead of
        being silently dropped (the popped settings used to be discarded when commit=False)."""
        from django.contrib.contenttypes.models import ContentType

        from netbox_routing.models import ISISSetting

        form = ISISInstanceForm(
            data={
                'device': self.device.pk,
                'net': '49.0001.0000.0000.0009.00',
                'is_type': 'level-1-2',
                'default_route_tag': 99,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        obj = form.save(commit=False)
        # The mixin must NOT have persisted yet (instance has no pk) and must not have
        # written any EAV row — commit=False defers the upsert to save_m2m().
        self.assertIsNone(obj.pk)
        self.assertFalse(ISISSetting.objects.filter(key='default_route_tag').exists())
        obj.save()
        form.save_m2m()
        ct = ContentType.objects.get_for_model(obj)
        setting = ISISSetting.objects.get(
            assigned_object_type=ct, assigned_object_id=obj.pk, key='default_route_tag'
        )
        self.assertEqual(setting.value, '99')

    def test_boolean_setting_initial_normalized_from_text(self):
        """A boolean ISISSetting can be stored as textual yes/no/1/0 (ISISSetting.clean()
        accepts those for booleans via the API/import paths). The edit form's NullBooleanField
        only matches real True/False, so a raw text initial would render blank and then be
        deleted on save. The form must normalize the stored text to a real bool."""
        from django.contrib.contenttypes.models import ContentType

        from netbox_routing.models import ISISInstance, ISISSetting

        instance = ISISInstance.objects.create(
            device=self.device, net='49.0001.0000.0000.0010.00', is_type='level-1-2'
        )
        ct = ContentType.objects.get_for_model(instance)
        cases = (
            ('yes', True),
            ('1', True),
            ('true', True),
            ('no', False),
            ('0', False),
            ('false', False),
        )
        for stored, expected in cases:
            with self.subTest(stored=stored):
                ISISSetting.objects.update_or_create(
                    assigned_object_type=ct,
                    assigned_object_id=instance.pk,
                    key='graceful_restart',
                    defaults={'value': stored},
                )
                form = ISISInstanceForm(instance=instance)
                self.assertIs(form.fields['graceful_restart'].initial, expected)


class ISISInterfaceFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.device = create_test_device(name='Device 1')
        cls.interface = Interface.objects.create(
            name='Interface 1', device=cls.device, type='virtual'
        )
        cls.instance = ISISInstance.objects.create(
            device=cls.device,
            process_tag='CORE',
            net='49.0001.0000.0000.0001.00',
            is_type='level-1-2',
        )

    def test_interface_with_correct_device(self):
        form = ISISInterfaceForm(
            data={
                'device': self.device.pk,
                'instance': self.instance.pk,
                'interface': self.interface.pk,
                'address_family': 'ipv4',
                'circuit_type': 'level-1-2',
                'network_type': 'point-to-point',
                'metric': 10,
                'passive': True,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertTrue(form.save())

    def test_interface_with_incorrect_device(self):
        device = create_test_device(name='Device 2')
        interface = Interface.objects.create(
            name='Interface 1', device=device, type='virtual'
        )

        form = ISISInterfaceForm(
            data={
                'device': device.pk,
                'instance': self.instance.pk,
                'interface': interface.pk,
                'address_family': 'ipv4',
            }
        )
        # Invalid specifically because of the instance/interface device-mismatch
        # rule in ISISInterfaceForm.clean(), not because of missing fields.
        self.assertFalse(form.is_valid())
        self.assertIn('interface', form.errors)
        self.assertIn('instance', form.errors)
        with self.assertRaises(ValueError):
            form.save()

    def test_interface_requires_hello_auth_key_when_type_is_set(self):
        form = ISISInterfaceForm(
            data={
                'device': self.device.pk,
                'instance': self.instance.pk,
                'interface': self.interface.pk,
                'address_family': 'ipv4',
                'hello_auth_type': 'md5',
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn('hello_auth_key', form.errors)

    def test_interface_requires_hello_auth_type_when_key_is_set(self):
        form = ISISInterfaceForm(
            data={
                'device': self.device.pk,
                'instance': self.instance.pk,
                'interface': self.interface.pk,
                'address_family': 'ipv4',
                'hello_auth_key': 'secret',
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn('hello_auth_type', form.errors)
