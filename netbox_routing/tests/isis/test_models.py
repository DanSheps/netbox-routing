# SPDX-License-Identifier: Apache-2.0

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase, override_settings

from dcim.models import Interface
from utilities.testing import create_test_device

from netbox_routing.models import (
    ISISFlexAlgo,
    ISISInstance,
    ISISInterface,
    ISISPrefixSID,
    ISISSRv6Locator,
    ISISSegmentRouting,
    ISISSetting,
)

__all__ = (
    'ISISInstanceModelTestCase',
    'ISISInterfaceModelTestCase',
    'ISISSettingModelTestCase',
    'ISISFlexAlgoModelTestCase',
    'ISISPrefixSIDModelTestCase',
    'ISISSegmentRoutingCleanTestCase',
    'ISISSRv6LocatorModelTestCase',
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

    def test_hmac_sha_auth_types_accepted(self):
        # Modern deployments authenticate with HMAC-SHA rather than md5/text
        # (IOS-XR hmac-sha-256, Junos/Nokia key-chain algorithms). full_clean
        # exercises both choice membership and the column length ('hmac-sha-256'
        # is 12 chars — longer than the original max_length=10).
        self._instance(
            area_auth_type='hmac-sha-256', area_auth_key='secret'
        ).full_clean()
        self._instance(
            domain_auth_type='hmac-sha-1', domain_auth_key='secret'
        ).full_clean()

    def test_fast_reroute_and_microloop_accepted(self):
        # Process-wide IP-FRR flavour (LFA / Remote-LFA / TI-LFA — IOS-XR
        # fast-reroute per-prefix [ti-lfa], Junos backup-spf-options, Nokia
        # loopfree-alternate) and micro-loop
        # avoidance, TI-LFA's usual companion knob.
        for flavour in ('lfa', 'remote-lfa', 'ti-lfa'):
            self._instance(fast_reroute=flavour).full_clean()
        self._instance(microloop_avoidance=True).full_clean()

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

    def test_hello_auth_hmac_sha_accepted(self):
        self._iface(
            n=14, hello_auth_type='hmac-sha-256', hello_auth_key='secret'
        ).full_clean()

    def test_frr_fields_accepted(self):
        # Per-interface fast-reroute: protection coverage (link/node — Junos
        # link-protection/node-link-protection, IOS-XR per-prefix protection)
        # and the tri-state enable, whose False is the EXPLICIT exclude form
        # (Nokia loopfree-alternate-exclude, IOS-XR fast-reroute exclude).
        self._iface(n=15, frr_enabled=True, frr_protection='node').full_clean()
        self._iface(n=16, frr_enabled=False).full_clean()
        self._iface(n=17, frr_protection='link').full_clean()

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
                assigned_object=self.instance,
                key='spf_second_wait',
                value='not-a-number',
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

    def test_te_router_id_keys_accepted(self):
        # The IS-IS traffic-engineering router-ID knob (IOS/XR 'mpls traffic-eng
        # router-id'; derived from the global
        # router-id on Junos/Nokia). Without vocabulary keys a reader-emitted
        # setting is silently filtered downstream and the value never lands.
        # full_clean exercises key choice membership; values are strings (an IP
        # or, on Cisco, an interface reference).
        for key, value in (
            ('te_ipv4_router_id', '192.0.2.1'),
            ('te_ipv6_router_id', '2001:db8::1'),
        ):
            ISISSetting(
                assigned_object=self.instance, key=key, value=value
            ).full_clean()

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


class ISISPrefixSIDModelTestCase(TestCase):
    """Per-prefix prefix-SID: index and absolute label are mutually exclusive
    (clean()), and the algorithm is 0 or the Flex-Algo range 128-255 (DB CheckConstraint
    is the backstop for direct writes that bypass full_clean())."""

    @classmethod
    def setUpTestData(cls):
        device = create_test_device(name='Device 1')
        instance = ISISInstance.objects.create(
            device=device, process_tag='CORE', net='49.0001.0000.0000.0001.00'
        )
        loopback = Interface.objects.create(
            name='Loopback0', device=device, type='virtual'
        )
        cls.isis_interface = ISISInterface.objects.create(
            instance=instance, interface=loopback, address_family='ipv4', passive=True
        )

    def test_clean_rejects_index_and_label_together(self):
        sid = ISISPrefixSID(
            interface=self.isis_interface, algorithm=0, sid_index=10, sid_label=16010
        )
        with self.assertRaises(ValidationError):
            sid.clean()

    def test_clean_accepts_index_only(self):
        ISISPrefixSID(interface=self.isis_interface, algorithm=0, sid_index=10).clean()

    def test_clean_accepts_label_only(self):
        ISISPrefixSID(
            interface=self.isis_interface, algorithm=128, sid_label=16010
        ).clean()

    def test_clean_rejects_out_of_range_algorithm(self):
        # clean() must reject the 1-127 gap (and >255) with a ValidationError
        # (HTTP 400) rather than deferring to the DB CheckConstraint, which would
        # surface as an IntegrityError (HTTP 500).
        for bad in (1, 127, 256):
            with self.subTest(algorithm=bad), self.assertRaises(ValidationError) as ctx:
                ISISPrefixSID(
                    interface=self.isis_interface, algorithm=bad, sid_index=1
                ).clean()
            self.assertIn('algorithm', ctx.exception.error_dict)

    def test_clean_accepts_valid_algorithm(self):
        for algo in (0, 128, 255):
            ISISPrefixSID(
                interface=self.isis_interface, algorithm=algo, sid_index=1
            ).clean()  # should not raise

    def test_db_constraint_rejects_out_of_range_algorithm(self):
        for bad in (1, 127, 256):
            with (
                self.subTest(algorithm=bad),
                self.assertRaises(IntegrityError),
                transaction.atomic(),
            ):
                ISISPrefixSID.objects.create(
                    interface=self.isis_interface, algorithm=bad, sid_index=1
                )

    def test_db_constraint_accepts_valid_algorithms(self):
        # 0 (SPF) and the 128/255 Flex-Algo boundaries must all round-trip.
        for algo in (0, 128, 255):
            ISISPrefixSID.objects.create(
                interface=self.isis_interface, algorithm=algo, sid_index=algo + 1
            )
        self.assertEqual(self.isis_interface.prefix_sids.count(), 3)

    def test_unique_interface_algorithm(self):
        ISISPrefixSID.objects.create(
            interface=self.isis_interface, algorithm=0, sid_index=1
        )
        with self.assertRaises(IntegrityError), transaction.atomic():
            ISISPrefixSID.objects.create(
                interface=self.isis_interface, algorithm=0, sid_index=2
            )


class ISISSegmentRoutingCleanTestCase(TestCase):
    """SRGB and SRLB are each a (start, range) pair — a lone bound is rejected."""

    @classmethod
    def setUpTestData(cls):
        device = create_test_device(name='Device 1')
        cls.instance = ISISInstance.objects.create(
            device=device, process_tag='CORE', net='49.0001.0000.0000.0001.00'
        )

    def _sr(self, **kwargs):
        return ISISSegmentRouting(instance=self.instance, **kwargs)

    def test_clean_rejects_srgb_start_without_range(self):
        with self.assertRaises(ValidationError):
            self._sr(srgb_start=16000).clean()

    def test_clean_rejects_srgb_range_without_start(self):
        with self.assertRaises(ValidationError):
            self._sr(srgb_range=8000).clean()

    def test_clean_rejects_srlb_start_without_range(self):
        with self.assertRaises(ValidationError):
            self._sr(srlb_start=15000).clean()

    def test_clean_accepts_complete_blocks(self):
        self._sr(
            srgb_start=16000, srgb_range=8000, srlb_start=15000, srlb_range=1000
        ).clean()

    def test_clean_accepts_no_blocks(self):
        self._sr(enabled=True, srv6_enabled=True).clean()


class ISISSRv6LocatorModelTestCase(TestCase):
    """SRv6 locator: RFC 8986 SID structure (block+node+function+argument) must fit
    128 bits when pinned; (instance, name) is unique; the prefix round-trips."""

    @classmethod
    def setUpTestData(cls):
        device = create_test_device(name='Device 1')
        cls.instance = ISISInstance.objects.create(
            device=device, process_tag='CORE', net='49.0001.0000.0000.0001.00'
        )

    def test_clean_rejects_oversized_sid_structure(self):
        # 40 + 24 + 48 + 32 = 144 > 128
        loc = ISISSRv6Locator(
            instance=self.instance,
            name='LOC1',
            prefix='2001:db8:0:a2::/64',
            block_length=40,
            node_length=24,
            function_length=48,
            argument_length=32,
        )
        with self.assertRaises(ValidationError):
            loc.clean()

    def test_clean_accepts_within_128(self):
        # 40 + 24 + 16 = 80
        ISISSRv6Locator(
            instance=self.instance,
            name='LOC1',
            prefix='2001:db8:0:a2::/64',
            block_length=40,
            node_length=24,
            function_length=16,
        ).clean()

    def test_clean_accepts_derived_lengths(self):
        # All lengths null → the device derives them; only the prefix is required.
        ISISSRv6Locator(
            instance=self.instance, name='LOC1', prefix='2001:db8:0:a2::/64'
        ).clean()

    def test_unique_instance_name(self):
        ISISSRv6Locator.objects.create(
            instance=self.instance, name='LOC1', prefix='2001:db8:0:a2::/64'
        )
        with self.assertRaises(IntegrityError), transaction.atomic():
            ISISSRv6Locator.objects.create(
                instance=self.instance, name='LOC1', prefix='2001:db8:0:a3::/64'
            )

    def test_prefix_roundtrips(self):
        loc = ISISSRv6Locator.objects.create(
            instance=self.instance, name='LOC2', prefix='2001:db8:0:a2::/64'
        )
        loc.refresh_from_db()
        self.assertEqual(str(loc.prefix), '2001:db8:0:a2::/64')


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
        'isisinstance',
        'isisinterface',
        'isissetting',
        'isislevel',
        'isisinterfacelevel',
        'isissegmentrouting',
        'isisflexalgo',
        'isisprefixsid',
        'isissrv6locator',
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

    # NetBox overrides makemigrations to refuse unless settings.DEVELOPER is True (or
    # --check is passed) — see core/management/commands/makemigrations.py. CI's
    # configuration_testing leaves DEVELOPER=False, so force it on for this in-process
    # dry-run; without it the command raises "development purposes only" and the guard
    # never runs. (Local isis_test config sets DEVELOPER=True, which is why this passed
    # locally but errored in CI.)
    @override_settings(DEVELOPER=True)
    def test_no_pending_isis_migrations(self):
        # makemigrations is per-app, so scope the assertion to IS-IS models: a pending
        # change to any of them (e.g. a model field dropped without the matching 0033
        # edit) names that model in the dry-run output. Pre-existing drift in other
        # netbox_routing models (e.g. OSPF) is out of scope for this PR.
        from io import StringIO

        from django.core.management import call_command

        out = StringIO()
        call_command(
            'makemigrations',
            'netbox_routing',
            dry_run=True,
            verbosity=1,
            stdout=out,
            stderr=out,
        )
        output = out.getvalue().lower()
        pending = [name for name in self.ISIS_MODELS if name in output]
        self.assertEqual(
            pending,
            [],
            f'pending IS-IS migration changes detected:\n{out.getvalue()}',
        )
