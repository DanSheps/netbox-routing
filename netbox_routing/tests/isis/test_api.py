# SPDX-License-Identifier: Apache-2.0

from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from dcim.models import Interface
from ipam.models import VRF
from utilities.testing import APITestCase, APIViewTestCases, create_test_device

from netbox_routing.models import (
    ISISInstance,
    ISISInterface,
    ISISSetting,
    ISISLevel,
    ISISInterfaceLevel,
    ISISSegmentRouting,
    ISISFlexAlgo,
)

__all__ = (
    'ISISInstanceAPITestCase',
    'ISISInterfaceAPITestCase',
    'ISISSettingAPITestCase',
    'ISISLevelAPITestCase',
    'ISISInterfaceLevelAPITestCase',
    'ISISSegmentRoutingAPITestCase',
    'ISISFlexAlgoAPITestCase',
    'ISISSettingPrefetchAPITestCase',
    'ISISChildDisplayPrefetchAPITestCase',
    'ISISSettingAssignmentAPITestCase',
)


class ISISInstanceAPITestCase(APIViewTestCases.APIViewTestCase):
    model = ISISInstance
    view_namespace = 'plugins-api:netbox_routing'
    # verbose_name 'IS-IS Instance' → default base name 'is-is_instance' (invalid
    # identifier); pin to the schema query field name.
    graphql_base_name = 'isis_instance'
    brief_fields = [
        'device',
        'display',
        'id',
        'is_type',
        'net',
        'process_tag',
        'url',
        'vrf',
    ]

    user_permissions = ('dcim.view_device',)
    bulk_update_data = {'description': 'A test description'}

    @classmethod
    def setUpTestData(cls):
        vrf = VRF.objects.create(name='Test VRF')
        device = create_test_device(name='Test Device')

        data = (
            cls.model(
                device=device,
                vrf=None,
                process_tag='CORE',
                net='49.0001.0000.0000.0001.00',
                is_type='level-1-2',
            ),
            cls.model(
                device=device,
                vrf=vrf,
                process_tag='EDGE',
                net='49.0001.0000.0000.0002.00',
                is_type='level-2-only',
            ),
            cls.model(
                device=device,
                vrf=None,
                process_tag='FABRIC',
                net='49.0001.0000.0000.0003.00',
                is_type='level-1',
            ),
        )
        cls.model.objects.bulk_create(data)

        cls.create_data = [
            {
                'device': device.pk,
                'vrf': vrf.pk,
                'process_tag': 'ACCESS',
                'net': '49.0001.0000.0000.0004.00',
                'is_type': 'level-1-2',
                'metric_style': 'wide',
                'spf_initial_wait': 50,
                'spf_max_wait': 5000,
                'lsp_lifetime': 65535,
                'lsp_refresh_interval': 32767,
                'lsp_mtu': 1492,
                'te_enabled': True,
                'sr_enabled': True,
                'distance': 115,
                'maximum_paths': 8,
            },
        ]


