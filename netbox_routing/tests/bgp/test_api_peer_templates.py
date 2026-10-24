# SPDX-License-Identifier: Apache-2.0

from django.urls import reverse
from netaddr import IPNetwork
from utilities.testing import APITestCase

from ipam.models import ASN, RIR, IPAddress
from netbox_routing.models import (
    BGPPeer,
    BGPPeerTemplate,
    BGPRouter,
    BGPScope,
    BGPSessionTemplate,
)

__all__ = ('BGPPeerTemplatesAPITestCase',)


class BGPPeerTemplatesAPITestCase(APITestCase):
    """A peer's group and session template are readable and writable over REST.

    Both are fields of BGPPeer (and of its form and GraphQL type), but the serializer
    left them out: an automation that writes through REST could not say which peer
    group a session belongs to.
    """

    user_permissions = (
        'netbox_routing.view_bgppeer',
        'netbox_routing.add_bgppeer',
        'netbox_routing.change_bgppeer',
        'netbox_routing.view_bgppeertemplate',
        'netbox_routing.view_bgpsessiontemplate',
        'netbox_routing.view_bgpscope',
        'ipam.view_ipaddress',
        'ipam.view_asn',
    )

    @classmethod
    def setUpTestData(cls):
        rir = RIR.objects.create(name='RIR 1', slug='rir-1')
        asn = ASN.objects.create(rir=rir, asn=64512)
        router = BGPRouter.objects.create(name='router', asn=asn)
        cls.scope = BGPScope.objects.create(router=router)
        cls.group = BGPPeerTemplate.objects.create(name='core')
        cls.session = BGPSessionTemplate.objects.create(name='session')
        cls.peer_ip = IPAddress.objects.create(address=IPNetwork('10.0.0.1/31'))

    def url(self, peer=None):
        if peer is None:
            return reverse('plugins-api:netbox_routing-api:bgppeer-list')
        return reverse('plugins-api:netbox_routing-api:bgppeer-detail', args=[peer.pk])

    def test_create_with_a_peer_group_and_session_template(self):
        response = self.client.post(
            self.url(),
            {
                'scope': self.scope.pk,
                'peer': self.peer_ip.pk,
                'peer_group': self.group.pk,
                'peer_session': self.session.pk,
            },
            format='json',
            **self.header,
        )
        self.assertEqual(response.status_code, 201, response.content)
        self.assertEqual(response.data['peer_group']['name'], 'core')
        self.assertEqual(response.data['peer_session']['name'], 'session')
        peer = BGPPeer.objects.get(pk=response.data['id'])
        self.assertEqual((peer.peer_group, peer.peer_session), (self.group, self.session))

    def test_patch_sets_and_clears_the_peer_group(self):
        peer = BGPPeer.objects.create(scope=self.scope, peer=self.peer_ip)
        response = self.client.patch(
            self.url(peer), {'peer_group': self.group.pk}, format='json', **self.header
        )
        self.assertEqual(response.status_code, 200, response.content)
        peer.refresh_from_db()
        self.assertEqual(peer.peer_group, self.group)
        response = self.client.patch(
            self.url(peer), {'peer_group': None}, format='json', **self.header
        )
        self.assertEqual(response.status_code, 200, response.content)
        peer.refresh_from_db()
        self.assertIsNone(peer.peer_group)

    def test_a_peer_without_templates_reads_them_as_null(self):
        peer = BGPPeer.objects.create(scope=self.scope, peer=self.peer_ip)
        response = self.client.get(self.url(peer), **self.header)
        self.assertEqual(response.status_code, 200, response.content)
        self.assertIsNone(response.data['peer_group'])
        self.assertIsNone(response.data['peer_session'])
