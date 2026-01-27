from utilities.testing import ViewTestCases

from netbox_routing.models.bgp import *
from netbox_routing.tests.base import *
from netbox_routing.tests.bgp.base import *

__all__ = (
    'BGPRouterTestCase',
    'BGPScopeTestCase',
)


class BGPAutomatedFormDataCreationMixin(AutomatedModelCreationMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.form_data = {
            'name': '{cls.model._meta.verbose_name}: 4',
        }


class BGPRouterTestCase(
    ASNMixin,
    BulkEditMixin,
    PluginBaseURLMixin,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    # ViewTestCases.BulkImportObjectsViewTestCase,
    model = BGPRouter

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        items = []
        name = 'BGP Router'
        for seq in range(1, 4):
            asn = ASN.objects.all()[seq - 1]
            items.append(
                cls.model(
                    name=f'{name} {seq}',
                    asn=asn,
                ),
            )
        cls.model.objects.bulk_create(items)

        cls.form_data = {'name': f'{name} 4', 'asn': ASN.objects.last().pk}


class BGPScopeTestCase(
    BGPRouterMixin,
    BulkEditMixin,
    PluginBaseURLMixin,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    # ViewTestCases.BulkImportObjectsViewTestCase,
    model = BGPScope

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        items = []
        for seq in range(1, 4):
            vrf = VRF.objects.create(name=f'VRF {seq}', rd=f'64512:{seq}')
            items.append(
                cls.model(
                    router=cls.router,
                    vrf=vrf,
                ),
            )
        cls.model.objects.bulk_create(items)

        cls.form_data = {
            'router': cls.router.pk,
        }


class BGPAddressFamilyTestCase(
    BGPScopeMixin,
    BulkEditMixin,
    PluginBaseURLMixin,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    # ViewTestCases.BulkImportObjectsViewTestCase,
    model = BGPAddressFamily

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        items = []
        for seq in ('ipv4-unicast', 'ipv6-unicast', 'vpnv4-unicast', 'vpnv6-unicast'):
            items.append(
                cls.model(
                    scope=cls.scope,
                    address_family=seq,
                ),
            )
        cls.model.objects.bulk_create(items)

        cls.form_data = {
            'scope': cls.scope.pk,
            'address_family': 'l2vpn-evpn',
        }


class BGPPeerTestCase(
    BGPScopeMixin,
    BulkEditMixin,
    PluginBaseURLMixin,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    # ViewTestCases.BulkImportObjectsViewTestCase,
    model = BGPPeer

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        items = []
        for seq in (
            '10.0.0.1/24',
            '10.0.0.2/24',
            '10.0.0.3/24',
            '10.0.0.4/24',
            '10.0.0.5/24',
            '10.0.0.6/24',
        ):
            peer = IPAddress.objects.create(address=IPNetwork(seq))
            items.append(
                cls.model(
                    name=f'BGP Peer: {seq}',
                    scope=cls.scope,
                    peer=peer,
                ),
            )
        cls.model.objects.bulk_create(items)

        peer = IPAddress.objects.create(address=IPNetwork('10.0.0.7/24'))
        cls.form_data = {
            'name': 'BGP Peer: 10.0.0.7/24',
            'scope': cls.scope.pk,
            'peer': peer.pk,
        }


class BGPPeerAddressFamilyTestCase(
    AutomatedModelCreationMixin,
    BGPPeerMixin,
    BGPAddressFamilyMixin,
    BulkEditMixin,
    PluginBaseURLMixin,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    # ViewTestCases.BulkImportObjectsViewTestCase,
    model = BGPPeerAddressFamily
    validation_excluded_fields = ('peer',)
    routing_required_fields = (
        ('assigned_object', 'peer'),
        ('address_family', 'address_families'),
        'enabled',
    )

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        af = BGPAddressFamily.objects.last()
        cls.form_data = {
            'peer': cls.peer.pk,
            'address_family': af.pk,
        }


class BGPPeerTemplateTestCase(
    AutomatedModelCreationMixin,
    BGPAddressFamilyMixin,
    BulkEditMixin,
    PluginBaseURLMixin,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    # ViewTestCases.BulkImportObjectsViewTestCase,
    model = BGPPeerTemplate
    routing_required_fields = ('name',)

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.form_data = {'name': f'{cls.model._meta.verbose_name} 5'}


class BGPPolicyTemplateTestCase(
    AutomatedModelCreationMixin,
    BGPAddressFamilyMixin,
    BulkEditMixin,
    PluginBaseURLMixin,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    # ViewTestCases.BulkImportObjectsViewTestCase,
    model = BGPPolicyTemplate
    routing_required_fields = ('name',)

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.form_data = {'name': f'{cls.model._meta.verbose_name} 5'}


class BGPSessionTemplateTestCase(
    AutomatedModelCreationMixin,
    BGPAddressFamilyMixin,
    BulkEditMixin,
    PluginBaseURLMixin,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    # ViewTestCases.BulkImportObjectsViewTestCase,
    model = BGPSessionTemplate
    routing_required_fields = ('name',)

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.form_data = {'name': f'{cls.model._meta.verbose_name} 5'}
