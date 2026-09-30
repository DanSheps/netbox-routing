# SPDX-License-Identifier: Apache-2.0

from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from netaddr import IPNetwork
from utilities.testing import APITestCase, create_test_device

from ipam.models import ASN, RIR, IPAddress
from netbox_routing.models import BGPPeer, BGPRouter, BGPScope

__all__ = ('BGPGraphQLTestCase',)


class BGPGraphQLTestCase(APITestCase):
    """The BGP lists page and filter on their relations.

    Without pagination a list is cut at MAX_PAGE_SIZE, so a client could not read past
    the first page of peers; without model fields on the filters it could not narrow
    them to one router.
    """

    user_permissions = (
        'netbox_routing.view_bgppeer',
        'netbox_routing.view_bgpscope',
        'netbox_routing.view_bgprouter',
        'ipam.view_ipaddress',
        'ipam.view_asn',
        'dcim.view_device',
    )

    @classmethod
    def setUpTestData(cls):
        rir = RIR.objects.create(name='RIR 1', slug='rir-1')
        local_as = ASN.objects.create(rir=rir, asn=64512)
        remote_as = ASN.objects.create(rir=rir, asn=64513)
        device_type = ContentType.objects.get_by_natural_key('dcim', 'device')
        cls.peers = {}
        for n, name in enumerate(('router-a', 'router-b'), start=1):
            device = create_test_device(name)
            router = BGPRouter.objects.create(
                name=name,
                asn=local_as,
                assigned_object_type=device_type,
                assigned_object_id=device.pk,
            )
            scope = BGPScope.objects.create(router=router)
            for i in range(1, 4):
                peer = IPAddress.objects.create(address=IPNetwork(f'10.{n}.0.{i}/31'))
                cls.peers[(name, i)] = BGPPeer.objects.create(
                    scope=scope,
                    peer=peer,
                    remote_as=remote_as if i == 1 else local_as,
                    status='active' if i < 3 else 'offline',
                )

    def query(self, query):
        response = self.client.post(
            reverse('graphql'),
            data={'query': query},
            content_type='application/json',
            **self.header,
        )
        self.assertEqual(response.status_code, 200, response.content)
        body = response.json()
        self.assertNotIn('errors', body, body)
        return body['data']

    def ids(self, query):
        (rows,) = self.query(query).values()
        return sorted(int(row['id']) for row in rows)

    def pks(self, *keys):
        return sorted(self.peers[key].pk for key in keys)

    def test_peer_list_pages(self):
        first = self.ids('{ bgp_peer_list(pagination: {offset: 0, limit: 4}) { id } }')
        rest = self.ids('{ bgp_peer_list(pagination: {offset: 4, limit: 4}) { id } }')
        self.assertEqual(len(first), 4)
        self.assertEqual(sorted(first + rest), self.pks(*self.peers))

    def test_peer_list_filters_on_the_router(self):
        self.assertEqual(
            self.ids(
                '{ bgp_peer_list(filters: {scope: {router: {name: {exact: "router-b"}}}}) { id } }'
            ),
            self.pks(('router-b', 1), ('router-b', 2), ('router-b', 3)),
        )

    def test_peer_list_filters_on_the_device_the_router_is_assigned_to(self):
        device_id = BGPRouter.objects.get(name='router-a').assigned_object_id
        self.assertEqual(
            self.ids(
                '{ bgp_peer_list(filters: {scope: {router: {assigned_object_id: "'
                f'{device_id}'
                '"}}}) { id } }'
            ),
            self.pks(('router-a', 1), ('router-a', 2), ('router-a', 3)),
        )

    def test_peer_list_filters_on_the_peer_address_remote_as_and_status(self):
        self.assertEqual(
            self.ids(
                '{ bgp_peer_list(filters: {peer: {address: {exact: "10.1.0.2/31"}}}) { id } }'
            ),
            self.pks(('router-a', 2)),
        )
        remote_as = ASN.objects.get(asn=64513).pk
        self.assertEqual(
            self.ids(f'{{ bgp_peer_list(filters: {{remote_as_id: "{remote_as}"}}) {{ id }} }}'),
            self.pks(('router-a', 1), ('router-b', 1)),
        )
        self.assertEqual(
            self.ids('{ bgp_peer_list(filters: {status: {exact: "offline"}}) { id } }'),
            self.pks(('router-a', 3), ('router-b', 3)),
        )

    def test_router_and_scope_lists_page_and_filter(self):
        self.assertEqual(
            len(self.ids('{ bgp_router_list(pagination: {limit: 1}) { id } }')), 1
        )
        self.assertEqual(
            len(
                self.ids(
                    '{ bgp_scope_list(filters: {router: {name: {exact: "router-a"}}}) { id } }'
                )
            ),
            1,
        )