class ISISInterfaceAPITestCase(APIViewTestCases.APIViewTestCase):
    model = ISISInterface
    view_namespace = 'plugins-api:netbox_routing'
    # verbose_name 'IS-IS Interface' → default base name 'is-is_interface' (invalid
    # identifier); pin to the schema query field name.
    graphql_base_name = 'isis_interface'
    brief_fields = [
        'address_family',
        'display',
        'id',
        'instance',
        'interface',
        'url',
    ]

    user_permissions = (
        'netbox_routing.view_isisinstance',
        'dcim.view_device',
        'dcim.view_interface',
    )
    bulk_update_data = {'description': 'A test description'}

    @classmethod
    def setUpTestData(cls):
        device = create_test_device(name='Test Device')
        instance = ISISInstance.objects.create(
            device=device,
            process_tag='CORE',
            net='49.0001.0000.0000.0001.00',
            is_type='level-1-2',
        )

        interfaces = (
            Interface(device=device, name='Interface 1', type='virtual'),
            Interface(device=device, name='Interface 2', type='virtual'),
            Interface(device=device, name='Interface 3', type='virtual'),
            Interface(device=device, name='Interface 4', type='virtual'),
        )
        Interface.objects.bulk_create(interfaces)

        data = (
            cls.model(
                instance=instance,
                interface=interfaces[0],
                address_family='ipv4',
                passive=True,
                hello_auth_type='md5',
                hello_auth_key='s3cret',
            ),
            cls.model(
                instance=instance,
                interface=interfaces[1],
                address_family='ipv6',
                passive=False,
            ),
            cls.model(
                instance=instance,
                interface=interfaces[2],
                address_family='ipv4',
            ),
        )
        cls.model.objects.bulk_create(data)

        cls.create_data = [
            {
                'instance': instance.pk,
                'interface': interfaces[3].pk,
                'address_family': 'ipv6',
                'circuit_type': 'level-1-2',
                'network_type': 'broadcast',
                'metric': 20,
                'passive': True,
                'hello_auth_type': 'md5',
                'hello_auth_key': 's3cret',
                'csnp_interval': 10,
                'retransmit_interval': 5,
                'lsp_interval': 100,
                'mesh_group': 'blocked',
            },
        ]


class ISISSettingAPITestCase(APIViewTestCases.APIViewTestCase):
    model = ISISSetting
    view_namespace = 'plugins-api:netbox_routing'
    graphql_base_name = 'isis_setting'
    brief_fields = ['assigned_object', 'display', 'id', 'key', 'url']

    user_permissions = (
        'netbox_routing.view_isisinstance',
        'dcim.view_device',
    )
    bulk_update_data = {'description': 'A test description'}

    @classmethod
    def setUpTestData(cls):
        device = create_test_device(name='Test Device')
        instance = ISISInstance.objects.create(
            device=device,
            process_tag='CORE',
            net='49.0001.0000.0000.0001.00',
            is_type='level-1-2',
        )
        ct = ContentType.objects.get_for_model(ISISInstance)

        data = (
            cls.model(assigned_object=instance, key='graceful_restart', value='true'),
            cls.model(assigned_object=instance, key='spf_second_wait', value='1000'),
            cls.model(assigned_object=instance, key='ldp_sync', value='true'),
        )
        cls.model.objects.bulk_create(data)

        cls.create_data = [
            {
                'assigned_object_type': f'{ct.app_label}.{ct.model}',
                'assigned_object_id': instance.pk,
                'key': 'prefix_suppression',
                'value': 'true',
            },
            {
                'assigned_object_type': f'{ct.app_label}.{ct.model}',
                'assigned_object_id': instance.pk,
                'key': 'log_adjacency_changes',
                'value': 'true',
            },
        ]


class ISISLevelAPITestCase(APIViewTestCases.APIViewTestCase):
    model = ISISLevel
    view_namespace = 'plugins-api:netbox_routing'
    graphql_base_name = 'isis_level'
    brief_fields = ['default_metric', 'display', 'id', 'level', 'url']
    user_permissions = ('netbox_routing.view_isisinstance',)
    bulk_update_data = {'default_metric': 50}

    @classmethod
    def setUpTestData(cls):
        device = create_test_device(name='Test Device')
        inst = ISISInstance.objects.create(
            device=device, process_tag='0', net='49.0001.0000.0000.0001.00', is_type='level-1-2'
        )
        ISISLevel.objects.create(instance=inst, level=1, default_metric=10)
        ISISLevel.objects.create(instance=inst, level=2, default_metric=10, wide_metrics_only=True)
        inst2 = ISISInstance.objects.create(device=device, process_tag='100')
        ISISLevel.objects.create(instance=inst2, level=1, default_metric=20)
        cls.create_data = [
            {'instance': inst2.pk, 'level': 2, 'default_metric': 30, 'wide_metrics_only': True},
        ]


