# SPDX-License-Identifier: Apache-2.0

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from dcim.models import Interface
from utilities.testing import create_test_device

from netbox_routing.models import (
    ISISFlexAlgo,
    ISISInstance,
    ISISInterface,
    ISISSetting,
)

__all__ = (
    'ISISInstanceModelTestCase',
    'ISISInterfaceModelTestCase',
    'ISISSettingModelTestCase',
    'ISISFlexAlgoModelTestCase',
    'ISISMigrationStateTestCase',
)


class ISISInstanceModelTestCase(TestCase):
    """Model-level (clean()) coverage for ISISInstance auth pairing."""

    @classmethod
    def setUpTestData(cls):
        cls.device = create_test_device(name='Device 1')

    def _instance(self, **kwargs):
        kwargs.setdefault('net', '49.0001.0000.0000.0001.00')
        return ISISInstance(
            device=self.device,
            process_tag='CORE',
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

    def test_clean_accepts_valid_net(self):
        self._instance(net='49.0001.1921.6800.1001.00').clean()  # should not raise

    def test_clean_accepts_blank_net(self):
        # net is optional (blank=True, default=''); an empty NET must pass.
        self._instance(net='').clean()

    def test_clean_rejects_malformed_net(self):
        # A NET has a fixed hex-grouped syntax; a malformed value must be rejected at
        # the model layer (form + API + import all run full_clean) rather than only
        # failing downstream when the adapter pushes it to the device.
        for bad in ('49.0001.bogus', 'not-a-net', '49.0001', '0000.0000.0001'):
            with self.subTest(net=bad):
                with self.assertRaises(ValidationError) as ctx:
                    self._instance(net=bad).clean()
                self.assertIn('net', ctx.exception.error_dict)

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


class ISISFlexAlgoModelTestCase(TestCase):
    """algo_id is constrained to the IS-IS Flex-Algo range 128-255.

    The model validators (MinValueValidator/MaxValueValidator) cover the
    form/API/import paths via full_clean(); a DB CheckConstraint is the backstop
    for direct writes (objects.create / bulk_create) that bypass full_clean(), so
    an out-of-range algo_id cannot be persisted through any path.
    """

    @classmethod
    def setUpTestData(cls):
        device = create_test_device(name='Device 1')
        cls.instance = ISISInstance.objects.create(
            device=device, process_tag='CORE', net='49.0001.0000.0000.0001.00'
        )

    def test_db_constraint_rejects_out_of_range_algo_id(self):
        for bad in (0, 127, 256):
            with (
                self.subTest(algo_id=bad),
                self.assertRaises(IntegrityError),
                transaction.atomic(),
            ):
                ISISFlexAlgo.objects.create(instance=self.instance, algo_id=bad)

    def test_db_constraint_accepts_boundary_algo_ids(self):
        # The 128 and 255 boundaries are valid and must round-trip.
        ISISFlexAlgo.objects.create(instance=self.instance, algo_id=128)
        ISISFlexAlgo.objects.create(instance=self.instance, algo_id=255)
        self.assertEqual(self.instance.flex_algos.count(), 2)


class ISISMigrationStateTestCase(TestCase):
    """The IS-IS migration must faithfully capture the models.

    Two guards: (1) every IS-IS model's *recorded* CreateModel bases must include
    PrimaryModel's DeleteMixin — a CreateModel that omits ``bases=`` silently records
    ``(models.Model,)`` instead, dropping DeleteMixin from the historical state used by
    data migrations (makemigrations does NOT detect a mixin-only bases drift, so nothing
    else catches it); (2) makemigrations finds no pending field/option drift, so a model
    field change (e.g. removing a column) can't land without the matching 0033 edit.
    """

    #: every IS-IS PrimaryModel — all subclass DeleteMixin via PrimaryModel
    ISIS_MODELS = (
        'isisinstance', 'isisinterface', 'isissetting', 'isislevel',
        'isisinterfacelevel', 'isissegmentrouting', 'isisflexalgo',
    )

    def test_migration_bases_include_delete_mixin(self):
        from django.db import connection
        from django.db.migrations.loader import MigrationLoader

        from netbox.models.deletion import DeleteMixin

        state = MigrationLoader(connection).project_state()
        dropped = [
            name
            for name in self.ISIS_MODELS
            if DeleteMixin not in state.models['netbox_routing', name].bases
        ]
        self.assertEqual(
            dropped, [], f'CreateModel bases dropped DeleteMixin for: {dropped}'
        )

    def test_no_pending_isis_migrations(self):
        # makemigrations is per-app, so scope the assertion to IS-IS models: a pending
        # change to any of them (e.g. a model field dropped without the matching 0033
        # edit) names that model in the dry-run output. Pre-existing drift in other
        # netbox_routing models (e.g. OSPF) is out of scope for this PR.
        from io import StringIO

        from django.core.management import call_command

        out = StringIO()
        call_command(
            'makemigrations', 'netbox_routing',
            dry_run=True, verbosity=1, stdout=out, stderr=out,
        )
        output = out.getvalue().lower()
        pending = [name for name in self.ISIS_MODELS if name in output]
        self.assertEqual(
            pending, [],
            f'pending IS-IS migration changes detected:\n{out.getvalue()}',
        )
