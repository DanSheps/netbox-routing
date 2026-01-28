from utilities.testing import APIViewTestCases

from netbox_routing.models.bgp import *
from netbox_routing.tests.base import *
from netbox_routing.tests.bgp.base import *

__all__ = (
    'BGPPeerTemplateTestCase',
    'BGPPolicyTemplateTestCase',
    'BGPSessionTemplateTestCase',
)


class BGPPeerTemplateTestCase(APIViewTestCases.APIViewTestCase):
    model = BGPPeerTemplate
    view_namespace = "plugins-api:netbox_routing"
    brief_fields = [
        'display',
        'id',
        'name',
        'remote_as',
        'url',
    ]

    bulk_update_data = {'description': 'Description'}
    routing_required_fields = ('name',)

    @classmethod
    def setUpTestData(cls):
        cls.instances = (
            cls.model(
                name=f'{cls.model._meta.verbose_name} {i}',
            )
            for i in range(1, 5)
        )
        cls.model.objects.bulk_create(cls.instances)
        cls.create_data = [
            {'name': f'{cls.model._meta.verbose_name} {i}'} for i in range(5, 7)
        ]


class BGPPolicyTemplateTestCase(APIViewTestCases.APIViewTestCase):
    model = BGPPolicyTemplate
    view_namespace = "plugins-api:netbox_routing"
    brief_fields = [
        'display',
        'id',
        'name',
        'url',
    ]

    bulk_update_data = {'description': 'Description'}
    routing_required_fields = ('name',)

    @classmethod
    def setUpTestData(cls):
        cls.instances = (
            cls.model(
                name=f'{cls.model._meta.verbose_name} {i}',
            )
            for i in range(1, 5)
        )
        cls.model.objects.bulk_create(cls.instances)

        cls.create_data = [
            {'name': f'{cls.model._meta.verbose_name} {i}'} for i in range(5, 7)
        ]


class BGPSessionTemplateTestCase(APIViewTestCases.APIViewTestCase):
    model = BGPSessionTemplate
    view_namespace = "plugins-api:netbox_routing"
    brief_fields = [
        'display',
        'id',
        'name',
        'parent',
        'url',
    ]

    bulk_update_data = {'description': 'Description'}
    routing_required_fields = ('name',)

    @classmethod
    def setUpTestData(cls):
        cls.instances = (
            cls.model(
                name=f'{cls.model._meta.verbose_name} {i}',
            )
            for i in range(1, 5)
        )
        cls.model.objects.bulk_create(cls.instances)

        cls.create_data = [
            {'name': f'{cls.model._meta.verbose_name} {i}'} for i in range(5, 7)
        ]


class BGPRouterTestCase(
    AutomatedModelCreationMixin, ASNMixin, APIViewTestCases.APIViewTestCase
):
    model = BGPRouter
    view_namespace = "plugins-api:netbox_routing"
    brief_fields = [
        'asn',
        'assigned_object',
        'display',
        'id',
        'name',
        'url',
    ]

    bulk_update_data = {'description': 'Description'}
    routing_required_fields = (
        'name',
        ('asn', 'asns'),
    )

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.create_data = [
            {'name': f'{cls.model._meta.verbose_name}: {i}', 'asn': cls.asns[i].pk}
            for i in range(5, 7)
        ]


class BGPScopeTestCase(
    AutomatedModelCreationMixin,
    BGPRouterMixin,
    VRFMixin,
    APIViewTestCases.APIViewTestCase,
):
    model = BGPScope
    view_namespace = "plugins-api:netbox_routing"
    brief_fields = [
        'display',
        'id',
        'router',
        'url',
        'vrf',
    ]

    bulk_update_data = {'description': 'Description'}
    routing_required_fields = (
        'router',
        ('vrf', 'vrfs'),
    )

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.create_data = [
            {'router': cls.router.pk, 'vrf': cls.vrfs[i].pk} for i in range(5, 7)
        ]


class BGPAddressFamilyTestCase(
    AutomatedModelCreationMixin, BGPScopeMixin, APIViewTestCases.APIViewTestCase
):
    model = BGPAddressFamily
    view_namespace = "plugins-api:netbox_routing"
    brief_fields = [
        'address_family',
        'display',
        'id',
        'scope',
        'url',
    ]

    bulk_update_data = {'description': 'Description'}
    routing_required_fields = (
        'scope',
        ('address_family', 'afs'),
    )
    afs = (
        'ipv4-unicast',
        'ipv6-unicast',
        'vpnv4-unicast',
        'vpnv6-unicast',
        'l2vpn-vpls',
        'l2vpn-evpn',
        'ipv4-multicast',
        'ipv6-multicast',
    )

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.create_data = [
            {'scope': cls.scope.pk, 'address_family': cls.afs[i]} for i in range(5, 7)
        ]


class BGPPeerTestCase(
    AutomatedModelCreationMixin,
    AddressesMixin,
    BGPScopeMixin,
    APIViewTestCases.APIViewTestCase,
):
    model = BGPPeer
    view_namespace = "plugins-api:netbox_routing"
    brief_fields = [
        'display',
        'enabled',
        'id',
        'name',
        'peer',
        'remote_as',
        'scope',
        'url',
    ]

    bulk_update_data = {'description': 'Description'}
    enabled = True
    routing_required_fields = (
        'name',
        'scope',
        'enabled',
        ('remote_as', 'asn'),
        ('peer', 'ip_addresses'),
    )

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.create_data = [
            {
                'name': f'{cls.model._meta.verbose_name}: {i}',
                'scope': cls.scope.pk,
                'enabled': cls.enabled,
                'remote_as': cls.asn.pk,
                'peer': cls.ip_addresses[i].pk,
            }
            for i in range(5, 7)
        ]


class BGPPeerAddressFamilyTestCase(
    AutomatedModelCreationMixin,
    BGPPeerMixin,
    BGPAddressFamilyMixin,
    APIViewTestCases.APIViewTestCase,
):
    model = BGPPeerAddressFamily
    view_namespace = "plugins-api:netbox_routing"
    brief_fields = [
        'address_family',
        'assigned_object',
        'display',
        'enabled',
        'id',
        'url',
    ]

    bulk_update_data = {'description': 'Description'}
    enabled = True
    routing_required_fields = (
        ('assigned_object', 'peer'),
        ('address_family', 'address_families'),
        'enabled',
    )

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        ctype = f'{cls.peer._meta.app_label}.{cls.peer._meta.model_name}'
        cls.create_data = [
            {
                'assigned_object_type': ctype,
                'assigned_object_id': cls.peer.pk,
                'enabled': cls.enabled,
                'address_family': cls.address_families[i].pk,
            }
            for i in range(5, 7)
        ]