class ISISInterfaceLevelAPITestCase(APIViewTestCases.APIViewTestCase):
    model = ISISInterfaceLevel
    view_namespace = 'plugins-api:netbox_routing'
    graphql_base_name = 'isis_interface_level'
    brief_fields = ['display', 'id', 'level', 'metric', 'url']
    user_permissions = ('netbox_routing.view_isisinterface',)
    bulk_update_data = {'metric': 99}

    @classmethod
    def setUpTestData(cls):
        device = create_test_device(name='Test Device')
        inst = ISISInstance.objects.create(device=device, process_tag='0')
        ifaces = [
            Interface.objects.create(device=device, name=f'Interface {n}', type='virtual')
            for n in range(1, 5)
        ]
        ri = [
            ISISInterface.objects.create(instance=inst, interface=ifaces[i], address_family='ipv4')
            for i in range(4)
        ]
        ISISInterfaceLevel.objects.create(interface=ri[0], level=1, metric=10)
        ISISInterfaceLevel.objects.create(interface=ri[1], level=2, metric=20)
        ISISInterfaceLevel.objects.create(interface=ri[2], level=1, metric=30)
        cls.create_data = [
            {'interface': ri[3].pk, 'level': 2, 'metric': 40, 'hello_interval': 3},
        ]


class ISISSegmentRoutingAPITestCase(APIViewTestCases.APIViewTestCase):
    model = ISISSegmentRouting
    view_namespace = 'plugins-api:netbox_routing'
    graphql_base_name = 'isis_segment_routing'
    brief_fields = ['display', 'enabled', 'id', 'prefix_sid_range', 'url']
    user_permissions = ('netbox_routing.view_isisinstance',)
    bulk_update_data = {'maximum_sid_depth': 11}

    @classmethod
    def setUpTestData(cls):
        device = create_test_device(name='Test Device')
        insts = [
            ISISInstance.objects.create(device=device, process_tag=str(n)) for n in range(4)
        ]
        ISISSegmentRouting.objects.create(instance=insts[0], enabled=True, prefix_sid_range='global')
        ISISSegmentRouting.objects.create(instance=insts[1], enabled=True, srgb_start=16000, srgb_range=8000)
        ISISSegmentRouting.objects.create(instance=insts[2], enabled=False)
        cls.create_data = [
            {'instance': insts[3].pk, 'enabled': True, 'prefix_sid_range': 'global', 'maximum_sid_depth': 10},
        ]


class ISISFlexAlgoAPITestCase(APIViewTestCases.APIViewTestCase):
    model = ISISFlexAlgo
    view_namespace = 'plugins-api:netbox_routing'
    graphql_base_name = 'isis_flex_algo'
    brief_fields = ['algo_id', 'display', 'id', 'instance', 'metric_type', 'url']
    user_permissions = ('netbox_routing.view_isisinstance',)
    bulk_update_data = {'priority': 50}

    @classmethod
    def setUpTestData(cls):
        device = create_test_device(name='Test Device')
        inst = ISISInstance.objects.create(device=device, process_tag='0')
        ISISFlexAlgo.objects.create(instance=inst, algo_id=128, metric_type='igp-metric', priority=100,
                                    admin_group_exclude='BLUE')
        ISISFlexAlgo.objects.create(instance=inst, algo_id=129, metric_type='igp-metric', priority=100,
                                    admin_group_exclude='RED')
        inst2 = ISISInstance.objects.create(device=device, process_tag='100')
        ISISFlexAlgo.objects.create(instance=inst2, algo_id=128, metric_type='te-metric')
        cls.create_data = [
            {'instance': inst2.pk, 'algo_id': 130, 'metric_type': 'delay-metric', 'priority': 200},
        ]


