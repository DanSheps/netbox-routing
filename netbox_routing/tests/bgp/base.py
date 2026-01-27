from netbox_routing.models import BGPRouter, BGPScope, BGPAddressFamily, BGPPeer
from netbox_routing.tests.base import ASNMixin, VRFMixin, AddressesMixin

__all__ = (
    'BGPRouterMixin',
    'BGPScopeMixin',
    'BGPAddressFamilyMixin',
    'BGPPeerMixin',
)


class BGPRouterMixin(ASNMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.router = BGPRouter.objects.create(name='BGP Router', asn=cls.asn)


class BGPScopeMixin(VRFMixin, BGPRouterMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.scope = BGPScope.objects.create(router=cls.router)


class BGPAddressFamilyMixin(BGPScopeMixin):
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
        for af in cls.afs:
            BGPAddressFamily.objects.create(scope=cls.scope, address_family=af)

        cls.af = BGPAddressFamily.objects.first()
        cls.address_family = BGPAddressFamily.objects.first()
        cls.address_families = BGPAddressFamily.objects.all()


class BGPPeerMixin(BGPScopeMixin, AddressesMixin):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.peer = BGPPeer.objects.create(
            name='BGP Peer', scope=cls.scope, peer=cls.peer_address
        )
