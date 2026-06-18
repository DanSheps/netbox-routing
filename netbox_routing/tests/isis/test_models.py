# SPDX-License-Identifier: Apache-2.0

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from dcim.models import Interface
from utilities.testing import create_test_device

from netbox_routing.models import ISISInstance, ISISInterface, ISISSetting

__all__ = (
    'ISISInstanceModelTestCase',
    'ISISInterfaceModelTestCase',
    'ISISSettingModelTestCase',
)


class ISISInstanceModelTestCase(TestCase):
    """Model-level (clean()) coverage for ISISInstance auth pairing."""

    @classmethod
    def setUpTestData(cls):
        cls.device = create_test_device(name='Device 1')

    def _instance(self, **kwargs):
        return ISISInstance(
            device=self.device,
            process_tag='CORE',
            net='49.0001.0000.0000.0001.00',
            is_type='level-1-2',
            **kwargs,
        )

    def test_clean_accepts_complete_auth_pair(self):
        self._instance(area_auth_type='md5', area_auth_key='secret').clean()

    def test_clean_accepts_no_auth(self):
        self._instance().clean()

    def test_clean_rejects_type_without_key(self):
        with self.assertRaises(ValidationError) as ctx:
            self._instance(area_auth_type='md5').clean()
        self.assertIn('area_auth_key', ctx.exception.error_dict)

    def test_clean_rejects_key_without_type(self):
        with self.assertRaises(ValidationError) as ctx:
            self._instance(domain_auth_key='secret').clean()
        self.assertIn('domain_auth_type', ctx.exception.error_dict)

    def test_unique_device_process_tag(self):
        # A device can't hold two IS-IS instances with the same process tag
        # (including two untagged '' defaults) — they'd be indistinguishable.
        ISISInstance.objects.create(device=self.device, process_tag='CORE')
        with self.assertRaises(IntegrityError), transaction.atomic():
            ISISInstance.objects.create(device=self.device, process_tag='CORE')

    def test_unique_default_process_tag(self):
        ISISInstance.objects.create(device=self.device, process_tag='')
        with self.assertRaises(IntegrityError), transaction.atomic():
            ISISInstance.objects.create(device=self.device, process_tag='')

    def test_same_process_tag_other_device_allowed(self):
        other = create_test_device(name='Device 2')
        ISISInstance.objects.create(device=self.device, process_tag='CORE')
        ISISInstance.objects.create(device=other, process_tag='CORE')  # no raise


class ISISInterfaceModelTestCase(TestCase):
    """Model-level (clean()) coverage for ISISInterface.

    Exercises the same-device enforcement at the ORM layer, which the
    form-layer tests in test_forms.py do not cover.
    """

    @classmethod
    def setUpTestData(cls):
        cls.device = create_test_device(name='Device 1')
        cls.other_device = create_test_device(name='Device 2')
        cls.instance = ISISInstance.objects.create(
            device=cls.device,
            process_tag='CORE',
            net='49.0001.0000.0000.0001.00',
            is_type='level-1-2',
        )

    def test_clean_accepts_matching_device(self):
        interface = Interface.objects.create(
            name='Interface 1', device=self.device, type='virtual'
        )
        isis_interface = ISISInterface(
            instance=self.instance,
            interface=interface,
            address_family='ipv4',
        )
        isis_interface.clean()  # should not raise

    def test_clean_rejects_device_mismatch(self):
        interface = Interface.objects.create(
            name='Interface 1', device=self.other_device, type='virtual'
        )
        isis_interface = ISISInterface(
            instance=self.instance,
            interface=interface,
            address_family='ipv4',
        )
        with self.assertRaises(ValidationError) as ctx:
            isis_interface.clean()
        self.assertIn('interface', ctx.exception.error_dict)

    def _iface(self, **kwargs):
        interface = Interface.objects.create(
            name=f'Interface {kwargs.pop("n", 1)}', device=self.device, type='virtual'
        )
        return ISISInterface(
            instance=self.instance, interface=interface, address_family='ipv4', **kwargs
        )

    def test_clean_accepts_complete_hello_auth_pair(self):
        self._iface(n=10, hello_auth_type='md5', hello_auth_key='secret').clean()

    def test_clean_accepts_no_hello_auth(self):
        self._iface(n=11).clean()

    def test_clean_rejects_hello_type_without_key(self):
        with self.assertRaises(ValidationError) as ctx:
            self._iface(n=12, hello_auth_type='md5').clean()
        self.assertIn('hello_auth_key', ctx.exception.error_dict)

    def test_clean_rejects_hello_key_without_type(self):
        with self.assertRaises(ValidationError) as ctx:
            self._iface(n=13, hello_auth_key='secret').clean()
        self.assertIn('hello_auth_type', ctx.exception.error_dict)

    def test_optional_charfields_default_to_empty_string(self):
        # circuit_type / network_type are blank=True, default='' (not nullable),
        # so an unset value round-trips as '' rather than NULL.
        iface = self._iface(n=20)
        iface.save()
        iface.refresh_from_db()
        self.assertEqual(iface.circuit_type, '')
        self.assertEqual(iface.network_type, '')

    def test_unique_interface_address_family(self):
        # One IS-IS interface per (interface, address_family).
        iface = self._iface(n=21)
        iface.save()
        with self.assertRaises(IntegrityError), transaction.atomic():
            ISISInterface.objects.create(
                instance=self.instance,
                interface=iface.interface,
                address_family=iface.address_family,
            )


