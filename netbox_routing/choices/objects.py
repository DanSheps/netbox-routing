from django.utils.translation import gettext_lazy as _
from graphene_django import DjangoObjectType

from utilities.choices import ChoiceSet


class PermitDenyChoices(ChoiceSet):
    PERMIT = 'permit'
    DENY = 'deny'

    CHOICES = [
        (PERMIT, 'Permit', 'blue'),
        (DENY, 'Deny', 'red')
    ]


class RouteMapOptions(ChoiceSet):
    # IPv4
    MATCH_V4_IP_PREFFIXLIST = 'match_v4_ip_prefixlist'
    MATCH_V4_IP_ACL = 'match_v4_ip_acl'
    MATCH_V4_IP_FLOWSPEC_SRC_PREFFIXLIST = 'match_v4_flowspec_src_prefixlist'
    MATCH_V4_IP_FLOWSPEC_DST_PREFFIXLIST = 'match_v4_flowspec_dst_prefixlist'
    MATCH_V4_IP_FLOWSPEC_SRC_ACL = 'match_v4_flowspec_src_acl'
    MATCH_V4_IP_FLOWSPEC_SRC_ACL = 'match_v4_flowspec_dst_acl'
    MATCH_V4_IP_NEXTHOP_PREFIXLIST = 'match_v4_nh_prefixlist'
    MATCH_V4_IP_NEXTHOP_ACL = 'match_v4_nh_acl'
    MATCH_V4_IP_REDISTRIBUTESOURCE_PREFIXLIST_ = 'match_v4_rds_prefixlist'
    MATCH_V4_IP_REDISTRIBUTESOURCE_ACL = 'match_v4_rds_acl'
    MATCH_V4_IP_ROUTESOURCE_PREFIXLIST = 'match_v4_rs_prefixlist'
    MATCH_V4_IP_ROUTESOURCE_ACL = 'match_v4_rs_acl'
    MATCH_V4_IP_ROUTESOURCE_REDISTRIBUTESOURCE_PREFIXLIST = 'match_v4_rs_rds_prefixlist'
    MATCH_V4_IP_ROUTESOURCE_REDISTRIBUTESOURCE_ACL = 'match_v4_rs_rds_acl'

    # IPv6
    MATCH_V6_IP_PREFFIXLIST = 'match_v6_ip_prefixlist'
    MATCH_V6_IP_ACL = 'match_v6_ip_acl'
    MATCH_V6_IP_FLOWSPEC_SRC_PREFFIXLIST = 'match_v6_flowspec_src_prefixlist'
    MATCH_V6_IP_FLOWSPEC_DST_PREFFIXLIST = 'match_v6_flowspec_dst_prefixlist'
    MATCH_V6_IP_FLOWSPEC_SRC_ACL = 'match_v6_flowspec_src_acl'
    MATCH_V6_IP_FLOWSPEC_SRC_ACL = 'match_v6_flowspec_dst_acl'
    MATCH_V6_IP_NEXTHOP_PREFIXLIST = 'match_v6_nh_prefixlist'
    MATCH_V6_IP_NEXTHOP_ACL = 'match_v6_nh_acl'
    MATCH_V6_IP_ROUTESOURCE_PREFIXLIST = 'match_v6_rs_prefixlist'
    MATCH_V6_IP_ROUTESOURCE_ACL = 'match_v6_rs_acl'
    
    MATCH_INTERFACE = 'match_interface'

    #
    # Set Options
    #

    # Set
    SET_INTERFACE = 'set_interface'
    SET_WEIGHT = 'set_weight'
    SET_METRIC = 'set_metric'

    CHOICES = [
        (MATCH_V4_IP_PREFFIXLIST, _('IPv4 Prefix List')),
        (MATCH_V6_IP_PREFFIXLIST, _('IPv6 Prefix List')),
        (MATCH_INTERFACE, _('Interface')),
        (SET_INTERFACE, _('Interface')),
    ]

    FIELD_TYPES = {
        MATCH_V4_IP_PREFFIXLIST: {'model': 'netbox_routing.PrefixList', 'multiple': True},
        MATCH_V6_IP_PREFFIXLIST: {'model': 'netbox_routing.PrefixList', 'multiple': True},
        MATCH_INTERFACE: 'char',
        SET_INTERFACE: 'char',
    }

    DYNAMIC_MODEL_RESTRICTIONS = {
        MATCH_V4_IP_PREFFIXLIST: {'family': 'ipv4', },
        MATCH_V6_IP_PREFFIXLIST: {'family': 'ipv6', }
    }