class ISISSettingPrefetchAPITestCase(APITestCase):
    """Regression for the assigned_object (GenericForeignKey) N+1.

    ISISSettingSerializer renders assigned_object, so the list view must
    GenericPrefetch it; otherwise each row fetches its target separately and
    the query count grows with the number of rows. We assert query-count
    invariance under row growth (with a fixed span of assigned content types),
    which is the N+1 signature without pinning a brittle absolute count.
    """

    user_permissions = (
        'netbox_routing.view_isissetting',
        'netbox_routing.view_isisinstance',
        'netbox_routing.view_isisinterface',
        'dcim.view_device',
        'dcim.view_interface',
    )

    @classmethod
    def setUpTestData(cls):
        cls.device = create_test_device(name='Prefetch Device')

    def _instance_setting(self, tag, key):
        inst = ISISInstance.objects.create(device=self.device, process_tag=tag)
        return ISISSetting.objects.create(assigned_object=inst, key=key, value='true')

    def _interface_setting(self, name, key):
        inst = ISISInstance.objects.create(device=self.device, process_tag=name)
        iface = Interface.objects.create(device=self.device, name=name, type='virtual')
        ri = ISISInterface.objects.create(instance=inst, interface=iface, address_family='ipv4')
        return ISISSetting.objects.create(assigned_object=ri, key=key, value='true')

    @staticmethod
    def _target_queries(ctx):
        # Queries that read an assigned_object target table. Without a
        # GenericPrefetch the serializer reads one per row (N+1); with it the
        # reads are batched per content type, so the count is constant. We count
        # only these tables to isolate THIS finding from unrelated per-row
        # queries (tags, custom fields) common to every NetBox list view.
        return [
            q
            for q in ctx.captured_queries
            if 'netbox_routing_isisinstance' in q['sql']
            or 'netbox_routing_isisinterface' in q['sql']
        ]

    def test_assigned_object_prefetched_no_n_plus_1(self):
        url = reverse('plugins-api:netbox_routing-api:isissetting-list') + '?limit=0'

        # Both phases span the same two content types (instance + interface), so
        # a correct GenericPrefetch keeps the target reads constant as rows grow.
        self._instance_setting('A', 'graceful_restart')
        self._interface_setting('if-a', 'graceful_restart')
        with CaptureQueriesContext(connection) as small:
            response = self.client.get(url, **self.header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)

        self._instance_setting('B', 'ldp_sync')
        self._instance_setting('C', 'graceful_restart')
        self._interface_setting('if-b', 'ldp_sync')
        self._interface_setting('if-c', 'graceful_restart')
        with CaptureQueriesContext(connection) as large:
            response = self.client.get(url, **self.header)
        self.assertEqual(response.json()['count'], 6)

        small_targets = len(self._target_queries(small))
        large_targets = len(self._target_queries(large))
        self.assertEqual(
            large_targets,
            small_targets,
            'assigned_object is not prefetched: target-table reads grew from '
            f'{small_targets} to {large_targets} as rows were added (expected constant)',
        )