class ISISSettingModelTestCase(TestCase):
    """An ISISSetting must be attached to an assigned object.

    The form enforces this (ISISSettingForm.clean); these tests cover the model
    layer (used by the API/bulk-import paths) and the DB CheckConstraint, so an
    orphan row cannot be persisted through any path.
    """

    @classmethod
    def setUpTestData(cls):
        device = create_test_device(name='Device 1')
        cls.instance = ISISInstance.objects.create(
            device=device, process_tag='CORE', net='49.0001.0000.0000.0001.00'
        )

    def test_clean_accepts_assigned_setting(self):
        ISISSetting(
            assigned_object=self.instance, key='graceful_restart', value='true'
        ).clean()  # should not raise

    def test_clean_rejects_orphan_setting(self):
        with self.assertRaises(ValidationError) as ctx:
            ISISSetting(key='graceful_restart', value='true').clean()
        self.assertIn('assigned to an object', str(ctx.exception))

    def test_clean_rejects_nonexistent_object(self):
        # A dangling assigned_object_id (valid type, no such row) is rejected by
        # NetBox's base NetBoxModel.clean() GFK-existence check, surfaced as a
        # field error. (The end-to-end API rejection is asserted in
        # ISISSettingAssignmentAPITestCase.)
        ct = ContentType.objects.get_for_model(ISISInstance)
        with self.assertRaises(ValidationError) as ctx:
            ISISSetting(
                assigned_object_type=ct,
                assigned_object_id=self.instance.pk + 9999,
                key='graceful_restart',
                value='true',
            ).clean()
        self.assertIn('assigned_object_id', ctx.exception.message_dict)

    def test_db_constraint_rejects_orphan_setting(self):
        # The CheckConstraint is the backstop for any path that bypasses
        # clean() (e.g. a raw create / bulk_create).
        with self.assertRaises(IntegrityError), transaction.atomic():
            ISISSetting.objects.create(key='graceful_restart', value='true')

    def test_clean_rejects_non_isis_assignment_type(self):
        # limit_choices_to only constrains the form picker; the model layer must
        # reject a non-IS-IS assigned type so the API/bulk-import paths cannot
        # attach a setting to (e.g.) a Device. The device exists, so the GFK
        # existence check passes and the type check is what fires.
        device_ct = ContentType.objects.get_for_model(self.instance.device)
        with self.assertRaises(ValidationError) as ctx:
            ISISSetting(
                assigned_object_type=device_ct,
                assigned_object_id=self.instance.device.pk,
                key='graceful_restart',
                value='true',
            ).clean()
        self.assertIn('assigned_object_type', ctx.exception.message_dict)

    def test_clean_rejects_non_integer_value_for_integer_key(self):
        with self.assertRaises(ValidationError) as ctx:
            ISISSetting(
                assigned_object=self.instance, key='spf_second_wait', value='not-a-number'
            ).clean()
        self.assertIn('value', ctx.exception.message_dict)

    def test_clean_accepts_integer_value_for_integer_key(self):
        ISISSetting(
            assigned_object=self.instance, key='spf_second_wait', value='250'
        ).clean()  # should not raise

    def test_clean_rejects_negative_integer_value_for_integer_key(self):
        # The form path enforces min_value=0; the model clean() is the backstop for the
        # API / import / direct-write paths, so it must reject negatives too.
        with self.assertRaises(ValidationError) as ctx:
            ISISSetting(
                assigned_object=self.instance, key='spf_second_wait', value='-1'
            ).clean()
        self.assertIn('value', ctx.exception.message_dict)

    def test_clean_rejects_non_boolean_value_for_boolean_key(self):
        with self.assertRaises(ValidationError) as ctx:
            ISISSetting(
                assigned_object=self.instance, key='graceful_restart', value='maybe'
            ).clean()
        self.assertIn('value', ctx.exception.message_dict)
