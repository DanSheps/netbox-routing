import uuid
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.translation import gettext as _

from netbox.context_managers import event_tracking
from netbox_routing.models.bgp import *
from netbox_routing.models.community import *
from netbox_routing.models.objects import *
from users.models import User
from utilities.request import NetBoxFakeRequest


def resolve_assigned_object(item):
    if getattr(item, 'device', None):
        return item.device
    elif getattr(item, 'virtualmachine', None):
        return item.virtualmachine
    elif getattr(item, 'site', None):
        return item.site
    return None


def pks_from_through_relationship(item, column):
    local_class = item.__class__
    local_column = getattr(local_class, column)
    remote_class = local_column.rel.related_model

    local_field = f'{local_class._meta.model_name}_id'
    remote_field = f'{remote_class._meta.model_name}_id'

    filter = {f'{local_field}': item.pk}

    pks = []
    for row in local_column.through.objects.filter(**filter):
        pks.append(getattr(row, f'{remote_field}'))

    return pks


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument('--plugin-version', dest='version', help="Version of Netbox-BGP")

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username='NetBox BGP Migration')
        except User.DoesNotExist:
            user = User(username='NetBox BGP Migration')
            user.save()

        request = NetBoxFakeRequest(
            {
                'META': {},
                'POST': {},
                'GET': {},
                'FILES': {},
                'user': user,
                'path': '',
                'id': uuid.uuid4(),
            }
        )

        from netbox_routing.models import netbox_bgp

        try:
            with transaction.atomic(), event_tracking(request):
                mapping = {
                    'community': {},
                    'community_list': {},
                    'community_list_entry': {},
                    'prefix_list': {},
                    'prefix_list_entry': {},
                    'aspath': {},
                    'aspath_entry': {},
                    'route_map': {},
                    'route_map_entry': {},
                    'router': {},
                    'peer_group': {},
                }

                local_as_default = None
                if sess := netbox_bgp.BGPSession.objects.filter(
                    device__isnull=True, site__isnull=True, local_as__isnull=False
                ).first():
                    local_as_default = sess.local_as
                elif sess := netbox_bgp.BGPSession.objects.filter(
                    site__isnull=True, local_as__isnull=False
                ).first():
                    local_as_default = sess.local_as
                elif sess := netbox_bgp.BGPSession.objects.filter(
                    local_as__isnull=False
                ).first():
                    local_as_default = sess.local_as

                if not local_as_default:
                    raise Exception(
                        _(
                            'You must have at least one session with an ASN defined to allow the creation of a '
                            'default router'
                        )
                    )

                router = BGPRouter(
                    name='default',
                    asn=local_as_default,
                    description='Default Router',
                )
                router.full_clean()
                router.save()
                mapping['router'][None] = router

                scope = BGPScope(
                    router=router,
                    description='Default Scope',
                )
                scope.full_clean()
                scope.save()

                af = BGPAddressFamily(
                    scope=scope,
                    address_family='ipv4-unicast',
                    description='Default v4 AF',
                )
                af.full_clean()
                af.save()

                af = BGPAddressFamily(
                    scope=scope,
                    address_family='ipv6-unicast',
                    description='Default v6 AF',
                )
                af.full_clean()
                af.save()

                for item in netbox_bgp.BGPSession.objects.all():
                    if not item.local_as:
                        raise Exception(_('All BGP Sessions require a local ASN'))

                    assigned_object = item.device if item.device else item.site
                    if assigned_object in mapping['router'].keys():
                        continue

                    try:
                        if item.device:
                            router = BGPRouter.objects.get(
                                device=assigned_object, asn=item.asn
                            )
                        elif item.site:
                            router = BGPRouter.objects.get(site=item.site, asn=item.asn)
                        else:
                            router = BGPRouter.objects.get(asn=item.asn)
                    except BGPRouter.DoesNotExist:
                        router = BGPRouter(
                            assigned_object=assigned_object,
                            asn=item.asn,
                        )
                        router.full_clean()
                        router.save()
                        mapping['router'][assigned_object] = router
                        if not mapping['router'].get(item.pk):
                            mapping['router'][item.pk] = router

                    try:
                        scope = BGPScope.objects.get(router=router)
                    except BGPScope.DoesNotExist:
                        scope = BGPScope(
                            router=router,
                        )
                        scope.full_clean()
                        scope.save()

                    try:
                        af = BGPAddressFamily.objects.get(
                            scope=scope, address_family='ipv4-unicast'
                        )
                    except BGPAddressFamily.DoesNotExist:
                        af = BGPAddressFamily(
                            scope=scope,
                            address_family='ipv4-unicast',
                            description='Default AF',
                        )
                        af.full_clean()
                        af.save()

                    try:
                        af = BGPAddressFamily.objects.get(
                            scope=scope, address_family='ipv6-unicast'
                        )
                    except BGPAddressFamily.DoesNotExist:
                        af = BGPAddressFamily(
                            scope=scope,
                            address_family='ipv6-unicast',
                            description='Default AF',
                        )
                        af.full_clean()
                        af.save()

                for item in netbox_bgp.Community.objects.all():
                    try:
                        entry = Community.objects.get(community=item.value)
                        if not mapping['community'].get(item.pk):
                            mapping['community'][item.pk] = entry
                    except Community.DoesNotExist:
                        entry = Community(
                            community=item.value,
                            status=item.status,
                            role=item.role,
                            tenant=item.tenant,
                            description=item.description,
                            comments=item.comments,
                        )
                        entry.full_clean()
                        entry.save()
                        mapping['community'][item.pk] = entry

                for item in netbox_bgp.CommunityList.objects.all():
                    try:
                        entry = CommunityList.objects.get(name=item.name)
                        if not mapping['community_list'].get(item.pk):
                            mapping['community_list'][item.pk] = entry
                    except CommunityList.DoesNotExist:
                        entry = CommunityList(
                            name=item.name,
                            description=item.description,
                            comments=item.comments,
                        )
                        entry.full_clean()
                        entry.save()
                        mapping['community_list'][item.pk] = entry

                for item in netbox_bgp.CommunityListRule.objects.all():
                    community = mapping['community'][item.community.pk]
                    community_list = mapping['community_list'][item.community_list.pk]

                    try:
                        entry = CommunityListEntry.objects.get(
                            community_list=community_list, community=community
                        )
                        if not mapping['community_list_entry'].get(item.pk):
                            mapping['community_list_entry'][item.pk] = entry
                    except CommunityListEntry.MultipleObjectsReturned:
                        for entry in CommunityListEntry.objects.filter(
                            community_list=community_list, community=community
                        ):
                            if not mapping['community_list_entry'].get(item.pk):
                                mapping['community_list_entry'][item.pk] = entry
                    except CommunityListEntry.DoesNotExist:
                        entry = CommunityListEntry(
                            community_list=community_list,
                            action=item.action,
                            community=community,
                            description=item.description,
                            comments=item.comments,
                        )
                        entry.full_clean()
                        entry.save()
                        mapping['community_list_entry'][item.pk] = entry

                for item in netbox_bgp.PrefixList.objects.all():
                    family = 4 if item.family == 'ipv4' else 6
                    try:
                        entry = PrefixList.objects.get(name=item.name)
                        if not mapping['prefix_list'].get(item.pk):
                            mapping['prefix_list'][item.pk] = entry
                    except PrefixList.DoesNotExist:
                        entry = PrefixList(
                            name=item.name,
                            family=family,
                            description=item.description,
                            comments=item.comments,
                        )
                        entry.full_clean()
                        entry.save()
                        mapping['prefix_list'][item.pk] = entry

                for item in netbox_bgp.PrefixListRule.objects.all():
                    prefix_list = mapping['prefix_list'][item.prefix_list.pk]
                    prefix = None
                    if item.prefix:
                        prefix = item.prefix
                    elif item.prefix_custom:
                        try:
                            prefix = CustomPrefix.objects.get(prefix=item.prefix_custom)
                        except CustomPrefix.DoesNotExist:
                            prefix = CustomPrefix(prefix=item.prefix_custom)
                            prefix.clean()
                            prefix.save()

                    try:
                        entry = PrefixListEntry.objects.get(
                            prefix_list=prefix_list, sequence=item.index
                        )
                        if not mapping['prefix_list_entry'].get(item.pk):
                            mapping['prefix_list_entry'][item.pk] = entry
                    except PrefixListEntry.DoesNotExist:
                        entry = PrefixListEntry(
                            prefix_list=prefix_list,
                            sequence=item.index,
                            action=item.action,
                            prefix=prefix,
                            ge=item.ge,
                            le=item.le,
                            description=item.description,
                            comments=item.comments,
                        )
                        entry.full_clean()
                        entry.save()
                        mapping['prefix_list_entry'][item.pk] = entry

                for item in netbox_bgp.ASPathList.objects.all():
                    try:
                        entry = ASPath.objects.get(name=item.name)
                        if not mapping['aspath'].get(item.pk):
                            mapping['aspath'][item.pk] = entry
                    except ASPath.DoesNotExist:
                        entry = ASPath(
                            name=item.name,
                            description=item.description,
                            comments=item.comments,
                        )
                        entry.full_clean()
                        entry.save()
                        mapping['aspath'][item.pk] = entry

                for item in netbox_bgp.ASPathListRule.objects.all():
                    aspath = mapping['aspath'][item.aspath_list.pk]
                    try:
                        entry = ASPathEntry.objects.get(
                            aspath=aspath, sequence=item.index
                        )
                        if not mapping['aspath_entry'].get(item.pk):
                            mapping['aspath_entry'][item.pk] = entry
                    except ASPathEntry.DoesNotExist:
                        entry = ASPathEntry(
                            aspath=aspath,
                            sequence=item.index,
                            action=item.action,
                            pattern=item.pattern,
                            description=item.description,
                            comments=item.comments,
                        )
                        entry.full_clean()
                        entry.save()
                        mapping['aspath_entry'][item.pk] = entry

                for item in netbox_bgp.RoutingPolicy.objects.all():
                    #
                    # Weight is discarded
                    #
                    try:
                        entry = RouteMap.objects.get(name=item.name)
                        if not mapping['route_map'].get(item.pk):
                            mapping['route_map'][item.pk] = entry
                    except RouteMap.DoesNotExist:
                        entry = RouteMap(
                            name=item.name,
                            description=item.description,
                            comments=item.comments,
                        )
                        entry.full_clean()
                        entry.save()
                        mapping['route_map'][item.pk] = entry

                for item in netbox_bgp.RoutingPolicyRule.objects.all():
                    route_map = mapping['route_map'][item.routing_policy.pk]
                    community_list = [
                        mapping['community_list'][cl].pk
                        for cl in item.match_community_list.values_list(
                            'communitylist_id', flat=True
                        )
                    ]
                    community = [
                        mapping['community'][c].pk
                        for c in item.match_community.values_list(
                            'community_id', flat=True
                        )
                    ]
                    aspath = [
                        mapping['aspath'][asp].pk
                        for asp in item.match_aspath_list.values_list(
                            'aspathlist_id', flat=True
                        )
                    ]
                    ipv4 = [
                        mapping['prefix_list'][pl].pk
                        for pl in item.match_ip_address.values_list(
                            'prefixlist_id', flat=True
                        )
                    ]
                    ipv6 = [
                        mapping['prefix_list'][pl].pk
                        for pl in item.match_ipv6_address.values_list(
                            'prefixlist_id', flat=True
                        )
                    ]
                    match = item.match_custom
                    if not match:
                        match = {}
                    match.update(
                        {
                            'community_list': community_list,
                            'community': community,
                            'aspath': aspath,
                            'ipv4': ipv4,
                            'ipv6': ipv6,
                        }
                    )
                    try:
                        entry = RouteMapEntry.objects.get(
                            route_map=route_map, sequence=item.index
                        )
                        if not mapping['route_map_entry'].get(item.pk):
                            mapping['route_map_entry'][item.pk] = entry
                    except RouteMapEntry.DoesNotExist:
                        entry = RouteMapEntry(
                            route_map=route_map,
                            sequence=item.index,
                            action=item.action,
                            match=match,
                            set=item.set_actions,
                            description=item.description,
                            comments=item.comments,
                        )
                        entry.full_clean()
                        entry.save()
                        mapping['route_map_entry'][item.pk] = entry

                for item in netbox_bgp.BGPPeerGroup.objects.all():

                    if (
                        item.import_policies.count() > 1
                        or item.import_policies.count() > 1
                    ):
                        error = (
                            f'Only 1 import or export policy is supported per Peer Template.  There are '
                            f'{item.import_policies.count()} Import Policies and {item.export_policies.count()} Export'
                            f' Policies. Only the first policy per type will be applied.'
                        )
                        # raise Exception(_(error))
                        print(error)

                    router = mapping['router'][None]
                    scope = router.scopes.first()
                    ipv4_af = scope.address_families.filter(
                        address_family='ipv4-unicast'
                    ).first()
                    ipv6_af = scope.address_families.filter(
                        address_family='ipv6-unicast'
                    ).first()
                    try:
                        entry = BGPPeerTemplate.objects.get(name=item.name)
                        if not mapping['peer_group'].get(item.pk):
                            mapping['peer_group'][item.pk] = entry
                    except BGPPeerTemplate.DoesNotExist:
                        entry = BGPPeerTemplate(
                            name=item.name,
                            description=item.description,
                            comments=item.comments,
                        )
                        entry.full_clean()
                        entry.save()
                        mapping['peer_group'][item.pk] = entry

                    import_policies = (
                        mapping['route_map'][
                            item.import_policies.first().routingpolicy.pk
                        ]
                        if item.import_policies
                        else None
                    )
                    export_policies = (
                        mapping['route_map'][
                            item.export_policies.first().routingpolicy.pk
                        ]
                        if item.export_policies
                        else None
                    )

                    try:
                        peer_af = BGPPeerAddressFamily.objects.get(
                            peer_group=entry, address_family=ipv4_af
                        )
                    except BGPPeerAddressFamily.DoesNotExist:
                        peer_af = BGPPeerAddressFamily(
                            assigned_object=entry,
                            address_family=ipv4_af,
                            routemap_in=import_policies,
                            routemap_out=export_policies,
                        )
                        peer_af.full_clean()
                        peer_af.save()

                    try:
                        peer_af = BGPPeerAddressFamily.objects.get(
                            peer_group=entry, address_family=ipv6_af
                        )
                    except BGPPeerAddressFamily.DoesNotExist:
                        peer_af = BGPPeerAddressFamily(
                            assigned_object=entry,
                            address_family=ipv6_af,
                            routemap_in=import_policies,
                            routemap_out=export_policies,
                        )
                        peer_af.full_clean()
                        peer_af.save()

                for item in netbox_bgp.BGPSession.objects.all():
                    if (
                        item.import_policies.count() > 1
                        or item.import_policies.count() > 1
                    ):
                        error = (
                            f'Only 1 import or export policy is supported per Peer Session.  There are '
                            f'{item.import_policies.count()} Import Policies and {item.export_policies.count()} Export'
                            f' Policies. Only the first policy per type will be applied.'
                        )
                        # raise Exception(_(error))
                        print(error)
                    assigned_object = resolve_assigned_object(item)
                    router = mapping['router'][assigned_object]
                    scope = router.scopes.first()

                    if item.local_address.address.version == 4:
                        af = scope.address_families.filter(
                            address_family='ipv4-unicast'
                        ).first()
                    else:
                        af = scope.address_families.filter(
                            address_family='ipv6-unicast'
                        ).first()
                    try:
                        peer = BGPPeer.objects.get(
                            scope=scope, peer=item.remote_address, name=item.name
                        )
                    except BGPPeer.DoesNotExist:
                        peer = BGPPeer(
                            name=item.name,
                            scope=scope,
                            source=item.local_address,
                            peer=item.remote_address,
                            remote_as=item.remote_as,
                            local_as=item.local_as,
                            peer_group=(
                                mapping['peer_group'].get(item.peer_group.pk)
                                if item.peer_group
                                else None
                            ),
                            enabled=True if item.status == 'active' else False,
                            tenant=item.tenant,
                            description=item.description,
                            comments=item.comments,
                        )
                        peer.full_clean()
                        peer.save()

                    import_policy = None
                    export_policy = None
                    if item.import_policies:
                        policy = item.import_policies.first()
                        import_policy = mapping['route_map'].get(
                            policy.routingpolicy.pk
                        )
                    if item.export_policies:
                        policy = item.export_policies.first()
                        export_policy = mapping['route_map'].get(
                            policy.routingpolicy.pk
                        )

                    try:
                        peeraf = BGPPeerAddressFamily.objects.get(
                            peer=peer, address_family=af
                        )
                    except BGPPeerAddressFamily.DoesNotExist:
                        peeraf = BGPPeerAddressFamily(
                            assigned_object=peer,
                            address_family=af,
                            routemap_in=import_policy,
                            routemap_out=export_policy,
                            prefixlist_in=(
                                mapping['prefix_list'].get(item.prefix_list_in.pk)
                                if item.prefix_list_in
                                else None
                            ),
                            prefixlist_out=(
                                mapping['prefix_list'].get(item.prefix_list_out.pk)
                                if item.prefix_list_out
                                else None
                            ),
                        )
                        peeraf.full_clean()
                        peeraf.save()
                # raise Exception('Finished')
        except Exception as e:
            print(f'Last item: {item} ({type(item)})')
            print(f'Exception encountered: {e}; rolling back migration')
            raise e

        user.delete()