class ISISChildDisplayPrefetchAPITestCase(APITestCase):
    """The IS-IS child list views render `display` = str(obj), whose __str__ walks
    an FK chain (e.g. ISISLevel -> instance -> device; ISISInterfaceLevel ->
    ISISInterface -> dcim Interface). Without select_related on that chain each row
    re-reads the related tables, so the read count grows with the row count. We
    assert those target-table reads stay constant as rows are added, which is the
    N+1 signature without pinning a brittle absolute count.
    """

    user_permissions = (
        'netbox_routing.view_isislevel',
        'netbox_routing.view_isisinterfacelevel',
        'netbox_routing.view_isissegmentrouting',
        'netbox_routing.view_isisflexalgo',
        'netbox_routing.view_isisinstance',
        'netbox_routing.view_isisinterface',
        'dcim.view_device',
        'dcim.view_interface',
    )

    @classmethod
    def setUpTestData(cls):
        cls.device = create_test_device(name='Prefetch Device')

    def _instance(self, tag):
        return ISISInstance.objects.create(device=self.device, process_tag=tag)

    def _isis_interface(self, name):
        iface = Interface.objects.create(device=self.device, name=name, type='virtual')
        return ISISInterface.objects.create(
            instance=self._instance(name), interface=iface, address_family='ipv4'
        )

    def _assert_constant_target_reads(self, url_name, tables, make_rows):
        url = reverse(f'plugins-api:netbox_routing-api:{url_name}-list') + '?limit=0'

        def reads(ctx):
            return [q for q in ctx.captured_queries if any(t in q['sql'] for t in tables)]

        make_rows(0)
        make_rows(1)
        with CaptureQueriesContext(connection) as small:
            self.assertEqual(self.client.get(url, **self.header).status_code, 200)
        for i in range(2, 6):
            make_rows(i)
        with CaptureQueriesContext(connection) as large:
            self.assertEqual(self.client.get(url, **self.header).status_code, 200)

        small_n, large_n = len(reads(small)), len(reads(large))
        self.assertEqual(
            large_n,
            small_n,
            f'{url_name}: {tables} reads grew from {small_n} to {large_n} as rows '
            'were added (expected constant — chain not select_related)',
        )

    def test_level_display_constant_queries(self):
        self._assert_constant_target_reads(
            'isislevel',
            ('netbox_routing_isisinstance', 'dcim_device'),
            lambda i: ISISLevel.objects.create(instance=self._instance(f'lvl{i}'), level=1),
        )

    def test_segmentrouting_display_constant_queries(self):
        self._assert_constant_target_reads(
            'isissegmentrouting',
            ('netbox_routing_isisinstance', 'dcim_device'),
            lambda i: ISISSegmentRouting.objects.create(instance=self._instance(f'sr{i}'), enabled=True),
        )

    def test_flexalgo_display_constant_queries(self):
        self._assert_constant_target_reads(
            'isisflexalgo',
            ('netbox_routing_isisinstance', 'dcim_device'),
            lambda i: ISISFlexAlgo.objects.create(instance=self._instance(f'fa{i}'), algo_id=128 + i),
        )

    def test_interfacelevel_display_constant_queries(self):
        self._assert_constant_target_reads(
            'isisinterfacelevel',
            ('netbox_routing_isisinterface', 'dcim_interface'),
            lambda i: ISISInterfaceLevel.objects.create(interface=self._isis_interface(f'ifl{i}'), level=1),
        )


class ISISSettingAssignmentAPITestCase(APITestCase):
    """The API must reject an unassigned ISISSetting with a clean 400 (via
    model.clean()), not a 500 and not a silently-persisted orphan row."""

    user_permissions = (
        'netbox_routing.add_isissetting',
        'netbox_routing.view_isissetting',
    )

    def test_create_without_assignment_is_rejected(self):
        url = reverse('plugins-api:netbox_routing-api:isissetting-list')
        response = self.client.post(
            url,
            {'key': 'graceful_restart', 'value': 'true'},
            format='json',
            **self.header,
        )
        self.assertEqual(response.status_code, 400, response.content)
        self.assertEqual(ISISSetting.objects.count(), 0)

    def test_create_with_nonexistent_object_is_rejected(self):
        # A GenericForeignKey has no DB FK, so a syntactically-valid type + a
        # dangling id must be rejected (400) rather than persisting an orphan row.
        ct = ContentType.objects.get_for_model(ISISInstance)
        url = reverse('plugins-api:netbox_routing-api:isissetting-list')
        response = self.client.post(
            url,
            {
                'assigned_object_type': f'{ct.app_label}.{ct.model}',
                'assigned_object_id': 999999,
                'key': 'graceful_restart',
                'value': 'true',
            },
            format='json',
            **self.header,
        )
        self.assertEqual(response.status_code, 400, response.content)
        self.assertEqual(ISISSetting.objects.count(), 0)
